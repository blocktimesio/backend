import scrapy
from ..models import News
from scrapy_djangoitem import DjangoItem


class NewsItem(DjangoItem):
    django_model = News

    domain = scrapy.Field()
    tags = scrapy.Field()