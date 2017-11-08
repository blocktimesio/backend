from datetime import datetime

import scrapy


class BaseItem(scrapy.Item):
    domain = scrapy.Field(serializer=str)

    url = scrapy.Field(serializer=str)
    slug = scrapy.Field(serializer=str)

    title = scrapy.Field(serializer=str)
    author = scrapy.Field(serializer=str)
    text = scrapy.Field(serializer=str)
    tags = scrapy.Field(serializer=str)
    pub_date = scrapy.Field(serializer=str)

    social = scrapy.Field(serializer=dict)

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


class TrustNodesItem(BaseItem):
    pass


class EthereumWorldNewsItem(BaseItem):
    pass


class NewsBitcoinWorldNewsItem(BaseItem):
    pass


class BitNewsTodayItem(BaseItem):
    pass


class InvestopediaItem(BaseItem):
    pass


class MoneyAndStateItem(BaseItem):
    pass


class BlogEthereumItem(BaseItem):
    pass


class PrestonByrneItem(BaseItem):
    pass