import datetime
import time
from data import *
import requests

token = tg_api_token


def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}}"


def get_coins_address():
    coin_address = {
        "DAI": f"{DAI_ADDRESS}",
        "WBTC": f"{WBTC_ADDRESS}",
        "WETH": f"{WETH_ADDRESS}",
        "ADA": f"{ADA_ADDRESS}"
    }

    return coin_address


def get_price_on_binance(coin_name):
    compare_value = "USDT"

    if coin_name == "WBTC":
        coin_name = "BTC"

    if coin_name == "WETH":
        coin_name = "ETH"

    payload = {"symbol": f"{coin_name}{compare_value}"}
    r = requests.get(url_binance_api, payload)
    status_code = r

    if coin_name == "BTC":
        coin_name = "WBTC"

    if coin_name == "ETH":
        coin_name = "WETH"

    response = r.json()
    if r:
        pass
    else:
        raise Exception(f"Something went wrong, {status_code}")

    final_price = response['price']
    final_price = toFixed(final_price, 5)

    #   Удаление последней точки
    if final_price.endswith('.'):
        final_price = final_price[:-1]

    result = {
        "name": coin_name,
        "price": final_price.strip()
    }

    return result


def get_price_on_flat_qube(coin_name):
    coin_list = get_coins_address()
    coin_address = coin_list[coin_name]

    r = requests.post(f"{url_flat_qube_api}{coin_address}")
    status_code = r
    response = r.json()

    if r:
        pass
    else:
        raise Exception(f"Wrong coin name, {status_code}")

    final_price = response['price']

    final_price = toFixed(final_price, 5)

    #   Удаление последней точки
    if final_price.endswith('.'):
        final_price = final_price[:-1]

    result = {
        "name": coin_name,
        "price": final_price.strip()
    }

    return result


def compare_prices():
    address_list = get_coins_address()
    target_procent = 4

    for items in address_list:
        b_items = get_price_on_binance(items)
        fq_items = get_price_on_flat_qube(items)

        b_price = float(b_items['price'])
        fq_price = float(fq_items['price'])
        print(f"Binance: {b_items['name']}: {b_price} $$$\n"
              f"FlatQube: {fq_items['name']}: {fq_price} $$$")
        print()

        result = 0
        if float(b_price) > float(fq_price):
            result = (b_price / fq_price - 1) * 100
            if result > target_procent:
                result_items = {
                    "market": "Binance",
                    "name": b_items["name"],
                    "b_price": b_price,
                    "fq_price": fq_price,
                    "procent": target_procent,
                    "target_procent": target_procent,
                    "different": f"{int(result)}%"
                }
                send_message(result_items)
                continue

        elif float(fq_price) > float(b_price):
            result = (fq_price / b_price - 1) * 100
            if result > target_procent:
                result_items = {
                    "market": "FlatQube.io",
                    "name": b_items["name"],
                    "b_price": b_price,
                    "fq_price": fq_price,
                    "target_procent": target_procent,
                    "different": f"{int(result)}%"
                }
                send_message(result_items)
                continue

    dt = datetime.datetime.now()
    dt_string = dt.strftime("Время: %H:%M:%S ")

    print(dt_string, target_procent %)
    time.sleep(30)


def send_message(items):
    dt = datetime.datetime.now()
    dt_string = dt.strftime("Время: %H:%M:%S ")

    if items["market"] == "FlatQube":
        coin_name = items["name"]
        market_name = items["market"]
        b_price = items["b_price"]
        fq_price = items["fq_price"]
        target_procent = items["target_procent"]

        link = None

        if coin_name == "DAI":
            link = "https://app.flatqube.io/swap/0:a519f99bb5d6d51ef958ed24d337ad75a1c770885dcd42d51d6663f9fcdacfb2/0:eb2ccad2020d9af9cec137d3146dde067039965c13a27d97293c931dae22b2b9"
        elif coin_name == "WBTC":
            link = "https://app.flatqube.io/swap/0:a519f99bb5d6d51ef958ed24d337ad75a1c770885dcd42d51d6663f9fcdacfb2/0:2ba32b75870d572e255809b7b423f30f36dd5dea075bd5f026863fceb81f2bcf"
        elif coin_name == "WETH":
            link = "https://app.flatqube.io/swap/0:a519f99bb5d6d51ef958ed24d337ad75a1c770885dcd42d51d6663f9fcdacfb2/0:59b6b64ac6798aacf385ae9910008a525a84fc6dcf9f942ae81f8e8485fe160d"
        elif coin_name == "ADA":
            link = "https://app.dexada.io/swap/0:152a7c50f7df2f305b56a1dd7e254d84a5aed018ba44b920f28def735215baa1/coin"

        if coin_name == "ADA":
            market_name = "Dexada.io"
        text = f"""‼️Покупать {coin_name} на {market_name}‼️️
Разница в цене на монету: {coin_name} на маркете - {market_name} составляет {items["different"]}, таргет процент - {target_procent}%
{market_name}: {coin_name} - {fq_price} $
Binance: {coin_name} - {b_price} $
Разница = {toFixed((fq_price - b_price), 5)} $
{dt_string}
{link}
        """
        requests.get(f"https://api.telegram.org/bot{tg_api_token}/sendMessage?chat_id=@dai_c0in&text={text}")

    elif items["market"] == "Binance":
        coin_name = items["name"]
        market_name = items["market"]
        b_price = items["b_price"]
        fq_price = items["fq_price"]
        target_procent = items["target_procent"]

        link = None

        if coin_name == "DAI":
            link = "https://app.flatqube.io/swap/0:a519f99bb5d6d51ef958ed24d337ad75a1c770885dcd42d51d6663f9fcdacfb2/0:eb2ccad2020d9af9cec137d3146dde067039965c13a27d97293c931dae22b2b9"
        elif coin_name == "WBTC":
            link = "https://app.flatqube.io/swap/0:a519f99bb5d6d51ef958ed24d337ad75a1c770885dcd42d51d6663f9fcdacfb2/0:2ba32b75870d572e255809b7b423f30f36dd5dea075bd5f026863fceb81f2bcf"
        elif coin_name == "WETH":
            link = "https://app.flatqube.io/swap/0:a519f99bb5d6d51ef958ed24d337ad75a1c770885dcd42d51d6663f9fcdacfb2/0:59b6b64ac6798aacf385ae9910008a525a84fc6dcf9f942ae81f8e8485fe160d"
        elif coin_name == "ADA":
            link = "https://app.dexada.io/swap/0:152a7c50f7df2f305b56a1dd7e254d84a5aed018ba44b920f28def735215baa1/coin"

        if coin_name == "ADA":
            market_name = "Dexada.io"
        text = f"""‼️Покупать {coin_name} на {market_name}‼️️
Разница в цене на монету: {coin_name} на маркете - {market_name} составляет {items["different"]}, таргет процент - {target_procent}%
{market_name}: {coin_name} - {fq_price} $
FlatQube.io: {coin_name} - {b_price} $
Разница = {toFixed((fq_price - b_price), 5)} $
{dt_string}
{link}
                """
        requests.get(f"https://api.telegram.org/bot{tg_api_token}/sendMessage?chat_id=@dai_c0in&text={text}")


