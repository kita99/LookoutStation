package main

import (
    "encoding/json"
    "io/ioutil"
    "net/http"
    "bytes"
    "fmt"
)

func PublishToQueue(queue string, message string) {
    url := "http://lookoutstation-worker-master/publish"
    values := map[string]string{"queue": queue, "message": message}
    jsonRequest, _ := json.Marshal(values)

    resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonRequest))

    if err != nil {
        fmt.Println("Could not communicate with master worker")
    }

    fmt.Println("response status:", resp.Status)
    fmt.Println("response headers:", resp.Header)

    body, _ := ioutil.ReadAll(resp.Body)
    fmt.Println("response body:", string(body))
}
