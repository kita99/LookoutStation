package main

import (
    "log"
    "time"
    "net/http"
    "io/ioutil"
    "encoding/json"
    "github.com/gorilla/mux"
    "github.com/jasonlvhit/gocron"

    "./queue"
)


type Response struct {
	Ips []string `json:"ips"`
}

func dailyScan() (err error) {
    res, err := http.Get("http://lookoutstation-api:8080/assets/ips/public")

    if err != nil {
        log.Printf("Could not fetch ip list from API, retrying in 10 seconds")
        time.Sleep(10 * time.Second)
        go dailyScan()

        return
    }

    body, err := ioutil.ReadAll(res.Body)
    if err != nil {
        log.Printf("Could not read response from API, retrying in 10 seconds")
        time.Sleep(10 * time.Second)
        go dailyScan()

        return
    }

    var response Response
    json.Unmarshal(body, &response)

    for _, ip := range response.Ips {
        queue.PublishScan("scans", ip + ":1-65535")
    }
    return
}

func main() {
    r := mux.NewRouter()

    gocron.Every(1).Day().Do(dailyScan)
    go dailyScan()

    // Misc
    r.HandleFunc("/status", QueueStatusCheck).
        Methods("GET")

    // Bind to a port and pass our router in
    log.Fatal(http.ListenAndServe(":80", r))
}
