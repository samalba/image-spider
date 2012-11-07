# -*- coding: ascii -*-

from . DataModel import DataModel
import pickle

class jobs(DataModel):

    def get_id(self):

        """
        Issue a new ID for the next job.

        Arguments: None.

        Returns: integer Job ID.
        """

        self.redis.setnx('job_id', '-1')
        return self.redis.incr('job_id')


    def get_status(self, job_id):

        """
        Get the status of a job.

        Arguments:
            job_id: integer Job ID.

        Returns: dict job_status if job exists else None.
        """

        result = self.redis.get('job_status:' + str(job_id))
        return pickle.loads(result) if result else None


    def job_exists(self, job_id):

        """
        Check to see whether a job currently exists.

        Arguments:
            job_id: integer Job ID.

        Returns: boolean truth value.
        """

        return True if self.get_status(job_id) else False
