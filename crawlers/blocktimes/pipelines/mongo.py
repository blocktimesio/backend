from .base import BaseMongoPipeline


class CoindeskMongoPipeline(BaseMongoPipeline):
    collection_name = 'coindesk_items'


class CoinTelegrapMongoPipeline(BaseMongoPipeline):
    collection_name = 'cointelegrap_items'


class NewsBtcMongoPipeline(BaseMongoPipeline):
    collection_name = 'newsbtc_items'


class BitcoinistMongoPipeline(BaseMongoPipeline):
    collection_name = 'bitcoinist_items'


class TrustNodesMongoPipeline(BaseMongoPipeline):
    collection_name = 'trustnodes_items'


class EthereumWorldNewsMongoPipeline(BaseMongoPipeline):
    collection_name = 'ethereumworldnews_items'


class NewsBitcoinMongoPipeline(BaseMongoPipeline):
    collection_name = 'newsbitcoin_items'
