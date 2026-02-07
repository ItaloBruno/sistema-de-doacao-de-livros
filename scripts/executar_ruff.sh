#!/bin/bash

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

ruff check --fix \
    --line-length 79 \
    --select I,F,E,W,PL,PT \
    --ignore PLR0913,PLR2004

ruff format \
    --line-length 79

ruff check \
    --line-length 79 \
    --select I,F,E,W,PL,PT \
    --ignore PLR0913,PLR2004
