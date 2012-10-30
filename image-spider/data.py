# -*- coding: ascii -*-

class _Storefront:

    """
    Connect to data stores.
    """

    def __init__(self):
        import postgresql
        import redis

        conf = json.loads(open('../environment.json').read())

        pq = 'pq://{0}:{1}@{2}:{3}/image_spider'
        pq = pq.format(conf['DOTCLOUD_POSTGRES_SQL_LOGIN'],
                       conf['DOTCLOUD_POSTGRES_SQL_PASSWORD'],
                       conf['DOTCLOUD_POSTGRES_SQL_HOST'],
                       conf['DOTCLOUD_POSTGRES_SQL_PORT'])

        redis_credentials = {'host': conf['DOTCLOUD_REDIS_REDIS_HOST'],
                             'port': int(conf['DOTCLOUD_REDIS_REDIS_PORT']),
                             'password': conf['DOTCLOUD_REDIS_REDIS_PASSWORD'],
                             'db': 0}

        self.pg = postgresql.open(pq)
        self.redis = redis.StrictRedis(**redis_credentials)
        pubsub = redis.StrictRedis(**redis_credentials)
        self.pubsub = pubsub.pubsub()

        setattr(self, 'add_webpages',
                self.pg.proc('add_webpages(text,text[],integer)'))

        setattr(self, 'get_webpage_info',
                self.pg.proc('get_webpage_info(text)'))

        setattr(self, 'complete_crawl',
                self.pg.proc('complete_crawl(text)'))


data = _Storefront()
