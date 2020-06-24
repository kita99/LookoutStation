package main

import (
	"strconv"
	"strings"
	"time"
	"fmt"
	"log"
	"os"

	"github.com/adjust/rmq"
    "github.com/r3labs/diff"

    "./responses"
)

func getEnv(key string, fallback int) int {
    value, exists := os.LookupEnv(key)

    if !exists {
        return fallback
    }

    int_value, _ := strconv.Atoi(value)
    return int_value
}



func main() {
	connection := rmq.OpenConnection("lookoustation-worker-feeder", "tcp", "lookoutstation-redis:6379", 1)
	queue := connection.OpenQueue("feeds")

	queue.StartConsuming(10, 500*time.Millisecond)
    queue.SetPushQueue(queue)

    for i := 0; i < getEnv("feeder-workers", 1); i++ {
		workerName := fmt.Sprintf("worker-%d", i)
		queue.AddConsumer(workerName, NewWorker(i))
	}

	select {}
}

type Worker struct {
	timestamp time.Time
}

type Payload struct {
    feedID string
    mode string
}

func NewWorker(tag int) *Worker {
    log.Println("Initiating a worker")

	return &Worker{
		timestamp: time.Now(),
	}
}

func (worker *Worker) Consume(delivery rmq.Delivery) {
    var payload Payload
    rawPayload := delivery.Payload()
    split := strings.Split(rawPayload, ":")

    if strings.Contains(rawPayload, ":") {
        payload = Payload{
            feedID: split[0],
            mode: split[1],
        }
    } else {
        payload = Payload{
            feedID: split[0],
            mode: "diff",
        }
    }

    // Get feed by id
    feed, err := GetFeed(payload.feedID)

    if err != nil {
        delivery.Reject()
        delivery.Push()
        return
    }

    // fetch metadata url and extract sha256 and size
    feedSourceMetadata, err := GetFeedSourceMetadata(feed.MetaURL)

    if err != nil {
        delivery.Reject()
        delivery.Push()
        return
    }

    feedSourceData, err := GetFeedSource(feed.URL)

    if err != nil {
        delivery.Reject()
        delivery.Push()
    }

    feedTask :=  FeedTask{
        ByteSize: feedSourceMetadata.Size,
        SHA256: feedSourceMetadata.SHA256,
        CVEAmount: feedSourceData.CVEDataNumberOfCVEs,
        FeedModificationDate: feedSourceMetadata.LastModifiedDate,
        RawJSON: feedSourceData,
    }

    switch mode := payload.mode; mode {
    case "diff":
        lastFeedTask, err := GetLastFeedTask(payload.feedID)

        if err != nil {
            delivery.Reject()
            delivery.Push()
        }

        feedTaskID, status := CreateFeedTask(payload.feedID, feedTask)

        if !status {
            delivery.Reject()
            delivery.Push()
        }

        changelog, err := diff.Diff(lastFeedTask.RawJSON, feedSourceData)

        if err != nil {
            delivery.Reject()
            delivery.Push()
        }

        var updates []responses.CVEItem
        var creates []responses.CVEItem
        var matches []int

        for _, change := range changelog {
            index, _ := strconv.Atoi(change.Path[1])

            if !StringInSlice(index, matches) {
                matches = append(matches, index)

                if change.Type == "create" {
                    creates = append(creates, feedSourceData.CVEItems[index])
                }

                if change.Type == "update" {
                    updates = append(creates, feedSourceData.CVEItems[index])
                }
            }
        }

        if len(creates) > 0 {
            if !StoreCVES(payload.feedID, feedTaskID, creates) {
                delivery.Reject()
                delivery.Push()

                return
            }
        }

        if len(updates) > 0 {
            if !StoreCVES(payload.feedID, feedTaskID, updates) {
                delivery.Reject()
                delivery.Push()

                return
            }
        }

        delivery.Ack()
    case "populate":
        feedTaskID, status := CreateFeedTask(payload.feedID, feedTask)

        if !status {
            delivery.Reject()
            delivery.Push()

            return
        }

        if !StoreCVES(payload.feedID, feedTaskID, feedSourceData.CVEItems) {
            delivery.Reject()
            delivery.Push()

            return
        }

        delivery.Ack()
    }
}
