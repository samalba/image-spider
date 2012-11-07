# -*- coding: ascii -*-

import models
from responder import responder

class stop:

    """
    This is the controller for the resource /stop. It's purpose is to abort
    a crawl.
    """

    def __init__(self):
        self.spirders_model = models.spiders()


    def post(self, query, postdata):

        """
        Send an abort-crawl request.

        Arguments:

            query: dict query having one of the following parameters:
                url: Optional string URL, required if job_id is unspecified.
                job_id: Optional integer Job ID, required if url is unspecified.

            postdata: Ignored.

        Returns: None
        """

        if 'url' in query:
            self.spirders_model.stop(url=query['url'])
        else:
            self.spirders_model.stop(job_id=query['job_id'])

        return responder(None, None, '202 Accepted')
