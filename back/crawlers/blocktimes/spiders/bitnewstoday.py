import os
import re
import logging
import scrapy as scrapy
from ..base_spiders import SpiderUrlMixin
from ..items import BitNewsTodayItem


class BitNewsTodaySpider(scrapy.Spider, SpiderUrlMixin):
    name = 'bitnewstoday'
    start_urls = ['https://bitnewstoday.com/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'blocktimes.pipelines.BitNewsTodayImagePipeline': 1,
            'blocktimes.pipelines.BitNewsTodayMongoPipeline': 2,
        },
    }

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

        yield BitNewsTodayItem(
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

            social={}
        )

    def _get_abs_url(self, path):
        return 'https://bitnewstoday.com{}'.format(path)
