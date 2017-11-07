import logging
from scrapy.http import HtmlResponse
from ..base_spiders import BaseFeedSpider
from ..items import TrustNodesItem


class TrustNodesFeedSpider(BaseFeedSpider):
    item = TrustNodesItem
    start_urls = ['http://www.trustnodes.com/feed']
    custom_settings = {
        'ITEM_PIPELINES': {
            'blocktimes.pipelines.TrustNodesImagePipeline': 1,
            'blocktimes.pipelines.TrustNodesMongoPipeline': 2,
        },
    }

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
