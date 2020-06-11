FROM python:3.8

COPY . /app/lookoutstation/

WORKDIR /app/lookoutstation/
RUN pip3 install -r requirements.txt

CMD flask run --host=0.0.0.0 --port=8080
