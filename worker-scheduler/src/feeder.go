package main

import (
    "log"
    "strconv"
)

func ProcessAllFeeds() {
    log.Println("Processing all feeds")

    feeds, err := GetFeeds()

    if err != nil {
        return
    }

    // Foreach one fetch the metadata url
    for _, feed := range feeds {
        feedID := strconv.Itoa(feed.ID)
        feedMetadata, err := GetFeedSourceMetadata(feed.MetaURL)

        if err != nil {
            return
        }

        feedTask, err := GetLastFeedTask(feedID)

        if err != nil {
            return
        }

        if feedTask == (FeedTask{}) {
            status := PublishToQueue("feeds", feedID + ":populate")

            if !status {
                return
            }

            return
        }

        if feedTask.SHA256 != feedMetadata.SHA256 {
            status := PublishToQueue("feeds", feedID)

            if !status {
                return
            }
        }
    }
}
