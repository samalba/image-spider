#!/usr/bin/env python3
# -*- coding: ascii -*-

"""
There is a script in dev_scripts called serve_crawl_target.py. It is expected to
be running prior to running these tests, in order to provide stable and
predictable results.
"""

import json
import os
import random
import sys
import time
import unittest
from urllib import parse, request as url_request
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '../interface'))
import wsgi

class WsgiInputStub:

    """
    Stub out wsgi.input's read method for wsgi.py.
    """

    def __init__(self, post_data):
        self.post_data = post_data

    def read(self, length):
        return bytes(self.post_data[0:length], 'utf8')


def request(method, resource, query_string='', post_data=''):
    """
    HTTP request stub.

    Arguments:
        method: string HTTP method.
        resource: string REST resource.
        query_string: optional string HTTP query string.
        post_data: optional string HTTP post data.

    Returns: dict having:
        http_status: string HTTP response status code and description.
        other_headers: list of tuples, each a name-value pair of HTTP response
                       headers other than the status.
        content: string HTTP response content.
    """
    result = {}

    def store_headers(http_status, other_headers):
        result['http_status'] = http_status
        result['other_headers'] = other_headers

    env = {'REQUEST_METHOD': method.upper(),
           'PATH_INFO': resource,
           'QUERY_STRING': query_string,
           'wsgi.input': WsgiInputStub(post_data)}

    if post_data:
        env['CONTENT_LENGTH'] = len(post_data)

    result['content'] = wsgi.application(env, store_headers)

    return result


class Disallowed(type):
    """
    This is a metaclass for disallowing HTTP methods. It's used by the function
    generate_disallowed_method_tests to create unittest classes for each
    disallowed method of each resource available.

    Arguments:
        name: string class name.
        method: string HTTP method.
        resource: string REST resource.

    Returns: unittest class
    """
    def __new__(cls, name, method, resource):

        def setUp(self):
            self.response = request(method, resource)

        def test_http_status(self):
            self.assertEqual(self.response['http_status'],
                             '405 Method Not Allowed')

        cls.dct = {'setUp': setUp, 'test_http_status': test_http_status}

        return type.__new__(cls, name, (unittest.TestCase,), cls.dct)

    def __init__(cls, name, method, resource):
        super(Disallowed, cls).__init__(name, (unittest.TestCase,), cls.dct)


def generate_disallowed_method_tests(disallowed_methods):
    """
    Use the Disallowed metaclass to create unittest classes for disallowed
    methods.

    Arguments:
        disallowed_methods: dict of tuples, where keys represent HTTP methods
                            and tuple values represent REST resources.

    Returns: list of unittest classes.
    """
    result = []

    for method in disallowed_methods:
        for resource in disallowed_methods[method]:
            name = resource.capitalize() + method.capitalize()
            resource = '/' + resource
            result.append(Disallowed(name, method, resource))

    return result


def get_test_urls(count):
    # We use the crawl target, served from dev_scripts/serve_crawl_target.py.
    base_url = 'http://127.0.0.1:8000/'
    return [base_url + str(random.randint(1, 1E7)) for i in range(3)]


def initiate_crawl():
    urls = get_test_urls(3)
    quoted_urls = parse.quote('\n'.join(urls))
    return urls, request('POST', '/', post_data='urls=' + quoted_urls)


class Get(unittest.TestCase):

    """
    Base class for GET tests.
    """

    def get_response(self, resource, query_string):
        self.response = request('GET', resource, query_string)
        self.json_response = json.loads(self.response['content'].decode())


    def wait_for_passing_response(self, resource, query_string, response_test):

        """
        Wait until we have a passing response if we're testing for content.

        Arguments:
            resource: string HTTP resource.
            query_string: string URL query_string
            response_test: function to test for acceptable response.

        Returns: None
        """

        if 'test_content' == self.id().rpartition('.')[2]:
            for i in range(50):
                if response_test():
                    break
                time.sleep(1)
                self.get_response(resource, query_string)
            if not response_test():
                self.fail('response_test never passed.')


    def setUp_for_GetByJobId(self, resource, response_test):

        """
        This is a setUp helper for tests classes that get by job_id. It sets the
        get_response and json_response properties.

        Arguments:
            resource: string HTTP resource.
            response_test: function to test for acceptable response.

        Returns: None
        """

        self.response = initiate_crawl()[1]
        json_response = json.loads(self.response['content'].decode())
        query_string = 'job_id=' + str(json_response['job_id'])
        self.get_response(resource, query_string)
        self.wait_for_passing_response(resource, query_string, response_test)


    def setUp_for_GetByUrl(self, resource, response_test):

        """
        This is a setUp helper for tests classes that get by URL. It sets the
        get_response and json_response properties.

        Arguments:
            resource: string HTTP resource.
            response_test: function to test for acceptable response.

        Returns: None
        """

        urls, self.response = initiate_crawl()
        json_response = json.loads(self.response['content'].decode())
        query_string = 'url=' + urls[0]
        self.get_response(resource, query_string)
        self.wait_for_passing_response(resource, query_string, response_test)


