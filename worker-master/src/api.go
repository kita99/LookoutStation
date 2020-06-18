package main

import (
    "encoding/json"
    "net/http"
)

type Response struct {
    Message string `json:"message"`
}

func QueueStatusCheck(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusOK)

    queueStats := CollectQueueStats()

    json.NewEncoder(w).Encode(queueStats)
}

func PublishToQueue(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")

    var message Message
    var response Response

    err := json.NewDecoder(r.Body).Decode(message)

    if err != nil {
        w.WriteHeader(http.StatusBadRequest)
        response.Message = "Could not process request"
        json.NewEncoder(w).Encode(response)
    }

    Publish(message.queue, message.message)

    w.WriteHeader(http.StatusOK)
    response.Message = "Message published"
    json.NewEncoder(w).Encode(response)
}
