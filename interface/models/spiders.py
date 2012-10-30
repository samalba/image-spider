# -*- coding: ascii -*-

from . DataModel import DataModel
import pickle

class spiders(DataModel):

    """
    This data model provides communication with the spiders, who are deployed as
    workers.
    """

    def stop(self, url):
        #TODO:docstring
        pass#TODO


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
