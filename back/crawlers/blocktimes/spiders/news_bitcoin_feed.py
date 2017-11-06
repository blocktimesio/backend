import re
import logging
from scrapy.http import HtmlResponse
from ..items import NewsBitcoinWorldNewsItem
from ..base_spiders import BaseFeedSpider


class NewsBitcoinFeedSpider(BaseFeedSpider):
    item = NewsBitcoinWorldNewsItem
    name = 'newsbitcoin_feed'
    domain = 'bitcoin.com'
    start_urls = ['https://news.bitcoin.com/feed/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'blocktimes.pipelines.NewsBitcoinImagePipeline': 1,
            'blocktimes.pipelines.NewsBitcoinMongoPipeline': 2,
        },
    }

    def get_image_url(self, entry: dict, response: HtmlResponse) -> str:
        nodes = response.css('.td-post-featured-image img::attr(src)')
        if len(nodes) > 0:
            return nodes[0].root
        else:
            log_message = 'IMAGE NOT FOUND {}'.format(response.url)
            self.log(log_message, logging.WARNING)
            return ''
