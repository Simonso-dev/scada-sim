#!/bin/bash

sudo docker compose up database &
DATABASE_PID=$!
echo "Database PID: $DATABASE_PID"

sudo docker compose up scadalts &
SCADALTS_PID=$!
echo "Scadalts PID: $SCADALTS_PID"

export DATABASE_PID
export SCADALTS_PID
