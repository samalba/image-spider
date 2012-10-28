#!/usr/bin/env python3
# -*- coding: ascii -*-

import unittest
import wsgi

def request(method, resource, query_string=''):
    """
    HTTP request stub.

    Arguments:
        method: string HTTP method.
        resource: string REST resource.
        query_string: optional string HTTP query string.

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
           'QUERY_STRING': query_string}

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
        self.response = request('POST', '/') #TODO:We need to test postdata.

    def test_http_status(self):
        self.assertEqual(self.response['http_status'], '202 Accepted')

    def test_content(self):
        self.assertTrue(False, 'TODO')#TODO
#         print(self.response['content'])


class StatusGet(unittest.TestCase):
    def setUp(self):
        self.response = request('GET', '/status', 'http://example.com')#XXX

    def test_http_status(self):
        self.assertEqual(self.response['http_status'], '200 OK')

    def test_content(self):
        self.assertTrue(False, 'TODO')#TODO
#         print(self.response['content'])


class ResultGet(unittest.TestCase):
    def setUp(self):
        self.response = request('GET', '/result', 'http://example.com')#XXX

    #TODO


class ResultDelete(unittest.TestCase):
    def setUp(self):
        self.response = request('DELETE', '/result', 'http://example.com')#XXX
        #TODO


class StopPost(unittest.TestCase):
    def setUp(self):
        self.response = request('POST', '/stop', 'http://example.com')#XXX
        #TODO

if __name__ == '__main__':
    disallowed_methods = {'get': ('stop',),
                          'post': ('status', 'result')} #TODO:Add to this
    tests = [CrawlGet, CrawlPost, StatusGet, ResultGet, ResultDelete, StopPost]\
             + generate_disallowed_method_tests(disallowed_methods)
    load = [unittest.TestLoader().loadTestsFromTestCase(test) for test in tests]
    suite = unittest.TestSuite(load)
    unittest.TextTestRunner(verbosity=2).run(suite)
