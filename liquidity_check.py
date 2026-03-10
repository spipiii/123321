
async def check_orderbook(exchange, symbol, depth):

    try:

        orderbook = await exchange.fetch_order_book(symbol)

        bids = orderbook["bids"][:depth]
        asks = orderbook["asks"][:depth]

        bid_volume = sum(b[1] for b in bids)
        ask_volume = sum(a[1] for a in asks)

        return bid_volume, ask_volume

    except:
        return 0,0
