from unittest.mock import patch, mock_open,Mock


from src.read_file import read_from_csv, read_from_excel

# === ТЕСТЫ ДЛЯ CSV ===


@patch("builtins.open", new_callable=mock_open, read_data="id;amount;comment\n1;100;Оплата\n2;;\n")
def test_read_from_csv_success(mock_file: Mock)->None:
    """Тест успешного чтения CSV с пустым значением."""
    result = read_from_csv("dummy.csv")

    # Проверки
    mock_file.assert_called_once_with("dummy.csv", mode="r", encoding="utf-8")
    assert len(result) == 2, "Должно быть 2 строки"
    assert result[0] == {"id": "1", "amount": "100", "comment": "Оплата"}
    assert result[1] == {"id": "2", "amount": "", "comment": ""}, "Пустые значения должны стать ''"


@patch("builtins.open", side_effect=FileNotFoundError)
def test_read_from_csv_file_not_found(mock_file: Mock)->None:
    """Тест обработки отсутствующего файла CSV."""
    result = read_from_csv("not_exists.csv")

    # Проверки
    assert mock_file.called
    assert result == [], "При ошибке должен возвращаться пустой список"


@patch("builtins.open", side_effect=Exception("Ошибка чтения"))
def test_read_from_csv_unexpected_error(mock_file: Mock)->None:
    """Тест обработки неожиданной ошибки при чтении CSV."""
    result = read_from_csv("broken.csv")

    # Проверки
    assert result == [], "При исключении должен возвращаться пустой список"


# === ТЕСТЫ ДЛЯ EXCEL ===
@patch("pandas.read_excel", side_effect=FileNotFoundError)
def test_read_from_excel_file_not_found(mock_read_excel: Mock)->None:
    """Тест обработки отсутствующего Excel-файла."""
    result = read_from_excel("not_exists.xlsx")

    # Проверки
    assert result == [], "При FileNotFoundError должен возвращаться пустой список"


@patch("pandas.read_excel", side_effect=Exception("Ошибка парсинга"))
def test_read_from_excel_unexpected_error(mock_read_excel: Mock)->None:
    """Тест обработки неожиданной ошибки при чтении Excel."""
    result = read_from_excel("corrupted.xlsx")

    # Проверки
    assert result == [], "При исключении должен возвращаться пустой список"
