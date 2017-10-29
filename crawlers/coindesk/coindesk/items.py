import scrapy


class CoindeskItem(scrapy.Item):
    url = scrapy.Field()
    slug = scrapy.Field()

    title = scrapy.Field()
    author = scrapy.Field()
    text = scrapy.Field()
    tags = scrapy.Field()
    pub_date = scrapy.Field()
    image_url = scrapy.Field()

    page_html = scrapy.Field()
