import pymongo
from .items import CoinTelegraphItem


class MongoCoinTelegraphPipeline(object):
    collection_name = 'cointelegraph_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_db = mongo_db
        self.mongo_uri = mongo_uri

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'cointelegraph')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item: CoinTelegraphItem, spider):
        collections = self.db[self.collection_name]
        count = collections.find({'slug': item['slug']}).count()
        if count:
            collections.update({'slug': item['slug']}, {'$set': dict(item)})
        else:
            collections.insert_one(dict(item))

        return item
