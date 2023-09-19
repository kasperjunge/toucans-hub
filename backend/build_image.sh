#!/bin/bash

docker image prune -f
source ../.env
docker build -t toucans .