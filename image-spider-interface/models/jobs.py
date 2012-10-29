# -*- coding: ascii -*-

from . DataModel import DataModel

class jobs(DataModel):

    def get_id(self):
        self.redis.setnx('job_id', '-1')
        return self.redis.incr('job_id')
