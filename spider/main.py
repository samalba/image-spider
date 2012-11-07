#!/usr/bin/env python3
# -*- coding: ascii -*-

import sys

# Append the path where dotCloud keeps its modules.
sys.path.append('/opt/ve/3.2/lib/python3.2/site-packages')

from data import data
from DeploymentManager import DeploymentManager
import pickle
import signal


def last_deployed_job(job_id=None):

    """
    Track the last job deployed to the deployment_manager.

    Arguments:
        job_id: optional integer Job ID.

    Returns: integer last assigned Job ID.
    """

    if int == type(job_id):
        last_deployed_job.job_id = job_id

    return getattr(last_deployed_job, 'job_id', None)


def graceful_exit(signum, frame):

    """
    Gracefully exit on SIGTERM or SIGINT. If a last_deployed_job has been
    specified then abort it.

    Arguments:
        signum: integer signal number (ignored).
        frame: current stack frame (ignored).

    Returns: None.
    """

    job_id = last_deployed_job()
    if int == type(job_id):
        data.abort(job_id)
    sys.exit(0)


def main(deployment_manager):

    """
    Listen for 'deploy' messages, and submit their data (job_id) to the
    deployment_manager for processing.
    """

    data.pubsub.subscribe('deploy')
    for item in data.pubsub.listen():
        if 'message' == item['type'] and 'deploy' == item['channel']:
            job_id = pickle.loads(item['data'])
            last_deployed_job(job_id)
            deployment_manager.enqueue(job_id)


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, graceful_exit) # `supervisorctl stop`
    signal.signal(signal.SIGINT, graceful_exit) # CTRL-C

    deployment_manager = DeploymentManager()

    main(deployment_manager)
