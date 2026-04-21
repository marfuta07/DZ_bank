import json
import os
from typing import Dict, List


def load_transactions_from_json(file_path: str) -> List[Dict]:
    """
    Принимает на вход путь до JSON-файла и возвращает список словарей
    с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, функция возвращает пустой список
    """
    # Проверяем, существует ли файл
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            # Проверяем, является ли данные списком
            if isinstance(data, list):
                return data
            else:
                return []
    except json.JSONDecodeError:
        # Если файл пустой или содержит некорректный JSON
        return []
    except FileNotFoundError:
        # Если файл пустой или содержит некорректный JSON
        return []


if __name__ == "__main__":
    print(load_transactions_from_json(os.path.join(os.path.dirname(__file__), "../data/operations.json")))
