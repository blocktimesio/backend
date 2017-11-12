import scrapy


class NewsItem(scrapy.Item):
    domain = scrapy.Field(serializer=str)

    url = scrapy.Field(serializer=str)
    url_raw = scrapy.Field(serializer=str)
    slug = scrapy.Field(serializer=str)

    title = scrapy.Field(serializer=str)
    author = scrapy.Field(serializer=str)
    text = scrapy.Field(serializer=str)
    tags = scrapy.Field(serializer=str)
    pub_date = scrapy.Field(serializer=str)

    social = scrapy.Field(serializer=dict)
    views = scrapy.Field(serializer=int)
    comments = scrapy.Field(serializer=int)

    image_url = scrapy.Field(serializer=str)
    image_file_path = scrapy.Field(serializer=str)
