from typing import List, Dict, Any, Callable
import pytest
from unittest.mock import patch, Mock
import sys
import os
import main

# Добавляем корень проекта в sys.path для импорта main
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# === Типы ===

Operation = Dict[str, Any]
InputMockSideEffect = List[str]
LoadDataMock = Callable[[str], List[Operation]]
MaskAccountMock = Callable[[str], str]
MaskCardMock = Callable[[str], str]


# === Тесты ===


@patch("builtins.input", side_effect=["1", "EXECUTED", "нет", "нет", "нет"])
@patch("main.load_data_from_json")
def test_main_json_executed_no_sort_no_rub_no_search(
    mock_load: Mock, mock_input: Mock, capsys: pytest.CaptureFixture[str]
) -> None:
    """Тест: JSON, фильтр по EXECUTED, без сортировки, без RUB-фильтра, без поиска."""
    mock_load.return_value = [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2019-12-08T22:46:21.935582",
            "description": "Открытие вклада",
            "to": "Счет 96527012349577388652",
            "operationAmount": {"amount": "40542", "currency": {"code": "RUB"}},
        }
    ]

    with (
        patch("main.get_mask_account", return_value="Счет **8652") as mock_mask_acc,
        patch("main.get_mask_card_number", return_value="7000 79** **** 6391") as mock_mask_card,
    ):
        main.main()

    captured: str = capsys.readouterr().out

    assert "Привет Добро пожаловать" in captured
    assert "Операции отфильтрованы по статусу" in captured
    assert "Всего банковских операций в выборке: 1" in captured
    assert "08.12.2019 Открытие вклада" in captured
    assert "Счет **8652" in captured
    assert "Сумма: 40542 RUB" in captured

    assert mock_mask_acc.call_count == 1
    assert mock_mask_card.call_count == 0  # "from" отсутствует


@patch("builtins.input", side_effect=["2", "executed", "да", "по убыванию", "да", "нет"])
@patch("main.load_data_from_csv")
def test_main_csv_case_insensitive_status_sort_desc_rub_only(
    mock_load: Mock, mock_input: Mock, capsys: pytest.CaptureFixture[str]
) -> None:
    """Тест: CSV, статус 'executed' (регистронезависимо), сортировка по убыванию, только рубли."""
    mock_load.return_value = [
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2018-07-18T12:12:12.123456",
            "description": "Перевод организации",
            "from": "Visa Platinum 7492658539607088",
            "to": "Счет 78829265035770381826",
            "operationAmount": {"amount": "8390", "currency": {"code": "RUB"}},
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2019-04-04T12:57:02.123456",
            "description": "Перевод со счета на счет",
            "from": "Счет 12345678901234567890",
            "to": "Счет 09876543210987654321",
            "amount": "8200",
            "currency_code": "EUR",
        },
    ]

    with (
        patch("main.get_mask_account", side_effect=["Счет **1826", "Счет **4321"]) as mock_mask_acc,
        patch("main.get_mask_card_number", return_value="7492 65** **** 7088") as mock_mask_card,
    ):
        main.main()

    captured: str = capsys.readouterr().out

    assert "Всего банковских операций в выборке: 1" in captured  # Только RUB
    assert "18.07.2018" in captured
    assert "04.04.2019" not in captured  # Не RUB
    assert "Сумма: 8390 RUB" in captured

    assert mock_mask_acc.call_count == 1
    assert mock_mask_card.call_count == 1


@patch("builtins.input", side_effect=["3", "PENDING", "да", "по возрастанию", "нет", "да", "перевод"])
@patch("main.load_data_from_xlsx")
def test_main_xlsx_pending_sort_asc_search_keyword(
    mock_load: Mock, mock_input: Mock, capsys: pytest.CaptureFixture[str]
) -> None:
    """Тест: XLSX, статус PENDING, сортировка по возрастанию, поиск по слову 'перевод'."""
    mock_load.return_value = [
        {
            "id": 4,
            "state": "PENDING",
            "date": "2020-01-01T00:00:00.000000",
            "description": "Перевод другу",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560",
            "operationAmount": {"amount": "1000", "currency": {"code": "USD"}},
        },
        {
            "id": 5,
            "state": "PENDING",
            "date": "2019-01-01T00:00:00.000000",
            "description": "Оплата телефона",
            "to": "Тинькофф 1234567890123456",
            "operationAmount": {"amount": "500", "currency": {"code": "RUB"}},
        },
        {
            "id": 6,
            "state": "PENDING",
            "date": "2019-06-06T06:06:06.000000",
            "description": "Перевод на карту",
            "from": "Счет 11112222333344445555",
            "to": "Visa Gold 5999414228426353",
            "operationAmount": {"amount": "2000", "currency": {"code": "EUR"}},
        },
    ]

    with (
        patch("main.get_mask_account", side_effect=["Счет **5560", "Счет **5555"]) as mock_mask_acc,
        patch(
            "main.get_mask_card_number", side_effect=["7158 30** **** 6758", "5999 41** **** 6353"]
        ) as mock_mask_card,
    ):
        main.main()

    captured: str = capsys.readouterr().out

    assert "Всего банковских операций в выборке: 2" in captured  # Только с "перевод"
    assert "01.01.2020" in captured
    assert "06.06.2019" in captured
    assert "01.01.2019" not in captured  # Нет "перевод" в описании

    # Проверка порядка: 06.06.2019 → 01.01.2020 (по возрастанию)
    pos_2019: int = captured.find("06.06.2019")
    pos_2020: int = captured.find("01.01.2020")
    assert pos_2019 != -1 and pos_2020 != -1
    assert pos_2019 < pos_2020

    assert mock_mask_acc.call_count == 2
    assert mock_mask_card.call_count == 2


@patch("builtins.input", side_effect=["4", "1"])
@patch("main.load_data_from_json")
def test_main_invalid_choice_then_correct(
    mock_load: Mock, mock_input: Mock, capsys: pytest.CaptureFixture[str]
) -> None:
    """Тест: некорректный выбор формата, затем корректный."""
    mock_load.return_value = []

    with patch("main.get_mask_account", return_value="Счет **0000"):
        main.main()

    captured: str = capsys.readouterr().out
    assert "Введите 1, 2 или 3." in captured
    assert "Для обработки выбран JSON-файл." in captured
