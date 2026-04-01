from typing import Dict, List, Any, Iterator


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency_code:
            yield transaction


transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
    {
        "id": 555123456,
        "state": "EXECUTED",
        "date": "2020-03-10T15:45:30.111222",
        "operationAmount": {"amount": "1500.50", "currency": {"name": "EUR", "code": "EUR"}},
        "description": "Перевод с карты на карту",
        "from": "Карта 4111111111111111",
        "to": "Карта 5555555555554444",
    },
]
usd_transactions = filter_by_currency(transactions, "USD")
for _ in range(2):
    print(next(usd_transactions))


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генератор, который возвращает описания операций из списка транзакций.
    """
    for transaction in transactions:
        # Проверяем наличие поля 'description' в транзакции
        if "description" in transaction:
            yield transaction["description"]
        else:
            # Если поле отсутствует, возвращаем пустую строку или можно пропустить элемент
            yield ""


descriptions = transaction_descriptions(transactions)
# Выводим первые 3 описания
for _ in range(3):
    print(next(descriptions))


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.
    """
    # Проверяем корректность границ
    if not (1 <= start <= 9999999999999999):
        raise ValueError("Начальное значение должно быть в диапазоне от 1 до 9999999999999999")
    if not (1 <= stop <= 9999999999999999):
        raise ValueError("Конечное значение должно быть в диапазоне от 1 до 9999999999999999")
    if start > stop:
        raise ValueError("Начальное значение не может быть больше конечного")

    for num in range(start, stop + 1):
        # Преобразуем число в строку и дополняем нулями слева до 16 символов
        num_str = str(num).zfill(16)
        # Разбиваем строку на блоки по 4 символа и соединяем пробелами
        formatted_card_number = f"{num_str[:4]} {num_str[4:8]} {num_str[8:12]} {num_str[12:]}"
        yield formatted_card_number


cards = card_number_generator(1, 5)
for card in cards:
    print(card)

cards = card_number_generator(1234567890123450, 1234567890123452)
for card in cards:
    print(card)
