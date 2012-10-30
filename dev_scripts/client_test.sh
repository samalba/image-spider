#!/bin/sh
echo -e | nc localhost 8880 <<EOF
GET / HTTP/1.1
Host: x
Connection: close

EOF

