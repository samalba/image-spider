# -*- coding: ascii -*-

from . DataModel import DataModel
import pickle

class jobs(DataModel):

    def get_id(self):
        self.redis.setnx('job_id', '-1')
        return self.redis.incr('job_id')


    def get_status(self, job_id):
        result = self.redis.get('jobstatus:' + str(job_id))
        return pickle.loads(result) if result else None
