#!/usr/bin/env python3
# -*- coding: ascii -*-

"""
There is a script in dev_scripts called serve_crawl_target.py. It is expected to
be running prior to running these tests, in order to provide stable and
predictable results. It's also advised to run the spider with CRAWL_DELAY=0, or
to deploy multiple spiders, in order to avoid timeouts.
"""

import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '../interface'))
from CrawlTarget import CrawlTarget
from Disallowed import generate_disallowed_method_tests
from Crawl import CrawlGet, CrawlPost
from Result import ResultGetByJobId, ResultGetByUrl, ResultDelete
from Status import StatusGetByJobId, StatusGetByUrl
from Stop import StopPost


if __name__ == '__main__':

    # Test REST interface.

    disallowed_methods = {'get': ('stop',),
                          'post': ('status', 'result'),
                          'delete': ('crawl', 'stop', 'status')}

    tests = [CrawlTarget, CrawlGet, CrawlPost, StatusGetByJobId, StatusGetByUrl,
             ResultGetByUrl, ResultGetByJobId, ResultDelete, StopPost] + \
             generate_disallowed_method_tests(disallowed_methods)

    load = [unittest.TestLoader().loadTestsFromTestCase(test) for test in tests]
    suite = unittest.TestSuite(load)
    unittest.TextTestRunner(verbosity=2).run(suite)
