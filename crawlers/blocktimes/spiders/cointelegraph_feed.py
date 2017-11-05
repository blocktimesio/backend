from scrapy.http import HtmlResponse
from ..base_spiders import BaseFeedSpider
from ..items import CoinTelegraphItem


class CoinTelegraphFeedSpider(BaseFeedSpider):
    item = CoinTelegraphItem
    name = 'cointelegraph_feed'
    slug_level = -1
    start_urls = ['https://cointelegraph.com/rss']
    custom_settings = {
        'ITEM_PIPELINES': {
            'blocktimes.pipelines.CoinTelegrapImagePipeline': 1,
            'blocktimes.pipelines.CoinTelegrapMongoPipeline': 2,
        },
    }

    def get_text(self, entry: dict, response: HtmlResponse) -> str:
        text = ''.join(
            [e.root for e in response.xpath('//div[@class="post-full-text contents"]//p//text()')]
        )
        return text

    def get_image_url(self, entry: dict, response: HtmlResponse):
        media_content = entry.get('media_content', [])
        if len(media_content):
            return media_content[0]['url']
        else:
            return ''
