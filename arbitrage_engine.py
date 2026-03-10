
from utils import calc_spread, estimate_profit

class ArbitrageEngine:

    def __init__(self, min_spread, fee_rate):

        self.min_spread = min_spread
        self.fee_rate = fee_rate

    def find(self, df):

        results = []

        if df.empty:
            return results

        symbols = df["symbol"].unique()

        for s in symbols:

            coin = df[df["symbol"] == s]

            if len(coin) < 2:
                continue

            buy = coin.loc[coin["price"].idxmin()]
            sell = coin.loc[coin["price"].idxmax()]

            spread = calc_spread(buy.price, sell.price)

            if spread < self.min_spread:
                continue

            profit = estimate_profit(buy.price, sell.price, self.fee_rate)

            results.append({
                "symbol": s,
                "buy_exchange": buy.exchange,
                "sell_exchange": sell.exchange,
                "buy_price": buy.price,
                "sell_price": sell.price,
                "spread": spread,
                "profit": profit
            })

        results.sort(key=lambda x: x["spread"], reverse=True)

        return results
