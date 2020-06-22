package main

import (
    "encoding/json"
    "net/http"
    "bytes"
    "strings"
    "log"
)

func UpdateScan(address string, results ScanResults) bool  {
    scanResults, _ := json.Marshal(results)

    client := &http.Client{}

    req, err := http.NewRequest(http.MethodPut, "http://lookoutstation-api/scans/" + address, bytes.NewBuffer(scanResults))

    if err != nil {
		log.Printf("Could not submit scan results: %s", err)
        return false
    }

    req.Header.Set("Content-Type", "application/json; charset=utf-8")
    resp, err := client.Do(req)

    if err != nil {
		log.Printf("Could not submit scan results: %s", err)
        return false
    }

    if resp.StatusCode != 200 {
		log.Printf("Could not submit scan results: %s", err)
        return false
    }

    return true
}

func NotifyScanStart(workerID string, payload string) bool {
    split := strings.Split(payload, ":")

    request := struct {
        WorkerID string `json:"worker_code"`
        Payload string `json:"payload"`
    }{
        workerID,
        payload,
    }

    notification, err := json.Marshal(request)

    if err != nil {
		log.Printf("Could not create json request: %s", err)
        return false
    }

    resp, err := http.Post("http://lookoutstation-api/scans/" + split[0], "application/json", bytes.NewBuffer(notification))

    if err != nil {
		log.Printf("Could not notify scan start: %s", err)
        return false
    }

    if resp.StatusCode != 200 {
        log.Println(request)
        log.Println(resp.Body)
        log.Printf("Could not notify scan start, API returned: %s", resp.StatusCode)
        return false
    }

    return true
}
