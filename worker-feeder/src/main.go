package main

import (
	"strconv"
	"strings"
	"time"
	"fmt"
	"log"

	"github.com/adjust/rmq"
    "github.com/r3labs/diff"

    "./responses"
)

const (
	workers = 10
)

func main() {
	connection := rmq.OpenConnection("lookoustation-worker-feeder", "tcp", "lookoutstation-redis:6379", 1)
	queue := connection.OpenQueue("feeds")

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

    feedTaskID, status := CreateFeedTask(feedTask)

    if !status {
        delivery.Reject()
        delivery.Push()
    }

    switch mode := payload.mode; mode {
    case "diff":
        lastFeedTask, err := GetLastFeedTask(payload.feedID)

        if err != nil {
            delivery.Reject()
            delivery.Push()
        }

        changelog, err := diff.Diff(lastFeedTask.RawJSON, feedSourceData)

        if err != nil {
            delivery.Reject()
            delivery.Push()
        }

        var updates []responses.CVE
        var creates []responses.CVE
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

        if !StoreCVES(payload.feedID, feedTaskID, creates) {
            delivery.Reject()
            delivery.Push()
        }

        if !UpdateCVES(payload.feedID, feedTaskID, updates) {
            delivery.Reject()
            delivery.Push()
        }

    case "populate":
        if !StoreCVES(payload.feedID, feedTaskID, feedSourceData.CVEItems) {
            delivery.Reject()
            delivery.Push()
        }
    }
}
