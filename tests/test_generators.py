from typing import Dict, List

import pytest
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

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
                         [("USD", 3),  # Три транзакции в USD
                          ("RUB", 2),  # Две транзакции в RUB
                          ("EUR", 0),  # Нет транзакций в EUR
                          ([], 0) ])
def test_filter_by_currency(transactions, currency_code, expected_count):
    result = list(filter_by_currency(transactions, currency_code))
    assert len(result) == expected_count