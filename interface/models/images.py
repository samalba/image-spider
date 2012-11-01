# -*- coding: ascii -*-

from . DataModel import DataModel

class images(DataModel):

    """
    This model represents image-URLs found when crawling.
    """

    def _uniq(self, seq):

        """
        Omit repeated items.

        Arguments:
            seq: iterable sequence

        Returns: seq reduced to uniques.
        """

        keys = {}
        for e in seq:
            keys[e] = 1
        return keys.keys()


    def get_by_job_id(self, job_id):

        """
        Get image URLs found from the specied job.

        Arguments:
            job_id: integer job id.

        Returns: list URLs.
        """

        get_webpage_info = self.pg.proc('get_webpage_info(text)')
        get_tree = self.pg.proc('get_tree(integer)')
        get_images = self.pg.proc('get_images(integer[])')

        urls = self.redis.smembers('job' + str(job_id) + ':init')
        if not urls or not len(urls):
            return

        result = []

        for url in urls:
            webpage_info = get_webpage_info(url.decode())
            if not webpage_info:
                continue
            parent_id = webpage_info['id']
            tree = get_tree(parent_id)
            child_ids = [row['child_id'] for row in tree]
            all_unique_ids = self._uniq(child_ids + [parent_id])
            images = list(get_images(all_unique_ids))
            result.extend(images)

        return result


    def get_by_url(self, url):

        """
        """

        pass#TODO
