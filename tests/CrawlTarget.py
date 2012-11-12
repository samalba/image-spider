#!/usr/bin/env python

# -*- coding: ascii -*-

import unittest
from urllib import request as url_request

class CrawlTarget(unittest.TestCase):

    def test_running(self):

        """
        Test that the crawl target is running.
        """

        content_len = len(url_request.urlopen('http://127.0.0.1:8000/').read())
        self.assertGreater(content_len, 0)
