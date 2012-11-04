#!/usr/bin/env python3
# -*- coding: ascii -*-

from http.server import HTTPServer, BaseHTTPRequestHandler
import random
import signal

class http_handler(BaseHTTPRequestHandler):
    def do_GET(self):
        rnd = random.randint(1, 1E7)
        htm = '<!doctype html>\n<title>{}</title>\n' \
              '<a href="/{}"><img alt="{}" src="/{}"></a>'
        response = htm.format(rnd, rnd, rnd, rnd)
        self.send_response(200, 'OK')
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(bytes(response, 'utf8'))


def run(port):
    httpd = HTTPServer(('', port), http_handler)
    httpd.serve_forever()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda x,y: exit(0))
    run(8000)
