from typing import Dict, List

import pytest
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


"""Тестирование функции filter_by_currency"""

def test_filter_usd_transactions():
    transactions_ = [
    {"operationAmount": {"currency": {"code": "USD"}}},
    {"operationAmount": {"currency": {"code": "RUB"}}} ]

    result = list(filter_by_currency(transactions_, "USD"))
    assert len(result) == 1
    assert result[0]['operationAmount']['currency']['code'] == "USD"

#Отсутствие транзакций в заданной валюте:

def test_no_transactions():
    transactions_ = [
    {"operationAmount": {"currency": {"code": "RUB"}}},
    {"operationAmount": {"currency": {"code": "EUR"}}} ]
    result = list(filter_by_currency(transactions_, "USD"))
    assert len(result) == 0


#Обработка пустого списка:
def test_empty_transactions():
    transactions_ = []
    result = list(filter_by_currency(transactions_, "USD"))
    assert len(result) == 0

@pytest.mark.parametrize("currency_code, expected_count",
                         [ ("USD", 3),  # Три транзакции в USD
                           ("RUB", 2),  # Две транзакции в RUB
                           ("EUR", 0),  ])
def test_filter_by_currency(transactions, currency_code, expected_count):
    result = list(filter_by_currency(transactions, currency_code))
    assert len(result) == expected_count

    result = list(filter_by_currency([], currency_code))  # Пустой список транзакций
    assert len(result) == 0



"""Тестирование функции transaction_descriptions"""
def setUp():
    """Подготовка тестовых данных перед каждым тестом."""
transactions_with_descriptions = [
    {
        "id": 939719570,
        "description": "Перевод организации",
        "amount": 9824.07
    },
    {
        "id": 142264268,
        "description": "Перевод со счета на счет",
        "amount": 79114.93
    },
    {
        "id": 555123456,
        "description": "Перевод с карты на карту",
        "amount": 1500.50
    }
]

transactions_mixed =[
    {
        "id": 1,
        "description": "Покупка в магазине"
    },
    {
        "id": 2
        # Нет поля description
    },
    {
        "id": 3,
        "description": "Оплата услуг"
    },
    {
        "id": 4,
        "description": ""
        # Пустое описание
    }
]


def test_normal_transactions():
    """Тест: корректное извлечение описаний из транзакций с полем description."""
    descriptions = list(transaction_descriptions(transactions_with_descriptions))

    expected = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод с карты на карту"
    ]

    assert len(descriptions) == len(expected), f"Ожидалось {len(expected)} описаний, получено {len(descriptions)}"

    for i, (actual, exp) in enumerate(zip(descriptions, expected)):
        assert actual == exp, f"Описание №{i + 1}: ожидалось '{exp}', получено '{actual}'"


def test_empty_transactions_list():
    """Тест: пустой список транзакций."""
    descriptions = list(transaction_descriptions([]))

    # Ожидаем пустой список
    assert len(descriptions) == 0, f"Ожидался пустой список, но получено {len(descriptions)} элементов"
    assert not descriptions, "Список не пуст"


def test_single_transaction():
    """Тест: одна транзакция в списке."""
    single_transaction = [{
        "id": 123,
        "description": "Единственный перевод"
    }]

    descriptions = list(transaction_descriptions(single_transaction))

    assert len(descriptions) == 1, f"Ожидался 1 элемент, но получено {len(descriptions)}"
    assert descriptions[0] == "Единственный перевод", f"Ожидалось 'Единственный перевод', получено '{descriptions[0]}'"


def test_transactions_without_description_field():
    """Тест: транзакции без поля description."""
    transactions_without_descriptions = [
        {"id": 1, "amount": 100},
        {"id": 2, "amount": 200},
        {"id": 3, "amount": 300}
    ]

    descriptions = list(transaction_descriptions(transactions_without_descriptions))

    # Ожидаем список пустых строк — по одной на каждую транзакцию
    expected = ['', '', '']

    assert len(descriptions) == len(expected), f"Ожидалось {len(expected)} элементов, получено {len(descriptions)}"

    for i, actual in enumerate(descriptions):
        assert actual == expected[i], f"Элемент №{i}: ожидалось '{expected[i]}', получено '{actual}'"


def test_mixed_transactions():
    """Тест: смешанный список транзакций (с description и без)."""
    descriptions = list(transaction_descriptions(transactions_mixed))

    expected = [
        "Покупка в магазине",
        "",  # транзакция без description
        "Оплата услуг",
        ""  # транзакция с пустым description
    ]

    assert len(descriptions) == len(expected), f"Ожидалось {len(expected)} элементов, получено {len(descriptions)}"

    for i, (actual, exp) in enumerate(zip(descriptions, expected)):
        assert actual == exp, f"Элемент №{i}: ожидалось '{exp}', получено '{actual}'"


def test_empty_description_string():
    """Тест: транзакция с пустым строковым значением description."""
    transactions = [
        {"id": 1, "description": ""},
        {"id": 2, "description": "Нормальное описание"},
        {"id": 3, "description": ""}
    ]

    descriptions = list(transaction_descriptions(transactions))

    expected = ["", "Нормальное описание", ""]

    assert len(descriptions) == len(expected), f"Ожидалось {len(expected)} элементов, получено {len(descriptions)}"

    for actual, exp in zip(descriptions, expected):
        assert actual == exp, f"Ожидалось '{exp}', получено '{actual}'"


@pytest.mark.parametrize("transactions_, expected_descriptions", [
    ([  # Непустой список транзакций
        {'description': 'Перевод организации'},
        {'description': 'Перевод со счета на счет'},
        {'description': 'Перевод со счета на счет'},
        {'description': 'Перевод с карты на карту'},
        {'description': 'Перевод организации'}
    ],
    [
        "Перевод организации", "Перевод со счета на счет", "Перевод со счета на счет",
        "Перевод с карты на карту", "Перевод организации"
    ]),
    ([], [])  # Пустой список транзакций
])
def test_transaction_descriptions(transactions_, expected_descriptions):
    result = list(transaction_descriptions(transactions_))
    assert result == expected_descriptions

