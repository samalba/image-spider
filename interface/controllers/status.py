# -*- coding: ascii -*-

from http_error import http_error
import json
import models
from responder import responder
from view import view

class status:

    def __init__(self):
        self.jobs_model = models.jobs()

    """
    Status provides information about webpages we have been asked to crawl.
    """

    def get(self, query=None):

        """
        Get the status of crawling a given URL.

        Arguments:
            query: Integer job_id, job_id=<JOB_ID> assignment, or
                   url=<URL> assignment.
        Returns: JSON spider status
        """

        url = query['url'] if 'url' in query else None

        job_id_specified = str(query['job_id']).isnumeric()

        if not (url or job_id_specified):
            return http_error('400 Bad Request')

        job_status = json.dumps(self.jobs_model.get_status(query['job_id']))

        #TODO:Where url is specified, webpages_model.get_status and get_tree.

        status_view = view('status.json', {'url': url,#XXX
                                           'job_status': job_status})
        return responder(status_view)
