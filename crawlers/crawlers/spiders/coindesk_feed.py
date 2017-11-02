import os
import scrapy
import feedparser
from ..items import CoindeskItem


class CoindeskFeedSpider(scrapy.Spider):
    name = 'coindesk_feed'
    start_urls = ['https://www.coindesk.com/feed/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawlers.pipelines.CoindeskMongoPipeline': 1,
            'crawlers.pipelines.CoindeskImagePipeline': 2,
        },
    }

    def parse(self, response):
        """ Load feed """
        feed = feedparser.parse(response.body.decode())
        for entry in feed.entries:
            yield response.follow(entry['link'], self.parse_article, meta={'entry': entry})

    def parse_article(self, response):
        entry = response.meta['entry']

        pub_date = response.css('.article-meta time::attr("datetime")')[0].root
        pub_date = str(pub_date)

        img_url = response.css('.article.article-featured .picture > img::attr("src")')[0].root

        paragraphs = response.css(".article-content-container.noskimwords p::text").extract()
        paragraphs = [p.strip() for p in paragraphs]
        text = '\n'.join(paragraphs)

        slug = response.url.split('/')[-2]

        file_name = os.path.basename(img_url)
        image_name = slug + os.path.splitext(file_name)[1]
        image_file_path = os.path.join(self.name, image_name)

        yield CoindeskItem(
            url=response.url,
            slug=slug,

            title=entry['title'],
            author=entry['author'],
            text=text,
            tags=','.join([t['term'] for t in entry['tags']]),
            pub_date=pub_date,
            image_url=img_url,
            image_file_path=image_file_path,
        )
