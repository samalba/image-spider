# -*- coding: ascii -*-

from data import data
import datetime
from claim import claim
from MyHtmlParser import MyHtmlParser
import pickle
import time
from urllib.request import urlopen, Request as urllib_Request
from urllib.error import HTTPError, URLError
from validate_url import validate_url

class DeploymentManager:

    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:16.0) ' \
                     'Gecko/20100101 Firefox/16.0'
        self.delay = 5 # Seconds to sleep between requests for politeness.
        self._queue = []
        self._active = False


    def _set_job_status(self, job_id, depth, index, total):

        """
        Set the spider's completion status for the current job.

        Arguments:
            job_id: integer id of the current job.
            depth: integer 0-based depth of current crawl level.
            index: integer in iteration of total URLs for this job.
            total: integer number of total URLs for this job.

        Returns: None.
        """

        depth += 1
        index += 1

        status = {'completed': index,
                  'total': total,
                  'percent': int(index / total * 1000) / 10,
                  'at_depth': depth}

        data.redis.set('jobstatus:' + job_id, pickle.dumps(status))


    def _less_than_15_min_ago(self, when):

        """
        Determine if a time was less than 15 minutes ago.

        Arguments:
            when: datetime to check.

        Returns: boolean truth value.
        """

        if not when:
            return False

        now = datetime.datetime.now()
        td = now - when
        return 900 > td.total_seconds()


    def _fetch_and_parse(self, url, depth):

        """
        Fetch a webpage and parse it for links and images.

        Arguments:
            url: string URL.
            depth: integer current depth.

        Returns: None.
        """

        html_parser = MyHtmlParser(url)
        request_headers = {'User-Agent': self.user_agent}
        request = urllib_Request(url, headers=request_headers)

        try:
            webpage = urlopen(request).read().decode()
        except (HTTPError, URLError, UnicodeDecodeError) as error:
            data.redis.set(url, 'failed')
            return

        html_parser.feed(webpage)
        data.add_webpages(url, html_parser.hyperlinks, depth)
        data.redis.set(url, 'complete')
        data.complete_crawl(url)

        if 0 < depth:
            data.redis.publish('deploy', pickle.dumps(html_parser.hyperlinks))


    def _deploy(self):

        """
        Deploy a spider to crawl the web. Use the DeploymentManager's enqueue
        method to specify which URLs to crawl. Depth should be assigned to each
        submitted URL prior to deployment.

        Arguments: None

        Returns: None
        """

        self._active = True
        queue_copy = self._queue[:]
        for index, url in enumerate(queue_copy):

            self._queue.remove(url)
            validated_url = validate_url(url)
            url = validated_url['url']
            webpage_info = data.get_webpage_info(url)

            if not claim(url):
                continue

            if not validated_url['valid']:
                continue

            # Ignore webpages crawled less than 15 min ago.
            if self._less_than_15_min_ago(webpage_info['completion_datetime']):
                continue

            # Database latency means depth is occasionally still unavailable.
            if not webpage_info['depth']:
                data.redis.set(url, 'ready')
                self._queue.append(url)
                continue

            depth = webpage_info['depth'] - 1

            #TODO: url on next line should be job_id
            self._set_job_status(url, depth, index, len(queue_copy))

            self._fetch_and_parse(url, depth)

            time.sleep(self.delay)

        if len(self._queue):
            self._deploy()
        else:
            self._active = False


    def enqueue(self, urls):

        """
        Enqueue URLs for the spider to crawl.

        Arguments:
            urls: list of string uniform resource locaters.

        Returns: None
        """

        self._queue.extend(urls)
        if not self._active:
            self._deploy()


    def abort(self):
        pass#TODO
