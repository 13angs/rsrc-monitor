# fuel_data_scraper.py

from bs4 import BeautifulSoup
import time
from db.db_context import DatabaseContext  # Import the generic DB manager
from db.fuel_repo import FuelRepsitory  # Import the fuel-specific DB manager
from my_env import db_params, fuel_data_scraper_url
import requests

class FuelDataScraper:
    def __init__(self, url: str, db_params: dict):
        self.url = url
        self.db_manager = DatabaseContext(db_params)  # Initialize DatabaseContext
        self.fuel_db_manager = FuelRepsitory(self.db_manager)  # Fuel-specific DB manager

    def fetch_data(self):
        """Fetch HTML content from the URL"""
        # response = requests.get(self.url)
        # if response.status_code != 200:
        #     raise Exception(f"Failed to load page {self.url}")
        # return response.content
        with open('./raw/gasprice.html', 'r', encoding='utf-8') as file:
            html_content = file.read()
        return html_content

    def parse_fuel_data(self, html_content: str, class_name: str, provider: str):
        """Parse HTML content to extract fuel prices"""
        soup = BeautifulSoup(html_content, 'html.parser')
        article = soup.find('article', class_=class_name)
        
        # Extract the fuel types and prices
        fuel_data = []
        for li in article.find_all('li'):
            fuel_type = li.find('span').text.strip()
            fuel_price = float(li.find('em').text.strip())  # Convert price to float
            fuel_data.append({
                'provider': provider,
                'type': fuel_type,
                'price': fuel_price
            })
        
        return fuel_data

    def save_fuel_data(self, fuel_data: list, provider: str):
        """Save parsed fuel data into the database"""
        self.fuel_db_manager.insert_fuel_data(fuel_data, provider)  # Use fuel-specific DB manager

    def scrape_ptt(self, html_content):
        print('Scraping PTT...')
        fuel_data = self.parse_fuel_data(html_content, 'gasprice ptt', 'ptt')
        self.save_fuel_data(fuel_data, 'ptt')
        print('Delay for 2 sec...')
        time.sleep(2)
    
    def scrape_bcp(self, html_content):
        print('Scraping BCP...')
        fuel_data = self.parse_fuel_data(html_content, 'gasprice bcp', 'bcp')
        self.save_fuel_data(fuel_data, 'bcp')
        print('Delay for 2 sec...')
        time.sleep(2)
    
    def scrape_shell(self, html_content):
        print('Scraping Shell...')
        fuel_data = self.parse_fuel_data(html_content, 'gasprice shell', 'shell')
        self.save_fuel_data(fuel_data, 'shell')
        print('Delay for 2 sec...')
        time.sleep(2)
    
    def scrape_esso(self, html_content):
        print('Scraping ESSO...')
        fuel_data = self.parse_fuel_data(html_content, 'gasprice esso', 'esso')
        self.save_fuel_data(fuel_data, 'esso')
        print('Delay for 2 sec...')
        time.sleep(2)
    
    def scrape_caltex(self, html_content):
        print('Scraping CALTEX...')
        fuel_data = self.parse_fuel_data(html_content, 'gasprice caltex', 'caltex')
        self.save_fuel_data(fuel_data, 'caltex')
        print('Delay for 2 sec...')
        time.sleep(2)
    
    def scrape_pt(self, html_content):
        print('Scraping PT...')
        fuel_data = self.parse_fuel_data(html_content, 'gasprice pt', 'pt')
        self.save_fuel_data(fuel_data, 'pt')
        print('Delay for 2 sec...')
        time.sleep(2)
    
    def scrape_susco(self, html_content):
        print('Scraping SUSCO...')
        fuel_data = self.parse_fuel_data(html_content, 'gasprice susco', 'susco')
        self.save_fuel_data(fuel_data, 'susco')
        print('Delay for 2 sec...')
        time.sleep(2)

    def run(self):
        """Main function to fetch, parse, and save data"""
        try:
            self.db_manager.connect()  # Connect to the database
            self.fuel_db_manager.create_fuel_table()  # Create fuel table
            html_content = self.fetch_data()
            self.scrape_ptt(html_content)
            self.scrape_bcp(html_content)
            self.scrape_shell(html_content)
            self.scrape_esso(html_content)
            self.scrape_caltex(html_content)
            self.scrape_pt(html_content)
            self.scrape_susco(html_content)
        finally:
            self.db_manager.close()  # Close the database connection

if __name__ == "__main__":
    scraper = FuelDataScraper(url=fuel_data_scraper_url, db_params=db_params)
    scraper.run()
