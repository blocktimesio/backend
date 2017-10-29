import os
import logging

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

BOT_NAME = 'coindesk'

SPIDER_MODULES = ['coindesk.spiders']
NEWSPIDER_MODULE = 'coindesk.spiders'

ROBOTSTXT_OBEY = False

LOG_LEVEL = logging.WARNING

CONCURRENT_REQUESTS = 32

DOWNLOAD_DELAY = 2

ITEM_PIPELINES = {
   'coindesk.pipelines.MongoCoinDeskPipeline': 1,
}

IMAGES_URLS_FIELD = 'image_url'
IMAGES_STORE = os.path.join(BASE_DIR, '../..', 'media', 'coindesk_images')

MONGO_DATABASE = 'coindesk'
MONGO_URI = 'mongodb://localhost:27017/{}'.format(MONGO_DATABASE)
