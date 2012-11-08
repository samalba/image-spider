# -*- coding: ascii -*-

from . DataModel import DataModel

class webpages(DataModel):

    def add(self, child_urls, parent_url=None, depth=2):

        """
        Add a webpage to be crawled.

        Arguments:
            child_urls: list of strings URLs.
            parent_url: optional string URL.
            depth: optional integer depth to crawl before stopping. Level 0 is
                   not crawled.

        Returns: None.
        """

        if parent_url:
            add_webpages = self.pg.proc('add_webpages(text,text[],integer)')
            add_webpages(parent_url, child_urls, depth)
        else:
            add_webpages = self.pg.proc('add_webpages(text[],integer)')
            add_webpages(child_urls, depth)


    def get_status(self, url):

        """
        Get the crawl status of a given URL.

        Arguments:
            url: string URL.

        Returns: string status value.
        """

        return self.redis.get(url) or 'ready'


    def set_status(self, url, status):

        """
        Set the crawl status of a given URL.

        Arguments:
            url: string URL.
            status: string crawl status.

        Returns: Redis success.
        """

        return self.redis.set(url, status)


    def get_webpage_info(self, url):

        """
        Get metadata about a webpage.

        Arguments:
            url: string URL.

        Returns: dict result of get_webpage_info stored function.
        """

        get_webpage_info = self.pg.proc('get_webpage_info(text)')
        return get_webpage_info(url)


    def register_job(self, job_id, urls):

        """
        Register a new job for specified URLs.

        Arguments:
            job_id: integer Job ID.
            urls: list of string URLs.

        Returns: None.
        """

        if urls:
            self.redis.sadd('job' + str(job_id), *urls) # This gets appened.
            self.redis.sadd('job' + str(job_id) + ':init', *urls)
            for url in urls:
                self.redis.rpush('reg:' + url, job_id)


    def get_job_ids(self, url):

        """
        Retrieve the IDs of any jobs that crawled to a specified URL.

        Arguments:
            url: string URL.

        Returns: list of integer Job IDs.
        """

        key = 'reg:' + url
        length = self.redis.llen(key)
        byte_list = self.redis.lrange(key, 0, length)
        return [int(i) for i in byte_list]


    def delete(self, url):

        """
        Delete a crawled webpage, any associated images, and all descendant
        children and their associated images from the datastores.

        Arguments:
            url: string URL.

        Returns: boolean success value.
        """

        self.redis.delete((url, 'reg' + url))
        webpage_id = self.get_webpage_info(url)[0]
        if webpage_id:
            delete_tree = self.pg.proc('delete_tree(integer)')
            delete_tree(webpage_id)
            return True
        else:
            return False
