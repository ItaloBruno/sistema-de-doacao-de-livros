#!/bin/bash

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

fastapi \
    dev \
    $FASTAPI_APP_DEV
