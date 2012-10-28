# -*- coding: ascii -*-

from http_error import http_error
from responder import responder
from view import view

class status:

    """
    Status provides information about webpages we have been asked to crawl.
    """

    def get(self, querystring=None):

        """
        Get the status of crawling a given URL.

        Arguments:
            querystring: String URL or url=<URL> assignment

        Returns: JSON spider status
        """

        if dict == type(querystring):
            url = querystring['url'][0]
        else:
            url = querystring

        if not url:
            return http_error('400 Bad Request')

        #TODO:Complete this. Provide actual status.
        status_view = view('status.json', {'url': url})
        return responder(status_view)
