import logging
from scrapy.http import HtmlResponse
from ..base_spiders import BaseFeedSpider
from ..items import PrestonByrneItem


class PrestonByrneFeedSpider(BaseFeedSpider):
    item = PrestonByrneItem
    name = 'prestonbyrne_feed'
    start_urls = ['https://prestonbyrne.com/feed/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'blocktimes.pipelines.PrestonByrneMongoPipeline': 1,
            'blocktimes.pipelines.PrestonByrneImagePipeline': 2,
        },
    }

    def get_text(self, entry: dict, response: HtmlResponse) -> str:
        pass

    def get_image_url(self, entry: dict, response: HtmlResponse) -> str:
        media_content = entry.get('media_content', [])
        if len(media_content):
            return media_content[0].get('url', '')
        return ''
