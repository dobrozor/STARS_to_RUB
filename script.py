import os
import requests
import re
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Fragment API настройки
FRAGMENT_API_URL = "https://api.fragment-api.com/v1"
TOKEN_FRAGMENT = "eyJhbGciO131313cCI6IkpXVCJ9.123123.123123123123123123" # Это фрагмент токен, создается https://fragment-api.com/dashboard в вкладке Fragment Connections

# Настройки отправки
username = "dobrozor"  # Любое имя, можно оставить моё
quantity = 50 


def get_ton_price():
    """Получение актуального курса TON к рублю с CoinGecko"""
    try:
        response = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=rub",
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            return data['the-open-network']['rub']
        else:
            print("❌ Не удалось получить курс TON, используем fallback 280 руб")
            return 280  # fallback курс
    except Exception as e:
        print(f"❌ Ошибка получения курса: {e}, используем fallback 280 руб")
        return 280  # fallback курс


def send_stars_directly(username, quantity):
    """Прямая отправка звезд пользователю"""
    try:
        # Отправка звезд
        data = {
            "username": username,
            "quantity": quantity,
            "show_sender": "false"
        }
        headers = {
            "Authorization": f"JWT {TOKEN_FRAGMENT}",
            "Content-Type": "application/json"
        }

        res = requests.post(f"{FRAGMENT_API_URL}/order/stars/", json=data, headers=headers)

        if res.status_code == 200:
            return True, "Успешно"
        else:
            # Извлекаем сумму из ошибки
            error_text = res.text
            amount_match = re.search(r"transaction total: (\d+\.\d+) TON", error_text)
            if amount_match:
                return False, amount_match.group(1) + " TON"
            else:
                return False, "Сумма не найдена в ошибке"

    except Exception as e:
        return False, str(e)


def send_stars_auto(username, quantity):
    """Функция для автоматической отправки"""
    success, message = send_stars_directly(username, quantity)
    return success, message


if __name__ == "__main__":
    # Получаем актуальный курс TON
    TON_TO_RUB = get_ton_price()

    print(f"📊 Цена 1 TON: {TON_TO_RUB:.2f} руб")

    success, message = send_stars_auto(username, quantity)

    if success:
        print(f"Ошибка обновления курсов. Звезды были отправлены. ВАЖНО! Кошелек должен быть пустой")
    else:
        if "TON" in message:
            ton_amount = message.replace(" TON", "")
            ton_float = float(ton_amount)
            rub_amount = ton_float * TON_TO_RUB

            one_star_ton = ton_float / quantity
            one_star_rub = rub_amount / quantity

            print(f"⭐ Цена 1 звезды: {one_star_ton:.6f} TON ({one_star_rub:.2f} руб)")
        else:
            print(f"❌ Ошибка: {message}")
