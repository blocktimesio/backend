import os
import logging
from datetime import timedelta
from celery.task import periodic_task
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner

logger = logging.getLogger('crawlers')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

from .utils import SocialCrawler
from crawlers.spiders.bitcoinist_feed import BitcoinistFeedSpider
from crawlers.spiders.bitnewstoday import BitNewsTodaySpider
from crawlers.spiders.blogethereum_feed import BlogEthereumFeedSpider
from crawlers.spiders.coindesk_feed import CoindeskFeedSpider
from crawlers.spiders.cointelegraph_feed import CoinTelegraphFeedSpider
from crawlers.spiders.ethereumworldnews_feed import EthereumWorldNewsFeedSpider
from crawlers.spiders.investopedia_feed import InvestopediaSpider
from crawlers.spiders.moneyandstate_feed import MoneyAndStateFeedSpider
from crawlers.spiders.news_bitcoin_feed import NewsBitcoinFeedSpider
from crawlers.spiders.newsbtc_feed import NewsBtcFeedSpider
from crawlers.spiders.prestonbyrne_feed import PrestonByrneFeedSpider
from crawlers.spiders.trustnodes_feed import TrustNodesFeedSpider


@periodic_task(run_every=timedelta(minutes=2))
def run_site_crawlers():
    runner = CrawlerRunner()
    spiders = [
        BitcoinistFeedSpider,
        BitNewsTodaySpider,
        BlogEthereumFeedSpider,
        CoindeskFeedSpider,
        CoinTelegraphFeedSpider,
        EthereumWorldNewsFeedSpider,
        InvestopediaSpider,
        MoneyAndStateFeedSpider,
        NewsBitcoinFeedSpider,
        NewsBtcFeedSpider,
        PrestonByrneFeedSpider,
        TrustNodesFeedSpider,
    ]
    for spider in spiders:
        runner.crawl(spider)

    try:
        runner = CrawlerRunner()
        for spider in spiders:
            runner.crawl(spider)
        d = runner.join()
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
    except Exception as e:
        logger.error('', exc_info=True)


@periodic_task(run_every=timedelta(minutes=1))
def crawl_social_latest():
    crawler = SocialCrawler()
    crawler.start()


@periodic_task(run_every=timedelta(hours=6))
def crawl_social_oldest():
    crawler = SocialCrawler(day_lte=8, day_gte=2)
    crawler.start()
