# -*- coding: ascii -*-

import json
import postgresql
import redis

class DataModel:

    def __init__(self):
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
        pubsub_redis = redis.StrictRedis(**redis_credentials)
        self.pubsub = pubsub_redis.pubsub()
