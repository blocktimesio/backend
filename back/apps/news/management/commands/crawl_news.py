from django.core.management import BaseCommand
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from apps.news.crawlers.spiders.bitcoinist_feed import BitcoinistFeedSpider
from apps.news.crawlers.spiders.bitnewstoday import BitNewsTodaySpider
from apps.news.crawlers.spiders.blogethereum_feed import BlogEthereumFeedSpider
from apps.news.crawlers.spiders.coindesk_feed import CoindeskFeedSpider
from apps.news.crawlers.spiders.cointelegraph_feed import CoinTelegraphFeedSpider
from apps.news.crawlers.spiders.ethereumworldnews_feed import EthereumWorldNewsFeedSpider
from apps.news.crawlers.spiders.investopedia_feed import InvestopediaSpider
from apps.news.crawlers.spiders.moneyandstate_feed import MoneyAndStateFeedSpider
from apps.news.crawlers.spiders.news_bitcoin_feed import NewsBitcoinFeedSpider
from apps.news.crawlers.spiders.newsbtc_feed import NewsBtcFeedSpider
from apps.news.crawlers.spiders.prestonbyrne_feed import PrestonByrneFeedSpider
from apps.news.crawlers.spiders.trustnodes_feed import TrustNodesFeedSpider


class Command(BaseCommand):
    help = 'Crawl news'

    def handle(self, *args, **options):
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

        runner = CrawlerRunner()
        for spider in spiders:
            runner.crawl(spider)
        d = runner.join()
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
