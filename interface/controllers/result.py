# -*- coding: ascii -*-

from http_error import http_error
import json
import models
from responder import responder
from view import view

class result:

    """
    This represents the result of a web crawl.
    """

    def __init__(self):
        self.images_model = models.Images()
        self.webpages_model = models.Webpages()


    def get(self, query=None):

        """
        Get a list of result images from a given web crawl.

        Arguments:
            query values:
                job_id: integer job id.

        Returns: JSON list of URLs referencing found image files.
        """

        if not query['job_id'] and not 'url' in query:
            return http_error('400 Bad Request')

        if query['job_id']:
            images = self.images_model.get_by_job_id(query['job_id'])
        else:
            images = self.images_model.get_by_url(query['url'])

        result_view = view('result.json', {'images': json.dumps(images)})
        return responder(result_view, 'application/json')


    def delete(self, query=None):

        """
        Delete the specified URL, all related images, and all crawled children
        of that URL from the datastores.

        Arguments:
            query values:
                url: string URL.

        Returns: HTTP 204 or 404.
        """

        if not 'url' in query:
            return http_error('400 Bad Request')

        if self.webpages_model.delete(query['url']):
            return responder(None, None, '204 No Content')
        else:
            return http_error('404 Not Found')
