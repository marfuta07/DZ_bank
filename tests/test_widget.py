import pytest
from src.widget import mask_account_card, get_date

"""Тесты для функции маскировки номера карты или счёта"""
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


"""Тесты для функции преобразования формата даты"""

def test_valid_date_format():
        """Тест с корректной датой в стандартном формате"""
        result = get_date("2024-03-11T02:26:18.671407")
        assert result == "11.03.2024"

def test_different_year():
        """Тест с другим годом"""
        result = get_date("2022-05-15T10:30:45.123456")
        assert result == "15.05.2022"

def test_different_month():
        """Тест с другим месяцем"""
        result = get_date("2024-12-25T08:15:30.987654")
        assert result == "25.12.2024"

def test_single_digit_day():
        """Тест с однозначным днём (с ведущим нулём)"""
        result = get_date("2024-03-05T14:20:10.123456")
        assert result == "05.03.2024"

def test_january():
        """Тест для января (месяц 01)"""
        result = get_date("2024-01-01T00:00:00.000000")
        assert result == "01.01.2024"

def test_december():
        """Тест для декабря (месяц 12)"""
        result = get_date("2024-12-31T23:59:59.999999")
        assert result == "31.12.2024"

def test_leap_year_date():
        """Тест даты в високосном году"""
        result = get_date("2024-02-29T12:00:00.000000")  # 2024 — високосный год
        assert result == "29.02.2024"

def test_boundary_dates():
        """Тест граничных дат"""
        test_cases = [
            ("2024-01-01T00:00:00.000000", "01.01.2024"),
            ("2024-12-31T23:59:59.999999", "31.12.2024")
        ]
        for input_date, expected in test_cases:
            result = get_date(input_date)
            assert result == expected

@pytest.mark.parametrize("input_date,expected", [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-07-25T15:45:30.123456", "25.07.2023"),
        ("2025-12-01T08:30:15.987654", "01.12.2025"),
        ("2020-02-29T00:00:00.000000", "29.02.2020"),  # Високосный год
    ])
def test_parametrized_valid_dates(input_date, expected):
        """Параметризованный тест для различных корректных дат"""
        result = get_date(input_date)
        assert result == expected

def test_invalid_format_missing_separator():
        """Тест с некорректным форматом (отсутствует разделитель)"""
        # Проверяем, что функция пытается обработать, но результат будет некорректным
        result = get_date("20240311T02:26:18.671407")  # Нет дефисов
        assert len(result) == 10  # Всё равно возвращает строку длиной 10
        # Но формат будет неправильным
        assert result != "11.03.2024"

def test_none_input():
        """Тест с None в качестве входных данных"""
        with pytest.raises(TypeError):
            get_date(None)

def test_function_returns_string():
        """Тест, что функция всегда возвращает строку"""
        result = get_date("2024-03-11T02:26:18.671407")
        assert isinstance(result, str)
        assert len(result) == 10  # Формат DD.MM.YYYY всегда 10 символов

def test_consistent_format():
        """Тест согласованности формата вывода"""
        result = get_date("2024-03-11T02:26:18.671407")
        parts = result.split('.')
        assert len(parts) == 3
        assert len(parts[0]) == 2  # День — 2 цифры
        assert len(parts[1]) == 2  # Месяц — 2 цифры
        assert len(parts[2]) == 4  # Год — 4 цифры
