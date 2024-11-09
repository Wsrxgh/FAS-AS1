FROM ubuntu:22.04

WORKDIR /code

RUN apt update

RUN apt upgrade

RUN apt install -y python3 python3-pip

RUN pip install mesa numpy matplotlib flask

COPY ./wildfire/ /code/

CMD python3 /code/wildfire/api.py
