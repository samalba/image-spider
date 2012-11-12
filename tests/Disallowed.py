# -*- coding: ascii -*-

import unittest
from request import request

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
