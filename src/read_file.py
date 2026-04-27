import csv
from typing import List, Dict, Any
import pandas as pd


def read_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из CSV-файла и возвращает список словарей.
    """
    transactions = []
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")  # Уточните разделитель: ',' или ';'
            for row in reader:
                transactions.append(dict(row))
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
    except Exception as e:
        print(f"Ошибка при чтении CSV: {e}")
    return transactions


data = read_from_csv("transactions.csv")
print(data)


def read_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из Excel-файла и возвращает список словарей.

    """
    transactions = []
    try:
        df = pd.read_excel(file_path)

        transactions = [
            {str(k): v for k, v in record.items()}
            for record in df.fillna("").to_dict(orient="records")
        ]
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
    except Exception as e:
        print(f"Ошибка при чтении Excel: {e}")
    return transactions


data_1 = read_from_excel("transactions_excel.xlsx")
print(data_1)
