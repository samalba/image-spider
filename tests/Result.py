# -*- coding: ascii -*-

from Get import Get
from initiate_crawl import initiate_crawl
import json
from MultiOp import MultiOp
from request import request
from urllib import parse, request as url_request

class ResultGet(Get):

    """
    Base class for testing GET /result
    """

    def test_http_status(self):
        self.assertEqual(self.response['http_status'], '200 OK')

    def test_content(self):
        self.assertGreater(len(self.json_response), 0)
        parsed_image_url = url_request.urlparse(self.json_response[0])
        self.assertEqual(parsed_image_url.scheme, 'http')
        self.assertEqual(parsed_image_url.netloc, '127.0.0.1:8000')
        self.assertRegex(parsed_image_url.path, r'^/\d+$')


class ResultGetByUrl(ResultGet):

    """
    Test GET /result by ?url
    """

    def setUp(self):
        test = lambda: list == type(self.json_response) and \
                       len(self.json_response)
        self.setUp_for_GetByUrl('/result', test)


class ResultGetByJobId(ResultGet):

    """
    Test GET /result by ?job_id
    """

    def setUp(self):
        test = lambda: list == type(self.json_response) and \
                       len(self.json_response)
        self.setUp_for_GetByJobId('/result', test)


class ResultDelete(MultiOp):

    """
    Test DELETE /result
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
        response = request('POST', '/stop', self.query_string)
        self.assertEqual(response['http_status'], '202 Accepted')
        self.get.wait_for_passing_content('/status', self.query_string,
                                          self._mk_response_test(['Aborted']))

        # Delete the results.
        for url in urls:
            self.response = request('DELETE', '/result',
                                    'url=' + parse.quote(url))

    def test_http_status(self):
        self.assertEqual(self.response['http_status'], '204 No Content')

    def test_success(self):
        response = request('GET', '/result', self.query_string)
        json_response = json.loads(response['content'].decode())
        self.assertEqual(0, len(json_response))
