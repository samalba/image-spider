# -*- coding: ascii -*-

from . DataModel import DataModel
import pickle

class Jobs(DataModel):

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


    def get_init_urls(self, job_id):

        """
        Get initial URLs specified for a given Job ID.

        Arguments:
            job_id: integer Job ID.

        Returns: list of string URLs.
        """

        smembers = self.redis.smembers('job' + str(job_id) + ':init')
        return [member.decode() for member in smembers]
