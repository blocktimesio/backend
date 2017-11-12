from scrapy.http import HtmlResponse
from ..base_spiders import BaseFeedSpider


class CoinTelegraphFeedSpider(BaseFeedSpider):
    name = 'cointelegraph_feed'
    start_urls = ['https://cointelegraph.com/rss']

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

    def get_total_views(self, entry: dict, response: HtmlResponse) -> int:
        nodes = response.css('.total-views .total-qty')
        if nodes:
            return nodes[0].root.text
        return 0
