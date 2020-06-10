#!/bin/bash
docker run --rm -it --env-file=$(pwd)/configs/postgres.env --name=gatherinfo-dev-api --net=gatherinfonet -v $(pwd)/:/develop/ python:3.8 /bin/bash
