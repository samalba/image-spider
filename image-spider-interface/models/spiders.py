# -*- coding: ascii -*-

from . DataModel import DataModel

class spiders(DataModel):

    """
    This data model provides communication with the spiders, who are deployed as
    workers.
    """

    def stop(self, url):
        #TODO:docstring
        pass#TODO


    def deploy(self, urls):

        """
        We expect one or more spider instances to be listening. Deploy them to
        crawl the specified URLs.

        Arguments:
            urls: list of string URLs to crawl.

        Returns: None
        """

        self.redis.publish('deploy', urls)
