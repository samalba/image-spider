# -*- coding: ascii -*-

import os
import postgresql
import redis

class DataModel:

    def __init__(self):
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
        pubsub_redis = redis.StrictRedis(**redis_cred)
        self.pubsub = pubsub_redis.pubsub()
