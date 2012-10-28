# -*- coding: ascii -*-

"""
Image-Crawler
Copyright (c) 2012 Bryan Kaplan <bkaplan@botker.com>
License: MIT

Image-Crawler crawls the web for images. See README.md for usage.

Because this was written as a code challenge, no third-party libraries were
used.

TODO: Describe more.
    # REST methods should correspond to controller methods.
    # the controller is requested as the http resource. our default controller
    # is 'crawl'.

Dependencies:

"""
#TODO:above

import os
import signal
from urllib.parse import parse_qs

# cd to app dir for package imports and for view-file reads.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import controllers
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
    querystring = env['QUERY_STRING'] or None
    postdata = None
    if 'post' == method: # Read postdata.
        length = env['CONTENT_LENGTH']
        if length.isnumeric():
            length = int(length)
        else:
            response = error('411 Length Required')
            return response(start_response)
        postdata = parse_qs(env['wsgi.input'].read(length))

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
            response = error('405 Method Not Allowed')
    else:
        response = error('404 Not Found')

    # Return our HTTP response to uwsgi.
    return response(start_response)
