from unittest.mock import patch, mock_open, Mock
import pandas as pd
from src.read_file import read_from_csv, read_from_excel

@patch("builtins.open", new_callable=mock_open, read_data="id;amount;currency\n1;100;USD\n")
@patch("csv.DictReader")
def test_read_from_csv(mock_dict_reader, mock_file):
    """Тест для CSV-чтения без использования self."""
    # Настраиваем поведение мока
    mock_dict_reader.return_value = [
        {"id": "1", "amount": "100", "currency": "USD"},
        {"id": "2", "amount": "200", "currency": "EUR"}
    ]

    result = read_from_csv("dummy.csv")

    assert mock_file.called, "Файл не был открыт"
    mock_file.assert_called_once_with("dummy.csv", mode="r", encoding="utf-8")
    assert len(result) == 2, f"Ожидалось 2 транзакции, получено: {len(result)}"
    assert result[0]["amount"] == "100", "Неверное значение amount в первой транзакции"


@patch("pandas.read_excel")
def test_read_from_excel(mock_read_excel):
    """Тест для Excel-чтения без использования self."""
    # Создаём мок для DataFrame
    mock_df = Mock()
    mock_df.where.return_value = mock_df
    mock_df.to_dict.return_value = [
        {"id": 1, "amount": "500", "currency": "RUB"},
        {"id": 2, "amount": "300", "currency": "USD"}
    ]
    mock_read_excel.return_value = mock_df

    result = read_from_excel("dummy.xlsx")

    # Проверки
    mock_read_excel.assert_called_once_with("dummy.xlsx")
    assert len(result) == 2, f"Ожидалось 2 транзакции, получено: {len(result)}"
    assert result[1]["amount"] == "300", "Неверное значение amount во второй транзакции"


