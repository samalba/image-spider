#!/usr/bin/env python3
# -*- coding: ascii -*-

import datetime
from html.parser import HTMLParser
import os
import pickle
import postgresql
import redis
from redis.exceptions import WatchError
import signal
import sys
import time
from urllib.request import urlparse, urlopen, Request as urllib_Request
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urldefrag

# Connect to data stores.
pq = 'pq://image_spider:p3nV7qE0bbHaC8n8i@localhost/image_spider'
pg = postgresql.open(pq)
redis_data = redis.StrictRedis(host='localhost', port=6379, db=0)
redis_pubsub = redis.StrictRedis(host='localhost', port=6379, db=0)
pubsub = redis_pubsub.pubsub()


def graceful_exit(signum, frame):
    #TODO:Cleanup
    sys.exit(0)


class MyHtmlParser(HTMLParser):

    def __init__(self, url):
        self.url = url
        self.hyperlinks = []
        super(MyHtmlParser, self).__init__()


    def handle_base(self, href):
        if href:
            self.url = href


    def handle_a(self, href):
        if href:
            validated_href = validate_url(href, self.url)
            if validated_href['valid']:
                target = urldefrag(urljoin(self.url, validated_href['url']))[0]
                self.hyperlinks.append(target)


    def handle_img(self, src):
        if src:
            relate_image = pg.proc('relate_image(text,text)')
            relate_image(self.url, urljoin(self.url, src))


    def handle_starttag(self, tag, attrs):

        def get_attr(arg_attr):
            matching_attrs = [attr for attr in attrs if arg_attr == attr[0]]
            return matching_attrs[0][1] if len(matching_attrs) else None

        if 'base' == tag:
            self.handle_base(get_attr('href'))

        elif 'a' == tag:
            self.handle_a(get_attr('href'))

        elif 'img' == tag:
            self.handle_img(get_attr('src'))


def claim(url):

    """
    Claim a URL for processing if it is available.

    Arguments:
        url: string URL to claim.

    Returns: boolean success.
    """

    try:
        pipe = redis_data.pipeline()
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


def validate_url(url, parent_url='http:'):

    """
    """
    #TODO:docstring

    parsed_url = urlparse(url)

    if not parsed_url.scheme:
        parent_scheme = urlparse(parent_url).scheme or 'http'
        url = parent_scheme + ':' + url

    valid = parsed_url.scheme in ('http', 'https', '')

    return {'valid': valid, 'url': url}


def deploy(urls):
    print('deploy', urls)#XXX

    """
    """
    #TODO:docstring

    add_webpages = pg.proc('add_webpages(text,text[],integer)')
    get_webpage_info = pg.proc('get_webpage_info(text)')
    complete_crawl = pg.proc('complete_crawl(text)')

    ua = 'Mozilla/5.0 (X11; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0'

    for index, url in enumerate(urls):

        if not claim(url):
            continue

        validated_url = validate_url(url)

        if not validated_url['valid']:
            continue

        url = validated_url['url']
        webpage_info = get_webpage_info(url)

        # Ignore webpages crawled less than 15 min ago.
        if webpage_info['completion_datetime']:
            now = datetime.datetime.now()
            td = now - webpage_info['completion_datetime']
            if 900 > td.total_seconds():
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
            redis_data.set(url, 'failed')
            continue

        html_parser.feed(webpage)
        add_webpages(url, html_parser.hyperlinks, depth)
        redis_data.set(url, 'complete')
        complete_crawl(url)

        time.sleep(5) # Sleep 5 seconds for politeness

        if 0 < depth:
            redis_data.publish('deploy',
                               pickle.dumps(html_parser.hyperlinks))


def main():

    pubsub.subscribe('deploy')
    for item in pubsub.listen():
        print('listen', item)#XXX
        if 'message' == item['type'] and 'deploy' == item['channel']:
            deploy(pickle.loads(item['data']))


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, graceful_exit) # `supervisorctl stop`
    signal.signal(signal.SIGINT, graceful_exit) # CTRL-C

    main()
