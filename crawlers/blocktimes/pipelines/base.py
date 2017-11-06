import os
import pymongo
from datetime import datetime
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline


class BaseMongoPipeline(object):
    collection_name = 'posts'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_db = mongo_db
        self.mongo_uri = mongo_uri

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collections = self.db[self.collection_name]
        count = collections.find({'slug': item['slug']}).count()
        data = dict(item)
        data['updated'] = datetime.now()
        if count:
            collections.update({'slug': item['slug']}, {'$set': data})
        else:
            data['created'] = data['updated']
            collections.insert_one(data)
        return item


class BaseImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        return request.meta['image_file_path']

    def get_media_requests(self, item, info):
        image_url = item.get('image_url')
        if not image_url:
            return

        file_path = item.get('image_file_path')
        if file_path:
            IMAGES_STORE = self.crawler.settings['IMAGES_STORE']
            full_path = os.path.join(IMAGES_STORE, file_path)
            if os.path.exists(full_path):
                return

            meta = {'image_file_path': item['image_file_path']}
            yield Request(url=item['image_url'], meta=meta)
