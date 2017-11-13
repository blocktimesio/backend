from scrapy.http import HtmlResponse
from ..base_spiders import BaseFeedSpider


class BlogEthereumFeedSpider(BaseFeedSpider):
    name = 'blogethereum_feed'
    start_urls = ['https://blog.ethereum.org/feed/']

    def get_image_url(self, entry: dict, response: HtmlResponse) -> str:
        return ''

    def get_image_path(self, image_url: str, slug: str) -> str:
        return ''
