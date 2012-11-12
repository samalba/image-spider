# -*- coding: ascii -*-

from Get import Get
import json
from initiate_crawl import initiate_crawl
from MultiOp import MultiOp
from request import request
import time

class StopPost(MultiOp):

    """
    Test POST /stop
    """

    def setUp(self):
        self.get = Get()
        urls, response = initiate_crawl()
        json_response = json.loads(response['content'].decode())
        job_id = json_response['job_id']
        self.query_string = 'job_id=' + str(job_id)

        # Wait until the initiated crawl has begun.
        self.get.wait_for_passing_content('/status', self.query_string,
                                          self._mk_response_test(['Running',
                                                                 'Complete']))

        # Stop the crawl.
        self.response = request('POST', '/stop', self.query_string)

    def test_http_status(self):
        self.assertEqual(self.response['http_status'], '202 Accepted')

    def test_content(self):
        self.get.wait_for_passing_content('/status', self.query_string,
                                          self._mk_response_test(['Aborted']))

        # Test that total results do not increase over 3 seconds.
        response = request('GET', '/result', self.query_string)
        json_response = json.loads(response['content'].decode())
        len0 = len(json_response)
        time.sleep(3)
        response = request('GET', '/result', self.query_string)
        json_response = json.loads(response['content'].decode())
        len1 = len(json_response)
        self.assertEqual(len0, len1)
