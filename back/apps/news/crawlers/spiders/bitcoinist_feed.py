import re
import logging
from scrapy.http import HtmlResponse
from ..base_spiders import BaseFeedSpider


class BitcoinistFeedSpider(BaseFeedSpider):
    name = 'bitcoinist_feed'
    start_urls = ['http://bitcoinist.com/feed/']

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
