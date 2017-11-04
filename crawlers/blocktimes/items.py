import scrapy


class BaseItem(scrapy.Item):
    url = scrapy.Field(serializer=str)
    slug = scrapy.Field(serializer=str)

    title = scrapy.Field(serializer=str)
    author = scrapy.Field(serializer=str)
    text = scrapy.Field(serializer=str)
    tags = scrapy.Field(serializer=str)
    pub_date = scrapy.Field(serializer=str)

    image_url = scrapy.Field(serializer=str)
    image_file_path = scrapy.Field(serializer=str)


class CoindeskItem(BaseItem):
    pass


class BitcoinistItem(BaseItem):
    pass


class CoinTelegraphItem(BaseItem):
    pass


class NewsBtcItem(BaseItem):
    pass
