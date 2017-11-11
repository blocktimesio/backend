from django.core.management.base import BaseCommand
from apps.news.utils import SocialCrawler


class Command(BaseCommand):
    help = 'Crawl social data for all news'

    def handle(self, *args, **options):
        crawler = SocialCrawler(is_all=True)
        crawler.start()
