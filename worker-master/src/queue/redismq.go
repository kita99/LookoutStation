package queue

import (
    "github.com/adjust/rmq"
)

func PublishScan(queue string, message string) {
    connection := rmq.OpenConnection("lookoutstation-publisher", "tcp", "redis:6379", 1)
    taskQueue := connection.OpenQueue(queue)

    taskQueue.Publish(message)
}