# def get_coin_price_on_name(coin_name):
#     final_coin_address = coin_addresses(coin_name)
#
#     r = requests.post(f"{url_to_api_fq}{final_coin_address}")
#
#     main_price = r.json()
#     print(toFixed(main_price["price"], 4), main_price["currency"])
#
#     return toFixed(main_price["price"], 4), main_price["currency"]
#
#
# def get_coin_price():
#     final_coin_address = coin_addresses("DAI")
#
#     r = requests.post(f"{url_to_api_fq}{final_coin_address}")
#
#     main_price = r.json()
#     time.sleep(15)
#
#     actual_price_info = main_price['price']
#     actual_price_change = main_price['priceChange']
#     actual_volume = main_price["volume24h"]
#     actual_volume = toFixed(float(actual_volume), 0)
#     actual_price_info = toFixed(float(actual_price_info), 3)
#
#     dt = datetime.datetime.now()
#     dt_string = dt.strftime("Время: %H:%M:%S ")
#
#     info_result = f"{dt_string}| DAI = {actual_price_info} $ | Price Change: {actual_price_change} | Volume24: {actual_volume} $\n"
#     print(info_result)
#
#     # with open("data.txt", "a") as f:
#     #     f.write(info_result)
#
#     return actual_price_info
#
#

#
#
# def compare_prices(target_procent):
#     DAI_default_price = 1
#     # target_price_up = (DAI_default_price * target_procent) / 100 + DAI_default_price
#     # target_price_down = DAI_default_price - ((DAI_default_price * target_procent) / 100)
#     target_price_up = 1.015
#     target_price_down = 0.985
#
#     for item in coin_address:
#         result = coin_address.get(item)
#         print(result)

# while True:
#
#     actual_price = get_coin_price()
#     actual_price = toFixed(float(actual_price), 4)
#     print(actual_price)
#
#     dt = datetime.datetime.now()
#     dt_string = dt.strftime("Время: %H:%M:%S ")
#
#     text_up = f'‼️‼️📈ПРОДАВАТЬ📈️‼️‼️\n' \
#               f'DAI price - {actual_price} $\n' \
#               f'{dt_string}\n' \
#               f'Target price - {target_price_up} $\n' \
#               f'Target procent - up/down {target_procent} %\n' \
#               f'https://app.flatqube.io/swap/0:eb2ccad2020d9af9cec137d3146dde067039965c13a27d97293c931dae22b2b9/0:a519f99bb5d6d51ef958ed24d337ad75a1c770885dcd42d51d6663f9fcdacfb2'
#
#     text_down = '‼️‼️️📉ПОКУПАТЬ📉️‼️‼️\n' \
#                 f'DAI price - {actual_price} $\n' \
#                 f'{dt_string}\n' \
#                 f'Target price - {target_price_down} $\n' \
#                 f'Target procent - up/down {target_procent} %\n' \
#                 f'https://app.flatqube.io/swap/0:a519f99bb5d6d51ef958ed24d337ad75a1c770885dcd42d51d6663f9fcdacfb2/0:eb2ccad2020d9af9cec137d3146dde067039965c13a27d97293c931dae22b2b9'
#
#     if float(actual_price) == target_price_up or float(actual_price) > target_price_up:
#         requests.get(f"https://api.telegram.org/bot{tg_api_token}/sendMessage?chat_id=@dai_c0in&text={text_up}")
#         time.sleep(300)
#
#     elif float(actual_price) == target_price_down or float(actual_price) < target_price_down:
#         requests.get(f"https://api.telegram.org/bot{tg_api_token}/sendMessage?chat_id=@dai_c0in&text={text_down}")
#         time.sleep(300)


def main():
    while True:
        compare_prices()


if __name__ == "__main__":
    main()
