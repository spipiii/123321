
import asyncio
from exchanges_factory import create_exchange

class MarketLoader:

    def __init__(self, exchange_names):

        self.exchange_names = exchange_names
        self.exchanges = {}

    async def initialize(self):

        for name in self.exchange_names:
            self.exchanges[name] = create_exchange(name)

        await asyncio.gather(
            *[ex.load_markets() for ex in self.exchanges.values()]
        )

    async def fetch_all_tickers(self):

        results = {}

        for name, ex in self.exchanges.items():

            try:
                tickers = await ex.fetch_tickers()
                results[name] = tickers
            except:
                results[name] = {}

        return results
