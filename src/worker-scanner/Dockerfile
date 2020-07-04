FROM golang:latest

COPY ./src /app
RUN mkdir /app/bin
ENV GOBIN /go/bin

RUN apt update
RUN apt install -y nmap

WORKDIR /go/src/github.com/go-redis/redis/
RUN git clone https://github.com/go-redis/redis.git .
RUN git checkout v7

WORKDIR /app
RUN go get -d ./...
RUN go install

CMD ["/go/bin/app"]
