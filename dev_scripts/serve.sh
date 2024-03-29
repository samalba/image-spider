#!/bin/sh

source $(dirname $0)/credentials.sh

app_file=/srv/http/interface/wsgi.py

sudo systemctl start nginx.service

sudo -Eu http uwsgi \
    --socket /tmp/uwsgi.sock \
    --file $app_file \
    --master \
    --enable-threads \
    --workers 1 \
    --touch-reload $app_file
