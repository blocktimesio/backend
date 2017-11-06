import os
import scrapy
import feedparser
from dateutil.parser import *
from scrapy.http import HtmlResponse


class BaseFeedSpider(scrapy.Spider):
    name = None
    domain = None
    start_urls = None
    item = None
    custom_settings = None
    slug_level = -2

    def parse(self, response):
        """ Load feed """
        feed = feedparser.parse(response.body.decode())
        for entry in feed.entries:
            yield scrapy.Request(entry['link'], self.parse_article, meta={'entry': entry})

    def parse_article(self, response):
        entry = response.meta['entry']

        slug = self.get_slug(entry, response)

        image_url = self.get_image_url(entry, response)

        image_file_path = ''
        if image_url:
            slug = self.get_slug(entry, response)
            image_file_path = self.get_image_path(image_url, slug)

        yield self.item(
            domain=self.domain,

            url=self.get_url(entry, response),
            slug=slug,

            title=self.get_title(entry, response),
            author=self.get_authors(entry, response),
            text=self.get_text(entry, response),
            tags=self.get_tags(entry, response),
            pub_date=self.get_pub_date(entry, response),

            image_url=image_url,
            image_file_path=image_file_path,
        )

    def get_url(self, entry: dict, response: HtmlResponse) -> str:
        return response.url

    def get_slug(self, entry: dict, response: HtmlResponse) -> str:
        return response.url.split('/')[self.slug_level]

    def get_title(self, entry: dict, response: HtmlResponse) -> str:
        return entry.get('title', '')

    def get_authors(self, entry: dict, response: HtmlResponse) -> str:
        return ','.join([a.get('name', '') for a in entry.get('authors', [])])

    def get_text(self, entry: dict, response: HtmlResponse) -> str:
        contents = entry.get('content', [])
        if len(contents) > 0:
            return contents[0].get('value')
        return ''

    def get_tags(self, entry: dict, response: HtmlResponse) -> str:
        return ','.join([t.get('term', '') for t in entry.get('tags', [])])

    def get_pub_date(self, entry: dict, response: HtmlResponse) -> str:
        published = entry.get('published')
        if published:
            return str(parse(published))
        return ''

    def get_image_url(self, entry: dict, response: HtmlResponse) -> str:
        raise NotImplementedError()

    def get_image_path(self, image_url, slug) -> str:
        file_name = os.path.basename(image_url)
        image_name = slug + os.path.splitext(file_name)[1]
        return os.path.join(self.name, image_name)
