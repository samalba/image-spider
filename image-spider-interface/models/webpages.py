# -*- coding: ascii -*-

from . DataModel import DataModel

class webpages(DataModel):

    def add(self, child_urls, parent_url=None):
        if parent_url:
            add_webpages = self.pg.proc('add_webpages(text,text[])')
            add_webpages(parent_url, child_urls)
        else:
            add_webpages = self.pg.proc('add_webpages(text[])')
            add_webpages(child_urls)



#XXX         self.redis.publish('crawl', url)
