#!/usr/bin/env python3
# -*- coding: ascii -*-

# Append the path where dotCloud keeps its modules.
sys.path.append('/opt/ve/3.2/lib/python3.2/site-packages')

from data import data
from DeploymentManager import DeploymentManager
import os
import pickle
import signal
import sys


deployment_manager = DeploymentManager()


def graceful_exit(signum, frame):
    deployment_manager.abort()
    sys.exit(0)


def main():

    """
    Listen for 'deploy' messages, and submit their data (URLs) to the
    deployment_manager for processing.
    """

    data.pubsub.subscribe('deploy')
    for item in data.pubsub.listen():
        if 'message' == item['type'] and 'deploy' == item['channel']:
            deployment_manager.enqueue(pickle.loads(item['data']))


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, graceful_exit) # `supervisorctl stop`
    signal.signal(signal.SIGINT, graceful_exit) # CTRL-C

    main()
