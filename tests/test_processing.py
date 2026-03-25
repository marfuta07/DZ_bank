import pytest
from typing import List, Dict
from src.processing import filter_by_state

"""Тесты для функции фильтрации словарей по статусу"""

def test_default_state_executed():
        """Тест фильтрации по умолчанию (статус 'EXECUTED')"""
        list_dicts = [
            {"id": 414288290, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        ]

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
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        ]

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
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        ]

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
            {"id": 2, "state": "EXECUTED", "date": "2024-01-02T00:00:00"},
        ]

        result = filter_by_state(list_dicts, "EXECUTED")

        assert len(result) == 2
        assert result == list_dicts

def test_items_without_state_key():
        """Тест со словарями, не содержащими ключа 'state'"""
        list_dicts = [
            {"id": 1, "date": "2024-01-01T00:00:00"},  # Нет ключа state
            {"id": 2, "state": "EXECUTED", "date": "2024-01-02T00:00:00"},
            {"id": 3, "date": "2024-01-03T00:00:00"},  # Нет ключа state
        ]

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
            {"id": 3, "state": "PENDING", "date": "2024-01-03"},
        ]

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
            {"id": 2, "state": "executed", "date": "2024-01-02"},  # В нижнем регистре
        ]

        result_upper = filter_by_state(list_dicts, "EXECUTED")
        result_lower = filter_by_state(list_dicts, "executed")

        assert len(result_upper) == 1
        assert len(result_lower) == 1
        assert result_upper[0]["id"] == 1
        assert result_lower[0]["id"] == 2

def test_function_returns_list_of_dicts():
        """Тест что функция всегда возвращает список словарей"""
        list_dicts = [
            {"id": 1, "state": "EXECUTED", "date": "2024-01-01"},
        ]

        result = filter_by_state(list_dicts)

        assert isinstance(result, list)
        if result:  # Если есть элементы
            assert all(isinstance(item, dict) for item in result)

