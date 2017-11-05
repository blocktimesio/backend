#!/usr/bin/env python

import os
import re
import time
import logging
from datetime import datetime

import requests
import subprocess
from uuid import uuid4
from requests import Response

logger = logging.getLogger('crawlers')

BASE_URL = os.environ.get('CRAWLERS_BASE_URL', 'http://localhost:6800')
SCRAPYD_DIR = os.environ.get('SCRAPYD_DIR', '/scrapyd')
CRAWLERS_DIR = os.environ.get('CRAWLERS_DIR', '/crawlers')
PROJECT_NAME = os.environ.get('CRAWLERS_PROJECT_NAME', 'blocktimes')

SPIDERS_PATH = os.path.join(CRAWLERS_DIR, PROJECT_NAME, 'spiders')
SPIDERS_INTERVAL_SECONDS = int(os.environ.get('SPIDERS_INTERVAL_SECONDS', 600))


class ScrapydClient(object):
    spiders_names = []

    def __init__(self, *args, **kwargs):
        self._load_spiders_names()

    def remove_projects(self):
        data_projects = self.execute_method('listprojects')
        for name in data_projects.get('projects', []):
            response_data = self.execute_method('delproject', 'post', project=name)
            if response_data.get('status', 'ok'):
                logger.info('Project "{}" is deleted'.format(name))
            else:
                logger.info('Project "{}" is not deleted'.format(name))

    def load_project(self):
        bash_command = 'cd {} && scrapyd-deploy -a -p {}'.format(CRAWLERS_DIR, PROJECT_NAME)
        subprocess.check_output(['bash', '-c', bash_command])

    def run_spiders(self) -> list:
        jobs_ids = []
        for name in self.spiders_names:
            cur_time = datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
            job_id = '{}_{}'.format(cur_time, self.short_uuid)
            data = {'project': PROJECT_NAME, 'spider': name, 'jobid': job_id}
            response_data = self.execute_method('schedule', method='post', **data)
            if response_data.get('status', '') == 'ok':
                jobs_ids.append(job_id)
                logger.info('Run spider {} jobid={}'.format(name, job_id))
            else:
                logger.info('Spider {} was not runned jobid={}'.format(name, job_id))

        return jobs_ids

    def cancel_job(self, jobid: str):
        self.execute_method('cancel', 'post', project=PROJECT_NAME, jobid=jobid)

    def _load_spiders_names(self):
        self.spiders_names = []
        for name in os.listdir(SPIDERS_PATH):
            if name == '__init__.py' or not re.match('^(.*)\.py$', name):
                continue
            name = os.path.splitext(name)[0]
            self.spiders_names.append(name)
            logging.debug('Load spider {}'.format(name))

    def execute_method(self, name: str, method='get', **kwargs) -> dict:
        url = self.get_url(name)
        if method == 'get':
            response = requests.get(url)  # type: Response
        elif method == 'post':
            response = requests.post(url, data=kwargs)  # type: Response
        else:
            message = 'Unknown method name "{}"'.format(method)
            raise TypeError(message)
        try:
            return response.json()
        except Exception as e:
            return {}

    def get_url(self, name: str):
        return '{}/{}.json'.format(BASE_URL, name)

    @property
    def short_uuid(self) -> str:
        return uuid4().hex[:8]


if __name__ == '__main__':
    os.system('cd /{} && scrapyd &'.format(SCRAPYD_DIR))  # Run scrapyd
    os.system('cd /{}'.format(CRAWLERS_DIR))  # Run scrapyd

    time.sleep(5)  # Sleep to wait the scrapyd will be up

    client = ScrapydClient()

    client.remove_projects()
    client.load_project()

    while True:
        logger.debug('Run the spiders')
        jobs_ids = client.run_spiders()

        logger.debug('Sleep {}'.format(SPIDERS_INTERVAL_SECONDS))
        time.sleep(SPIDERS_INTERVAL_SECONDS)

        logger.debug('Stop all jobs')
        for job_id in jobs_ids:
            client.cancel_job(job_id)
