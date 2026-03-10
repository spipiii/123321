import asyncio
from config import *
from market_loader import MarketLoader
from scanner import MarketScanner
from logger import get_logger
from telegram_alerts import send_alert

log = get_logger()

async def main():

    log.info("Starting arbitrage scanner")

    loader = MarketLoader(EXCHANGES)

    try:

        # загрузка рынков
        await loader.initialize()

        scanner = MarketScanner(
            loader,
            MIN_SPREAD_PERCENT,
            TRADE_FEE_RATE
        )

        opportunities = await scanner.scan()

        print("\nTOP ARBITRAGE OPPORTUNITIES\n")

        for arb in opportunities[:TOP_RESULTS]:

            line = (
                f"{arb['symbol']} | "
                f"BUY {arb['buy_exchange']} {arb['buy_price']} -> "
                f"SELL {arb['sell_exchange']} {arb['sell_price']} | "
                f"Spread {arb['spread']:.2f}% | "
                f"Profit {arb['profit']:.2f}%"
            )

            print(line)

            if ENABLE_TELEGRAM:
                send_alert(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, line)

    finally:

        # ВАЖНО — закрываем соединения бирж
        for ex in loader.exchanges.values():
            await ex.close()

if __name__ == "__main__":
    asyncio.run(main())