import os
import scrapy
import feedparser
from ..items import TrustNodesItem
from dateutil.parser import *


class TrustNodesFeedSpider(scrapy.Spider):
    name = 'trustnodes_feed'
    start_urls = ['http://www.trustnodes.com/feed']
    custom_settings = {
        'ITEM_PIPELINES': {
            'blocktimes.pipelines.TrustNodesImagePipeline': 1,
            'blocktimes.pipelines.TrustNodesMongoPipeline': 2,
        },
    }

    def parse(self, response):
        """ Load feed """
        feed = feedparser.parse(response.body.decode())
        for entry in feed.entries:
            yield scrapy.Request(entry['link'], self.parse_article, meta={'entry': entry})

    def parse_article(self, response):
        entry = response.meta['entry']

        text = ''.join([e.root for e in response.css('div.post-content p::text')])

        slug = response.url.split('/')[-1]

        image_node = response.css('.wp-post-image::attr("src")')
        if image_node:
            image_url = image_node[0].root
            file_name = os.path.basename(image_url)
            image_name = slug + os.path.splitext(file_name)[1]
            image_file_path = os.path.join(self.name, image_name)
        else:
            image_url = ''
            image_file_path = ''

        yield TrustNodesItem(
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
