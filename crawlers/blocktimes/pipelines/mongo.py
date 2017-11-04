from .base import BaseMongoPipeline


class CoindeskMongoPipeline(BaseMongoPipeline):
    collection_name = 'coindesk_items'


class CoinTelegrapMongoPipeline(BaseMongoPipeline):
    collection_name = 'cointelegrap_items'


class NewsBtcMongoPipeline(BaseMongoPipeline):
    collection_name = 'newsbtc_items'
