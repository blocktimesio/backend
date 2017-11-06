import re
import logging
from scrapy.http import HtmlResponse
from ..items import BitcoinistItem
from ..base_spiders import BaseFeedSpider


class BitcoinistFeedSpider(BaseFeedSpider):
    item = BitcoinistItem
    name = 'bitcoinist_feed'
    domain = 'bitcoinist.com'
    start_urls = ['http://bitcoinist.com/feed/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'blocktimes.pipelines.BitcoinistImagePipeline': 1,
            'blocktimes.pipelines.BitcoinistMongoPipeline': 2,
        },
    }

    def get_image_url(self, entry: dict, response: HtmlResponse) -> str:
        nodes = response.css('.post-header > div::attr("style")')
        if len(nodes) > 0:
            m = re.match('(.*)url\(\'(.*)\'\)', nodes[0].root)
            if m:
                return m.group(2)
        else:
            log_message = 'IMAGE NOT FOUND {}'.format(response.url)
            self.log(log_message, logging.WARNING)
        return ''
