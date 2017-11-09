import logging
from scrapy.http import HtmlResponse
from ..base_spiders import BaseFeedSpider


class CoindeskFeedSpider(BaseFeedSpider):
    name = 'coindesk_feed'
    start_urls = ['https://www.coindesk.com/feed/']

    def get_image_url(self, entry: dict, response: HtmlResponse) -> str:
        nodes = response.css('.article.article-featured .picture > img::attr("src")')
        if len(nodes):
            return nodes[0].root
        else:
            log_message = 'IMAGE NOT FOUND {}'.format(response.url)
            self.log(log_message, logging.WARNING)
            return ''
