from collections import defaultdict
from telegram import Bot
import asyncio
from my_env import db_params, telegram_bot_config
from db.fuel_repo import FuelRepsitory
from db.db_context import DatabaseContext

# Telegram Bot Token and Chat ID (replace these with your own)
TELEGRAM_BOT_TOKEN = telegram_bot_config['token']
TELEGRAM_CHAT_ID = telegram_bot_config['chat_id']

# Query fuel prices for specific types and today's date
def get_fuel_prices():
    db_context = DatabaseContext(db_params)
    fuel_repo = FuelRepsitory(db_context)
    db_context.connect()
    try:

        return fuel_repo.get_fuel_prices()
    except Exception as e:
        print(f"Error querying the database: {e}")
        return None
    finally:
        db_context.close()


# Format the fuel prices by grouping them by type
def format_fuel_prices(prices):
    if not prices:
        return "No fuel prices available for today."

    # Group data by fuel type
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

# Send the message to Telegram (async function)
async def send_to_telegram(message):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

# Main function to execute the alert (async)
async def send_fuel_price_alert():
    prices = get_fuel_prices()
    formatted_message = format_fuel_prices(prices)
    await send_to_telegram(formatted_message)

# Run the async function using asyncio
if __name__ == '__main__':
    asyncio.run(send_fuel_price_alert())