# -*- coding: ascii -*-

from responder import responder
from view import view

def http_error(status):

    """
    Create an HTTP error response.

    Arguments:
        status: string HTTP status including code number and description.

    Returns: HTTP response
    """

    error_view = view('error.htm', {'error': status})
    response = responder(error_view, 'text/html', status)
    return response
