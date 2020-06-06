package queue

import (
    "github.com/adjust/rmq"
)

func PublishScan(queue string, message string) {
    connection := rmq.OpenConnection("scannex-api-publisher", "tcp", "redis:6379", 1)

    scanQueue := connection.OpenQueue("scans")
    scanQueue.Publish(message)
}
