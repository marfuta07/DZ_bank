import os
import requests
from dotenv import load_dotenv
from typing import Dict, Optional, Union


# Константы для API
load_dotenv()
API_KEY = os.getenv("API_KEY")
EXCHANGE_API_URL = "https://api.apilayer.com/exchangerates_data/latest"


def get_exchange_rate(base_currency: str, target_currency: str = "RUB") -> Optional[float]:
    """
    Получает курс валюты через Exchange Rates Data API.

    Параметры:
        base_currency (str): Исходная валюта (например, 'USD', 'EUR').
        target_currency (str): Целевая валюта (по умолчанию — 'RUB').

    Возвращает:
        Текущий курс в виде float или None при ошибке.
    """
    headers = {"apikey": API_KEY}
    params = {"base": base_currency, "symbols": target_currency}

    try:
        response = requests.get(EXCHANGE_API_URL, headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data["rates"][target_currency]
    except (requests.RequestException, KeyError, ValueError):
        return None
    return None


def convert_currency_to_rub(transaction: Dict) -> float:
    """
    Возвращает сумму транзакции в рублях.

    Параметры:
        transaction (dict): Словарь с данными о транзакции. Должен содержать ключи:
            - 'amount' (число) — сумма операции
            - 'currency' (str) — валюта ('RUB', 'USD', 'EUR' и т.д.)

    Возвращает:
        Сумму транзакции в рублях (float). Если валюта не поддерживается или ошибка — возвращается 0.0.
    """
    try:
        amount = float(transaction["amount"])
        currency = transaction.get("currency", "RUB").upper()

        # Если валюта уже RUB — конвертация не нужна
        if currency == "RUB":
            return amount

        # Поддерживаем конвертацию из USD и EUR
        if currency in ("USD", "EUR"):
            rate = get_exchange_rate(currency, "RUB")
            if rate is not None:
                return round(amount * rate, 2)

        # Если валюта неизвестна или конвертация не удалась
        return 0.0

    except (KeyError, ValueError, TypeError):
        return 0.0

transaction_rub = {"amount": 1000, "currency": "RUB"}
transaction_usd = {"amount": 50, "currency": "USD"}
transaction_eur = {"amount": 30, "currency": "EUR"}

print(convert_currency_to_rub(transaction_rub))  # 1000.0
print(convert_currency_to_rub(transaction_usd))  # ~3800–4200 (зависит от курса)
print(convert_currency_to_rub(transaction_eur))  # ~4500–5000