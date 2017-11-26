from scrapy.http import HtmlResponse
from ..base_spiders import BaseFeedSpider


class PrestonByrneFeedSpider(BaseFeedSpider):
    name = 'prestonbyrne_feed'
    start_urls = ['https://prestonbyrne.com/feed/']

    def get_text(self, entry: dict, response: HtmlResponse) -> str:
        text = ''.join(
            [e.root for e in response.xpath('//div[@class="entry-content-container"]//p//text()')]
        )
        return text

    def get_image_url(self, entry: dict, response: HtmlResponse) -> str:
        media_content = entry.get('media_content', [])
        if len(media_content):
            return media_content[0].get('url', '')
        return ''
