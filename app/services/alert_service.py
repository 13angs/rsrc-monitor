# app/services/fuel_alert_service.py

from collections import defaultdict
from telegram import Bot
from my_env import telegram_bot_config
from db.fuel_repo import FuelRepository
from db.db_context import DatabaseContext

class AlertService:
    def __init__(self):
        self.db_context = DatabaseContext()
        self.fuel_repo = FuelRepository(self.db_context)
        self.telegram_token = telegram_bot_config['token']
        self.chat_id = telegram_bot_config['chat_id']

    def get_fuel_prices(self):
        """Query fuel prices from the database."""
        self.db_context.connect()
        try:
            return self.fuel_repo.get_fuel_prices()
        except Exception as e:
            print(f"Error querying the database: {e}")
            return None

    def format_fuel_prices(self, prices):
        """Format the fuel prices by grouping them by type."""
        if not prices:
            return "No fuel prices available for today."

        grouped_data = defaultdict(list)
        for provider, fuel_type, price in prices:
            grouped_data[fuel_type].append((provider, price))

        # Create a formatted message
        message = "🚗 Fuel Prices for Today:\n\n"
        for fuel_type, entries in grouped_data.items():
            message += f"🔹 {fuel_type}:\n"
            for provider, price in entries:
                message += f"  - {provider}: {price:.2f} THB\n"
            message += "\n"

        return message

    async def send_to_telegram(self, message):
        """Send the formatted message to Telegram."""
        bot = Bot(token=self.telegram_token)
        await bot.send_message(chat_id=self.chat_id, text=message)

    async def send_fuel_price_alert(self):
        """Main function to send the fuel price alert to Telegram."""
        prices = self.get_fuel_prices()
        formatted_message = self.format_fuel_prices(prices)
        await self.send_to_telegram(formatted_message)
