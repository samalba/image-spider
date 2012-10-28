# -*- coding: ascii -*-

import datetime
from http_error import http_error
import models
from responder import responder
from view import view

class crawl:

    """
    crawl is the controller for resource '/'. Issuing a GET returns usage
    documentation and a basic web UI. Issuing a POST asks spiders to crawl.
    """

    def __init__(self):
        self.webpages_model = models.webpages()
        self.spiders_model = models.spiders()


    def get(self):

        """
        """
        #TODO:docstring

        demo_view = view('demo.htm')
        return responder(demo_view, 'text/html')


    def post(self, querystring, postdata):

        """
        Posting to crawl (AKA /) requests spider(s) to crawl each of the
        specified webpages.

        Arguments:
            querystring: Optional string depth=n, where the default is 2.
            postdata: form-urlencoded string must contain newline-separated URLs
                      assigned to a 'urls' variable.

        Returns: HTTP 202 Accepted or 400 Bad Request.
        """

        if 'urls' in postdata:
            urls = postdata['urls'][0].splitlines()
        else:
            return http_error('400 Bad Request')

        qs = querystring
        if qs and 'depth' in qs and qs['depth'][0].isnumeric():
            depth = int(qs['depth'][0])
        else:
            depth = 0

        for url in urls:
            status = self.webpages_model.get_status(url)
            webpage_info = self.webpages_model.get_webpage_info(url)

            if 'processing' == status and depth > webpage_info['depth']:
                self.spiders_model.stop(url)

            elif webpage_info['completion_datetime']:
                # Ignore webpages with good depth crawled less than 15 min ago.
                now = datetime.datetime.now()
                td = now - webpage_info['completion_datetime']
                if 900 > td.total_seconds() and depth <= webpage_info['depth']:
                    urls.remove(url)

        self.webpages_model.add(urls, depth=depth)
        self.spiders_model.deploy(urls)

        return responder(None, None, '202 Accepted')
