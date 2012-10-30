# -*- coding: ascii -*-

from data import data
from redis.exceptions import WatchError

def claim(url):

    """
    Claim a URL for processing if it hasn't already been claimed by a concurrent
    spider.

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
