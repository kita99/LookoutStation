package main

import (
    "log"
    "time"
    "net/http"
    "io/ioutil"
    "encoding/json"
)

type Response struct {
	Ips []string `json:"ips"`
}

func ScanAssets() (err error) {
    res, err := http.Get("http://lookoutstation-api/assets/ips/public")

    if err != nil {
        log.Printf("Could not fetch ip list from API, retrying in 10 seconds")
        time.Sleep(10 * time.Second)
        go ScanAssets()

        return
    }

    body, err := ioutil.ReadAll(res.Body)
    if err != nil {
        log.Printf("Could not read response from API, retrying in 10 seconds")
        time.Sleep(10 * time.Second)
        go ScanAssets()

        return
    }

    var response Response
    json.Unmarshal(body, &response)

    for _, ip := range response.Ips {
        PublishToQueue("scans", ip + ":1-65535")
    }
    return
}
