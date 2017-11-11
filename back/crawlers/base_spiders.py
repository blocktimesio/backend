import os
import re
import scrapy
import logging
import feedparser
from dateutil.parser import *
from urllib.parse import (urlparse, ParseResult)
from scrapy.http import HtmlResponse
from .items import NewsItem


class SpiderUrlMixin(object):
    def get_domain(self, url: str) -> str:
        res = urlparse(url)  # type: ParseResult
        return re.sub(':\d+$', '', res.netloc)  # Remove port

    def get_url(self, url: str) -> str:
        res = urlparse(url)  # type: ParseResult
        return '{}{}'.format(res.netloc, res.path)

    def get_slug(self, url: str) -> str:
        res = urlparse(url)  # type: ParseResult
        slug = re.sub('/$', '', res.path).split('/')[-1]  # type: str
        return slug


class BaseFeedSpider(scrapy.Spider, SpiderUrlMixin):
    name = None
    domain = None
    start_urls = None
    item = NewsItem
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawlers.pipelines.ImagePipeline': 1,
            'crawlers.pipelines.MongoPipeline': 2,
        },

        'MONGODB_URI': os.environ.get('MONGO_URI', 'mongodb://localhost/blocktimes'),
        'MONGODB_DATABASE': os.environ.get('MONGO_DATABASE', 'blocktimes'),

        'IMAGES_STORE': os.environ.get('IMAGES_STORE_PATH', 'media'),
        'IMAGES_URLS_FIELD': 'image_url',

        'ROBOTSTXT_OBEY': False,

        'LOG_LEVEL': logging.WARNING,

        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS': 32,
    }

    def parse(self, response):
        """ Load feed """
        feed = feedparser.parse(response.body.decode())
        for entry in feed.entries:
            yield scrapy.Request(entry['link'], self.parse_article, meta={'entry': entry})

    def parse_article(self, response):
        entry = response.meta['entry']

        slug = self.get_slug(response.url)

        image_url = self.get_image_url(entry, response)

        image_file_path = ''
        if image_url:
            slug = self.get_slug(response.url)
            image_file_path = self.get_image_path(image_url, slug)

        yield self.item(
            domain=self.get_domain(response.url),

            url=self.get_url(response.url),
            url_raw=response.url,
            slug=slug,

            title=self.get_title(entry, response),
            author=self.get_authors(entry, response),
            text=self.get_text(entry, response),
            tags=self.get_tags(entry, response),
            pub_date=self.get_pub_date(entry, response),

            image_url=image_url,
            image_file_path=image_file_path,

            social={}
        )

    def get_title(self, entry: dict, response: HtmlResponse) -> str:
        return entry.get('title', '')

    def get_authors(self, entry: dict, response: HtmlResponse) -> str:
        return ','.join([a.get('name', '') for a in entry.get('authors', [])])

    def get_text(self, entry: dict, response: HtmlResponse) -> str:
        contents = entry.get('content', [])
        if len(contents) > 0:
            return contents[0].get('value')
        return ''

    def get_tags(self, entry: dict, response: HtmlResponse) -> list:
        return [t.get('term', '') for t in entry.get('tags', [])]

    def get_pub_date(self, entry: dict, response: HtmlResponse) -> str:
        published = entry.get('published')
        if published:
            return parse(published)
        return ''

    def get_image_url(self, entry: dict, response: HtmlResponse) -> str:
        raise NotImplementedError()

    def get_image_path(self, image_url, slug) -> str:
        file_name = os.path.basename(image_url)
        image_name = slug + os.path.splitext(file_name)[1]
        return os.path.join(self.name, image_name)
