# -*- coding: ascii -*-

import os
import pickle
import postgresql
import redis

class _Storefront:

    """
    Connect to data stores.
    """

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
        pubsub = redis.StrictRedis(**redis_cred)
        self.pubsub = pubsub.pubsub()

        setattr(self, 'add_webpages',
                self.pg.proc('add_webpages(text,text[],integer)'))

        setattr(self, 'get_webpage_info',
                self.pg.proc('get_webpage_info(text)'))

        setattr(self, 'complete_crawl',
                self.pg.proc('complete_crawl(text)'))


    def abort(self, job_id):

        """
        Set the state of the specified job to 'Aborted', causing spider(s) to
        stop processing it.

        Arguments:
            job_id: integer Job ID.

        Returns: None.
        """

        previous_job_status = self.redis.get('job_status:' + str(job_id))
        if previous_job_status:
            job_status = pickle.loads(previous_job_status)
            job_status['state'] = 'Aborted'
        else:
            job_status = {'state': 'Aborted'}
        self.redis.set('job_status:' + str(job_id), pickle.dumps(job_status))


    def job_is_aborted(self, job_id):

        """
        Check to see whether the specified job has been aborted.

        Arguments:
            job_id: integer Job ID.

        Returns: boolean truth value.
        """

        job_status = self.redis.get('job_status:' + str(job_id))
        state = pickle.loads(job_status)['state'] if job_status else None
        return 'Aborted' == state


data = _Storefront()
