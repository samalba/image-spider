# -*- coding: ascii -*-

class _Storefront:

    """
    Connect to data stores.
    """

    def __init__(self):
        import postgresql
        import redis

        pq = 'pq://image_spider:p3nV7qE0bbHaC8n8i@localhost/image_spider'
        self.pg = postgresql.open(pq)
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
        pubsub = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.pubsub = pubsub.pubsub()

        setattr(self, 'add_webpages',
                self.pg.proc('add_webpages(text,text[],integer)'))

        setattr(self, 'get_webpage_info',
                self.pg.proc('get_webpage_info(text)'))

        setattr(self, 'complete_crawl',
                self.pg.proc('complete_crawl(text)'))


data = _Storefront()
