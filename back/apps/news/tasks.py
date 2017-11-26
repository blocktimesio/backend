import logging
from datetime import timedelta
from celery.task import periodic_task
from scrapy.crawler import CrawlerProcess
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

logger = logging.getLogger('crawlers')

crawler_process = CrawlerProcess()
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
    crawler_process.crawl(spider)

TASK_CRAWL_DELAY = 60 * 10  # seconds


@periodic_task(run_every=timedelta(seconds=TASK_CRAWL_DELAY))
def run_sites_crawlers():
    try:
        crawler_process.start()
    except Exception as e:
        logger.error('Error at run crawlers', exc_info=True)
