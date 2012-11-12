# -*- coding: ascii -*-

import random
from request import request
from urllib import parse

def _get_test_urls(count):
    # We use the crawl target, served from dev_scripts/serve_crawl_target.py.
    base_url = 'http://127.0.0.1:8000/'
    return [base_url + str(random.randint(1, 1E7)) for i in range(3)]


def initiate_crawl():
    urls = _get_test_urls(3)
    quoted_urls = parse.quote('\n'.join(urls))
    return urls, request('POST', '/', post_data='urls=' + quoted_urls)
