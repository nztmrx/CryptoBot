import datetime
import json
import time
from data import *
import requests

token = tg_api_token

coin_address = {
    "DAI": f"{DAI_ADDRESS}",
    "WEVER": f"{WEVER_ADDRESS}",
    "USD": f"{USD_ADDRESS}"
}


def coin_addresses(coin_name):
    if coin_name == "DAI":
        return coin_address["DAI"]
    elif coin_name == "WEVER":
        return coin_address["WEVER"]
    elif coin_name == "USD":
        return coin_address["USD"]


def get_coin_price_on_name(coin_name):
    final_coin_address = coin_addresses(coin_name)

    r = requests.post(f"{url_to_api_fq}{final_coin_address}")

    main_price = r.json()
    print(toFixed(main_price["price"], 4), main_price["currency"])

    return toFixed(main_price["price"], 4), main_price["currency"]


def get_coin_price():
    final_coin_address = coin_addresses("DAI")

    r = requests.post(f"{url_to_api_fq}{final_coin_address}")

    main_price = r.json()
    time.sleep(15)

    actual_price_info = main_price['price']
    actual_price_change = main_price['priceChange']
    actual_volume = main_price["volume24h"]
    actual_volume = toFixed(float(actual_volume), 0)
    actual_price_info = toFixed(float(actual_price_info), 3)

    dt = datetime.datetime.now()
    dt_string = dt.strftime("Время: %H:%M:%S ")

    info_result = f"{dt_string}| DAI = {actual_price_info} $ | Price Change: {actual_price_change} | Volume24: {actual_volume} $\n"
    print(info_result)

    # with open("data.txt", "a") as f:
    #     f.write(info_result)

    return actual_price_info


def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


def compare_prices(target_procent):
    DAI_default_price = 1
    # target_price_up = (DAI_default_price * target_procent) / 100 + DAI_default_price
    # target_price_down = DAI_default_price - ((DAI_default_price * target_procent) / 100)
    target_price_up = 1.015
    target_price_down = 0.985

    while True:

        actual_price = get_coin_price()
        actual_price = toFixed(float(actual_price), 4)
        print(actual_price)

        dt = datetime.datetime.now()
        dt_string = dt.strftime("Время: %H:%M:%S ")

        text_up = f'‼️‼️📈ПРОДАВАТЬ📈️‼️‼️\n' \
                  f'DAI price - {actual_price} $\n' \
                  f'{dt_string}\n' \
                  f'Target price - {target_price_up} $\n' \
                  f'Target procent - up/down {target_procent} %\n' \
                  f'https://app.flatqube.io/swap/0:eb2ccad2020d9af9cec137d3146dde067039965c13a27d97293c931dae22b2b9/0:a519f99bb5d6d51ef958ed24d337ad75a1c770885dcd42d51d6663f9fcdacfb2'

        text_down = '‼️‼️️📉ПОКУПАТЬ📉️‼️‼️\n' \
                    f'DAI price - {actual_price} $\n' \
                    f'{dt_string}\n' \
                    f'Target price - {target_price_down} $\n' \
                    f'Target procent - up/down {target_procent} %\n' \
                    f'https://app.flatqube.io/swap/0:a519f99bb5d6d51ef958ed24d337ad75a1c770885dcd42d51d6663f9fcdacfb2/0:eb2ccad2020d9af9cec137d3146dde067039965c13a27d97293c931dae22b2b9'

        if float(actual_price) == target_price_up or float(actual_price) > target_price_up:
            requests.get(f"https://api.telegram.org/bot{tg_api_token}/sendMessage?chat_id=@dai_c0in&text={text_up}")
            time.sleep(300)

        elif float(actual_price) == target_price_down or float(actual_price) < target_price_down:
            requests.get(f"https://api.telegram.org/bot{tg_api_token}/sendMessage?chat_id=@dai_c0in&text={text_down}")
            time.sleep(300)


def main():
    compare_prices(1.5)


if __name__ == "__main__":
    main()
