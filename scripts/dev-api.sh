#!/bin/bash
docker run --rm -it --env-file=$(pwd)/configs/postgres.env --name=lookoutstation-dev-api --net=lookoutstationnet -v $(pwd)/:/develop/ python:3.8 /bin/bash
sudo rm -rf $(pwd)/api/lookoutstation_api.egg-info
