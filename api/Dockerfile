FROM python:3.8

COPY . /app
WORKDIR /app

RUN pip3 install .
WORKDIR /app/lookoutstation

EXPOSE 80

CMD flask run --host=0.0.0.0 --port=80
