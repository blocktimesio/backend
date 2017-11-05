import re
import logging
from scrapy.http import HtmlResponse
from ..base_spiders import BaseFeedSpider
from ..items import NewsBtcItem


class NewsBtcFeedSpider(BaseFeedSpider):
    item = NewsBtcItem
    name = 'newsbtc_feed'
    start_urls = ['http://www.newsbtc.com/feed/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'blocktimes.pipelines.NewsBtcImagePipeline': 1,
            'blocktimes.pipelines.NewsBtcMongoPipeline': 2,
        },
    }

    def get_image_url(self, entry: dict, response: HtmlResponse):
        # TODO: fix for http://www.newsbtc.com/2017/11/04/bitcoin-cash-holders-spends-funds-within-six-hours-receiving/
        nodes = response.css('.wp-post-image::attr("src")')
        if len(nodes):
            return nodes[0].root
        else:
            log_message = 'IMAGE NOT FOUND {}'.format(response.url)
            self.log(log_message, logging.WARNING)
        return ''
