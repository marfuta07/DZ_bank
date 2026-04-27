from typing import List, Dict, Any
from src.process_bank import process_bank_search


def test_search_case_insensitive()->None:
    """Поиск должен быть нечувствителен к регистру."""
    data = [
        {"id": 1, "description": "Оплата в кафе", "amount": 350.0},
        {"id": 2, "description": "оплата ЖКХ", "amount": 3000.0},
        {"id": 3, "description": "Перевод", "amount": 500.0},
    ]
    result = process_bank_search(data, "оплата")
    expected_ids = [1, 2]
    passed = all(op["id"] in expected_ids for op in result) and len(result) == 2


def test_search_exact_match()->None:
    """Тест точного совпадения."""
    data = [{"id": 1, "description": "Перевод другу", "amount": 1500.0}]
    result = process_bank_search(data, "Перевод другу")
    passed = len(result) == 1 and result[0]["id"] == 1


def test_search_partial_match()->None:
    """Поиск по части слова."""
    data = [{"id": 1, "description": "Возврат средств", "amount": 1200.0}]
    result = process_bank_search(data, "возврат")
    passed = len(result) == 1 and result[0]["id"] == 1


def test_no_match_returns_empty()->None:
    """Если нет совпадений — возвращается пустой список."""
    data = [{"id": 1, "description": "Оплата", "amount": 100.0}]
    result = process_bank_search(data, "ипотека")
    passed = result == []


def test_empty_data()->None:
    """Пустой список на входе — пустой список на выходе."""
    result = process_bank_search([], "оплата")
    passed = result == []


def test_missing_description_key()->None:
    """Операции без 'description' игнорируются, но не вызывают ошибок."""
    data: List[Dict[str, Any]]= [
        {"id": 1, "description": "Оплата", "amount": 100.0},
        {"id": 2, "amount": 200.0},  # нет description
    ]
    result = process_bank_search(data, "оплата")
    passed = len(result) == 1 and result[0]["id"] == 1


def test_special_characters_in_search()->None:
    """Поиск строки с спецсимволами (например, точка, вопросительный знак)."""
    data = [
        {"id": 1, "description": "Покупка на Amazon.com", "amount": 2000.0},
        {"id": 2, "description": "Возврат за товар?", "amount": 500.0},
    ]
    result1 = process_bank_search(data, "Amazon.com")
    result2 = process_bank_search(data, "товар?")
    passed = len(result1) == 1 and len(result2) == 1


def test_empty_search_string()->None:
    """Пустая строка — совпадает со всеми, где есть description."""
    data:List[Dict[str, Any]] = [
        {"id": 1, "description": "Оплата", "amount": 100.0},
        {"id": 2, "description": "Перевод", "amount": 200.0},
        {"id": 3, "amount": 300.0},  # без description
    ]
    result = process_bank_search(data, "")
    passed = len(result) == 2  # Только первые два имеют description


def test_search_with_spaces()->None:
    """Поиск строки с пробелами."""
    data = [{"id": 1, "description": "Оплата за интернет", "amount": 600.0}]
    result = process_bank_search(data, "за интернет")
    passed = len(result) == 1 and result[0]["id"] == 1
