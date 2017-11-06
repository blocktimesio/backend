import os
import socialshares
from queue import Queue
from threading import Thread
from datetime import timedelta
from django.utils import timezone
from celery.task import periodic_task
from pymongo import MongoClient
from bson.objectid import ObjectId

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

from django.conf import settings


@periodic_task(run_every=timedelta(minutes=10))
def crawl_social_latest():
    crawler = SocialCrawler()
    crawler.start()


@periodic_task(run_every=timedelta(hours=6))
def crawl_social_oldest():
    crawler = SocialCrawler(day_lte=8, day_gte=2)
    crawler.start()


class SocialCrawler(object):
    _queue = Queue()
    _thread_count = 10

    def __init__(self, day_gte: int=2, day_lte: int=0, thread_count: int=None):
        self._day_gte = day_gte
        self._day_lte = day_lte

        if day_lte:
            if day_gte > day_lte:
                raise ValueError('Day GTE < day LTE')

        if thread_count:
            self._thread_count = thread_count
        else:
            self._thread_count = settings.SOCIAL_CRAWLER_THREAD_COUNT

        client = MongoClient(host=settings.MONGODB_HOST)
        self._collection = client[settings.MONGODB_DB].posts

    def start(self, count: int=None) -> None:
        for post in self._get_post_list():
            uid = str(post['_id'])
            self._queue.put(uid)
        
        if not count:
            count = self._thread_count
        
        for i in range(count):
            t = Thread(target=SocialCrawler._social_worker, args=(self, ))
            t.daemon = True
            t.start()

        self._queue.join()
    
    def _social_worker(self):
        while True:
            uid = self._queue.get()
            try:
                post = self._get_post_detail(uid)
                if post:
                    data = self._process(post)
                    self._update_post(post['_id'], **data)
                    # TODO: log
                else:
                    pass  # TODO: log
            except Exception as e:
                pass  # TODO: log
            finally:
                self._queue.task_done()

            if self._queue.empty():
                break
    
    def _get_post_list(self) -> list:
        day_gte = timezone.now() - timedelta(days=self._day_gte)
        filter_params = {'$gte': day_gte}
        if self._day_lte:
            filter_params['$lte'] = timezone.now() - timedelta(days=self._day_lte)
        return self._collection.find({'created': filter_params})
    
    def _get_post_detail(self, uid: str) -> dict:
        return self._collection.find_one({'_id': ObjectId(uid)})
    
    def _process(self, post: dict) -> dict:
        social_data = socialshares.fetch(
            post['url'],
            ['facebook', 'pinterest', 'linkedin', 'google', 'reddit']
        )
        return {'social': social_data}

    def _update_post(self, uid, **kwargs):
        kwargs.update({'updated': timezone.now()})
        self._collection.update_one({'_id': ObjectId(uid)}, {'$set': kwargs})
