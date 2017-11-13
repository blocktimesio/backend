import re
import logging
from scrapy.http import HtmlResponse
from ..base_spiders import BaseFeedSpider


class NewsBitcoinFeedSpider(BaseFeedSpider):
    name = 'newsbitcoin_feed'
    start_urls = ['https://news.bitcoin.com/feed/']

    def get_image_url(self, entry: dict, response: HtmlResponse) -> str:
        nodes = response.css('.td-post-featured-image img::attr(src)')
        if len(nodes) > 0:
            return nodes[0].root
        else:
            log_message = 'IMAGE NOT FOUND {}'.format(response.url)
            self.log(log_message, logging.WARNING)
            return ''

    def get_total_comments(self, entry: dict, response: HtmlResponse) -> int:
        nodes = response.css('.td-post-views span')
        if nodes:
            comments = nodes[0].root.text
            if comments.isdigit():
                return int(comments)
        return 0

    def get_total_views(self, entry: dict, response: HtmlResponse) -> int:
        nodes = response.xpath('//div[@class="td-post-comments"]//a//text()')
        if nodes:
            comments = nodes[0].root
            if comments.isdigit():
                return int(comments)
        return 0
