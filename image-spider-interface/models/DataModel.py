# -*- coding: ascii -*-

import postgresql
import redis

class DataModel:

    def __init__(self):
        pq = 'pq://image_spider:p3nV7qE0bbHaC8n8i@localhost/image_spider'
        self.pg = postgresql.open(pq)
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
