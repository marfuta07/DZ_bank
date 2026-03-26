import pytest
from src.masks import get_mask_card_number, get_mask_account
"""Тесты для функции маскировки номера банковской карты"""


@pytest.mark.parametrize(
    "invalid_input",
    [
        "",
        "123",
        "abc",
        "!@#",
        "12a4567890123456",
        " " * 16,
    ],
)
def test_various_invalid_inputs(invalid_input:str)->None:
    """Параметризованный тест для различных некорректных входных данных"""
    result = get_mask_card_number(invalid_input)
    assert result == "Введен некорректный номер карты"


@pytest.mark.parametrize(
    "valid_input,expected",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("7000792289606361  ", "7000 79** **** 6361"),
        ("7000-7922-8960-6361", "7000 79** **** 6361"),
        ("7000 7922 8960 6361", "7000 79** **** 6361"),
    ],
)
def test_various_valid_formats(valid_input:str, expected:str)-> None:
    """Параметризованный тест для различных корректных форматов ввода"""
    result = get_mask_card_number(valid_input)
    assert result == expected


def test_valid_16_digit_card()-> None:
    """Тест корректного 16‑значного номера карты"""
    result = get_mask_card_number("7000792289606361")
    assert result == "7000 79** **** 6361"


def test_card_with_spaces()->None:
    """Тест номера карты с пробелами"""
    result = get_mask_card_number("7000 7922 8960 6361")
    assert result == "7000 79** **** 6361"


def test_card_with_dashes()-> None:
    """Тест номера карты с дефисами"""
    result = get_mask_card_number("7000-7922-8960-6361")
    assert result == "7000 79** **** 6361"


def test_card_with_mixed_separators()-> None:
    """Тест номера карты со смешанными разделителями"""
    result = get_mask_card_number("7000 7922-8960 6361")
    assert result == "7000 79** **** 6361"


def test_leading_trailing_whitespace()-> None:
    """Тест номера карты с ведущими и trailing пробелами"""
    result = get_mask_card_number("  7000792289606361  ")
    assert result == "7000 79** **** 6361"


def test_empty_string()-> None:
    """Тест пустой строки"""
    result = get_mask_card_number("")
    assert result == "Введен некорректный номер карты"


def test_short_number()-> None:
    """Тест слишком короткого номера карты"""
    result = get_mask_card_number("1234")
    assert result == "Введен некорректный номер карты"


def test_long_number()-> None:
    """Тест слишком длинного номера карты"""
    result = get_mask_card_number("12345678901234567890")
    assert result == "Введен некорректный номер карты"


def test_14_digit_number()-> None:
    """Тест 14‑значного номера (некорректная длина)"""
    result = get_mask_card_number("12345678901234")
    assert result == "Введен некорректный номер карты"


def test_17_digit_number()-> None:
    """Тест 17‑значного номера (некорректная длина)"""
    result = get_mask_card_number("12345678901234567")
    assert result == "Введен некорректный номер карты"


def test_letters_in_number()-> None:
    """Тест номера с буквами"""
    result = get_mask_card_number("7000AB2289606361")
    assert result == "Введен некорректный номер карты"


def test_special_characters()-> None:
    """Тест номера со специальными символами"""
    result = get_mask_card_number("7000!@#$%^&*()6361")
    assert result == "Введен некорректный номер карты"


def test_only_separators()-> None:
    """Тест строки, содержащей только разделители"""
    result = get_mask_card_number("----    ----")
    assert result == "Введен некорректный номер карты"


def test_single_digit()-> None:
    """Тест одного символа"""
    result = get_mask_card_number("5")
    assert result == "Введен некорректный номер карты"


def test_all_zeros()-> None:
    """Тест номера из всех нулей"""
    result = get_mask_card_number("0000000000000000")
    assert result == "0000 00** **** 0000"


def test_repeating_digits()-> None:
    """Тест номера с повторяющимися цифрами"""
    result = get_mask_card_number("1111222233334444")
    assert result == "1111 22** **** 4444"


"""Тесты для функции маскировки номера банковского счёта"""


def test_valid_account_number()-> None:
    """Тест с корректным 20‑значным номером счёта"""
    result = get_mask_account("12345678901234567890")
    assert result == "**** **** **** **** 7890"


def test_account_number_with_leading_zeros()-> None:
    """Тест с номером счёта, начинающимся с нулей"""
    result = get_mask_account("00001234567890123456")
    assert result == "**** **** **** **** 3456"


def test_short_account_number()-> None:
    """Тест с номером счёта меньше 20 цифр"""
    result = get_mask_account("1234567890")
    assert "некорректный номер" in result.lower()


def test_long_account_number()-> None:
    """Тест с номером счёта больше 20 цифр"""
    result = get_mask_account("123456789012345678901")
    assert "некорректный номер" in result.lower()


def test_non_digit_character()-> None:
    """Тест с номером счёта, содержащим буквы"""
    result = get_mask_account("12345abc678901234567")
    assert "некорректный номер" in result.lower()


def test_special_charact()-> None:
    """Тест с номером счёта, содержащим спецсимволы"""
    result = get_mask_account("12345@#$%67890123456")
    assert "некорректный номер" in result.lower()


def test2_empty_string()-> None:
    """Тест с пустой строкой"""
    result = get_mask_account("")
    assert "некорректный номер" in result.lower()


def test_whitespace_only()-> None:
    """Тест со строкой, содержащей только пробелы"""
    result = get_mask_account("                    ")
    assert "некорректный номер" in result.lower()


@pytest.mark.parametrize(
    "invalid_input",
    [
        "1234567890123456789",  # 19 цифр
        "123456789012345678901",  # 21 цифра
        "12345abc678901234567",  # с буквами
        "12345@#$%67890123456",  # со спецсимволами
        "",  # пустая строка
        "    " * 20,
    ],
)
def test1_various_invalid_inputs(invalid_input:str)-> None:
    """Параметризованный тест для различных некорректных входных данных"""
    result = get_mask_account(invalid_input)
    assert "некорректный номер" in result.lower()
