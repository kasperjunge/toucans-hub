#!/bin/bash

# Source the environment variables
source ../.env

# Base docker command with --rm to remove container after exit
DOCKER_CMD="docker run --rm"

# If ENVIRONMENT is "dev", add the -it flags
if [ "$ENVIRONMENT" == "dev" ]; then
    DOCKER_CMD="$DOCKER_CMD -it"
fi

# Append the rest of the arguments to the docker command
DOCKER_CMD="$DOCKER_CMD \
    -v $(pwd):/app \
    -p 8000:8000 toucans"

# Run the constructed docker command
$DOCKER_CMD