package main

import (
    "log"
    "net/http"
    "github.com/gorilla/mux"
)


func main() {
    r := mux.NewRouter()

    r.HandleFunc("/queues", QueueStatusCheck).
        Methods("GET")

    r.HandleFunc("/publish", PublishToQueue).
        Methods("POST")

    log.Fatal(http.ListenAndServe(":80", r))
}
