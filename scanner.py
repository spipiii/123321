import asyncio
from withdraw_check import get_transfer_network

class MarketScanner:

    def __init__(self, loader, min_spread, fee_rate):
        """
        Scanner for arbitrage
        """
        self.loader = loader
        self.min_spread = min_spread
        self.fee_rate = fee_rate
        """
        loader - объект, который содержит подключенные биржи в self.loader.exchanges
        engine - объект арбитражного движка, который ищет возможности
        """
        self.loader = loader

    async def scan(self, df):
        """
        df - DataFrame с котировками или список монет
        Возвращает отфильтрованный список возможностей
        """
        # находим все арбитражные возможности через движок
        opportunities = self.engine.find(df)

        filtered = []

        for op in opportunities:

            # фильтр минимального спреда
            if op["spread"] < MIN_SPREAD:
                continue

            # фильтр объема за последние 24 часа
            volume = op.get("quoteVolume", 0)
            if volume < MIN_VOLUME_24H or volume > MAX_VOLUME_24H:
                continue

            # получаем объекты бирж
            buy_ex = self.loader.exchanges.get(op["buy_exchange"])
            sell_ex = self.loader.exchanges.get(op["sell_exchange"])
            if not buy_ex or not sell_ex:
                continue

            # проверяем возможность перевода между биржами
            transfer = await get_transfer_network(
                buy_ex,
                sell_ex,
                op["symbol"]
            )

            if not transfer:
                continue

            # добавляем данные о сети и комиссии в результат
            op["network"] = transfer["network"]
            op["withdraw_fee"] = transfer["fee"]

            filtered.append(op)

        return filtered

    async def notify_opportunities(self, opportunities, notifier):
        """
        Форматирует и отправляет уведомления
        notifier - объект для отправки сообщений (Telegram, Discord и т.д.)
        """
        for op in opportunities:

            message = f"""
COIN: {op['symbol']}

BUY: {op['buy_exchange']}
PRICE: {op['buy_price']}

SELL: {op['sell_exchange']}
PRICE: {op['sell_price']}

SPREAD: {op['spread']} %

NETWORK: {op['network']}
WITHDRAW FEE: {op['withdraw_fee']}
"""

            await notifier.send(message)
