# -*- coding: ascii -*-

import wsgi
from WsgiInputStub import WsgiInputStub

def request(method, resource, query_string='', post_data=''):

    """
    HTTP request stub.

    Arguments:
        method: string HTTP method.
        resource: string REST resource.
        query_string: optional string HTTP query string.
        post_data: optional string HTTP post data.

    Returns: dict having:
        http_status: string HTTP response status code and description.
        other_headers: list of tuples, each a name-value pair of HTTP response
                       headers other than the status.
        content: string HTTP response content.
    """

    result = {}

    def store_headers(http_status, other_headers):
        result['http_status'] = http_status
        result['other_headers'] = other_headers

    env = {'REQUEST_METHOD': method.upper(),
           'PATH_INFO': resource,
           'QUERY_STRING': query_string,
           'wsgi.input': WsgiInputStub(post_data)}

    if 'POST' == method:
        env['CONTENT_LENGTH'] = len(post_data)

    result['content'] = wsgi.application(env, store_headers)

    return result
