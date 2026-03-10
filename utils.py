
def calc_spread(buy, sell):
    return (sell - buy) / buy * 100


def estimate_profit(buy_price, sell_price, fee_rate):

    gross = sell_price - buy_price

    fee_buy = buy_price * fee_rate
    fee_sell = sell_price * fee_rate

    net = gross - fee_buy - fee_sell

    percent = net / buy_price * 100

    return percent
