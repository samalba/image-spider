# -*- coding: ascii -*-

"""
Controllers must be imported and registered here in order to be made available
to the application.
"""

from . crawl import crawl
from . result import result
from . status import status
from . stop import stop

__all__ = ['crawl', 'result', 'status', 'stop']
