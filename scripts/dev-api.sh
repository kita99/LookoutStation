#!/bin/bash
docker run --rm -it --env-file=$(pwd)/src/configs/postgres.env -e "FLASK_APP=main.py" --name=lookoutstation-api-dev --net=lookoutstationnet -v $(pwd)/src/api:/app python:3.8 /bin/bash
sudo rm -rf $(pwd)/src/api/lookoutstation_api.egg-info
