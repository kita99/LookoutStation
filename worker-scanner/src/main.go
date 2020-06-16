package main

import (
	"log"
	"net/http"
	"time"
	"fmt"
	"strings"
	"bytes"
    "context"
    "encoding/json"

	"github.com/adjust/rmq"
    "github.com/Ullaakut/nmap"
)

const (
	workers = 10
)

func main() {
	connection := rmq.OpenConnection("lookoustation-worker-scanner", "tcp", "redis:6379", 1)
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
    split := strings.Split(payload, ":")
    target := split[0]
    portRange := split[1]

    log.Printf("Processing a scan:")
    log.Printf(payload)


    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Minute)
	defer cancel()

	// Equivalent to `/usr/local/bin/nmap -p 80,443,843 google.com facebook.com youtube.com`,
	// with a 5 minute timeout.
	scanner, err := nmap.NewScanner(
		nmap.WithTargets(target),
		nmap.WithPorts(portRange),
		nmap.WithContext(ctx),
	)

	if err != nil {
        delivery.Reject()
        delivery.Push()

		log.Fatalf("unable to create nmap scanner: %v", err)
	}

	result, _, err := scanner.Run()
	if err != nil {
        delivery.Reject()
        delivery.Push()

		log.Fatalf("unable to run nmap scan: %v", err)
	}

    delivery.Ack()

    jsonResponse, _ := json.Marshal(result.Hosts)
    resp, err := http.Post("http://lookoustation-api/scans/" + target, "application/json", bytes.NewBuffer(jsonResponse))

	if err != nil {
        delivery.Reject()
        delivery.Push()

		log.Fatalf("could not submit scan result: %v", err)
	}

    log.Println(resp)
}
