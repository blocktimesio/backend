import re
import logging
from scrapy.http import HtmlResponse
from ..items import MoneyAndStateItem
from ..base_spiders import BaseFeedSpider


class MoneyAndStateFeedSpider(BaseFeedSpider):
    item = MoneyAndStateItem
    name = 'moneyandstate_feed'
    domain = 'bitcoinist.com'
    start_urls = ['http://bitcoinist.com/feed/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'blocktimes.pipelines.MoneyAndStateImagePipeline': 1,
            'blocktimes.pipelines.MoneyAndStateMongoPipeline': 2,
        },
    }

    def get_image_url(self, entry: dict, response: HtmlResponse) -> str:
        log_message = 'IMAGE NOT FOUND {}'.format(response.url)
        styles_node = response.xpath('//div[contains(@class, "post-header")]//div[1]/@style')
        if len(styles_node):
            m = re.match('(.*)url\(\'(.*)\'\)', styles_node[0].root)
            if m:
                return m.group(2)
            else:
                self.log(log_message, logging.WARNING)
        else:
            self.log(log_message, logging.WARNING)
        return ''
