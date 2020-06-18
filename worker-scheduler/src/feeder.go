package main

import (
    "log"
)

func ProcessAllFeeds() {
    log.Println("Processing all feeds")

    feeds, err := GetFeeds()

    if err != nil {
        return
    }

    // Foreach one fetch the metadata url
    for _, feed := range feeds {
        feedMetadata, err := GetFeedSourceMetadata(feed.MetaURL)

        if err != nil {
            return
        }

        feedTask, err := GetLastFeedTask(feed.ID)

        if err != nil {
            return
        }

        if feedTask.SHA256 != feedMetadata.SHA256 {
            status := PublishToQueue("feeds", feed.ID)

            if !status {
                return
            }
        }
    }
}
