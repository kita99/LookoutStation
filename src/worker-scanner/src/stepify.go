package main

import (
    "fmt"
    "math"
    "strconv"
    "strings"
)

const (
    ChunkSize = 1000
)

type ScanStep struct {
    IP string
    Ports string
    Progress float64
}

func roundUp(number float64) int {
    return int(math.Ceil(number))
}

func StepifyScan(payload string) []ScanStep {
    var scanSteps []ScanStep
    var steps int
    var rangeStart int
    var rangeEnd int
    var end int

    split := strings.Split(payload, ":")

    if !strings.Contains(split[1], "-") {
        scanStep := ScanStep{
            IP: split[0],
            Ports: split[1],
            Progress: 100.0,
        }

        scanSteps = append(scanSteps, scanStep)
        return scanSteps
    }

    if split[1] != "-" {
        subSplit := strings.Split(split[1], "-")

        rangeStart, _ = strconv.Atoi(subSplit[0])
        rangeEnd, _ = strconv.Atoi(subSplit[1])
    } else {
        rangeStart = 0
        rangeEnd = 65535
    }

    steps = roundUp((float64(rangeEnd) - float64(rangeStart)) / float64(ChunkSize))
    progress := 0.0
    progressStep := 100.0 / float64(steps)

    for i := 1; i < steps + 1; i++ {
        start := rangeStart + (i * ChunkSize) - ChunkSize

        if start == 0 {
            start++
        }

        if i < steps {
            progress = progress + progressStep
            end = rangeStart + (i * ChunkSize)
        } else {
            progress = 100
            end = rangeEnd
        }

        scanStep := ScanStep{
            IP: split[0],
            Ports: fmt.Sprintf("%d-%d", start, end),
            Progress: math.Round(progress*100)/100,
        }

        scanSteps = append(scanSteps, scanStep)
    }

    return scanSteps
}
