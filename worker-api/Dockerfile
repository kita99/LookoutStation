FROM golang:latest

COPY ./src /app/scannex
RUN mkdir /app/scannex/bin
ENV GOBIN /go/bin

WORKDIR /app/scannex
RUN go get -d ./...
RUN go install


EXPOSE 80
CMD ["/go/bin/scannex"]
