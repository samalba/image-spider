# -*- coding: ascii -*-

from . DataModel import DataModel
import pickle

class Spiders(DataModel):

    """
    This data model provides communication with the spiders, who are deployed as
    workers.
    """

    def stop(self, job_id):

        """
        Send an abort request to spiders for the specified Job ID.

        Arguments:
            job_id: integer Job ID to stop.

        Returns: None
        """

        previous_job_status = self.redis.get('job_status:' + str(job_id))
        if previous_job_status:
            job_status = pickle.loads(previous_job_status)
            job_status['state'] = 'Aborted'
        else:
            job_status = {'state': 'Aborted'}
        self.redis.set('job_status:' + str(job_id), pickle.dumps(job_status))



    def deploy(self, job_id):

        """
        We expect one or more spider instances to be listening. Deploy them to
        crawl the specified URLs.

        Arguments:
            job_id: string job_id that's registered with a list of URLs to
                    crawl.

        Returns: None
        """

        self.redis.publish('deploy', pickle.dumps(job_id))
