import pytest
from typing import List, Dict
from src.processing import filter_by_state, sort_by_date
"""Тесты для функции фильтрации словарей по статусу"""
def test_default_state_executed():
        """Тест фильтрации по умолчанию (статус 'EXECUTED')"""
        list_dicts = [
            {"id": 414288290, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"}, ]

        result = filter_by_state(list_dicts)

        assert len(result) == 2
        assert result[0]["id"] == 414288290
        assert result[1]["id"] == 939719570
        for item in result:
            assert item["state"] == "EXECUTED"

def test_specific_state_canceled():
        """Тест фильтрации по конкретному статусу ('CANCELED')"""
        list_dicts = [
            {"id": 414288290, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"}, ]

        result = filter_by_state(list_dicts, "CANCELED")

        assert len(result) == 2
        assert result[0]["id"] == 594226727
        assert result[1]["id"] == 615064591
        for item in result:
            assert item["state"] == "CANCELED"

def test_no_matching_items():
        """Тест когда нет элементов с заданным статусом"""
        list_dicts = [
            {"id": 414288290, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}, ]

        result = filter_by_state(list_dicts, "PENDING")

        assert len(result) == 0
        assert isinstance(result, list)

def test_empty_list():
        """Тест с пустым списком входных данных"""
        result = filter_by_state([])
        assert len(result) == 0
        assert isinstance(result, list)

def test_all_items_match():
        """Тест когда все элементы соответствуют статусу"""
        list_dicts = [
            {"id": 1, "state": "EXECUTED", "date": "2024-01-01T00:00:00"},
            {"id": 2, "state": "EXECUTED", "date": "2024-01-02T00:00:00"}, ]

        result = filter_by_state(list_dicts, "EXECUTED")

        assert len(result) == 2
        assert result == list_dicts

def test_items_without_state_key():
        """Тест со словарями, не содержащими ключа 'state'"""
        list_dicts = [
            {"id": 1, "date": "2024-01-01T00:00:00"},  # Нет ключа state
            {"id": 2, "state": "EXECUTED", "date": "2024-01-02T00:00:00"},
            {"id": 3, "date": "2024-01-03T00:00:00"}, ]

        result = filter_by_state(list_dicts, "EXECUTED")

        assert len(result) == 1
        assert result[0]["id"] == 2

@pytest.mark.parametrize("state_value", [
        "EXECUTED",
        "CANCELED",
        "PENDING",
        "COMPLETED",
        "",  ])
def test_various_state_values(state_value):
        """Параметризованный тест для разных значений статуса"""
        list_dicts = [
            {"id": 1, "state": "EXECUTED", "date": "2024-01-01"},
            {"id": 2, "state": "CANCELED", "date": "2024-01-02"},
            {"id": 3, "state": "PENDING", "date": "2024-01-03"}, ]

        # Подсчитываем ожидаемое количество элементов
        expected_count = sum(1 for item in list_dicts if item.get("state") == state_value)
        result = filter_by_state(list_dicts, state_value)

        assert len(result) == expected_count
        for item in result:
            assert item["state"] == state_value

def test_case_sensitive_matching():
        """Тест чувствительности к регистру"""
        list_dicts = [
            {"id": 1, "state": "EXECUTED", "date": "2024-01-01"},
            {"id": 2, "state": "executed", "date": "2024-01-02"}, ]

        result_upper = filter_by_state(list_dicts, "EXECUTED")
        result_lower = filter_by_state(list_dicts, "executed")

        assert len(result_upper) == 1
        assert len(result_lower) == 1
        assert result_upper[0]["id"] == 1
        assert result_lower[0]["id"] == 2

def test_function_returns_list_of_dicts():
        """Тест что функция всегда возвращает список словарей"""
        list_dicts = [
            {"id": 1, "state": "EXECUTED", "date": "2024-01-01"}, ]

        result = filter_by_state(list_dicts)

        assert isinstance(result, list)
        if result:  # Если есть элементы
            assert all(isinstance(item, dict) for item in result)
"""Тесты для функции сортировки списка словарей по дате"""
@pytest.fixture
def sample_data() -> List[Dict]:
        """Фикстура с тестовыми данными"""
        return [
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},]

def test_sort_descending_default(sample_data: List[Dict]):
        """Тест сортировки по убыванию (по умолчанию)"""
        result = sort_by_date(sample_data)
        # Ожидаемый порядок: самая новая дата первая
        expected_dates = [
            "2019-07-03T18:35:29.512364",
            "2018-10-14T08:21:33.419441",
            "2018-09-12T21:27:25.241689",
            "2018-06-30T02:08:58.425572"  ]

        result_dates = [item["date"] for item in result]
        assert result_dates == expected_dates

def test_sort_ascending(sample_data: List[Dict]):
    """Тест сортировки по возрастанию"""
    result = sort_by_date(sample_data, reverse=False)

    # Ожидаемый порядок: самая старая дата первая
    expected_dates = [
        "2018-06-30T02:08:58.425572",
        "2018-09-12T21:27:25.241689",
        "2018-10-14T08:21:33.419441",
        "2019-07-03T18:35:29.512364"]

    result_dates = [item["date"] for item in result]
    assert result_dates == expected_dates

def test_empty_list():
    """Тест с пустым списком"""
    result = sort_by_date([])
    assert result == []

def test_single_item_list(sample_data: List[Dict]):
    """Тест со списком из одного элемента"""
    single_item = [sample_data[0]]
    result = sort_by_date(single_item)
    assert result == single_item

def test_identical_dates():
    """Тест с одинаковыми датами"""
    data = [
        {"id": 1, "state": "A", "date": "2024-01-01T00:00:00.000000"},
        {"id": 2, "state": "B", "date": "2024-01-01T00:00:00.000000"},
        {"id": 3, "state": "C", "date": "2024-01-01T00:00:00.000000"}]
    result = sort_by_date(data)
    # При одинаковых датах порядок должен сохраняться
    result_ids = [item["id"] for item in result]
    expected_ids = [1, 2, 3]
    assert result_ids == expected_ids

def test_original_list_unchanged(sample_data: List[Dict]):
    """Тест, что исходная коллекция не изменяется"""
    original_copy = sample_data.copy()
    sort_by_date(sample_data)
    # Исходный список должен остаться неизменным
    assert sample_data == original_copy

def test_returns_new_list(sample_data: List[Dict]):
    """Тест, что функция возвращает новый список, а не модифицирует исходный"""
    result = sort_by_date(sample_data)
    assert result is not sample_data  # Это разные объекты в памяти

def test_different_data_structure():
    """Тест с другим набором полей в словарях"""
    data = [
        {"name": "Alice", "date": "2024-03-01T10:00:00.000000"},
        {"name": "Bob", "date": "2024-02-15T15:30:00.000000"},
        {"name": "Charlie", "date": "2024-04-10T08:45:00.000000"}]
    result = sort_by_date(data, reverse=False)
    expected_dates = [
        "2024-02-15T15:30:00.000000",
        "2024-03-01T10:00:00.000000",
        "2024-04-10T08:45:00.000000"]
    result_dates = [item["date"] for item in result]
    assert result_dates == expected_dates

@pytest.mark.parametrize("reverse,expected_order", [
    (True, [
        "2019-07-03T18:35:29.512364",
        "2018-10-14T08:21:33.419441",
        "2018-09-12T21:27:25.241689",
        "2018-06-30T02:08:58.425572"]),
    (False, [
        "2018-06-30T02:08:58.425572",
        "2018-09-12T21:27:25.241689",
        "2018-10-14T08:21:33.419441",
        "2019-07-03T18:35:29.512364"])])
def test_parametrized_sorting_orders(sample_data: List[Dict], reverse: bool, expected_order: List[str]):
    """Параметризованный тест для проверки обоих направлений сортировки"""
    result = sort_by_date(sample_data, reverse=reverse)
    result_dates = [item["date"] for item in result]
    assert result_dates == expected_order


def test_consistent_output_type(sample_data: List[Dict]):
    """Тест, что функция всегда возвращает список словарей"""
    result = sort_by_date(sample_data)
    assert isinstance(result, list)
    for item in result:
        assert isinstance(item, dict)
        assert "date" in item
