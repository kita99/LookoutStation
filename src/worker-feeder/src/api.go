package main

import (
    "compress/gzip"
    "encoding/json"
    "io/ioutil"
    "net/http"
    "strings"
    "strconv"
    "fmt"
    "bytes"
    "log"

    "./responses"
)

type Feed struct  {
    Name string `json:"name"`
    Description string `json:"description"`
    Organization string `json:"organization"`
    URL string `json:"url"`
    MetaURL string `json:"meta_url"`
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
    ID int `json:"id"`
    Message string `json:"message"`
}

func PublishToQueue(queue string, message string) bool {
    url := "http://lookoutstation-worker-master/publish"
    values := map[string]string{"queue": queue, "message": message}
    jsonRequest, _ := json.Marshal(values)

    resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonRequest))

    if err != nil {
        log.Printf("Could not publish message to queue: %s", err)
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

    if res.StatusCode != 200 {
        err := fmt.Errorf("Could not fetch feed from API (code %d)", res.StatusCode)
        log.Println(err)
        return feed, err
    }

    body, _ := ioutil.ReadAll(res.Body)
    err = json.Unmarshal(body, &feed)

    if err != nil {
        log.Printf("Could not fetch feed from API: %s", err)
        return feed, err
    }

    return feed, nil
}

func GetLastFeedTask(id string) (FeedTask, error) {
    var response struct {
        FeedTask FeedTask `json:"feed_task"`
    }

    res, err := http.Get("http://lookoutstation-api/feeds/" + id + "/tasks/latest")

    if err != nil {
        log.Printf("Could not fetch latest feed task from API: %s", err)
        return response.FeedTask, err
    }

    if res.StatusCode != 200 {
        log.Println("Could not fetch last feed task from API")
        return response.FeedTask, nil
    }

    body, _ := ioutil.ReadAll(res.Body)
	json.Unmarshal(body, &response.FeedTask)

    return response.FeedTask, nil
}

func CreateFeedTask(feedID string, feedTask FeedTask) (string, bool) {
    var response Response
    url := "http://lookoutstation-api/feeds/" + feedID + "/tasks"
    jsonRequest, _ := json.Marshal(feedTask)

    resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonRequest))

    if err != nil {
        log.Printf("Could not create feed task: %s", err)
        return "", false
    }

    if resp.StatusCode != 200 {
        return "", false
    }

    body, _ := ioutil.ReadAll(resp.Body)
	json.Unmarshal(body, &response)

    feedTaskID := strconv.Itoa(response.ID)

    return feedTaskID, true
}

func GetFeedSourceMetadata(metaURL string) (FeedSourceMetadata, error) {
    var split []string
    var feedSourceMetadata FeedSourceMetadata

    res, err := http.Get(metaURL)

    if err != nil {
        log.Printf("Could not fetch metadata from feed source: %s", err)
        return feedSourceMetadata, err
    }

    body, _ := ioutil.ReadAll(res.Body)
    body_string := string(body)

    lines := strings.Split(body_string, "\n")

    for _, line := range lines {
        split = strings.Split(line, ":")

        if split[0] == "lastModifiedDate" {
            feedSourceMetadata.LastModifiedDate = strings.Join(split[1:], ":")
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
        log.Printf("Could not fetch data from feed source: %s", err)
        return feedSourceData, err
    }

    reader, err := gzip.NewReader(res.Body)
    err = json.NewDecoder(reader).Decode(&feedSourceData)

    return feedSourceData, nil
}

func StoreCVES(feedID string, feedTaskID string, cves []responses.CVEItem) bool {
    url := "http://lookoutstation-api/feeds/" + feedID + "/tasks/" + feedTaskID + "/cves"

    request := struct {
        CVES []responses.CVEItem `json:"cves"`
    }{
        cves,
    }
    jsonRequest, _ := json.Marshal(request)

    resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonRequest))

    if err != nil {
        log.Printf("Could not create CVEs: %s", err)
        return false
    }

    if resp.StatusCode != 200 {
        log.Printf("Could not create CVEs: %s", err)
        return false
    }

    return true
}

func UpdateCVES(feedID string, feedTaskID string, cves []responses.CVEItem) bool {
    url := "http://lookoutstation-api/feeds/" + feedID + "/tasks/" + feedTaskID + "/cves"

    request := struct {
        CVES []responses.CVEItem `json:"cves"`
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
