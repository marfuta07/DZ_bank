import re
from typing import List, Dict


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """
    Фильтрует список банковских операций по строке поиска в описании операции.
    Предполагается, что каждый словарь в списке `data` содержит ключ 'description' (описание),
    в котором может встречаться искомая строка.
    *Используется модуль `re` для поиска с учётом нечувствительности к регистру.*
    Параметры:
    - data: список словарей с данными операций
    - search: строка поиска
    """
    # Компилируем регулярное выражение с флагом IGNORECASE для поиска без учёта регистра
    pattern = re.compile(re.escape(search), re.IGNORECASE)

    # Фильтруем данные: проверяем, есть ли совпадение в поле 'description'
    result = [
        operation for operation in data
        if 'description' in operation and pattern.search(operation['description'])
    ]

    return result

bank_data = [
    {"id": 1, "description": "Оплата в кафе 'Уют'", "amount": 450.0},
    {"id": 2, "description": "Перевод другу", "amount": 2000.0},
    {"id": 3, "description": "Оплата за интернет", "amount": 600.0},
    {"id": 4, "description": "Возврат средств за возврат товара", "amount": 1200.0}
]

# Поиск операций, где в описании есть слово "оплата"
result = process_bank_search(bank_data, "оплата")
print(result)
