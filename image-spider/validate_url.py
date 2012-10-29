# -*- coding: ascii -*-

from urllib.request import urlparse

def validate_url(url, parent_url='http:'):

    """
    """
    #TODO:docstring

    parsed_url = urlparse(url)

    if not parsed_url.scheme:
        parent_scheme = urlparse(parent_url).scheme or 'http'
        url = parent_scheme + ':' + url

    valid = parsed_url.scheme in ('http', 'https', '')

    return {'valid': valid, 'url': url}
