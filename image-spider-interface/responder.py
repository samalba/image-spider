# -*- coding: ascii -*-

def responder(content, content_type='application/json', status='200 OK'):

    """
    This is an HTTP responder to create a response for the client. This is used
    to pass the payload back to uwsgi's start_response.

    Arguments:
        content: string HTTP content
        content_type: Mime-type of content
        status: string HTTP status including code number and description.

    Returns: function response.
    """

    content_type += '; charset=utf-8'
    response_headers = [('Content-type', content_type)]

    def response(start_response):

        """
        Deliver the payload to start_response.

        Arguments:
            start_response: function provided by uwsgi to application.

        Returns: HTTP response.
        """

        start_response(status, response_headers)
        return content

    return response
