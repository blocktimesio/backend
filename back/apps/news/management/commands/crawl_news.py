from django.core.management import BaseCommand
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
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


class Command(BaseCommand):
    help = 'Crawl news'

    def handle(self, *args, **options):
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

        runner = CrawlerRunner()
        for spider in spiders:
            runner.crawl(spider)
        d = runner.join()
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
