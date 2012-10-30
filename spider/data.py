# -*- coding: ascii -*-

class _Storefront:

    """
    Connect to data stores.
    """

    def __init__(self):
        import os
        import postgresql

        pq = 'pq://{0}:{1}@{2}:{3}/image_spider'
        pq = pq.format(os.environ['DOTCLOUD_POSTGRES_SQL_LOGIN'],
                       os.environ['DOTCLOUD_POSTGRES_SQL_PASSWORD'],
                       os.environ['DOTCLOUD_POSTGRES_SQL_HOST'],
                       os.environ['DOTCLOUD_POSTGRES_SQL_PORT'])

        redis_cred = {'host': os.environ['DOTCLOUD_REDIS_REDIS_HOST'],
                      'port': int(os.environ['DOTCLOUD_REDIS_REDIS_PORT']),
                      'password': os.environ['DOTCLOUD_REDIS_REDIS_PASSWORD'],
                      'db': 0}

        self.pg = postgresql.open(pq)
        self.redis = redis.StrictRedis(**redis_cred)
        pubsub = redis.StrictRedis(**redis_cred)
        self.pubsub = pubsub.pubsub()

        setattr(self, 'add_webpages',
                self.pg.proc('add_webpages(text,text[],integer)'))

        setattr(self, 'get_webpage_info',
                self.pg.proc('get_webpage_info(text)'))

        setattr(self, 'complete_crawl',
                self.pg.proc('complete_crawl(text)'))


data = _Storefront()
