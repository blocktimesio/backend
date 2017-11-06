from unittest import TestCase
from apps.post.tasks import SocialCrawler


class SocialCrawlerTest(TestCase):
    def test_main(self):
        crawler = SocialCrawler()
        crawler.start()
