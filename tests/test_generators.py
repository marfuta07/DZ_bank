from typing import Any, Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions

"""Тестирование функции filter_by_currency"""


def test_filter_usd_transactions() -> None:
    transactions_ = [
        {"operationAmount": {"currency": {"code": "USD"}}},
        {"operationAmount": {"currency": {"code": "RUB"}}},
    ]

    result = list(filter_by_currency(transactions_, "USD"))
    assert len(result) == 1
    assert result[0]["operationAmount"]["currency"]["code"] == "USD"


# Отсутствие транзакций в заданной валюте:
def test_no_transactions() -> None:
    transactions_ = [
        {"operationAmount": {"currency": {"code": "RUB"}}},
        {"operationAmount": {"currency": {"code": "EUR"}}},
    ]
    result = list(filter_by_currency(transactions_, "USD"))
    assert len(result) == 0


@pytest.mark.parametrize(
    "currency_code, expected_count",
    [
        ("USD", 3),  # Три транзакции в USD
        ("RUB", 2),  # Две транзакции в RUB
        ("EUR", 0),
    ],
)
def test_filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str, expected_count: int) -> None:
    result = list(filter_by_currency(transactions, currency_code))
    assert len(result) == expected_count

    result = list(filter_by_currency([], currency_code))  # Пустой список транзакций
    assert len(result) == 0


"""Тестирование функции transaction_descriptions"""


def test_dan() -> None:
    """Подготовка тестовых данных перед каждым тестом."""


transactions_with_descriptions = [
    {"id": 939719570, "description": "Перевод организации", "amount": 9824.07},
    {"id": 142264268, "description": "Перевод со счета на счет", "amount": 79114.93},
    {"id": 555123456, "description": "Перевод с карты на карту", "amount": 1500.50},
]


def test_normal_transactions() -> None:
    """Тест: корректное извлечение описаний из транзакций с полем description."""
    descriptions = list(transaction_descriptions(transactions_with_descriptions))

    expected = ["Перевод организации", "Перевод со счета на счет", "Перевод с карты на карту"]

    assert len(descriptions) == len(expected), f"Ожидалось {len(expected)} описаний, получено {len(descriptions)}"

    for i, (actual, exp) in enumerate(zip(descriptions, expected)):
        assert actual == exp, f"Описание №{i + 1}: ожидалось '{exp}', получено '{actual}'"


def test_empty_transactions_list() -> None:
    """Тест: пустой список транзакций."""
    descriptions = list(transaction_descriptions([]))

    # Ожидаем пустой список
    assert len(descriptions) == 0, f"Ожидался пустой список, но получено {len(descriptions)} элементов"
    assert not descriptions, "Список не пуст"


def test_single_transaction() -> None:
    """Тест: одна транзакция в списке."""
    single_transaction = [{"id": 123, "description": "Единственный перевод"}]

    descriptions = list(transaction_descriptions(single_transaction))

    assert len(descriptions) == 1, f"Ожидался 1 элемент, но получено {len(descriptions)}"
    assert descriptions[0] == "Единственный перевод", f"Ожидалось 'Единственный перевод', получено '{descriptions[0]}'"


def test_transactions_without_description_field() -> None:
    """Тест: транзакции без поля description."""
    transactions_without_descriptions = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}, {"id": 3, "amount": 300}]

    descriptions = list(transaction_descriptions(transactions_without_descriptions))

    # Ожидаем список пустых строк — по одной на каждую транзакцию
    expected = ["", "", ""]

    assert len(descriptions) == len(expected), f"Ожидалось {len(expected)} элементов, получено {len(descriptions)}"

    for i, actual in enumerate(descriptions):
        assert actual == expected[i], f"Элемент №{i}: ожидалось '{expected[i]}', получено '{actual}'"


def test_empty_description_string() -> None:
    """Тест: транзакция с пустым строковым значением description."""
    transactions = [
        {"id": 1, "description": ""},
        {"id": 2, "description": "Нормальное описание"},
        {"id": 3, "description": ""},
    ]

    descriptions = list(transaction_descriptions(transactions))

    expected = ["", "Нормальное описание", ""]

    assert len(descriptions) == len(expected), f"Ожидалось {len(expected)} элементов, получено {len(descriptions)}"

    for actual, exp in zip(descriptions, expected):
        assert actual == exp, f"Ожидалось '{exp}', получено '{actual}'"


