# -*- coding: ascii -*-

from urllib.request import urlparse

def validate_url(url, parent_url='http:'):

    """
    Validate a URL to be a string having an explicit recognized scheme.

    Arguments:
        url: string URL
        parent_url: optional string URL from which to inherit an implicit
                    scheme.

    Returns: dict having:
        valid: boolean truth value.
        url: string modified URL.
    """

    if bytes == type(url):
        url = url.decode()

    parsed_url = urlparse(url)

    if not parsed_url.scheme:
        parent_scheme = urlparse(parent_url).scheme or 'http'
        url = parent_scheme + ':' + url

    valid = parsed_url.scheme in ('http', 'https', '')

    return {'valid': valid, 'url': url}
