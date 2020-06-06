package main

import (
    "log"
    "net/http"
    "github.com/gorilla/mux"
)

func main() {
    r := mux.NewRouter()

    // Misc
    r.HandleFunc("/status", QueueStatusCheck).
        Methods("GET")

    // Bind to a port and pass our router in
    log.Fatal(http.ListenAndServe(":80", r))
}
