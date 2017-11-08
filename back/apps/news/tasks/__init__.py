import os
import logging
from datetime import timedelta
from celery.task import periodic_task

logger = logging.getLogger('crawlers')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

from .scrapy_client import ScrapydClient
from .social_crawler import SocialCrawler


@periodic_task(run_every=timedelta(minutes=10))
def run_site_crawlers():
    client = ScrapydClient()

    client.remove_projects()
    client.load_project()

    jobs_ids = client.run_spiders()

    logger.debug('Stop all jobs')
    for job_id in jobs_ids:
        client.cancel_job(job_id)


@periodic_task(run_every=timedelta(minutes=5))
def crawl_social_latest():
    crawler = SocialCrawler()
    crawler.start()


@periodic_task(run_every=timedelta(hours=6))
def crawl_social_oldest():
    crawler = SocialCrawler(day_lte=8, day_gte=2)
    crawler.start()
