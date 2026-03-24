import pytest
from src.widget import mask_account_card

"""Тесты для функции маскировки номера карты или счёта"""


def test_wid_cards():
    assert mask_account_card("Visa Platinum 7000792289606361") == "Visa Platinum 7000 79** **** 6361"


def test_mask_credit_card():
    """Тест маскировки кредитной карты (не 'счёт')"""
    result = mask_account_card("Visa Platinum 7000792289606361")
    assert result == "Visa Platinum 7000 79** **** 6361"


def test_mask_debit_card():
    """Тест маскировки дебетовой карты (не 'счёт')"""
    result = mask_account_card("Maestro 5555555555444444")
    assert result == "Maestro 5555 55** **** 4444"


def test_mask_bank_account():
    """Тест маскировки банковского счёта (когда имя = 'счёт')"""
    result = mask_account_card("Счет 73654108430135874305")
    assert result == "Счет **** **** **** **** 4305"


def test_case_insensitive_account():
    """Тест регистронезависимого сравнения для 'счёт'"""

    result1 = mask_account_card("счет 73654108430135874305")
    result2 = mask_account_card("СЧЕТ 73654108430135874305")
    result3 = mask_account_card("Счёт 73654108430135874305")  # Кириллическая 'ё'
    assert result1 == "счет **** **** **** **** 4305"
    assert result2 == "СЧЕТ **** **** **** **** 4305"
    assert result3 == "Счёт Введен некорректный номер карты"


def test_multiple_words_in_name():
    """Тест с многословным названием карты"""
    result = mask_account_card("American Express Gold 4111111111111111")
    assert result == "American Express Gold 4111 11** **** 1111"


def test_empty_input():
    """Тест с пустой строкой"""
    with pytest.raises(IndexError):
        mask_account_card("")


def test_whitespace_only_input():
    """Тест со строкой, содержащей только пробелы"""
    with pytest.raises(IndexError):
        mask_account_card("   ")


@pytest.mark.parametrize(
    "input_data, expected_card_call",
    [
        ("Visa 1234567890123456", "Visa 1234 56** **** 3456"),
        ("MasterCard 5555555555554444", "MasterCard 5555 55** **** 4444"),
        ("Discover 6011000990139424", "Discover 6011 00** **** 9424"),
    ],
)
def test_various_card_types(input_data, expected_card_call):
    """Параметризованный тест для разных типов карт"""
    result = mask_account_card(input_data)
    assert result == expected_card_call


def test_function_returns_string():
    """Тест, что функция всегда возвращает строку"""
    result1 = mask_account_card("Visa 1111222233334444")
    result2 = mask_account_card("Счет 12345678901234567890")

    assert isinstance(result1, str)
    assert isinstance(result2, str)
