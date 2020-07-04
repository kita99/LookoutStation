package main

import (
    "math/rand"
    "context"
    "strconv"
    "strings"
	"time"
	"log"
	"fmt"
    "os"

	"github.com/adjust/rmq"
    "github.com/Ullaakut/nmap"
)

type ScanResults struct {
    Hosts []nmap.Host `json:"hosts"`
    WorkerID string `json:"worker_code"`
    Progress float64 `json:"progress"`
    Ports string `json:"ports"`
}

func getEnv(key string, fallback int) int {
    value, exists := os.LookupEnv(key)

    if !exists {
        return fallback
    }

    int_value, _ := strconv.Atoi(value)
    return int_value
}


func main() {
    // seed to assure workerID randomness
    rand.Seed(time.Now().UTC().UnixNano())

	connection := rmq.OpenConnection("lookoustation-worker-scanner", "tcp", "lookoutstation-redis:6379", 1)
	queue := connection.OpenQueue("scans")

	queue.StartConsuming(10, 500*time.Millisecond)
    queue.SetPushQueue(queue)

    for i := 0; i < getEnv("scanner-workers", 10); i++ {
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

type Payload struct {
    ipaddress string
    ports string
}

func (worker *Worker) Consume(delivery rmq.Delivery) {
    var payload Payload
    rawPayload := delivery.Payload()
    split := strings.Split(rawPayload, ":")

    log.Printf("Worker %s initiating scan with payload: %s", worker.ID, rawPayload)

    if strings.Contains(rawPayload, ":") {
        payload = Payload{
            ipaddress: split[0],
            ports: split[1],
        }
    } else {
        payload = Payload{
            ipaddress: split[0],
            ports: "-",
        }
    }

    status := NotifyScanStart(worker.ID, rawPayload)

    if !status {
        delivery.Reject()
        delivery.Push()

        DeleteScan(payload.ipaddress, worker.ID)
        return
    }

    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Minute)
	defer cancel()

    steps := StepifyScan(rawPayload)

    for _, step := range steps {
        scanner, err := nmap.NewScanner(
            nmap.WithTargets(step.IP),
            nmap.WithPorts(step.Ports),
            nmap.WithContext(ctx),
        )

        if err != nil {
            delivery.Reject()
            delivery.Push()

            DeleteScan(payload.ipaddress, worker.ID)
            log.Printf("Unable to create nmap scanner: ", err)
            return
        }

	    result, _, err := scanner.Run()

        if err != nil {
            delivery.Reject()
            delivery.Push()

            DeleteScan(payload.ipaddress, worker.ID)
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

            DeleteScan(payload.ipaddress, worker.ID)
            return
        }
    }


    delivery.Ack()
    log.Printf("Worker %s finished processing %s", worker.ID, payload)
}
