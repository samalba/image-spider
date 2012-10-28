# -*- coding: ascii -*-

import models
from responder import responder
from view import view

class crawl:

#TODO:Docstrings
    """
    """

    def __init__(self):
        self.webpages = models.webpages()

    def get(self):

        """
        """

        demo_view = view('demo.htm')
        return responder(demo_view, 'text/html')


    def post(self, querystring, postdata):

        """
        """

        print(postdata)
        print(postdata[b'urls'])
        url='http://example.rom'#XXX
        depth=2#XXX
        self.webpages.add([url])#XXX

        #TODO:For each URL
#             if websites.get(url).status == 'processing':

#XXX XXX XXX
# 1. Add a URL to crawl add(depth) -- we add(2) by default.
# 2. Is the URL already listed with a 'processing' state? If so:
#     Does the URL have a depth of specified or larger?
#         If so, return.
#         Otherwise, stop that spider. Update the depth. Re-call add().
# 3. Has the URL already been parsed within the last 15 minutes? If so, return.
# 4. Are there any crawlers inactive? If not then add one.
# 5. Alert the first inactive crawler that a URL has been added.
# 6. Crawler updates state to 'processing'
# 7. Crawler parses resource at URL for images and links
# 8. If depth is greater than 0:
#     - Crawler adds URLs from each link, to return to Step 1.
#     - Crawler updates children with their foreign keys.
#     - Sounds like a stored function.
# 9. Crawler stores image addresses related to URL.
# 10. Crawler updates the state to 'complete' and sets the completion_datetime.
#XXX XXX XXX


        #TODO
        return responder('', 'text/html', '202 Accepted') #XXX Drop mimetype
