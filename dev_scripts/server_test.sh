#!/bin/sh
uwsgi --http-socket localhost:8880 --file current/wsgi.py
