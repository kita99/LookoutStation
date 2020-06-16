FROM golang:latest

COPY ./src /app
RUN mkdir /app/bin
ENV GOBIN /go/bin

WORKDIR /go/src/github.com/go-redis/redis/
RUN git clone https://github.com/go-redis/redis.git .
RUN git checkout v7

WORKDIR /app
RUN go get -d ./...
RUN go install


EXPOSE 80
CMD ["/go/bin/app"]
