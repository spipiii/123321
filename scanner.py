import asyncio


class MarketScanner:

    def __init__(self, loader, min_spread, fee_rate):
        self.loader = loader
        self.min_spread = min_spread
        self.fee_rate = fee_rate

    async def scan(self):

        opportunities = []

        # получаем тикеры со всех бирж
        tickers = await self.loader.fetch_all_tickers()

        # находим общие торговые пары между биржами
        symbol_sets = []

        for exchange, markets in tickers.items():
            symbol_sets.append(set(markets.keys()))

        if not symbol_sets:
            return []

        common_symbols = set.intersection(*symbol_sets)

        print(f"Common symbols across exchanges: {len(common_symbols)}")

        symbols = {}

        # собираем цены по символам
        for exchange, markets in tickers.items():
            for symbol, ticker in markets.items():

                if symbol not in common_symbols:
                    continue

                price = ticker.get("last")

                if price is None:
                    continue

                if symbol not in symbols:
                    symbols[symbol] = []

                symbols[symbol].append({
                    "exchange": exchange,
                    "price": price
                })

        # ищем арбитраж
        for symbol, prices in symbols.items():

            if len(prices) < 2:
                continue

            for buy in prices:
                for sell in prices:

                    if buy["exchange"] == sell["exchange"]:
                        continue

                    buy_price = buy["price"]
                    sell_price = sell["price"]

                    spread = ((sell_price - buy_price) / buy_price) * 100

                    # учитываем комиссии
                    spread_after_fee = spread - (self.fee_rate * 2 * 100)

                    if spread_after_fee >= self.min_spread:

                        opportunities.append({
                            "symbol": symbol,
                            "buy_exchange": buy["exchange"],
                            "buy_price": buy_price,
                            "sell_exchange": sell["exchange"],
                            "sell_price": sell_price,
                            "spread": spread,
                            "profit": spread_after_fee
                        })

        # сортировка по прибыли
        opportunities.sort(key=lambda x: x["profit"], reverse=True)

        return opportunities
