# -*- coding: ascii -*-

from Get import Get

class StatusGet(Get):

    """
    Base class for tests to GET /status.
    """

    def test_http_status(self):
        self.assertEqual(self.response['http_status'], '200 OK')

    def _test_job_status(self, job_status):
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


    def test_content(self):
        self.assertIn('urls', self.json_response)
        self.assertIn('job_status', self.json_response)
        urls = self.json_response['urls']
        self.assertEqual(list, type(urls))
        job_status = self.json_response['job_status']
        test_case = self.id().split('.')[1]
        if 'StatusGetByJobId' == test_case:
            self.assertEqual(dict, type(job_status))
            self._test_job_status(job_status)
        elif 'StatusGetByUrl' == test_case:
            self.assertEqual(list, type(job_status))
            self.assertGreater(len(job_status), 0)
            for status in job_status:
                self._test_job_status(status)


class StatusGetByUrl(StatusGet):

    """
    Test GET /status by ?url
    """

    def setUp(self):
        test = lambda: self.json_response['job_status']
        self.setUp_for_GetByUrl('/status', test)


class StatusGetByJobId(StatusGet):

    """
    Test GET /status by ?job_id
    """

    def setUp(self):
        test = lambda: self.json_response['job_status']
        self.setUp_for_GetByJobId('/status', test)
