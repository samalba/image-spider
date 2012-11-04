# -*- coding: ascii -*-

"""
Image-Crawler
Copyright (c) 2012 Bryan Kaplan <bkaplan@botker.com>
License: MIT

Image-Crawler crawls the web for images. See README.md for details.

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
# Append the path where dotCloud keeps its modules.
sys.path.append('/opt/ve/3.2/lib/python3.2/site-packages')
import controllers
from http_error import http_error
from responder import responder
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

    # We accept two forms of query-strings. The first form is key-value pairs.
    # When using the first form, we only consider the first provided value for
    # any given key. The second form is an integer that implicitly designates
    # a job_id value.
    #
    # In either case, the query dict delivered to every controller has
    # a guaranteed value assignment, even if that value is None. No other query
    # variables are guaranteed.
    #
    querystring = parse_qs(env['QUERY_STRING']) or env['QUERY_STRING'] or None
    try:
        query = {k:v[0] for k,v in querystring.items()}
    except AttributeError:
        query = {'job_id': querystring}
    try:
        query['job_id'] = int(query['job_id'])
    except (KeyError, TypeError, ValueError):
        query['job_id'] = None

    # If the controller is registered in controllers/__init__.py, and it offers
    # a method that corresponds with the HTTP method in use, then request a
    # response from it. Otherwise our response will be an HTTP error.
    if controller_name in controllers.__all__:
        controller = getattr(controllers, controller_name)()
        request = getattr(controller, method, None)
        if request:
            if 'post' == method:
                try:
                    length = int(env['CONTENT_LENGTH'])
                except KeyError:
                    response = http_error('411 Length Required')
                    return response(start_response)
                postdata = parse_qs(env['wsgi.input'].read(length).decode())

                response = request(query, postdata)
            else:
                response = request(query) if query else request()
        else:
            response = http_error('405 Method Not Allowed')
    else:
        response = http_error('404 Not Found')

    # Return our HTTP response to uwsgi.
    return response(start_response)
