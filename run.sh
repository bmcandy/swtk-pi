#!/bin/bash

# Load environment variables from .env
export $(grep -v '^#' .env | xargs)

# Replace placeholders in init.sql
envsubst < ./database/init.sql > ./database/init_resolved.sql

# Start the containers using docker-compose
docker-compose up -d