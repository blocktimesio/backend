import logging
from scrapy.http import HtmlResponse
from ..base_spiders import BaseFeedSpider


class TrustNodesFeedSpider(BaseFeedSpider):
    name = 'trustnodes_feed'
    start_urls = ['http://www.trustnodes.com/feed']

    def get_text(self, entry: dict, response: HtmlResponse):
        return ''.join([e.root for e in response.css('div.post-content p::text')])

    def get_image_url(self, entry: dict, response: HtmlResponse):
        nodes = response.css('.wp-post-image::attr("src")')
        if len(nodes):
            return nodes[0].root
        else:
            log_message = 'IMAGE NOT FOUND {}'.format(response.url)
            self.log(log_message, logging.WARNING)
        return ''
