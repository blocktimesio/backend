import re
import logging
from scrapy.http import HtmlResponse
from ..items import BlogEthereumItem
from ..base_spiders import BaseFeedSpider


class BlogEthereumFeedSpider(BaseFeedSpider):
    item = BlogEthereumItem
    name = 'blogethereum_feed'
    start_urls = ['https://blog.ethereum.org/feed/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'blocktimes.pipelines.BlogEthereumImagePipeline': 1,
            'blocktimes.pipelines.BlogEthereumMongoPipeline': 2,
        },
    }

    def get_image_url(self, entry: dict, response: HtmlResponse) -> str:
        return ''

    def get_image_path(self, image_url: str, slug: str) -> str:
        return ''
