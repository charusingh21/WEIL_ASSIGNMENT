#!/bin/bash

## Build the Docker image
docker build -t flask-api .

## Run the Docker container
docker-compose up
