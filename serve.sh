#!/bin/sh

app_file=/srv/http/image-spider-interface/wsgi.py

export DOTCLOUD_POSTGRES_SQL_LOGIN='image_spider'
export DOTCLOUD_POSTGRES_SQL_PASSWORD='p3nV7qE0bbHaC8n8i'
export DOTCLOUD_POSTGRES_SQL_HOST='localhost'
export DOTCLOUD_POSTGRES_SQL_PORT=5432
export DOTCLOUD_REDIS_REDIS_HOST='localhost'
export DOTCLOUD_REDIS_REDIS_PORT=6379
export DOTCLOUD_REDIS_REDIS_PASSWORD=

sudo systemctl start nginx.service

sudo -Eu http uwsgi \
    --socket /tmp/uwsgi.sock \
    --file $app_file \
    --master \
    --enable-threads \
    --workers 1 \
    --touch-reload $app_file
