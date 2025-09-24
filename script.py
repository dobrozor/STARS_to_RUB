import requests


def get_crypto_price(currency_id, vs_currencies):
    """
    Получает цену криптовалюты по её ID.
    """
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={currency_id}&vs_currencies={vs_currencies}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if not data or currency_id not in data or vs_currencies not in data[currency_id]:
            print(f"Не удалось получить цену для {currency_id}.")
            return None

        return data[currency_id][vs_currencies]
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при запросе к API: {e}")
        return None


def main():
    usd_price_rub = get_crypto_price("usd", "rub")
    ton_price_usd = get_crypto_price("the-open-network", "usd")
    star_price_usd = 0.015
    ton_price_rub = get_crypto_price("the-open-network", "rub")

    if usd_price_rub and ton_price_usd:
        star_price_rub = star_price_usd * usd_price_rub
        star_price_ton = star_price_usd / ton_price_usd
        print(f"Цена 1 TON = {ton_price_rub:.2f} RUB")
        print(f"Цена 1 Звезды ({star_price_ton:.5f} TON) = {star_price_rub:.2f} RUB")
    else:
        print("Не удалось получить курсы")


if __name__ == "__main__":
    main()
