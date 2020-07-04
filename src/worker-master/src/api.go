package main

import (
    "encoding/json"
    "net/http"
)

type PublishRequest struct {
    Queue string `json:"queue"`
    Message string `json:"message"`
}

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

    var request PublishRequest
    var response Response

    err := json.NewDecoder(r.Body).Decode(&request)

    if err != nil {
        w.WriteHeader(http.StatusBadRequest)
        response.Message = "Could not process request"
        json.NewEncoder(w).Encode(response)
        return
    }

    Publish(request.Queue, request.Message)

    w.WriteHeader(http.StatusOK)
    response.Message = "Message published"
    json.NewEncoder(w).Encode(response)
}

func CleanQueue(w http.ResponseWriter, r *http.Request) {
    var response Response

    Clean()

    w.WriteHeader(http.StatusOK)
    response.Message = "Cleanup successful"
    json.NewEncoder(w).Encode(response)
}
