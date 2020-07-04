package main

import (
    "net/http"
    "log"

    "github.com/jasonlvhit/gocron"
    "github.com/gorilla/mux"
)

func ManualTrigger(w http.ResponseWriter, r *http.Request) {
    log.Println("Manually triggering all tasks")

    go ScanAssets()
    go ProcessAllFeeds()
}

func main() {
    r := mux.NewRouter()

    gocron.Every(1).Day().Do(ScanAssets)
    gocron.Every(1).Day().Do(ProcessAllFeeds)

    r.HandleFunc("/trigger", ManualTrigger).
        Methods("GET")

    log.Fatal(http.ListenAndServe(":80", r))
}
