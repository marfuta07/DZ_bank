import pytest
from src.masks import get_mask_card_number

 """Тесты для функции маскировки номера банковской карты"""

    def test_valid_16_digit_card(self):
        """Тест корректного 16‑значного номера карты"""
        result = get_mask_card_number("7000792289606361")
        assert result == "7000 79** **** 6361"

    def test_valid_15_digit_card_amex(self):
        """Тест корректного 15‑значного номера карты (American Express)"""
        result = get_mask_card_number("378282246310005")
        assert result == "3782 8***** 0005"

    def test_card_with_spaces(self):
        """Тест номера карты с пробелами"""
        result = get_mask_card_number("7000 7922 8960 6361")
        assert result == "7000 79** **** 6361"

    def test_card_with_dashes(self):
        """Тест номера карты с дефисами"""
        result = get_mask_card_number("7000-7922-8960-6361")
        assert result == "7000 79** **** 6361"

    def test_card_with_mixed_separators(self):
        """Тест номера карты со смешанными разделителями"""
        result = get_mask_card_number("7000 7922-8960 6361")
        assert result == "7000 79** **** 6361"

    def test_leading_trailing_whitespace(self):
        """Тест номера карты с ведущими и trailing пробелами"""
        result = get_mask_card_number("  7000792289606361  ")
        assert result == "7000 79** **** 6361"

    def test_empty_string(self):
        """Тест пустой строки"""
        result = get_mask_card_number("")
        assert result == "Введён некорректный номер карты"

    def test_none_input(self):
        """Тест None в качестве входных данных"""
        with pytest.raises(TypeError):
            get_mask_card_number(None)

    def test_non_string_input(self):
        """Тест нестрокового ввода"""
        with pytest.raises(TypeError):
            get_mask_card_number(1234567890123456)

    def test_short_number(self):
        """Тест слишком короткого номера карты"""
        result = get_mask_card_number("1234")
        assert result == "Введён некорректный номер карты"

    def test_long_number(self):
        """Тест слишком длинного номера карты"""
        result = get_mask_card_number("12345678901234567890")
        assert result == "Введён некорректный номер карты"

    def test_14_digit_number(self):
        """Тест 14‑значного номера (некорректная длина)"""
        result = get_mask_card_number("12345678901234")
        assert result == "Введён некорректный номер карты"

    def test_17_digit_number(self):
        """Тест 17‑значного номера (некорректная длина)"""
        result = get_mask_card_number("12345678901234567")
        assert result == "Введён некорректный номер карты"

    def test_letters_in_number(self):
        """Тест номера с буквами"""
        result = get_mask_card_number("7000AB2289606361")
        assert result == "Введён некорректный номер карты"

    def test_special_characters(self):
        """Тест номера со специальными символами"""
        result = get_mask_card_number("7000!@#$%^&*()6361")
        assert result == "Введён некорректный номер карты"

    def test_only_separators(self):
        """Тест строки, содержащей только разделители"""
        result = get_mask_card_number("----    ----")
        assert result == "Введён некорректный номер карты"

    def test_single_digit(self):
        """Тест одного символа"""
        result = get_mask_card_number("5")
        assert result == "Введён некорректный номер карты"

    def test_all_zeros(self):
        """Тест номера из всех нулей"""
        result = get_mask_card_number("0000000000000000")
        assert result == "0000 00** **** 0000"

    def test_repeating_digits(self):
        """Тест номера с повторяющимися цифрами"""
        result = get_mask_card_number("1111222233334444")
        assert result == "1111 22** **** 4444"


    @pytest.mark.parametrize("invalid_input", [
        "",
        "123",
        "abc",
        "!@#",
        "12a4567890123456",
        " " * 16,  # строка из 16 пробелов
    ])
    def test_various_invalid_inputs(self, invalid_input):
        """Параметризованный тест для различных некорректных входных данных"""
        result = get_mask_card_number(invalid_input)
        assert result == "Введён некорректный номер карты"

    @pytest.mark.parametrize("valid_input,expected", [
        ("7000792289606361", "7000 79** **** 6361"),
        ("  7000792289606361  ", "7000 79** **** 6361"),
        ("7000-7922-8960-6361", "7000 79** **** 6361"),
        ("7000 7922 8960 6361", "7000 79** **** 6361"),
    ])
    def test_various_valid_formats(self, valid_input, expected):
        """Параметризованный тест для различных корректных форматов ввода"""
        result = get_mask_card_number(valid_input)
        assert result == expected