# -*- coding: ascii -*-

def responder(content, content_type='application/json', status='200 OK'):

    """
    This is an HTTP responder to create a response for the client. This is used
    to pass the payload back to uwsgi's start_response.

    Arguments:
        content: string HTTP content or None
        content_type: String mime-type of content or None with no content
        status: string HTTP status including code number and description.

    Returns: function response.
    """

    response_headers = []
    if content_type:
        content_type += '; charset=utf-8'
        response_headers.append(('Content-type', content_type))

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
