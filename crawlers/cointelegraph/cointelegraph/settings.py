import os
import logging

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

BOT_NAME = 'cointelegraph'

SPIDER_MODULES = ['cointelegraph.spiders']
NEWSPIDER_MODULE = 'cointelegraph.spiders'

ROBOTSTXT_OBEY = False

LOG_LEVEL = logging.WARNING

CONCURRENT_REQUESTS = 32

DOWNLOAD_DELAY = 2

ITEM_PIPELINES = {
   'cointelegraph.pipelines.MongoCoinTelegraphPipeline': 1,
}

IMAGES_URLS_FIELD = 'image_url'
IMAGES_STORE = os.path.join(BASE_DIR, '../..', 'media', 'cointelegraph_images')

MONGO_DATABASE = 'cointelegraph'
MONGO_URI = 'mongodb://localhost:27017/{}'.format(MONGO_DATABASE)
