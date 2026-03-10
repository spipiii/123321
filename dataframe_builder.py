
import pandas as pd

def build_dataframe(market_data):

    rows = []

    for exchange, tickers in market_data.items():

        for symbol, data in tickers.items():

            price = data.get("last")
            volume = data.get("quoteVolume", 0)

            if not price:
                continue

            rows.append({
                "exchange": exchange,
                "symbol": symbol,
                "price": price,
                "volume": volume
            })

    return pd.DataFrame(rows)
