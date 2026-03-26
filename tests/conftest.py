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
