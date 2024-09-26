from bs4 import BeautifulSoup
import requests
from app.errors.handlers import DatabaseException
from db.db_context import DatabaseContext
from db.fuel_repo import FuelRepository
from my_env import debug, fuel_data_scraper_url


class FuelDataService:
    def __init__(self):
        self.url = fuel_data_scraper_url
        self.db_manager = DatabaseContext()  # Initialize DatabaseContext
        self.fuel_repo = FuelRepository(
            self.db_manager)  # Fuel-specific DB manager

    def fetch_data(self):
        """Fetch HTML content from the URL"""

        if debug:
            print('Using ./raw/gasprice.html as a sample html file...')
            with open('./raw/gasprice.html', 'r', encoding='utf-8') as file:
                html_content = file.read()
            return html_content
        response = requests.get(self.url)
        if response.status_code != 200:
            raise Exception(f"Failed to load page {self.url}")
        return response.content

    def parse_fuel_data(self, html_content: str, class_name: str, provider: str):
        """Parse HTML content to extract fuel prices"""
        soup = BeautifulSoup(html_content, 'html.parser')
        article = soup.find('article', class_=class_name)

        # Extract the fuel types and prices
        fuel_data = []
        for li in article.find_all('li'):
            fuel_type = li.find('span').text.strip()
            fuel_price = float(li.find('em').text.strip()
                               )  # Convert price to float
            fuel_data.append({
                'provider': provider,
                'type': fuel_type,
                'price': fuel_price
            })

        return fuel_data

    def save_fuel_data(self, fuel_data: list, provider: str):
        """Save parsed fuel data into the database"""
        self.fuel_repo.insert_fuel_data(
            fuel_data, provider)  # Use fuel-specific DB manager

    def run(self):
        """Scrape data from all fuel providers"""
        self.db_manager.connect()  # Connect to the database
        self.fuel_repo.create_fuel_table()  # Create fuel table
        html_content = self.fetch_data()

        # Provider-class map
        class_map = {
            "ptt": "gasprice ptt",
            "bcp": "gasprice bcp",
            "shell": "gasprice shell",
            "esso": "gasprice esso",
            "caltex": "gasprice caltex",
            "pt": "gasprice pt",
            "susco": "gasprice susco"
        }

        all_fuel_data = []

        # Scrape all providers
        for provider, class_name in class_map.items():
            fuel_data = self.parse_fuel_data(
                html_content, class_name, provider)
            self.save_fuel_data(fuel_data, provider)
            all_fuel_data.extend(fuel_data)

        return all_fuel_data