#!/bin/bash
docker run --rm -it --env-file=$(pwd)/configs/postgres.env --name=gatherinfo-dev-frontend --net=gatherinfonet -v $(pwd)/frontend:/develop/ node:lts-alpine /bin/bash
