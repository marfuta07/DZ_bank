import os
import requests
from dotenv import load_dotenv
from typing import Dict, Optional

# Константы для API
load_dotenv()
API_KEY = os.getenv("API_KEY")
EXCHANGE_API_URL = "https://api.apilayer.com/exchangerates_data/latest"


def get_exchange_rate(base_currency: str, target_currency: str = "RUB") -> Optional[float]:
    """
    Функция, которая принимает на вход транзакцию
    и возвращает сумму транзакции (amount) в рублях, тип данных — float.
    """
    headers = {"apikey": API_KEY}
    params = {"base": base_currency, "symbols": target_currency}

    try:
        response = requests.get(EXCHANGE_API_URL, headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return float(data["rates"][target_currency])
    except requests.RequestException:
        return None
    except KeyError:
        return None
    except ValueError:
        return None
    return None


def convert_currency_to_rub(transaction: Dict) -> float:
    """
    Если транзакция была в USD  или EUR,
    происходит обращение к внешнему API
    для получения текущего курса валют и конвертации суммы операции в рубли.
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

    except KeyError:
        return 0.0
    except ValueError:
        return 0.0
    except TypeError:
        return 0.0


transaction_rub = {"amount": 1000, "currency": "RUB"}
transaction_usd = {"amount": 50, "currency": "USD"}
transaction_eur = {"amount": 30, "currency": "EUR"}

print(convert_currency_to_rub(transaction_rub))  # 1000.0
print(convert_currency_to_rub(transaction_usd))  # ~3800–4200 (зависит от курса)
print(convert_currency_to_rub(transaction_eur))  # ~4500–5000
