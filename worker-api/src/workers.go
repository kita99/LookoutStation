package main

import (
    "encoding/json"
    "strings"
    "io/ioutil"
    "net/http"
)

type Queue struct {
    Name string `json:"name"`
    Info map[string]string `json:"info"`
    Connections []map[string]string `json:"connections"`
}

func QueueStatusCheck(w http.ResponseWriter, r *http.Request) {
    resp, err := http.Get("http://gatherinfo-worker:8080/status")

    if err != nil {
        // handle error
    }

    defer resp.Body.Close()
    body, err := ioutil.ReadAll(resp.Body)
    body_string := string(body)

    if err != nil {
        // handle error
    }

    var stats []Queue
    currentStat := new(Queue)
    connections := map[string][]map[string]string{}
    connection := map[string]string{}
    var queueName string
    info := map[string]string{}

    lines := strings.Split(body_string, "\n")

    for index, value := range lines {
        if len(value) > 1 {
            if value[4:9] == "queue" || index == len(lines) - 2 {
                if index > 1 {
                    currentStat.Name = queueName

                    if _, ok := connections[queueName]; ok {
                        currentStat.Connections = connections[queueName]
                    }

                    stats = append(stats, *currentStat)
                }

                currentStat = new(Queue)
                info = map[string]string{}

                for _, val := range strings.Split(value, " ") {
                    key_value := strings.Split(val, ":")

                    if len(key_value) > 1 {
                        info[key_value[0]] = key_value[1]
                    }
                }

                currentStat.Info = info
                queueName = info["queue"]
            } else {
                connection = map[string]string{}

                for _, val := range strings.Split(value, " ") {
                    key_value := strings.Split(val, ":")

                    if len(key_value) > 1 {
                        if key_value[0] == "connection" {
                            connection["name"] = key_value[1]
                        } else {
                            connection[key_value[0]] = key_value[1]
                        }
                    }
                }

                connections[queueName] = append(connections[queueName], connection)
            }
        }
    }

    json_data, _ := json.Marshal(stats)

    w.Header().Set("Conten-Type", "application/json")
    w.Write(json_data)
}
