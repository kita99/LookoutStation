FROM python:3.8

COPY . /app
WORKDIR /app

RUN pip3 install .
WORKDIR /app/lookoutstation

EXPOSE 8080

CMD flask run --host=0.0.0.0 --port=8080
