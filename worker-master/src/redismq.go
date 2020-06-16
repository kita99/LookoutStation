package main

import (
    "encoding/json"
    "github.com/adjust/rmq"
)

struct Message {
    queue string
    message string
}

func Publish(queue string, message string) {
    connection := rmq.OpenConnection("lookoutstation-worker-master", "tcp", "lookoutstation-redis:6379", 1)
    taskQueue := connection.OpenQueue(queue)

    taskQueue.Publish(message)
}

func CollectQueueStats() rmq.Stats {
	connection := rmq.OpenConnection("lookoustation-worker-master", "tcp", "redis:6379", 1)

	queues := connection.GetOpenQueues()
    queueStats := connection.CollectStats(queues)

    return queueStats
}
