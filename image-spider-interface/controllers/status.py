# -*- coding: ascii -*-

from responder import responder
from view import view

class status:

#TODO:Docstrings
    """
    """

    def get(self, querystring=None):

        """
        """

        #TODO:if not url
        status_view = view('status.json', {'url': url})
        return responder(status_view)
