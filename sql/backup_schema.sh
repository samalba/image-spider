#!/bin/sh
pg_dump --create --oids --schema-only image_spider > $(dirname $0)/schema.sql
