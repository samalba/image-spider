# -*- coding: ascii -*-

from . DataModel import DataModel

class webpages(DataModel):

    def add(self, child_urls, parent_url=None, depth=2):
        if parent_url:
            add_webpages = self.pg.proc('add_webpages(text,text[],integer)')
            add_webpages(parent_url, child_urls, depth)
        else:
            add_webpages = self.pg.proc('add_webpages(text[],integer)')
            add_webpages(child_urls, depth)


    def get_status(self, url):
        return self.redis.get(url) or 'ready'


    def set_status(self, url, status):
        return self.redis.set(url, status)


    def get_webpage_info(self, url):
        get_webpage_info = self.pg.proc('get_webpage_info(text)')
        return get_webpage_info(url)


    def register_job(self, job_id, urls):
        if urls:
            self.redis.sadd('job' + str(job_id), *urls) # This gets appened.
            self.redis.sadd('job' + str(job_id) + ':init', *urls)
