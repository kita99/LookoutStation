package status

import (
	"fmt"
	"net/http"

	"github.com/adjust/rmq"
)

func Health() {
	connection := rmq.OpenConnection("gatherinfo-reporter", "tcp", "redis:6379", 2)
	http.Handle("/status", NewHandler(connection))
    http.ListenAndServe(":8080", nil)
}

type Handler struct {
	connection rmq.Connection
}

func NewHandler(connection rmq.Connection) *Handler {
	return &Handler{connection: connection}
}

func (handler *Handler) ServeHTTP(writer http.ResponseWriter, request *http.Request) {
	queues := handler.connection.GetOpenQueues()
	stats := handler.connection.CollectStats(queues)
	fmt.Fprint(writer, stats)
}

