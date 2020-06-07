#!/bin/bash
docker run --rm -it --env-file=$(pwd)/configs/postgres.env --name=gatherinfodev --net=gatherinfonet -v $(pwd)/:/develop/ python:3.8 /bin/bash
