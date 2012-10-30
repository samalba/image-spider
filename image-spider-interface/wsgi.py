# -*- coding: ascii -*-

"""
Image-Crawler
Copyright (c) 2012 Bryan Kaplan <bkaplan@botker.com>
License: MIT

Image-Crawler crawls the web for images. See README.md for usage.

Because this was written for a code challenge, I used as few third-party
libraries as reasonable. Under normal circumstances I would probably at least
have relied on an router framework. But given that this is a relatively simple
application, it's acceptable.

Some general notes on the architecture:

* REST methods should correspond to controller methods.

* The default controller is 'crawl'.

* This interface code is separate from the spider code. Multiple spiders can be
  deployed simultaneously to share the workload.

* I chose to use postgresql and redis even though neo4j would have been a more
  appropriate choice for this app. But since neo4j support on dotCloud is still
  alpha, and I've had a variety of deployment setbacks already, I decided to
  stick with datastores I know will work. Switching to Neo4j would avoid the
  need to paginate results.

Dependencies: See requirements.txt.
"""

import os
import signal
from urllib.parse import parse_qs
import sys

# cd to app dir for package imports and for view-file reads.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Explicitly append this current.
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
# Append the path where dotCloud keeps its modules, since cd'ing loses them.
sys.path.append('/opt/ve/3.2/lib/python3.2/site-packages')
import controllers
from http_error import http_error
from responder import responder
import tests
from view import view


def application(env, start_response):

    """
    Main application for uwsgi to run.

    Arguments:
        env: array of server environmental variables.
        start_response: uwsgi function to start HTTP response.

    Returns: None
    """
    method = env['REQUEST_METHOD'].lower()
    controller_name = env['PATH_INFO'][1:] or 'crawl'
    querystring = parse_qs(env['QUERY_STRING']) or env['QUERY_STRING'] or None
    postdata = None

    if 'post' == method: # Read postdata.
        length = env['CONTENT_LENGTH']
        if length.isnumeric():
            length = int(length)
        else:
            response = http_error('411 Length Required')
            return response(start_response)
        postdata = parse_qs(env['wsgi.input'].read(length).decode())

    # If the controller is registered in controllers/__init__.py, and it offers
    # a method that corresponds with the HTTP method in use, then request a
    # response from it. Otherwise our response will be an HTTP error.
    if controller_name in controllers.__all__:
        controller = getattr(controllers, controller_name)()
        request = getattr(controller, method, None)
        if request:
            if 'post' == method:
                response = request(querystring, postdata)
            else:
                response = request(querystring) if querystring else request()
        else:
            response = http_error('405 Method Not Allowed')
    else:
        response = http_error('404 Not Found')

    # Return our HTTP response to uwsgi.
    return response(start_response)
