package main

import (
    "log"
    "time"
)

func ScanAssets() {
    ips, err := GetPublicIPs()

    if err != nil {
        log.Printf("Retrying in 10 seconds")
        time.Sleep(10 * time.Second)
        go ScanAssets()

        return
    }

    for _, ip := range ips {
        PublishToQueue("scans", ip + ":1-65535")
    }
}
