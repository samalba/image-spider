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

    def get(self, querystring=None):

        """
        Get the status of crawling a given URL.

        Arguments:
            querystring: Integer job_id, job_id=<JOB_ID> assignment, or
                         url=<URL> assignment.
        Returns: JSON spider status
        """

        url = job_id = None

        if dict == type(querystring):
            if 'job_id' in querystring:
                job_id = int(querystring['job_id'][0])
            if 'url' in querystring:
                url = querystring['url'][0]
        else:
            job_id = int(querystring)

        job_id_specified = str(job_id).isnumeric()

        if not (url or job_id_specified):
            return http_error('400 Bad Request')

        job_status = json.dumps(self.jobs_model.get_status(job_id))

        status_view = view('status.json', {'url': url,
                                           'job_status': job_status})
        return responder(status_view)
