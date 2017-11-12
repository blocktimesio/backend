import re
import logging
from scrapy.http import HtmlResponse
from ..base_spiders import BaseFeedSpider


class EthereumWorldNewsFeedSpider(BaseFeedSpider):
    name = 'ethereumworldnews_feed'
    start_urls = ['http://ethereumworldnews.com/feed/']

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

    def get_total_views(self, entry: dict, response: HtmlResponse) -> int:
        nodes = response.css('.post-share-btn-views .number')
        if nodes:
            return nodes[1].root.replace(',', '')
        return 0
