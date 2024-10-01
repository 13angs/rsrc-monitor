# test_alert_service.py
import asyncio
import pytest
from unittest.mock import MagicMock, patch
from app.services.alert_service import AlertService

# Mocking external dependencies
@pytest.fixture
def mock_alert_service():
    with patch("app.services.alert_service.DatabaseContext") as MockDBContext, \
         patch("app.services.alert_service.FuelRepository") as MockFuelRepo, \
         patch("app.services.alert_service.Bot") as MockBot:
        
        # Setup Mock Database and Repo
        mock_db = MockDBContext.return_value
        mock_repo = MockFuelRepo.return_value
        mock_bot = MockBot.return_value
        
        # Create an instance of the service
        service = AlertService()
        yield service, mock_db, mock_repo, mock_bot

# Test getting fuel prices
def test_get_fuel_prices(mock_alert_service):
    service, _, mock_repo, _ = mock_alert_service

    # Mock fuel prices
    mock_prices = [
        ("Provider1", "FuelType1", 10.99),
        ("Provider2", "FuelType2", 11.99),
    ]
    mock_repo.get_fuel_prices.return_value = mock_prices

    # Call the method
    result = service.get_fuel_prices()

    # Verify the result
    assert result == mock_prices

# Test formatting fuel prices
def test_format_fuel_prices(mock_alert_service):
    service, _, _, _ = mock_alert_service

    # Mock fuel prices
    mock_prices = [
        ("Provider1", "FuelType1", 10.99),
        ("Provider2", "FuelType2", 11.99),
    ]

    # Call the method
    result = service.format_fuel_prices(mock_prices)

    # Verify the result
    expected_result = "🚗 Fuel Prices for Today:\n\n🔹 FuelType1:\n  - Provider1: 10.99 THB\n\n🔹 FuelType2:\n  - Provider2: 11.99 THB\n\n"
    assert result == expected_result

# Test sending a message to Telegram
@patch("app.services.alert_service.telegram_bot_config", {"token": "mock_token", "chat_id": "mock_chat_id"})
async def test_send_to_telegram(mock_alert_service):
    service, _, _, mock_bot = mock_alert_service

    # Mock message
    mock_message = "Hello, world!"

    # Call the method
    await service.send_to_telegram(mock_message)

    # Verify the bot was called
    mock_bot.return_value.send_message.assert_called_once_with(chat_id="mock_chat_id", text=mock_message)

# Test sending a fuel price alert
async def test_send_fuel_price_alert(mock_alert_service):
    service, _, mock_repo, mock_bot = mock_alert_service

    # Mock fuel prices
    mock_prices = [
        ("Provider1", "FuelType1", 10.99),
        ("Provider2", "FuelType2", 11.99),
    ]
    mock_repo.get_fuel_prices.return_value = mock_prices

    # Call the method
    await service.send_fuel_price_alert()

    # Verify the bot was called
    expected_message = "🚗 Fuel Prices for Today:\n\n🔹 FuelType1:\n  - Provider1: 10.99 THB\n\n🔹 FuelType2:\n  - Provider2: 11.99 THB\n"
    mock_bot.send_message.assert_called_once_with(chat_id="mock_chat_id", text=expected_message)