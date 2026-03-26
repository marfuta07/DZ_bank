import pytest
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


@pytest.mark.parametrize(
    "input_data, expected_card_call",
    [
        ("Visa 1234567890123456", "Visa 1234 56** **** 3456"),
        ("MasterCard 5555555555554444", "MasterCard 5555 55** **** 4444"),
        ("Discover 6011000990139424", "Discover 6011 00** **** 9424"),
    ],
)
def test_various_card_types(input_data:str, expected_card_call:str)-> None:
    """Параметризованный тест для разных типов карт"""
    result = mask_account_card(input_data)
    assert result == expected_card_call

@pytest.mark.parametrize(
    "input_date,expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-07-25T15:45:30.123456", "25.07.2023"),
        ("2025-12-01T08:30:15.987654", "01.12.2025"),
        ("2020-02-29T00:00:00.000000", "29.02.2020"),  # Високосный год
    ],
)
def test_parametrized_valid_dates(input_date:str, expected:str)->None:
    """Параметризованный тест для различных корректных дат"""
    result = get_date(input_date)
    assert result == expected


@pytest.mark.parametrize(
    "state_value",
    [
        "EXECUTED",
        "CANCELED",
        "PENDING",
        "COMPLETED",
        "",
    ],
)
def test_various_state_values(state_value:str)->None:
    """Параметризованный тест для разных значений статуса"""
    list_dicts = [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-01"},
        {"id": 2, "state": "CANCELED", "date": "2024-01-02"},
        {"id": 3, "state": "PENDING", "date": "2024-01-03"},
    ]

    # Подсчитываем ожидаемое количество элементов
    expected_count = sum(1 for item in list_dicts if item.get("state") == state_value)
    result = filter_by_state(list_dicts, state_value)

    assert len(result) == expected_count
    for item in result:
        assert item["state"] == state_value


@pytest.fixture
def sample_data() -> List[Dict]:
    """Фикстура с тестовыми данными"""
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


def test_sort_descending_default(sample_data: List[Dict])-> None:
    """Тест сортировки по убыванию (по умолчанию)"""
    result = sort_by_date(sample_data)
    # Ожидаемый порядок: самая новая дата первая
    expected_dates = [
        "2019-07-03T18:35:29.512364",
        "2018-10-14T08:21:33.419441",
        "2018-09-12T21:27:25.241689",
        "2018-06-30T02:08:58.425572",
    ]

    result_dates = [item["date"] for item in result]
    assert result_dates == expected_dates


@pytest.mark.parametrize(
    "reverse,expected_order",
    [
        (
            True,
            [
                "2019-07-03T18:35:29.512364",
                "2018-10-14T08:21:33.419441",
                "2018-09-12T21:27:25.241689",
                "2018-06-30T02:08:58.425572",
            ],
        ),
        (
            False,
            [
                "2018-06-30T02:08:58.425572",
                "2018-09-12T21:27:25.241689",
                "2018-10-14T08:21:33.419441",
                "2019-07-03T18:35:29.512364",
            ],
        ),
    ],
)
def test_parametrized_sorting_orders(sample_data: List[Dict], reverse: bool, expected_order: List[str])-> None:
    """Параметризованный тест для проверки обоих направлений сортировки"""
    result = sort_by_date(sample_data, reverse=reverse)
    result_dates = [item["date"] for item in result]
    assert result_dates == expected_order