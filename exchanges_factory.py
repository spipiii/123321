
import ccxt.async_support as ccxt

def create_exchange(name):

    if name == "bybit":
        return ccxt.bybit({"enableRateLimit": True})

    if name == "okx":
        return ccxt.okx({"enableRateLimit": True})

    if name == "mexc":
        return ccxt.mexc({"enableRateLimit": True})

    if name == "htx":
        return ccxt.htx({"enableRateLimit": True})

    raise ValueError("Unsupported exchange")
