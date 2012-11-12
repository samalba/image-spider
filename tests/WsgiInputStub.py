# -*- coding: ascii -*-
class WsgiInputStub:

    """
    Stub out wsgi.input's read method for wsgi.py.
    """

    def __init__(self, post_data):
        self.post_data = post_data

    def read(self, length):
        return bytes(self.post_data[0:length], 'utf8')
