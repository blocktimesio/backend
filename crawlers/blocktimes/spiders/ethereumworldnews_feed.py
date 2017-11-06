import re
import logging
from scrapy.http import HtmlResponse
from ..base_spiders import BaseFeedSpider
from ..items import EthereumWorldNewsItem


class EthereumWorldNewsFeedSpider(BaseFeedSpider):
    item = EthereumWorldNewsItem
    name = 'ethereumworldnews_feed'
    domain = 'ethereumworldnews.com'
    start_urls = ['http://ethereumworldnews.com/feed/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'blocktimes.pipelines.EthereumWorldNewsImagePipeline': 1,
            'blocktimes.pipelines.EthereumWorldNewsMongoPipeline': 2,
        },
    }

    def get_image_url(self, entry: dict, response: HtmlResponse):
        log_message = 'IMAGE NOT FOUND {}'.format(response.url)

        # TODO: fix it
        nodes = response.css('.container > .post-header::attr(style)')
        if len(nodes):
            m = re.match('(.*)url\(\'(.*)\'\)', nodes[0].root)
            if m:
                return m.group(2)
            else:
                self.log(log_message, logging.WARNING)
        else:
            self.log(log_message, logging.WARNING)
        return ''
