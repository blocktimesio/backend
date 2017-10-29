import re
import json
import scrapy
import logging
import dateutil.parser
from datetime import datetime
from scrapy import FormRequest
from scrapy.http import Request
from ..items import CoinTelegraphItem


class DailySpider(scrapy.Spider):
    name = 'daily'
    start_urls = ['https://cointelegraph.com/api/v1/content/search/result']

    page = 1

    def __init__(self, date=None, *args, **kwargs):
        super(DailySpider, self).__init__(*args, **kwargs)

        # Parse the target date
        if date:
            self.date = datetime.strptime(date, '%Y-%m-%d')
        else:
            self.date = datetime.now()
        self.date = self.date.date()

    def start_requests(self):
        data = {'page': '1'}
        yield FormRequest(self.start_urls[0], self.parse, formdata=data, meta=data)

    def parse(self, response):
        has_next_page = True

        posts = json.loads(response.text).get('posts', [])
        for post in posts:
            if 'ago' in post['created'].lower():
                cur_date = datetime.now().date()
            else:
                cur_date = dateutil.parser.parse(post['created']).date()

            delta = cur_date - self.date
            if delta.days == 0:
                yield response.follow(post['url'], self.parse_article, meta=post)
            elif delta.days < 0:
                has_next_page = False
                break

        if not has_next_page:
            return

        page = int(response.meta.get('page')) + 1
        data = {'page': str(page)}
        yield FormRequest(response.url, self.parse, formdata=data, meta=data)

    def parse_article(self, response):
        text = 'post-full-text contents'
        yield CoinTelegraphItem(
            url=response.url,
            slug=response.url.split('/')[-1],

            title=response.meta['title'],
            author=response.meta['author'],
            text='',
            tags=','.join(response.meta['types']),
            pub_date=str(self.date),
            image_url='',

            page_html=response.text,
        )
