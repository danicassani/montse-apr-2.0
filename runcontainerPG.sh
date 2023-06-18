#!/bin/bash
docker rm -fv PostgresDB
source .env
# echo $POSTGRES_PASSWORD
docker run -d \
    --name PostgresDB \
    -p 5432:5432 \
    -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    -v /home/wsl/repositorios/montse-apr-2.0/db/postgresql/data:/var/lib/postgresql/data \
    postgres:14