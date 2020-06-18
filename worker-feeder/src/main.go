package main

import (
	"time"
	"fmt"
	"log"

	"github.com/adjust/rmq"
    "github.com/r3labs/diff"
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

func NewWorker(tag int) *Worker {
    log.Println("Initiating a worker")

	return &Worker{
		timestamp: time.Now(),
	}
}

func (worker *Worker) Consume(delivery rmq.Delivery) {
    feedId := delivery.Payload()

    // Get feed by id
    feed, err := GetFeed(feedId)

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

    if CreateFeedTask(feedTask) {
        delivery.Reject()
        delivery.Push()
    }

    changelog, err := diff.Diff(feedSourceData, feedTask.RawJSON)

    if err != nil {
        delivery.Reject()
        delivery.Push()
    }

    // TODO: handle changes and send them over to the API
    for _, value := range changelog {
        log.Println(value)
    }
}
