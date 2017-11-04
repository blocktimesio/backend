import os
import scrapy
import feedparser
from ..items import CoinTelegraphItem
from dateutil.parser import *


class CoinTelegraphFeedSpider(scrapy.Spider):
    name = 'cointelegraph_feed'
    start_urls = ['https://cointelegraph.com/rss']
    custom_settings = {
        'ITEM_PIPELINES': {
            'blocktimes.pipelines.CoinTelegrapImagePipeline': 1,
            'blocktimes.pipelines.CoinTelegrapMongoPipeline': 2,
        },
    }

    def parse(self, response):
        """ Load feed """
        feed = feedparser.parse(response.body.decode())
        for entry in feed.entries:
            yield scrapy.Request(entry['link'], self.parse_article, meta={'entry': entry})

    def parse_article(self, response):
        entry = response.meta['entry']

        text = ''.join(
            [e.root for e in response.xpath('//div[@class="post-full-text contents"]//p//text()')]
        )

        slug = response.url.split('/')[-1]

        file_name = os.path.basename(entry['media_content'][0]['url'])
        image_name = slug + os.path.splitext(file_name)[1]
        image_file_path = os.path.join(self.name, image_name)

        yield CoinTelegraphItem(
            url=response.url,
            slug=slug,

            title=entry['title'],
            author=entry['author'],
            text=text,
            tags=','.join([t['term'] for t in entry['tags']]),
            pub_date=str(parse(entry['published'])),
            image_url=entry['media_content'][0]['url'],
            image_file_path=image_file_path,
        )
