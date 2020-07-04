package main

import (
    "encoding/json"
    "io/ioutil"
    "net/http"
    "strings"
    "bytes"
    "log"
)

type FeedsResponse struct {
	Feeds []Feed `json:"feeds"`
}

type Feed struct {
    ID           int `json:"id"`
    Name         string `json:"name"`
    Description  string `json:"description"`
    Organization string `json:"organization"`
    URL          string `json:"url"`
    MetaURL      string `json:"meta_url"`
}

type PublicIPsResponse struct {
    IPs []string `json:"ips"`
}

type FeedTaskResponse struct {
    FeedTask FeedTask `json:"feed_task"`
}

type FeedTask struct {
    ByteSize int `json:"byte_size"`
    CVEFeedId int `json:"cve_feed_id"`
    SHA256 string `json:"sha256"`
    CVEAmount int `json:"cve_amount"`
    FeedModificationDate string `json:"feed_modification_date"`
}

type FeedSourceMetadata struct {
    LastModifiedDate string
    Size string
    SHA256 string
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

    if resp.StatusCode != 200 {
        return false
    }

    return true
}

func GetPublicIPs() ([]string, error) {
    var response PublicIPsResponse
    res, err := http.Get("http://lookoutstation-api/assets/ips/public")

    if err != nil {
        log.Printf("Could not fetch ip list from API: %s", err)
        return response.IPs, err
    }

    body, _ := ioutil.ReadAll(res.Body)
    err = json.Unmarshal(body, &response)

    if err != nil {
        log.Println("Could not process API response: %s", err)
        return response.IPs, err
    }

    return response.IPs, nil
}

func GetFeeds() ([]Feed, error) {
    var response FeedsResponse
    res, err := http.Get("http://lookoutstation-api/feeds")

    if err != nil {
        log.Println("Could not fetch feeds from API: %s", err)
        return response.Feeds, err
    }

    body, _ := ioutil.ReadAll(res.Body)
    err = json.Unmarshal(body, &response)

    if err != nil {
        log.Printf("Could not process API response: %s", err)
        return response.Feeds, err
    }

    return response.Feeds, nil
}

func GetLastFeedTask(id string) (FeedTask, error) {
	var response FeedTaskResponse
    res, err := http.Get("http://lookoutstation-api/feeds/" + id + "/tasks/latest")

    if err != nil {
        log.Printf("Could not fetch last feed task from API: %s", err)
        return response.FeedTask, err
    }

    if res.StatusCode != 200 {
        log.Println("Could not fetch last feed task from API")
        return response.FeedTask, err
    }

    body, _ := ioutil.ReadAll(res.Body)
	json.Unmarshal(body, &response)

    return response.FeedTask, nil
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
