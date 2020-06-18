package main

import (
    "net/http"
    "bytes"
    "log"
)

func StoreScanResults(address string, scanResults []byte) bool  {
    resp, err := http.Post("http://lookoustation-api/scans/" + address, "application/json", bytes.NewBuffer(scanResults))

    if err != nil {
		log.Fatalf("Could not submit scan results: %v", err)
        return false
    }

    if resp.Status != "200" {
		log.Fatalf("Could not submit scan results: %v", err)
        return false
    }

    return true
}
