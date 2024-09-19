import os
from dotenv import load_dotenv

load_dotenv('.env')

fuel_data_scraper_url = 'https://gasprice.kapook.com/gasprice.php'

db_params = {
    'dbname': os.getenv('DATABASE_NAME'),
    'user': os.getenv('DATABASE_USER'),
    'password': os.getenv('DATABASE_PASSWORD'),
    'host': os.getenv('DATABASE_HOST'),
    'port': os.getenv('DATABASE_PORT')
}

telegram_bot_config = {
    'token': os.getenv('TELEGRAM_BOT_TOKEN'),
    'chat_id': os.getenv('TELEGRAM_BOT_CHAT_ID'),
}