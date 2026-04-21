import logging

logger = logging.getLogger('utils')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('logs/utils.log', 'w', encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

import json
import os
from typing import Dict, List


def load_transactions_from_json(file_path: str) -> List[Dict]:
    """
    Принимает на вход путь до JSON-файла и возвращает список словарей
    с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, функция возвращает пустой список
    """
    logger.debug(f"Попытка загрузить транзакции из файла: {file_path}")
    # Проверяем, существует ли файл
    if not os.path.exists(file_path):
        logger.warning(f"Файл не найден: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            logger.info(f"Файл найден. Начинаем чтение: {file_path}")
            data = json.load(file)
            logger.debug(f"Данные успешно загружены. Тип данных: {type(data).__name__}")

            # Проверяем, является ли данные списком
            if isinstance(data, list):
                logger.info(f"Успешно загружено {len(data)} транзакций из файла: {file_path}")
                return data
            else:
                logger.warning(
                    f"Ожидался список транзакций, но получен объект типа {type(data).__name__}. "
                    f"Файл: {file_path}"
                )
                return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка парсинга JSON в файле {file_path}: {e}")
        return []
    except PermissionError:
        logger.error(f"Нет прав на чтение файла: {file_path}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при загрузке файла {file_path}: {e}")
        return []

if __name__ == "__main__":
    print(load_transactions_from_json(os.path.join(os.path.dirname(__file__), "../data/operations.json")))
