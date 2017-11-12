import re
import logging
from scrapy.http import HtmlResponse
from ..base_spiders import BaseFeedSpider


class MoneyAndStateFeedSpider(BaseFeedSpider):
    name = 'moneyandstate_feed'
    start_urls = ['http://moneyandstate.com/feed/']

    def get_image_url(self, entry: dict, response: HtmlResponse) -> str:
        log_message = 'IMAGE NOT FOUND {}'.format(response.url)
        styles_node = response.xpath('//header[contains(@class, "image-header")]/@style')
        if styles_node:
            m = re.match('(.*)url\(\'(.*)\'\)', styles_node[0].root)
            if m:
                return m.group(2)
            else:
                self.log(log_message, logging.WARNING)
        else:
            self.log(log_message, logging.WARNING)
        return ''

    def get_total_comments(self, entry: dict, response: HtmlResponse) -> int:
        nodes = response.xpath('//div[@class="post-header"]//div[@class="info"]//div[1]//span//text()')
        if nodes:
            comments = nodes[0].root
            if comments.isdigit():
                return int(comments)
        return 0
