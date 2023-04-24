# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN mkdir mosaic_tx

COPY . /mosaic_tx

WORKDIR /mosaic_tx/python

VOLUME $(pwd)/results:/results