class CrawlTarget(unittest.TestCase):
    def test_running(self):
        content_len = len(url_request.urlopen('http://127.0.0.1:8000/').read())
        self.assertGreater(content_len, 0)


class CrawlGet(unittest.TestCase):
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
    def setUp(self):
        self.response = initiate_crawl()[1]

    def test_http_status(self):
        self.assertEqual(self.response['http_status'], '202 Accepted')

    def test_content(self):
        json_response = json.loads(self.response['content'].decode())
        self.assertIn('job_id', json_response)
        self.assertEqual(int, type(json_response['job_id']))


class StatusGetByUrl(Get):

    def setUp(self):
        test = lambda: self.json_response['url']
        self.setUp_for_GetByUrl('/status', test)

    def test_http_status(self):
        self.assertEqual(self.response['http_status'], '200 OK')

    def test_content(self):
        json_response = json.loads(self.response['content'].decode())
        self.fail('TODO')#TODO


class StatusGetByJobId(Get):

    def setUp(self):
        test = lambda: self.json_response['job_status']
        self.setUp_for_GetByJobId('/status', test)

    def test_http_status(self):
        self.assertEqual(self.response['http_status'], '200 OK')

    def test_content(self):
        self.assertIn('url', self.json_response)#TODO:This may change or be
                                            #incomplete.
        self.assertIn('job_status', self.json_response)
        job_status = self.json_response['job_status']
        self.assertEqual(dict, type(job_status))
        self.assertIn('current_depth', job_status)
        self.assertEqual(int, type(job_status['current_depth']))
        self.assertIn('depth_percent_complete', job_status)
        self.assertIn(type(job_status['depth_percent_complete']), [int, float])
        self.assertIn('pages_completed_at_depth', job_status)
        self.assertEqual(int, type(job_status['pages_completed_at_depth']))
        self.assertIn('pages_completed_at_greater_depth', job_status)
        self.assertEqual(int,
                         type(job_status['pages_completed_at_greater_depth']))
        self.assertIn('total_depth', job_status)
        self.assertEqual(int, type(job_status['total_depth']))
        self.assertIn('total_pages_at_depth', job_status)
        self.assertEqual(int, type(job_status['total_pages_at_depth']))
        self.assertIn('total_pages_completed', job_status)
        self.assertEqual(int, type(job_status['total_pages_completed']))
        self.assertIn('total_pages_queued', job_status)
        self.assertEqual(int, type(job_status['total_pages_queued']))


class ResultGet(Get):

    """
    This class is inherited by ResultGetByUrl and ResultGetByJobId.
    """

    def test_http_status(self):
        self.assertEqual(self.response['http_status'], '200 OK')

    def test_content(self):
        self.assertEqual(1, len(self.json_response))
        parsed_image_url = url_request.urlparse(self.json_response[0])
        self.assertEqual(parsed_image_url.scheme, 'http')
        self.assertEqual(parsed_image_url.netloc, '127.0.0.1:8000')
        self.assertRegex(parsed_image_url.path, r'^/\d+$')


class ResultGetByUrl(ResultGet):
    def setUp(self):
        test = lambda: list == type(self.json_response) and \
                       len(self.json_response)
        self.setUp_for_GetByUrl('/result', test)


class ResultGetByJobId(ResultGet):

    def setUp(self):
        test = lambda: list == type(self.json_response) and \
                       len(self.json_response)
        self.setUp_for_GetByJobId('/result', test)


class ResultDelete(unittest.TestCase):
    def setUp(self):
        # TODO:We need to request for this and then get it separately.
#         self.response = request('DELETE', '/result', get_test_urls(1))
        pass#XXX

    def test_http_status(self):
        self.assertEqual(self.response['http_status'], '200 OK')#XXX correct?

    def test_content(self):
        self.fail('TODO')#TODO


class StopPostByUrl(unittest.TestCase):
    def setUp(self):
        # TODO:We need to request for this and then get it separately.
#         self.response = request('POST', '/stop', get_test_urls(1))
        pass#XXX

    def test_http_status(self):
        self.assertEqual(self.response['http_status'], '200 OK')

    def test_content(self):
        self.fail('TODO')#TODO


class StopPostByJobId(unittest.TestCase):
    def setUp(self):
        # TODO:We need to request for this and then get it separately.
#         self.response = request('POST', '/stop', get_test_urls(1))
        pass#XXX

    def test_http_status(self):
        self.assertEqual(self.response['http_status'], '200 OK')

    def test_content(self):
        self.fail('TODO')#TODO


if __name__ == '__main__':
    #TODO:Test for bad request, length requered, etc.
    disallowed_methods = {'get': ('stop',),
                          'post': ('status', 'result')} #TODO:Add to this
    tests = [CrawlTarget, CrawlGet, CrawlPost, StatusGetByJobId, StatusGetByUrl,
             ResultGetByUrl, ResultGetByJobId, ResultDelete, StopPostByUrl,
             StopPostByJobId] + \
             generate_disallowed_method_tests(disallowed_methods)
    load = [unittest.TestLoader().loadTestsFromTestCase(test) for test in tests]
    suite = unittest.TestSuite(load)
    unittest.TextTestRunner(verbosity=2).run(suite)
