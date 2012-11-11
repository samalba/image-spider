#!/bin/sh

function error {
    echo Error: $1
    exit 1
}

if [ 1 -gt $# ]; then error 'No command provided.'; fi

case $1 in

--help)
    echo -e "Available arguments:\n--reset\n--start DOMAIN_NAME\n--stop JOB_ID"
    ;;

--reset)
    redis-cli flushall
    psql image_spider -c 'DELETE FROM webpages;'
    psql image_spider -c 'DELETE FROM images;'
    ;;

--start)
    if [ 2 -gt $# ]; then error 'No DOMAIN_NAME provided.'; fi

    len=$(( 20 + $(echo $2 | wc -c) ))

    cat | nc 127.0.0.1 80 <<EOF
POST /?depth=4 HTTP/1.1
Host: image.spider
Content-Length: $len
Content-Type: application/x-www-form-urlencoded
Connection: close

urls=http%3A%2F%2F$2%2F
EOF
    ;;

--stop)
    if [ 2 -gt $# ]; then error 'No JOB_ID provided.'; fi

    cat | nc 127.0.0.1 80 <<EOF
POST /stop?job_id=$2 HTTP/1.1
Host: image.spider
Content-Length: 0
Content-Type: application/x-www-form-urlencoded
Connection: close

EOF
    ;;

*)
    error 'Unknown command.'
esac
