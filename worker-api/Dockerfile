FROM golang:latest

COPY ./src /app
RUN mkdir /app/bin
ENV GOBIN /go/bin

WORKDIR /app
RUN go get -d ./...
RUN go install


EXPOSE 80
CMD ["/go/bin/scannex"]
