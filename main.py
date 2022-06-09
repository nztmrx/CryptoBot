import datetime
import time

import data
from data import *
import requests
import logging

token = tg_api_token

logging.basicConfig(level=logging.INFO)


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
    try:
        compare_value = "USDT"

        if coin_name == "WBTC":
            coin_name = "BTC"

        if coin_name == "WETH":
            coin_name = "ETH"

        payload = {"symbol": f"{coin_name}{compare_value}"}
        s = requests.Session()
        r = s.get(url_binance_api, params=payload)
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

    except ConnectionError as e:
        print(e)


def get_price_on_flat_qube(coin_name):
    try:
        coin_list = get_coins_address()
        coin_address = coin_list[coin_name]
        s = requests.Session()
        r = s.post(f"{url_flat_qube_api}{coin_address}")
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
    except ConnectionError as e:
        print(e)


def compare_prices():
    try:
        address_list = get_coins_address()
        # target_procent = target_procent
        target_procent = 3.7
        for items in address_list:
            b_items = get_price_on_binance(items)
            fq_items = get_price_on_flat_qube(items)
            print()
            b_price = float(b_items['price'])
            fq_price = float(fq_items['price'])
            print(f"Binance: {b_items['name']}: {b_price} $$$\n"
                  f"FlatQube: {fq_items['name']}: {fq_price} $$$")
            if b_price > fq_price:
                print(f"Разница = {toFixed((b_price - fq_price), 5)} $")
                try:
                    result = (b_price / fq_price - 1) * 100
                except ZeroDivisionError:
                    continue
                print(f"Разница в процентах = {toFixed(result, 2)}%")

            elif fq_price > b_price:
                print(f"Разница = {toFixed((fq_price - b_price), 5)} $")
                try:
                    result = (fq_price / b_price - 1) * 100
                except ZeroDivisionError:
                    continue
                print(f"Разница в процентах = {toFixed(result, 2)}%")
            print()

            result = 0
            if float(b_price) > float(fq_price):
                try:
                    result = (b_price / fq_price - 1) * 100
                except ZeroDivisionError:
                    continue
                if result > target_procent:
                    result_items = {
                        "market": "Binance",
                        "name": b_items["name"],
                        "b_price": b_price,
                        "fq_price": fq_price,
                        "procent": target_procent,
                        "target_procent": target_procent,
                        "different": f"{round(result, 2)}%"
                    }
                    send_message(result_items)
                continue

            elif float(fq_price) > float(b_price):
                try:
                    result = (fq_price / b_price - 1) * 100
                except ZeroDivisionError:
                    continue
                if result > target_procent:
                    result_items = {
                        "market": "FlatQube.io",
                        "name": b_items["name"],
                        "b_price": b_price,
                        "fq_price": fq_price,
                        "target_procent": target_procent,
                        "different": f"{round(result, 2)}%"
                    }
                    send_message(result_items)
                continue

        dt = datetime.datetime.now()
        dt_string = dt.strftime("Время: %H:%M:%S")

        print(f"{dt_string}, TargetProcent: {target_procent}%")
        time.sleep(60)
    except ConnectionError as e:
        print(e)


def send_message(items):
    dt = datetime.datetime.now()
    dt_string = dt.strftime("Время: %H:%M:%S ")

    if items["market"] == "FlatQube.io":
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
Binance: {coin_name} - {b_price} $
Разница = {toFixed((fq_price - b_price), 5)} $
{dt_string}
{link}
                """

        requests.get(f"https://api.telegram.org/bot{tg_api_token}/sendMessage?chat_id=@dai_c0in&text={text}")


def check_sub(user_id):
    print(data.user_list)
    print(user_id)
    if str(user_id) in data.user_list:
        access = True
    else:
        access = False
    return access


def main():
    while True:
        compare_prices()
    # print(check_sub('785023632')
    pass

if __name__ == "__main__":
    main()
