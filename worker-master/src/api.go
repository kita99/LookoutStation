package main

import (
    "encoding/json"
    "net/http"
)

struct Response {
    Message `json:"message"`
}

func QueueStatusCheck(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusOk)

    queueStats := CollectQueueStats()
    jsonQueueStats, _ := json.Marshal(queueStats)

    json.NewEncoder(w).Encode(data)
}

func PublishToQueue(w http.ResponseWriter, r *http.Request) {
    connection := rmq.OpenConnection("lookoutstation-worker-master", "tcp", "lookoutstation-redis:6379", 1)
    w.Header().Set("Content-Type", "application/json")

    var message Message
    var response Response


    err = json.NewDecoder(r.Body).Decode(message)

    if err != nil {
        w.WriteHeader(http.StatusBadRequest)
        response.Message = "Message published"
        json.NewEncoder(w).Encode(response)
    }

    taskQueue := connection.OpenQueue(message.queue)
    taskQueue.Publish(message.message)

    w.WriteHeader(http.StatusOk)
    response.Message = "Message published"
    json.NewEncoder(w).Encode(response)
}
