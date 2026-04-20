from unittest.mock import patch, Mock

from src.external_api import convert_currency_to_rub, get_exchange_rate


@patch("src.external_api.requests.get")
def test_get_exchange_rate_success(mock_get: Mock) -> None:
    """Проверка успешного получения сконвертированной суммы."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"success": True, "result": 750.0}

    # Теперь: amount=10, base_currency="USD", target_currency="RUB"
    result = get_exchange_rate(10.0, "USD", "RUB")

    assert result == 750.0
    mock_get.assert_called_once()


@patch("src.external_api.requests.get")
def test_get_exchange_rate_invalid_response(mock_get: Mock) -> None:
    """Проверка при некорректном ответе от API (нет поля 'result')."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"success": False}

    result = get_exchange_rate(10.0, "USD", "RUB")

    assert result is None


@patch("src.external_api.requests.get")
def test_get_exchange_rate_non_200_status(mock_get: Mock) -> None:
    """Проверка при статусе ответа, отличном от 200."""
    mock_get.return_value.status_code = 401

    result = get_exchange_rate(10.0, "USD", "RUB")

    assert result is None


@patch("src.external_api.get_exchange_rate")
def test_rub_to_rub_no_conversion_needed(mock_get_rate: Mock) -> None:
    """Конвертация из RUB в RUB — функция get_exchange_rate не вызывается."""
    transaction = {"operationAmount": {"amount": "1000", "currency": {"code": "RUB"}}}

    result = convert_currency_to_rub(transaction)

    assert result == 1000.0
    mock_get_rate.assert_not_called()


@patch("src.external_api.get_exchange_rate")
def test_usd_to_rub_conversion_success(mock_get_rate: Mock) -> None:
    """Конвертация из USD в RUB с успешным получением суммы."""
    mock_get_rate.return_value = 755.0  # Уже 10 * 75.5
    transaction = {"operationAmount": {"amount": "10", "currency": {"code": "USD"}}}

    result = convert_currency_to_rub(transaction)

    assert result == 755.0
    mock_get_rate.assert_called_once_with(10.0, "USD", "RUB")


@patch("src.external_api.get_exchange_rate")
def test_eur_to_rub_conversion_success(mock_get_rate: Mock) -> None:
    """Конвертация из EUR в RUB."""
    mock_get_rate.return_value = 411.5  # 5 * 82.3
    transaction = {"operationAmount": {"amount": "5", "currency": {"code": "EUR"}}}

    result = convert_currency_to_rub(transaction)

    assert result == 411.5


@patch("src.external_api.get_exchange_rate")
def test_conversion_fails_returns_zero(mock_get_rate: Mock) -> None:
    """Если курс не удалось получить — возвращается 0.0."""
    mock_get_rate.return_value = None
    transaction = {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}}

    result = convert_currency_to_rub(transaction)

    assert result == 0.0


def test_invalid_amount_type() -> None:
    """Если amount не число — возвращается 0.0."""
    transaction = {"operationAmount": {"amount": "invalid", "currency": {"code": "USD"}}}

    result = convert_currency_to_rub(transaction)

    assert result == 0.0


def test_missing_amount_key() -> None:
    """Если в транзакции нет amount — возвращается 0.0."""
    transaction = {"operationAmount": {"currency": {"code": "USD"}}}

    result = convert_currency_to_rub(transaction)

    assert result == 0.0


def test_missing_currency_key() -> None:
    """Если нет currency — возвращается 0.0 (ключ обязателен)."""
    transaction = {"operationAmount": {"amount": "500"}}

    result = convert_currency_to_rub(transaction)

    assert result == 0.0


def test_unsupported_currency_returns_zero() -> None:
    """Валюта не поддерживается — возвращается 0.0."""
    transaction = {"operationAmount": {"amount": "100", "currency": {"code": "JPY"}}}

    result = convert_currency_to_rub(transaction)

    assert result == 0.0
