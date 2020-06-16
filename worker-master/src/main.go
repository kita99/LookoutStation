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

    // Bind to a port and pass our router in
    log.Fatal(http.ListenAndServe(":80", r))
}
