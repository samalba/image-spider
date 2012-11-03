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
        self.images_model = models.images()


    def get(self, query=None):

        """
        Get a list of result images from a given web crawl.

        Arguments:
            query values:
                job_id: integer job id.

        Returns: JSON list of URLs referencing found image files.
        """

        #TODO:Allow this to support url queries too. Abstract status controller
        #     for GET method.

        if not query['job_id']:
            return http_error('400 Bad Request')

        images = self.images_model.get_by_job_id(query['job_id'])

        result_view = view('result.json', {'images': json.dumps(images)})
        return responder(result_view, 'application/json')


    def delete(self, query=None):

        """
        """
        #TODO:docstring

        pass#TODO
