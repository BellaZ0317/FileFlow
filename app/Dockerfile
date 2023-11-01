FROM python:3.6

MAINTAINER Bella Zhong "abigailzhong219@gmail.com"

COPY . /fileflow
WORKDIR /fileflow

RUN pip install -r /fileflow/requirements.txt

CMD python /fileflow/server.py
