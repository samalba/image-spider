# -*- coding: ascii -*-

from initiate_crawl import initiate_crawl
import json
from request import request
import time
import unittest

class Get(unittest.TestCase):

    """
    Base class for GET tests.
    """

    def get_response(self, resource, query_string):

        """
        GET a response from a resource.

        Arguments:
            resource: string resource to GET.
            query_string: string query-string.

        Returns: tuple (dict request() response, dict json_response content).
        """

        response = request('GET', resource, query_string)
        is_404 = lambda: '404 Not Found' == response['http_status']

        for i in range(50):

            if not is_404():
                break

            time.sleep(1)

            response = request('GET', resource, query_string)

        if is_404():
            self.fail('Response was 404 Not Found for GET ' + resource + \
                      '?' + query_string)

        return response, json.loads(response['content'].decode())


    def wait_for_passing_content(self, resource, query_string, response_test):

        """
        Wait until we have a passing response if we're testing for content.

        Arguments:
            resource: string HTTP resource.
            query_string: string URL query_string
            response_test: function to test for acceptable response.

        Returns: None
        """

        test_name = self.id().rpartition('.')[2]
        # We accept tests named "test_content" for those inheriting from Get or
        # "runTest" for those instantiating it for use in setUp.
        if 'test_content' == test_name or 'runTest' == test_name:

            for i in range(50):

                response, json_response = self.get_response(resource,
                                                           query_string)
                self.response = response
                self.json_response = json_response

                if response_test():
                    break

                time.sleep(1)

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
        self.response, self.json_response = self.get_response(resource,
                                                              query_string)
        self.wait_for_passing_content(resource, query_string, response_test)


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
        self.response, self.json_response = self.get_response(resource,
                                                              query_string)
        self.wait_for_passing_content(resource, query_string, response_test)
