from collections import defaultdict
import psycopg2
from datetime import datetime
from telegram import Bot
import asyncio
from my_env import db_params, telegram_bot_config

# Telegram Bot Token and Chat ID (replace these with your own)
TELEGRAM_BOT_TOKEN = telegram_bot_config['token']
TELEGRAM_CHAT_ID = telegram_bot_config['chat_id']

# Connect to PostgreSQL database
# Connect to PostgreSQL database
def connect_db():
    try:
        conn = psycopg2.connect(**db_params)
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

# Query fuel prices for specific types and today's date
def get_fuel_prices():
    conn = connect_db()
    if not conn:
        return None

    today_date = datetime.now().strftime('%Y-%m-%d')
    query = """
    SELECT provider, type, price
    FROM fuel_prices
    WHERE type IN ('แก๊สโซฮอล์ 95', 'แก๊สโซฮอล์ E20', 'ดีเซล B7')
    AND date = %s
    ORDER BY provider, type;
    """
    
    try:
        cur = conn.cursor()
        cur.execute(query, (today_date,))
        rows = cur.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"Error querying the database: {e}")
        return None

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