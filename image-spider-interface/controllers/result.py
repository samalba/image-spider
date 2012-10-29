# -*- coding: ascii -*-

from http_error import http_error
import json
import models
from responder import responder
from view import view

class result:

#TODO:Docstrings
    """
    """

    def __init__(self):
        self.images_model = models.images()


    def get(self, querystring=None):

        """
        Get a list of result images from a given web crawl.

        Arguments:
            querystring: job_id=<JOB_ID>

        Returns: JSON list of URLs referencing found image files.
        """

        #TODO:Add pagination support. See images controller, get_tree.

        #TODO:Allow this to support url queries too. Abstract status controller
        #     for GET method.

        if dict == type(querystring) and 'job_id' in querystring:
            job_id = int(querystring['job_id'][0])
        else:
            return http_error('400 Bad Request')

        images = self.images_model.get_by_job_id(job_id)

        result_view = view('result.json', {'images': json.dumps(images)})
        return responder(result_view, 'application/json')


    def delete(self, querystring=None):

        """
        """
        #TODO:docstring

        pass#TODO
