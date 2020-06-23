FROM tiangolo/meinheld-gunicorn-flask:python3.8

COPY . /app
WORKDIR /app

RUN pip3 install -e .
EXPOSE 80
