package main

import (
    "github.com/jasonlvhit/gocron"
)

func main() {
    gocron.Every(1).Day().Do(ScanAssets)
    gocron.Every(1).Day().Do(FetchAllFeeds)
}
