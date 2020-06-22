package main

import (
    "encoding/json"
    "io/ioutil"
    "net/http"
    "strings"
    "bytes"
    "log"

    "./responses"
)

type Feed struct  {
    Name string `json:"name"`
    Description string `json:"description"`
    Organization string `json:"name"`
    URL string `json:"name"`
    MetaURL string `json:"name"`
}

type FeedSourceMetadata struct  {
    LastModifiedDate string
    Size string
    SHA256 string
}

type FeedTask struct {
    ByteSize string `json:"byte_size"`
    CVEFeedId string `json:"cve_feed_id"`
    SHA256 string `json:"sha256"`
    CVEAmount string `json:"cve_amount"`
    FeedModificationDate string `json:"feed_modification_date"`
    RawJSON responses.CVEFeed `json:"raw_json"`
}

type Response struct {
    ID string `json:"id"`
    Message string `json:"message"`
}

func PublishToQueue(queue string, message string) bool {
    url := "http://lookoutstation-worker-master/publish"
    values := map[string]string{"queue": queue, "message": message}
    jsonRequest, _ := json.Marshal(values)

    resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonRequest))

    if err != nil {
        log.Println("Could not publish message to queue: %s", err)
        return false
    }

    if resp.Status != "200" {
        return false
    }

    return true
}

func GetFeed(id string) (Feed, error) {
	var feed Feed
    res, err := http.Get("http://lookoutstation-api/feeds/" + id)

    if err != nil {
        log.Printf("Could not fetch feed from API: %s", err)
        return feed, err
    }

    body, _ := ioutil.ReadAll(res.Body)
	json.Unmarshal(body, &feed)

    return feed, nil
}

func GetLastFeedTask(id string) (FeedTask, error) {
	var feedTask FeedTask
    res, err := http.Get("http://lookoutstation-api/feeds/" + id + "/tasks/latest")

    if err != nil {
        log.Printf("Could not fetch latest feed task from API: %s", err)
        return feedTask, err
    }

    body, _ := ioutil.ReadAll(res.Body)
	json.Unmarshal(body, &feedTask)

    return feedTask, nil
}

func CreateFeedTask(feedTask FeedTask) (string, bool) {
    var response Response
    url := "http://lookoutstation-api/feeds/" + feedTask.CVEFeedId + "/tasks"
    jsonRequest, _ := json.Marshal(feedTask)

    resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonRequest))

    if err != nil {
        log.Println("Could not create feed task: %s": err)
        return "", false
    }

    if resp.StatusCode != 200 {
        return "", false
    }

    body, _ := ioutil.ReadAll(resp.Body)
	json.Unmarshal(body, &response)

    return response.ID, true
}

func GetFeedSourceMetadata(metaURL string) (FeedSourceMetadata, error) {
    var split []string
    var feedSourceMetadata FeedSourceMetadata

    res, err := http.Get(metaURL)

    if err != nil {
        log.Println("Could not fetch metadata from feed source: %s", err)
        return feedSourceMetadata, err
    }

    body, _ := ioutil.ReadAll(res.Body)
    body_string := string(body)

    lines := strings.Split(body_string, "\n")

    for _, line := range lines {
        split = strings.Split(line, ":")

        if split[0] == "lastModifiedDate" {
            feedSourceMetadata.LastModifiedDate = split[1]
        }

        if split[0] == "size" {
            feedSourceMetadata.Size = split[1]
        }

        if split[0] == "sha256" {
            feedSourceMetadata.SHA256 = split[1]
        }
    }

    return feedSourceMetadata, nil
}

func GetFeedSource(sourceURL string) (responses.CVEFeed, error) {
    var feedSourceData responses.CVEFeed

    res, err := http.Get(sourceURL)

    if err != nil {
        log.Println("Could not fetch data from feed source: %s", err)
        return feedSourceData, err
    }

    body, _ := ioutil.ReadAll(res.Body)
	json.Unmarshal(body, &feedSourceData)

    return feedSourceData, nil
}

func StoreCVES(feedID string, feedTaskID string, cves []responses.CVE) bool {
    url := "http://lookoutstation-api/feeds/" + feedID + "/tasks/" + feedTaskID + "/cves"

    request := struct {
        CVES []responses.CVE `json:"cves"`
    }{
        cves,
    }
    jsonRequest, _ := json.Marshal(request)

    resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonRequest))

    if err != nil {
        log.Println("Could not create CVEs: %s", err)
        return false
    }

    if resp.StatusCode != 200 {
        log.Println("Could not create CVEs: %s", err)
        return false
    }

    return true
}

func UpdateCVES(feedID string, feedTaskID string, cves []responses.CVE) bool {
    url := "http://lookoutstation-api/feeds/" + feedID + "/tasks/" + feedTaskID + "/cves"

    request := struct {
        CVES []responses.CVE `json:"cves"`
    }{
        cves,
    }
    jsonRequest, _ := json.Marshal(request)

    client := &http.Client{}
    req, err := http.NewRequest(http.MethodPut, url, bytes.NewBuffer(jsonRequest))

    if err != nil {
		log.Printf("Could not update cves: %s", err)
        return false
    }

    req.Header.Set("Content-Type", "application/json; charset=utf-8")
    resp, err := client.Do(req)

    if err != nil {
		log.Printf("Could not update cves: %s", err)
        return false
    }

    if resp.StatusCode != 200 {
		log.Printf("Could not update cves: %s", err)
        return false
    }

    return true
}
