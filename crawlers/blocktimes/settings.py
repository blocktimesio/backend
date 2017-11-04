import os
import logging

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

BOT_NAME = 'blocktimes'

SPIDER_MODULES = ['blocktimes.spiders']
NEWSPIDER_MODULE = 'blocktimes.spiders'

ROBOTSTXT_OBEY = False

LOG_LEVEL = logging.WARNING

CONCURRENT_REQUESTS = 32

DOWNLOAD_DELAY = 2

ITEM_PIPELINES = {}

IMAGES_URLS_FIELD = 'image_url'
IMAGES_STORE = os.path.join(BASE_DIR, '../../back/media')

MONGO_DATABASE = 'blocktimes'
MONGO_URI = 'mongodb://localhost:27017/{}'.format(MONGO_DATABASE)
