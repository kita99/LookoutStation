#!/bin/bash

docker run --rm -it --env-file=$(pwd)/configs/postgres.env --net=gatherinfonet -v $(pwd)/backend/:/develop/ python:3.8 /bin/bash
