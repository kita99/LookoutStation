#!/bin/bash
docker run --rm -it --env-file=$(pwd)/configs/postgres.env --name=lookoutstation-dev-frontend --net=lookoutstationnet -v $(pwd)/frontend:/develop/ node:lts-alpine /bin/bash
