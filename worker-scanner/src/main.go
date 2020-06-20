package main

import (
    "math/rand"
    "context"
	"time"
	"log"
	"fmt"

	"github.com/adjust/rmq"
    "github.com/Ullaakut/nmap"
)

const (
	workers = 10
)

type ScanResults struct {
    Hosts []nmap.Host `json:"hosts"`
    WorkerID string `json:"worker_id"`
    Progress float64 `json:"progress"`
    Ports string `json:"ports"`
}

func main() {
    // seed to assure workerID randomness
    rand.Seed(time.Now().UTC().UnixNano())

	connection := rmq.OpenConnection("lookoustation-worker-scanner", "tcp", "lookoutstation-redis:6379", 1)
	queue := connection.OpenQueue("scans")

	queue.StartConsuming(10, 500*time.Millisecond)
    queue.SetPushQueue(queue)

    for i := 0; i < workers; i++ {
        workerID := GenerateRandomString(12)
		workerName := fmt.Sprintf("worker-scanner-%s", workerID)
		queue.AddConsumer(workerName, NewWorker(workerID))
	}

	select {}
}

type Worker struct {
	ID string
	timestamp time.Time
}

func NewWorker(workerID string) *Worker {
    log.Printf("Scanner worker %s ready", workerID)

	return &Worker{
        ID: workerID,
		timestamp: time.Now(),
	}
}

func (worker *Worker) Consume(delivery rmq.Delivery) {
    payload := delivery.Payload()
    log.Printf("Worker %s initiating scan with payload: %s", worker.ID, payload)

    status := NotifyScanStart(worker.ID, payload)

    if !status {
        delivery.Reject()
        delivery.Push()

        return
    }

    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Minute)
	defer cancel()

    steps := StepifyScan(payload)

    for _, step := range steps {
        scanner, err := nmap.NewScanner(
            nmap.WithTargets(step.IP),
            nmap.WithPorts(step.Ports),
            nmap.WithContext(ctx),
        )

        if err != nil {
            delivery.Reject()
            delivery.Push()

            log.Printf("Unable to create nmap scanner: ", err)
            return
        }

	    result, _, err := scanner.Run()

        if err != nil {
            delivery.Reject()
            delivery.Push()

            log.Printf("Unable to run nmap scan: ", err)
            return
        }

        scanResults := ScanResults{
            Hosts: result.Hosts,
            WorkerID: worker.ID,
            Progress: step.Progress,
            Ports: step.Ports,
        }

        status := UpdateScan(step.IP, scanResults)

        if !status {
            delivery.Reject()
            delivery.Push()

            return
        }
    }


    delivery.Ack()
    log.Printf("Worker %s finished processing %s", worker.ID, payload)
}
