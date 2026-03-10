async def get_transfer_network(buy_exchange, sell_exchange, symbol):

    try:

        coin = symbol.split("/")[0]

        buy_currencies = await buy_exchange.fetch_currencies()
        sell_currencies = await sell_exchange.fetch_currencies()

        if coin not in buy_currencies or coin not in sell_currencies:
            return None

        buy_networks = buy_currencies[coin].get("networks", {})
        sell_networks = sell_currencies[coin].get("networks", {})

        for net_name, net_data in buy_networks.items():

            withdraw = net_data.get("withdraw", False)
            fee = net_data.get("fee")

            if not withdraw:
                continue

            if net_name in sell_networks:

                deposit = sell_networks[net_name].get("deposit", False)

                if deposit:

                    return {
                        "network": net_name,
                        "fee": fee
                    }

        return None

    except:
        return None