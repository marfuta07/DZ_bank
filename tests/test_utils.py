from unittest.mock import patch, mock_open
import json

from src.utils import load_transactions_from_json


def test_file_not_found_returns_empty_list()->None:
    """Если файл не существует — возвращается пустой список."""
    with patch("os.path.exists", return_value=False):
        result = load_transactions_from_json("data/operations.json")
        assert result == []


def test_empty_file_returns_empty_list()->None:
    """Если файл пустой — возвращается пустой список."""
    with patch("os.path.exists", return_value=True), patch("builtins.open", mock_open(read_data="")):
        result = load_transactions_from_json("data/operations.json")
        assert result == []


def test_invalid_json_returns_empty_list()->None:
    """Если файл содержит некорректный JSON — возвращается пустой список."""
    with patch("os.path.exists", return_value=True), patch("builtins.open", mock_open(read_data="{invalid_json}")):
        result = load_transactions_from_json("data/operations.json")
        assert result == []


def test_json_with_not_a_list_returns_empty_list()->None:
    """Если JSON содержит не список — возвращается пустой список."""
    with patch("os.path.exists", return_value=True), patch("builtins.open", mock_open(read_data='{"key": "value"}')):
        result = load_transactions_from_json("data/operations.json")
        assert result == []


def test_valid_list_json_returns_list()->None:
    """Если JSON содержит список — он возвращается как есть."""
    mock_data = [
        {"id": 1, "amount": 100, "description": "Пополнение"},
        {"id": 2, "amount": -50, "description": "Покупка"},
    ]
    with (
        patch("os.path.exists", return_value=True),
        patch("builtins.open", mock_open(read_data=json.dumps(mock_data))),
    ):
        result = load_transactions_from_json("data/operations.json")
        assert result == mock_data


def test_nested_data_preserved()->None:
    """Проверка, что вложенные структуры данных не изменяются."""
    mock_data = [
        {"id": 1, "amount": 200, "category": "food", "tags": ["groceries", "supermarket"], "meta": {"source": "card"}}
    ]
    with (
        patch("os.path.exists", return_value=True),
        patch("builtins.open", mock_open(read_data=json.dumps(mock_data))),
    ):
        result = load_transactions_from_json("data/operations.json")
        assert result == mock_data
