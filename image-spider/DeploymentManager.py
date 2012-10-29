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
        self._queue = []
        self._active = False
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:16.0) ' \
                          'Gecko/20100101 Firefox/16.0'
        self.delay = 5 # Seconds to sleep between requests for politeness.


    def _set_job_status(job_id, depth, index, total):

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
                  'percent': int(index / total * 1000) / 10
                  'at_depth': depth}

        data.redis.set('jobstatus:' + job_id, pickle.dumps(status))


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

            if not claim(url):
                continue

            validated_url = validate_url(url)

            if not validated_url['valid']:
                continue

            url = validated_url['url']
            webpage_info = data.get_webpage_info(url)

            # Ignore webpages crawled less than 15 min ago.
            if webpage_info['completion_datetime']:
                now = datetime.datetime.now()
                td = now - webpage_info['completion_datetime']
                if 900 > td.total_seconds():
                    continue

            # Database latency means depth is occasionally still unavailable.
            if not webpage_info['depth']:
                data.redis.set(url, 'ready')
                self._queue.append(url)
                continue

            depth = webpage_info['depth'] - 1

            #TODO: url on next line should be job_id
            _set_job_status(url, depth, index, len(queue_copy))

            html_parser = MyHtmlParser(url)
            request = urllib_Request(url,
                                     headers={'User-Agent': self.user_agent})
            try:
                webpage = urlopen(request).read().decode()
            except (HTTPError, URLError, UnicodeDecodeError) as error:
                #TODO:logging.error(error)
                data.redis.set(url, 'failed')
                continue

            html_parser.feed(webpage)
            data.add_webpages(url, html_parser.hyperlinks, depth)
            data.redis.set(url, 'complete')
            data.complete_crawl(url)

            time.sleep(self.delay)

            if 0 < depth:
                data.redis.publish('deploy',
                                   pickle.dumps(html_parser.hyperlinks))

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
