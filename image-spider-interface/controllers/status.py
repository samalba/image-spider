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
            querystring: Integer URL job_id, url=<URL> assignment, or
                         job_id=<JOB_ID> assignment.

        Returns: JSON spider status
        """

        url = job_id = None
        if dict == type(querystring):
            if 'url' in querystring:
                url = querystring['url'][0]
            if 'job_id' in querystring:
                job_id = int(querystring['job_id'][0])
        else:
            job_id = querystring

        if not url:
            return http_error('400 Bad Request')

        url = url or 'null'
        job_id = job_id if str(job_id).isnumeric() else 'null'

        #TODO:Complete this. Provide actual status.
        status_view = view('status.json', {'url': url, 'job_id': job_id})
        return responder(status_view)
