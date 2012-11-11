# -*- coding: ascii -*-

from http_error import http_error
import json
import models
from responder import responder
from view import view

class status:

    """
    Status provides information about webpages we have been asked to crawl.
    """

    def __init__(self):
        self.jobs_model = models.jobs()
        self.webpages_model = models.webpages()


    def get(self, query=None):

        """
        Get the status of crawling a given URL.

        Arguments:
            query: Integer job_id, job_id=<JOB_ID> assignment, or
                   url=<URL> assignment.
        Returns: JSON spider status
        """

        url = query['url'] if 'url' in query else None
        job_id = query['job_id'] if 'job_id' in query else None
        job_id_specified = int == type(job_id)
        webpage_id = None
        if url:
            webpage_id = self.webpages_model.get_webpage_info(url)['id']

        if not url and not job_id_specified:
            return http_error('400 Bad Request')

        if job_id_specified and not self.jobs_model.job_exists(job_id):
            return http_error('404 Not Found')
        elif url and not webpage_id:
            return http_error('404 Not Found')

        if job_id_specified:
            urls = json.dumps(self.jobs_model.get_init_urls(job_id))
            job_status = json.dumps(self.jobs_model.get_status(job_id))
        else:
            urls = json.dumps([url])
            get_status = self.jobs_model.get_status
            job_ids = self.webpages_model.get_job_ids(url)
            job_status_list = [get_status(job_id) for job_id in job_ids]
            job_status_list = [status for status in job_status_list if status]
            job_status = json.dumps(job_status_list)

        status_view = view('status.json', {'urls': urls,
                                           'job_status': job_status})
        return responder(status_view)
