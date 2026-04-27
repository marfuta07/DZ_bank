from typing import List, Dict, Any
from src.bank_operations import process_bank_operations


def test_exact_match_case_insensitive() -> None:
    """Проверка точного совпадения без учёта регистра."""
    data: List[Dict[str, Any]] = [
        {"description": "Оплата интернета"},
        {"description": "перевод другу"},
        {"description": "Кафе 'Уют'"},
    ]
    categories: List[str] = ["Оплата", "Перевод", "Кафе"]
    result = process_bank_operations(data, categories)
    expected: Dict[str, int] = {"Оплата": 1, "Перевод": 1, "Кафе": 1}
    passed = result == expected


def test_partial_match_in_description() -> None:
    """Поиск по части слова в описании."""
    data: List[Dict[str, Any]] = [
        {"description": "Оплата за электричество"},
        {"description": "Покупка в магазине"},
        {"description": "Перевод на счёт"},
    ]
    categories: List[str] = ["оплата", "покупка", "перевод"]
    result = process_bank_operations(data, categories)
    expected: Dict[str, int] = {"оплата": 1, "покупка": 1, "перевод": 1}
    passed = result == expected


def test_no_matches_returns_zeros() -> None:
    """Если ни одна категория не найдена — все значения нулевые."""
    data: List[Dict[str, Any]] = [
        {"description": "Снятие наличных"},
        {"description": "Обслуживание счёта"},
    ]
    categories: List[str] = ["оплата", "перевод", "кафе"]
    result = process_bank_operations(data, categories)
    expected: Dict[str, int] = {"оплата": 0, "перевод": 0, "кафе": 0}
    passed = result == expected


def test_empty_data() -> None:
    """Пустой список операций — все категории с нулём."""
    data: List[Dict[str, Any]] = []
    categories: List[str] = ["оплата", "перевод"]
    result = process_bank_operations(data, categories)
    expected: Dict[str, int] = {"оплата": 0, "перевод": 0}
    passed = result == expected


def test_empty_categories() -> None:
    """Пустой список категорий — возвращается пустой словарь."""
    data: List[Dict[str, Any]] = [{"description": "Оплата"}]
    categories: List[str] = []
    result = process_bank_operations(data, categories)
    expected: Dict[str, int] = {}
    passed = result == expected


def test_operation_matches_first_category_only() -> None:
    """Операция с несколькими совпадениями учитывается только по первой найденной категории."""
    data: List[Dict[str, Any]] = [
        {"description": "Оплата и перевод другу"},  # подходит под "оплата" и "перевод"
    ]
    categories: List[str] = ["оплата", "перевод"]  # сначала "оплата" — она и попадёт в счётчик
    result = process_bank_operations(data, categories)
    expected: Dict[str, int] = {"оплата": 1, "перевод": 0}
    passed = result == expected


def test_missing_description_key() -> None:
    """Операции без поля 'description' игнорируются."""
    data: List[Dict[str, Any]] = [
        {"description": "Оплата в кафе"},
        {"id": 1, "amount": 100},  # нет description
    ]
    categories: List[str] = ["оплата", "кафе"]
    result = process_bank_operations(data, categories)
    expected: Dict[str, int] = {"оплата": 1, "кафе": 0}
    passed = result == expected


def test_category_with_special_characters() -> None:
    """Категория с символами, которые могут быть в regex (проверка на безопасность)."""
    data: List[Dict[str, Any]] = [
        {"description": "Оплата: интернет"},
        {"description": "Скидка 50% на покупку"},
    ]
    categories: List[str] = ["оплата:", "50%"]
    result = process_bank_operations(data, categories)
    expected: Dict[str, int] = {"оплата:": 1, "50%": 1}
    passed = result == expected


def test_overlapping_categories() -> None:
    """Проверка, что более короткие категории не перехватывают части других."""
    data: List[Dict[str, Any]] = [
        {"description": "оплата интернета"},
        {"description": "оплата"},
        {"description": "платёж за услуги"},
    ]
    categories: List[str] = ["оплата", "платёж"]
    result = process_bank_operations(data, categories)
    # "оплата" найдёт первые две, "платёж" — третью
    expected: Dict[str, int] = {"оплата": 2, "платёж": 1}
    passed = result == expected
