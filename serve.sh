#!/bin/sh

app_file=/srv/http/image-spider-interface/wsgi.py

sudo systemctl start nginx.service

sudo -u http uwsgi \
    --socket /tmp/uwsgi.sock \
    --file $app_file \
    --master \
    --enable-threads \
    --workers 1 \
    --touch-reload $app_file
