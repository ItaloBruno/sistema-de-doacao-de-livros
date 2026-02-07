#!/bin/bash

if [ -f .env.testes ]; then
    export $(grep -v '^#' .env.testes | xargs)
fi

pytest \
    -p no:warnings \
    -s \
    -x \
    --cov=contextos_de_negocio \
    --cov=utilitarios \
    -vv

coverage html
