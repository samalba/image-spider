#!/usr/bin/env python3
# -*- coding: ascii -*-

from data import data
import datetime
from MyHtmlParser import MyHtmlParser
import os
import pickle
from redis.exceptions import WatchError
import signal
import sys
import time
from urllib.request import urlopen, Request as urllib_Request
from urllib.error import HTTPError, URLError
from validate_url import validate_url


def graceful_exit(signum, frame):
    #TODO:Cleanup
    sys.exit(0)


def claim(url):

    """
    Claim a URL for processing if it is available.

    Arguments:
        url: string URL to claim.

    Returns: boolean success.
    """

    try:
        pipe = data.redis.pipeline()
        pipe.watch(url)
        current_status = (pipe.get(url) or b'').decode()
        pipe.multi()
        if 'processing' == current_status:
            success = False
        else:
            pipe.set(url, 'processing')
            success = True
        pipe.execute()

    except WatchError as e:
        success = False

    finally:
        pipe.reset()

    return success


def deploy(urls):
    print('deploy', urls)#XXX

    """
    """
    #TODO:docstring

    ua = 'Mozilla/5.0 (X11; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0'

    for index, url in enumerate(urls):

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
            print('  Defering', url)#XXX
            data.redis.set(url, 'ready')
            data.redis.publish('deploy', pickle.dumps([url]))
            continue

        depth = webpage_info['depth'] - 1
        print('depth', depth, 'complete', index + 1, 'of', len(urls),#XXX
            str(int((index + 1) / len(urls) * 100)) + '%', url)#XXX
        html_parser = MyHtmlParser(url)
        request = urllib_Request(url, headers={'User-Agent': ua})
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

        time.sleep(5) # Sleep 5 seconds for politeness

        if 0 < depth:
            data.redis.publish('deploy',
                               pickle.dumps(html_parser.hyperlinks))


def main():

    data.pubsub.subscribe('deploy')
    for item in data.pubsub.listen():
        if 'message' == item['type'] and 'deploy' == item['channel']:
            deploy(pickle.loads(item['data']))


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, graceful_exit) # `supervisorctl stop`
    signal.signal(signal.SIGINT, graceful_exit) # CTRL-C

    main()
