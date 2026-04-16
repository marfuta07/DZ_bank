from unittest.mock import patch, Mock

from src.external_api import convert_currency_to_rub, get_exchange_rate

"""Тесты для функции get_exchange_rate."""


@patch("src.external_api.requests.get")
def test_get_exchange_rate_success(mock_get: Mock) -> None:
    """Проверка успешного получения курса валюты."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"rates": {"RUB": 75.0}}

    rate = get_exchange_rate("USD", "RUB")

    assert rate == 75.0
    mock_get.assert_called_once()


@patch("src.external_api.requests.get")
def test_get_exchange_rate_invalid_response(mock_get: Mock) -> None:
    """Проверка при некорректном ответе от API (нет ключа 'rates')."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {}

    rate = get_exchange_rate("USD", "RUB")

    assert rate is None


@patch("src.external_api.requests.get")
def test_get_exchange_rate_non_200_status(mock_get: Mock) -> None:
    """Проверка при статусе ответа, отличном от 200."""
    mock_get.return_value.status_code = 401

    rate = get_exchange_rate("USD", "RUB")

    assert rate is None


# --- Тесты для convert_currency_to_rub ---
@patch("src.external_api.get_exchange_rate")
def test_rub_to_rub_no_conversion_needed(mock_get_rate: Mock) -> None:
    """Конвертация из RUB в RUB — курс не запрашивается."""
    transaction = {"amount": 1000, "currency": "RUB"}

    result = convert_currency_to_rub(transaction)

    assert result == 1000.0
    mock_get_rate.assert_not_called()


@patch("src.external_api.get_exchange_rate")
def test_usd_to_rub_conversion_success(mock_get_rate: Mock) -> None:
    """Конвертация из USD в RUB с успешным получением курса."""
    mock_get_rate.return_value = 75.5
    transaction = {"amount": 10, "currency": "USD"}

    result = convert_currency_to_rub(transaction)

    assert result == 755.0  # 10 * 75.5
    mock_get_rate.assert_called_with("USD", "RUB")


@patch("src.external_api.get_exchange_rate")
def test_eur_to_rub_conversion_success(mock_get_rate: Mock) -> None:
    """Конвертация из EUR в RUB."""
    mock_get_rate.return_value = 82.3
    transaction = {"amount": 5, "currency": "EUR"}

    result = convert_currency_to_rub(transaction)

    assert result == 411.5  # 5 * 82.3


@patch("src.external_api.get_exchange_rate")
def test_conversion_fails_returns_zero(mock_get_rate: Mock) -> None:
    """Если курс не удалось получить — возвращается 0.0."""
    mock_get_rate.return_value = None
    transaction = {"amount": 100, "currency": "USD"}

    result = convert_currency_to_rub(transaction)

    assert result == 0.0


def test_invalid_amount_type() -> None:
    """Если amount не число — возвращается 0.0."""
    transaction = {"amount": "invalid", "currency": "USD"}

    result = convert_currency_to_rub(transaction)

    assert result == 0.0


def test_missing_amount_key() -> None:
    """Если в транзакции нет amount — возвращается 0.0."""
    transaction = {"currency": "USD"}

    result = convert_currency_to_rub(transaction)

    assert result == 0.0


def test_missing_currency_key() -> None:
    """Если нет currency — по умолчанию RUB."""
    transaction = {"amount": 500}

    result = convert_currency_to_rub(transaction)

    assert result == 500.0


def test_unsupported_currency_returns_zero() -> None:
    """Валюта не поддерживается — возвращается 0.0."""

    transaction = {"amount": 100, "currency": "JPY"}
    if transaction is None:
        return 0.0
    result = convert_currency_to_rub(transaction)

    assert result == 0.0