@pytest.mark.parametrize(
    "transactions_, expected_descriptions",
    [
        (
            [  # Непустой список транзакций
                {"description": "Перевод организации"},
                {"description": "Перевод со счета на счет"},
                {"description": "Перевод со счета на счет"},
                {"description": "Перевод с карты на карту"},
                {"description": "Перевод организации"},
            ],
            [
                "Перевод организации",
                "Перевод со счета на счет",
                "Перевод со счета на счет",
                "Перевод с карты на карту",
                "Перевод организации",
            ],
        ),
        ([], []),  # Пустой список транзакций
    ],
)
def test_transaction_descriptions(transactions_: List[Dict[str, Any]], expected_descriptions: str) -> None:
    result = list(transaction_descriptions(transactions_))
    assert result == expected_descriptions


"""Тестирование генератора card_number_generator"""


def test_correct_formatting() -> None:
    """Тест: проверка корректности форматирования номеров карт."""
    generator = card_number_generator(1234567890123456, 1234567890123456)
    card_number = next(generator)
    # Проверяем формат: 4 цифры, пробел, 4 цифры, пробел, 4 цифры, пробел, 4 цифры
    assert card_number == "1234 5678 9012 3456", f"Некорректный формат: {card_number}"
    # Проверяем длину строки (16 цифр + 3 пробела = 19 символов)
    assert len(card_number) == 19, f"Некорректная длина номера: {len(card_number)}"


def test_leading_zeros() -> None:
    """Тест: проверка ведущих нулей для небольших чисел."""
    generator = card_number_generator(1, 1)
    card_number = next(generator)

    assert card_number == "0000 0000 0000 0001", f"Ведущие нули отсутствуют: {card_number}"


def test_range_generation() -> None:
    """Тест: генерация нескольких номеров в заданном диапазоне."""
    generator = card_number_generator(9999999999999997, 9999999999999999)
    cards = list(generator)

    expected = ["9999 9999 9999 9997", "9999 9999 9999 9998", "9999 9999 9999 9999"]

    assert len(cards) == len(expected), f"Ожидалось {len(expected)} карт, получено {len(cards)}"
    for i, (actual, exp) in enumerate(zip(cards, expected)):
        assert actual == exp, f"Карта №{i + 1}: ожидалось '{exp}', получено '{actual}'"


def test_single_card() -> None:
    """Тест: генерация одного номера карты."""
    generator = card_number_generator(1234123412341234, 1234123412341234)
    cards = list(generator)

    assert len(cards) == 1, f"Ожидался 1 номер карты, получено {len(cards)}"
    assert cards[0] == "1234 1234 1234 1234", f"Некорректный номер: {cards[0]}"


def test_edge_values() -> None:
    """Тест: проверка крайних значений диапазона."""
    # Минимальное значение
    min_generator = card_number_generator(1, 1)
    min_card = next(min_generator)
    assert min_card == "0000 0000 0000 0001", f"Ошибка в минимальном значении: {min_card}"

    # Максимальное значение
    max_generator = card_number_generator(9999999999999999, 9999999999999999)
    max_card = next(max_generator)
    assert max_card == "9999 9999 9999 9999", f"Ошибка в максимальном значении: {max_card}"


def test_large_range() -> None:
    """Тест: большой диапазон номеров (проверка производительности и корректности)."""
    generator = card_number_generator(1111222233334440, 1111222233334442)
    cards = list(generator)

    expected = ["1111 2222 3333 4440", "1111 2222 3333 4441", "1111 2222 3333 4442"]

    assert len(cards) == len(expected), f"Ожидалось {len(expected)} карт, получено {len(cards)}"
    for actual, exp in zip(cards, expected):
        assert actual == exp, f"Ожидалось '{exp}', получено '{actual}'"


def test_format_consistency() -> None:
    """Тест: последовательная проверка формата для нескольких номеров."""
    generator = card_number_generator(123, 125)
    cards = list(generator)

    for card in cards:
        # Проверяем, что строка состоит из 19 символов
        assert len(card) == 19, f"Длина номера некорректна: {len(card)}"
        # Проверяем наличие пробелов на правильных позициях
        assert card[4] == " " and card[9]


@pytest.mark.parametrize(
    "start, stop, expected",
    [
        (1, 2, ["0000 0000 0000 0001", "0000 0000 0000 0002"]),
        (5, 5, ["0000 0000 0000 0005"]),
    ],
)
def test_card_number_generator(start: int, stop: int, expected: List[str]) -> None:
    result = list(card_number_generator(start, stop))
    assert result == expected
