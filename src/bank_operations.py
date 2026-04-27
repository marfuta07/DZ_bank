from collections import Counter
from typing import List, Dict, Any


def process_bank_operations (data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество банковских операций в каждой из заданных категорий.
    Категории определяются по вхождению строки из `categories`
    в поле `description` каждой операции (регистронезависимо).
    *Используется `Counter` для эффективного подсчёта.*
    Параметры:
    - data: список словарей с данными операций (обязательно с полем 'description')
    - categories: список строк — названия категорий для поиска
    Возвращает:
    - словарь: ключ — категория, значение — количество операций, где она найдена
    """
    # Список для хранения найденных категорий по каждой операции
    matched_categories = []

    # Приводим категории к нижнему регистру для регистронезависимого поиска
    lower_categories = [cat.lower() for cat in categories]

    for operation in data:
        desc = operation.get("description", "").lower()
        # Проверяем, к какой категории относится описание
        for cat in lower_categories:
            if cat in desc:
                matched_categories.append(cat)
                break  # Операция относится только к одной категории (первая найденная)

    # Считаем количество по каждой категории
    counts = Counter(matched_categories)
    # Возвращаем обычный словарь, включая категории с нулём, если нужно их явно указать
    return {cat: counts.get(cat.lower(), 0) for cat in categories}

bank_data = [
    {"id": 1, "description": "Оплата в кафе 'Уголок'", "amount": 450.0},
    {"id": 2, "description": "Перевод другу", "amount": 2000.0},
    {"id": 3, "description": "Оплата за интернет", "amount": 600.0},
    {"id": 4, "description": "Покупка в магазине продуктов", "amount": 800.0},
    {"id": 5, "description": "Кафе 'Старбакс'", "amount": 300.0},
    {"id": 6, "description": "Оплата ЖКХ", "amount": 3500.0},
]

# Список категорий
categories = ["оплата", "перевод", "кафе", "покупка", "транспорт"]
# Обработка
result = process_bank_operations(bank_data, categories)
# Вывод
print("Количество операций по категориям:")
for category, count in result.items():
    print(f"  • {category}: {count}")