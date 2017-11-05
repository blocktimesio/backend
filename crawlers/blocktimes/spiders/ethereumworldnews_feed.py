import os
import re
import scrapy
import feedparser
from ..items import EthereumWorldNewsItem
from dateutil.parser import *


class EthereumWorldNewsFeedSpider(scrapy.Spider):
    name = 'ethereumworldnews_feed'
    start_urls = ['http://ethereumworldnews.com/feed/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'blocktimes.pipelines.EthereumWorldNewsImagePipeline': 1,
            'blocktimes.pipelines.EthereumWorldNewsMongoPipeline': 2,
        },
    }

    def parse(self, response):
        """ Load feed """
        feed = feedparser.parse(response.body.decode())
        for entry in feed.entries:
            yield scrapy.Request(entry['link'], self.parse_article, meta={'entry': entry})

    def parse_article(self, response):
        entry = response.meta['entry']

        text = ''.join([e.root for e in response.css('.entry-content p::text')])

        slug = response.url.split('/')[-2]

        # TODO: доделать тут
        m = re.match('(.*)url\(\'(.*)\'\)', response.css('.post-header > div::attr("style")')[0].root)
        if m:
            image_url = m.group(2)
            file_name = os.path.basename(image_url)
            image_name = slug + os.path.splitext(file_name)[1]
            image_file_path = os.path.join(self.name, image_name)
        else:
            image_url = ''
            image_file_path = ''

        yield EthereumWorldNewsItem(
            url=response.url,
            slug=slug,

            title=entry['title'],
            author=','.join([a['name'] for a in entry['authors']]),
            text=text,
            tags=','.join([t['term'] for t in entry['tags']]),
            pub_date=str(parse(entry['published'])),
            image_url=image_url,
            image_file_path=image_file_path,
        )
