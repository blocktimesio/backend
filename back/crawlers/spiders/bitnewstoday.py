import os
import re
import logging
import requests
import scrapy as scrapy
from ..items import NewsItem
from ..base_spiders import SpiderUrlMixin


class BitNewsTodaySpider(scrapy.Spider, SpiderUrlMixin):
    name = 'bitnewstoday'
    start_urls = ['https://bitnewstoday.com/']

    def parse(self, response):
        path = '//ul[contains(@class, "cnAllMenu-items")]/li[position()<3]/ul[@class="sections"]/li/a/@href'
        links_nodes = response.xpath(path)
        for node in links_nodes:
            url = self._get_abs_url(node.root)
            yield scrapy.Request(url, callback=self.parse_category)

    def parse_category(self, response):
        for node in response.xpath('//div[@class="desc"]/a/@href'):
            url = self._get_abs_url(node.root)
            yield scrapy.Request(url, callback=self.parse_article)

    def parse_article(self, response):
        slug = self.get_slug(response.url)

        text = ''.join([n.root for n in response.xpath('//div[@class="contentNews"]//p//text()')])
        text = text.strip()

        pub_date = ''
        date_nodes = response.xpath('//div[@class="signNews"]/text()')
        if len(date_nodes):
            m = re.search('(\d{2}\.\d{2}\.\d{4})', date_nodes[0].root)
            if m:
                pub_date = m.group(1)

        img_nodes = response.xpath('//img[@class="detailPhotoNews"]/@src')
        if len(img_nodes):
            image_url = self._get_abs_url(img_nodes[0].root)

            file_name = os.path.basename(image_url)
            image_name = slug + os.path.splitext(file_name)[1]
            image_file_path = os.path.join(self.name, image_name)
        else:
            image_url = ''
            image_file_path = ''

            log_message = 'IMAGE NOT FOUND {}'.format(response.url)
            self.log(log_message, logging.WARNING)

        comments = 0
        try:
            news_id = re.search('news\d+', response.body.decode())
            if news_id:
                url = 'https://bitnewstoday.com/ajax/comments/get.php'
                response = requests.post(url, data={'resource': news_id[0], 'showMore': False})
                data = response.json()
                total = re.match('\d+', data.get('total', ''))
                if total:
                    comments = int(total[0])
        except Exception as e:
            logging.error('Error at getting comment', exc_info=True)

        yield NewsItem(
            domain=self.get_domain(response.url),

            url=self.get_url(response.url),
            slug=slug,

            title=response.xpath('//h1/text()')[0].root,
            author='',
            text=text,
            tags='',
            pub_date=pub_date,

            image_url=image_url,
            image_file_path=image_file_path,

            views=0,
            comments=comments,
        )

    def _get_abs_url(self, path):
        return 'https://bitnewstoday.com{}'.format(path)
