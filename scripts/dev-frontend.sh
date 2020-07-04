#!/bin/bash
docker run --rm -it --env-file=$(pwd)/src/configs/postgres.env --name=lookoutstation-frontend-dev --net=lookoutstationnet -v $(pwd)/src/frontend:/app node:lts-alpine /bin/bash
