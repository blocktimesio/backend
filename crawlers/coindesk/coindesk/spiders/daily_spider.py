import re
import scrapy
import logging
import dateutil.parser
from datetime import datetime
from ..items import CoindeskItem


class DailySpider(scrapy.Spider):
    name = 'daily'
    start_urls = ['https://www.coindesk.com/page/1/?s']

    def __init__(self, date=None, *args, **kwargs):
        super(DailySpider, self).__init__(*args, **kwargs)

        # Parse the target date
        if date:
            self.date = datetime.strptime(date, '%Y-%m-%d')
        else:
            self.date = datetime.now()
        self.date = self.date.date()

    def parse(self, response):
        has_next_page = True
        for post_el in response.css('div.post-info'):
            date_text = post_el.xpath('.//time/@datetime')[0].root
            cur_date = dateutil.parser.parse(date_text).date()
            delta = cur_date - self.date
            if delta.days == 0:
                url = post_el.css('a.fade::attr(href)')[0].root
                yield response.follow(url, self.parse_article)
            elif delta.days < 0:
                has_next_page = False
                break

        if not has_next_page:
            return

        match = re.match('https://www.coindesk.com/page/(\d+)/\?s', response.url)
        if match:
            cur_page_num = match.group(1)  # type: str
            if cur_page_num.isdigit():
                cur_page_num = int(cur_page_num)
                url = re.sub('\d+', str(cur_page_num + 1), response.url)
                yield response.follow(url, self.parse)
        else:
            self.log('Can\'t find page number in {}'.format(response.url), logging.WARNING)

    def parse_article(self, response):
        slug = response.url.split('/')[-2]
        title = response.css('h3.featured-article-title::text')[0].root.strip()
        author = response.css('p.timeauthor > a::text')[0].root.strip()
        tags = ','.join([t.root.strip() for t in response.css('.single-tags > a::text') if t.root.strip()])
        image_url = response.css('img.size-full.wp-post-image::attr(src)')[0].root

        paragraphs = response.xpath('//div[@class="article-content-container noskimwords"]/p/text()').extract()
        text = '\n'.join([p for p in paragraphs if p.strip()])

        yield CoindeskItem(
            url=response.url,
            slug=slug,

            title=title,
            author=author,
            text=text,
            tags=tags,
            pub_date=str(self.date),
            image_url=image_url,

            page_html=response.text,
        )
