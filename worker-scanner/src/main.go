package main

import (
	"log"
	"time"
	"fmt"
	"strings"
    "context"
    "encoding/json"

	"github.com/adjust/rmq"
    "github.com/Ullaakut/nmap"
)

const (
	workers = 10
)

func main() {
	connection := rmq.OpenConnection("lookoustation-worker-scanner", "tcp", "lookoutstation-redis:6379", 1)
	queue := connection.OpenQueue("scans")

	queue.StartConsuming(10, 500*time.Millisecond)
    queue.SetPushQueue(queue)

    for i := 0; i < workers; i++ {
		workerName := fmt.Sprintf("worker-%d", i)
		queue.AddConsumer(workerName, NewWorker(i))
	}

	select {}
}

type Worker struct {
	timestamp time.Time
}

func NewWorker(tag int) *Worker {
    log.Printf("Initiating a worker")

	return &Worker{
		timestamp: time.Now(),
	}
}

func (worker *Worker) Consume(delivery rmq.Delivery) {
    payload := delivery.Payload()
    log.Printf("Initiating scan for: %s", payload)

    split := strings.Split(payload, ":")
    target := split[0]
    portRange := split[1]

    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Minute)
	defer cancel()

	scanner, err := nmap.NewScanner(
		nmap.WithTargets(target),
		nmap.WithPorts(portRange),
		nmap.WithContext(ctx),
	)

	if err != nil {
        delivery.Reject()
        delivery.Push()

		log.Fatalf("Unable to create nmap scanner: %v", err)
	}

	result, _, err := scanner.Run()
	if err != nil {
        delivery.Reject()
        delivery.Push()

		log.Fatalf("Unable to run nmap scan: %v", err)
	}

    scanResults, _ := json.Marshal(result.Hosts)
    status := StoreScanResults(target, scanResults)

	if !status {
        delivery.Reject()
        delivery.Push()
	}

    delivery.Ack()
    log.Printf("Finished scan for: %s", payload)
}
