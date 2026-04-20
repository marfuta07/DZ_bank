import os
from typing import Dict, Optional

import requests
from dotenv import load_dotenv

# Константы для API
load_dotenv()
API_KEY = os.getenv("API_KEY")
EXCHANGE_API_URL = "https://api.apilayer.com/exchangerates_data/convert"

headers = {"apikey": API_KEY}


def get_exchange_rate(amount: float, base_currency: str, target_currency: str = "RUB") -> Optional[float]:
    """
    Функция, которая принимает на вход транзакцию
    и возвращает сумму транзакции (amount) в рублях, тип данных — float.
    """
    if not API_KEY:
        print("Ошибка: API_KEY не найден в .env файле.")
        return None

    params:dict[str, str|int|float]= {"from": base_currency, "to": target_currency, "amount": amount}
    try:
        response = requests.get(EXCHANGE_API_URL, headers=headers, params=params, timeout=5)
        response.raise_for_status()  # Проверка HTTP-статуса
        data = response.json()

        if "result" in data:
            return round(float(data["result"]), 2)
        else:
            print(f"Поле 'result' отсутствует в ответе: {data}")
            return None

    except requests.exceptions.HTTPError as e:
        if response.status_code == 429:
            print("Ошибка: превышен лимит запросов к API (429 Too Many Requests)")
        elif response.status_code == 401:
            print("Ошибка: неверный или отсутствующий API-ключ (401 Unauthorized)")
        else:
            print(f"HTTP ошибка: {e}")
        return None
    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Ошибка сети или обработки ответа: {e}")
        return None


def convert_currency_to_rub(transaction: Dict) -> float:
    """
    Если транзакция была в USD  или EUR,
    происходит обращение к внешнему API
    для получения текущего курса валют и конвертации суммы операции в рубли.
    """
    try:
        amount = float(transaction["operationAmount"]["amount"])
        currency = transaction["operationAmount"]["currency"]["code"].upper()

        # Если валюта уже RUB — конвертация не нужна
        if currency == "RUB":
            return amount

        # Поддерживаем конвертацию из USD и EUR
        if currency in ("USD", "EUR"):
            # Получаем конвертированную сумму напрямую: amount USD → ? RUB
            converted_amount = get_exchange_rate(amount, currency, "RUB")
            if converted_amount is not None:
                return converted_amount

        print(f"Валюта {currency} не поддерживается или конвертация не удалась.")
        return 0.0

    except (KeyError, ValueError, TypeError) as e:
        print(f"Ошибка при обработке транзакции: {e}")
        return 0.0


transaction_rub = {"operationAmount": {"amount": "1000", "currency": {"code": "RUB"}}}
transaction_usd = {"operationAmount": {"amount": "50", "currency": {"code": "USD"}}}
transaction_eur = {"operationAmount": {"amount": "30", "currency": {"code": "EUR"}}}

print(convert_currency_to_rub(transaction_rub))  # 1000.0
print(convert_currency_to_rub(transaction_usd))  # ~3800–4200 (зависит от курса)
print(convert_currency_to_rub(transaction_eur))  # ~4500–5000
