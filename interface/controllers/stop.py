# -*- coding: ascii -*-

from http_error import http_error
import models
from responder import responder

class stop:

    """
    This is the controller for the resource /stop. It's purpose is to abort
    a crawl.
    """

    def __init__(self):
        self.spiders_model = models.Spiders()
        self.jobs_model = models.Jobs()


    def post(self, query, postdata):

        """
        Send an abort-crawl request.

        Arguments:

            query: dict query having the following parameter:
                job_id: integer Job ID.

            postdata: Ignored.

        Returns: None
        """

        job_id = query['job_id']
        if self.jobs_model.job_exists(job_id):
            self.spiders_model.stop(job_id)
            return responder(None, None, '202 Accepted')
        else:
            return http_error('404 Not Found')
