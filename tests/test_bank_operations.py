from typing import List, Dict, Any
from src.bank_operations import process_bank_operations

def test_exact_match_case_insensitive()->None:
    """Проверка точного совпадения без учёта регистра."""
    data = [
        {"description": "Оплата интернета"},
        {"description": "перевод другу"},
        {"description": "Кафе 'Уют'"},
    ]
    categories = ["Оплата", "Перевод", "Кафе"]
    result = process_bank_operations(data, categories)
    expected = {"Оплата": 1, "Перевод": 1, "Кафе": 1}
    passed = result == expected


def test_partial_match_in_description()->None:
    """Поиск по части слова в описании."""
    data = [
        {"description": "Оплата за электричество"},
        {"description": "Покупка в магазине"},
        {"description": "Перевод на счёт"},
    ]
    categories = ["оплата", "покупка", "перевод"]
    result = process_bank_operations(data, categories)
    expected = {"оплата": 1, "покупка": 1, "перевод": 1}
    passed = result == expected


def test_no_matches_returns_zeros()->None:
    """Если ни одна категория не найдена — все значения нулевые."""
    data = [
        {"description": "Снятие наличных"},
        {"description": "Обслуживание счёта"},
    ]
    categories = ["оплата", "перевод", "кафе"]
    result = process_bank_operations(data, categories)
    expected = {"оплата": 0, "перевод": 0, "кафе": 0}
    passed = result == expected


def test_empty_data()->None:
    """Пустой список операций — все категории с нулём."""
    data = []
    categories = ["оплата", "перевод"]
    result = process_bank_operations(data, categories)
    expected = {"оплата": 0, "перевод": 0}
    passed = result == expected


def test_empty_categories()->None:
    """Пустой список категорий — возвращается пустой словарь."""
    data = [{"description": "Оплата"}]
    categories = []
    result = process_bank_operations(data, categories)
    expected = {}
    passed = result == expected


def test_operation_matches_first_category_only()->None:
    """Операция с несколькими совпадениями учитывается только по первой найденной категории."""
    data = [
        {"description": "Оплата и перевод другу"},  # подходит под "оплата" и "перевод"
    ]
    categories = ["оплата", "перевод"]  # сначала "оплата" — она и попадёт в счётчик
    result = process_bank_operations(data, categories)
    expected = {"оплата": 1, "перевод": 0}
    passed = result == expected


def test_missing_description_key()->None:
    """Операции без поля 'description' игнорируются."""
    data = [
        {"description": "Оплата в кафе"},
        {"id": 1, "amount": 100},  # нет description
    ]
    categories = ["оплата", "кафе"]
    result = process_bank_operations(data, categories)
    expected = {"оплата": 1, "кафе": 0}
    passed = result == expected


def test_category_with_special_characters()->None:
    """Категория с символами, которые могут быть в regex (проверка на безопасность)."""
    data = [
        {"description": "Оплата: интернет"},
        {"description": "Скидка 50% на покупку"},
    ]
    categories = ["оплата:", "50%"]
    result = process_bank_operations(data, categories)
    expected = {"оплата:": 1, "50%": 1}
    passed = result == expected


def test_overlapping_categories()->None:
    """Проверка, что более короткие категории не перехватывают части других."""
    data = [
        {"description": "оплата интернета"},
        {"description": "оплата"},
        {"description": "платёж за услуги"},
    ]
    categories = ["оплата", "платёж"]
    result = process_bank_operations(data, categories)
    # "оплата" найдёт первые две, "платёж" — третью
    expected = {"оплата": 2, "платёж": 1}
    passed = result == expected
