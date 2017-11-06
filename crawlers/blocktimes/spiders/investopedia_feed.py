from scrapy.http import HtmlResponse
from ..base_spiders import BaseFeedSpider
from ..items import InvestopediaItem


class InvestopediaSpider(BaseFeedSpider):
    item = InvestopediaItem
    name = 'investopedia_feed'
    domain = 'investopedia.com'
    start_urls = ['http://www.investopedia.com/feedbuilder/feed/getfeed/?feedName=rss_headline']
    custom_settings = {
        'ITEM_PIPELINES': {
            'blocktimes.pipelines.InvestopediaMongoPipeline': 1,
            'blocktimes.pipelines.InvestopediaImagePipeline': 2,
        },
    }

    def get_text(self, entry: dict, response: HtmlResponse) -> str:
        return ''.join(
            [e.root for e in response.xpath('//div[@class="content-box"]//p//text()')]
        )

    def get_image_url(self, entry: dict, response: HtmlResponse) -> str:
        return ''

    def get_image_path(self, image_url: str, slug: str) -> str:
        return ''
