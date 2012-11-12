# -*- coding: ascii -*-

from initiate_crawl import initiate_crawl
import json
from request import request
import unittest

class CrawlGet(unittest.TestCase):

    """
    Test GET /crawl
    """

    def setUp(self):
        self.response = request('GET', '/')

    def test_http_status(self):
        self.assertEqual(self.response['http_status'], '200 OK')

    def test_content_type(self):
        known_content_types = ['application/json', 'text/html']
        # We assume that other_headers is a list of tuples.
        content_type = [header for header in self.response['other_headers'] if
                        lambda header: header[0] == 'Content-type'][0][1]
        content_type = [string.strip() for string in content_type.split(';')]
        self.assertIn(content_type[0], known_content_types)
        self.assertEqual(content_type[1], 'charset=utf-8')


class CrawlPost(unittest.TestCase):

    """
    Test POST /crawl
    """

    def setUp(self):
        self.response = initiate_crawl()[1]

    def test_http_status(self):
        self.assertEqual(self.response['http_status'], '202 Accepted')

    def test_content(self):
        json_response = json.loads(self.response['content'].decode())
        self.assertIn('job_id', json_response)
        self.assertEqual(int, type(json_response['job_id']))
