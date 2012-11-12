# -*- coding: ascii -*-

import unittest

class MultiOp(unittest.TestCase):

    """
    This is a base class for multi-operational tests, meaning they must issue
    multiple requests sequentially.
    """

    def _mk_response_test(self, desired_job_states):

        """
        Make a response test for use with Get.wait_for_passing_content().

        Arguments:
            desired_job_states: iterable of string job states to match.

        Returns: function response_test.
        """

        def response_test():
            if dict == type(self.get.json_response) and \
                    'job_status' in self.get.json_response:
                job_status = self.get.json_response['job_status']
                return dict == type(job_status) and \
                       'state' in job_status and \
                       job_status['state'] in desired_job_states
            else:
                return False
        return response_test
