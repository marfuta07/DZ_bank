from typing import Any, Dict, List, Optional
import os
import json
import csv
from src.masks import get_mask_card_number, get_mask_account
import os

# Определяем тип операции
Operation = Dict[str, Any]


def load_data_from_json(file_path: str) -> List[Dict[str, Any]]:
    """Загружает данные из JSON-файла."""
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден.")
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [op for op in data if isinstance(op, dict)]
    except Exception as e:
        print(f"Ошибка при чтении JSON: {e}")
        return []


def load_data_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """Загружает данные из CSV-файла."""
    if not os.path.exists(file_path):
        print(f" Файл {file_path} не найден.")
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return [row for row in reader]
    except Exception as e:
        print(f" Ошибка при чтении CSV: {e}")
        return []


def load_data_from_xlsx(file_path: str) -> List[Operation]:
    """
    Загружает данные из XLSX-файла и возвращает список словарей.
    Ключи в словарях — строки (названия столбцов).

    Args:
        file_path: Путь к XLSX-файлу.

    Returns:
        Список операций в формате списка словарей с строковыми ключами.
        При ошибке — пустой список.
    """
    try:
        import pandas as pd
    except ImportError:
        print("Ошибка: не установлен pandas. Установите: pip install pandas")
        return []

    if not os.path.exists(file_path):
        print(f"Файл не найден: {file_path}")
        return []

    try:
        df = pd.read_excel(file_path)
        # Явно преобразуем ключи в строки, чтобы mypy был доволен
        records: List[Operation] = []
        for record in df.to_dict(orient="records"):
            # Принудительно делаем ключи строками
            str_record: Operation = {str(k): v for k, v in record.items()}
            records.append(str_record)
        return records
    except Exception as e:
        print(f"Ошибка при чтении XLSX-файла: {e}")
        return []


# === Фильтрация и обработка ===


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """Фильтрует операции по подстроке в 'description' (регистронезависимо)."""
    if not search.strip():
        return data
    query = search.strip().lower()
    return [op for op in data if "description" in op and query in op["description"].lower()]


def filter_by_status(data: List[Dict[str, Any]], status: str) -> Optional[List[Dict[str, Any]]]:
    """Фильтрация по статусу: EXECUTED, CANCELED, PENDING."""
    upper_status = status.upper()
    allowed = {"EXECUTED", "CANCELED", "PENDING"}
    if upper_status not in allowed:
        return None
    return [op for op in data if str(op.get("state", "")).upper() == upper_status]


def sort_operations(data: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """Сортировка по дате."""
    from datetime import datetime

    def parse_date(date_str: str) -> datetime:
        try:
            return datetime.fromisoformat(date_str.replace("T", " ").replace("Z", "+00:00"))
        except:
            return datetime.min

    return sorted(data, key=lambda x: parse_date(x.get("date", "")), reverse=reverse)


def filter_rub_only(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Только рублёвые операции."""
    return [
        op
        for op in data
        if str(op.get("currency_code", "")).upper() in {"RUB", "RUR"}
        or str(op.get("operationAmount", {}).get("currency", {}).get("code")) == "RUB"
    ]


def format_amount(op: Dict[str, Any]) -> str:
    """Форматирует сумму и валюту."""
    amount = op.get("amount") or op.get("operationAmount", {}).get("amount")
    currency = op.get("currency_code") or op.get("operationAmount", {}).get("currency", {}).get("code", "Неизвестно")
    try:
        return f"{int(float(amount))} {currency}"
    except:
        return f"{amount} {currency}"


def print_operations(operations: List[Dict[str, Any]]) -> None:
    """Выводит операции с маскировкой через get_mask_card_number и get_mask_account."""
    if not operations:
        print("❌ Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"\n📊 Всего банковских операций в выборке: {len(operations)}\n")

    for op in operations:
        # Дата и описание
        date_str = op.get("date", "")
        try:
            from datetime import datetime

            date = datetime.fromisoformat(date_str.replace("T", " ").replace("Z", "+00:00"))
            print(date.strftime("%d.%m.%Y"), end=" ")
        except:
            print("??/??/????", end=" ")

        print(op.get("description", "Без описания"))

        # Откуда → Куда
        from_field = op.get("from", "")
        to_field = op.get("to", "")

        # Маскировка через функции из masks.py
        if from_field:
            if "Счет" in from_field:
                acc_num = "".join(filter(str.isdigit, from_field))
                from_field = get_mask_account(acc_num)
            else:
                from_field = get_mask_card_number(from_field)

        if to_field:
            if "Счет" in to_field:
                acc_num = "".join(filter(str.isdigit, to_field))
                to_field = get_mask_account(acc_num)
            else:
                to_field = get_mask_card_number(to_field)

        if from_field and to_field:
            print(f"{from_field} -> {to_field}")
        elif to_field:
            print(to_field)

        # Сумма
        print(f"Сумма: {format_amount(op)}\n")


# === Основная логика ===


def main() -> None:
    """Основная функция — связывает все модули и взаимодействует с пользователем."""
    print("Привет Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    data: List[Dict[str, Any]] = []
    while True:
        choice = input("Введите номер: ").strip()
        if choice == "1":
            print("📁 Для обработки выбран JSON-файл.")
            data = load_data_from_json("data/operations.json")
            break
        elif choice == "2":
            print("📁 Для обработки выбран CSV-файл.")
            data = load_data_from_csv("data/operations.csv")
            break
        elif choice == "3":
            print("📁 Для обработки выбран XLSX-файл.")
            data = load_data_from_xlsx("data/operations.xlsx")
            break
        else:
            print("Введите 1, 2 или 3.")

    if not data:
        print("Нет данных для обработки. Завершение.")
        return

    # === Фильтрация по статусу ===
    allowed_statuses = {"EXECUTED", "CANCELED", "PENDING"}
    while True:
        print(f"\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные для фильтровки статусы: {', '.join(allowed_statuses)}")
        status = input("Введите статус: ").strip()
        result = filter_by_status(data, status)
        if result is None:
            print(f' Статус операции "{status}" недоступен.')
        else:
            data = result
            print(f' Операции отфильтрованы по статусу "{status.upper()}"')
            break

    # === Сортировка по дате ===
    if input("\n Отсортировать операции по дате? Да/Нет: ").strip().lower() in {"да", "д"}:
        order = input(" Отсортировать по возрастанию или по убыванию? ").strip().lower()
        reverse = "возрастанию" not in order
        data = sort_operations(data, reverse=reverse)

    # === Только рубли? ===
    if input("\n🇷🇺 Выводить только рублёвые транзакции? Да/Нет: ").strip().lower() in {"да", "д"}:
        data = filter_rub_only(data)

    # === Поиск по описанию — используем нашу функцию ===
    if input("\n Отфильтровать по слову в описании? Да/Нет: ").strip().lower() in {"да", "д"}:
        query = input("Введите слово для поиска: ").strip()
        data = process_bank_search(data, query)
        print(f' Найдено {len(data)} операций по запросу "{query}"')

    # === Вывод результата ===
    print("\n  Распечатываю итоговый список транзакций...")
    print_operations(data)


# Запуск
if __name__ == "__main__":
    main()
