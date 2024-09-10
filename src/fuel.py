import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime
import time

class FuelDataScraper:
    def __init__(self, url: str, output_filename: str = None):
        self.url = url
        self.output_filename = output_filename
    
    def fetch_data(self):
        """Fetch HTML content from the URL"""
        response = requests.get(self.url)
        if response.status_code != 200:
            raise Exception(f"Failed to load page {self.url}")
        return response.content
    
    def parse_fuel_data(self, html_content: str, class_name: str):
        """Parse HTML content to extract fuel prices"""
        soup = BeautifulSoup(html_content, 'html.parser')
        article = soup.find('article', class_=class_name)
        
        # Extract the header info (logo alt text and title)
        header_title = article.find('header').find('h3').text.strip()

        # Generate filename if not provided
        # if not self.output_filename:
        self.output_filename = header_title + '.csv'
        
        # Extract the fuel types and prices
        fuel_prices = {}
        for li in article.find_all('li'):
            fuel_type = li.find('span').text.strip()
            fuel_price = li.find('em').text.strip()
            fuel_prices[fuel_type] = fuel_price
        
        return fuel_prices

    def file_has_data(self, filename: str) -> bool:
        """Check if the file exists and contains data"""
        if not os.path.exists(filename):
            return False
        
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            return any(row for row in reader)  # Check if the file has any rows

    def save_to_csv(self, fuel_prices: dict):
        """Save fuel prices to a CSV file"""
        current_date = datetime.now().strftime('%d-%m-%Y')
        file_exists = self.file_has_data(self.output_filename)
        
        # Open the file in append mode if it has data, otherwise write mode
        with open(self.output_filename, mode='a' if file_exists else 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Write the header if the file is empty
            if not file_exists:
                writer.writerow(['วันที่'] + list(fuel_prices.keys()))

            # Write the data row
            writer.writerow([current_date] + list(fuel_prices.values()))

        print(f"Data saved to {self.output_filename}")
    
    def scrape_ptt(self):
        print('Scraping PTT...')
        html_content = self.fetch_data()
        fuel_prices = self.parse_fuel_data(html_content, 'gasprice ptt')
        self.save_to_csv(fuel_prices)
        print('Delay for 2 sec...')
        time.sleep(2)
    
    def scrape_bcp(self):
        print('Scraping BCP...')
        html_content = self.fetch_data()
        fuel_prices = self.parse_fuel_data(html_content, 'gasprice bcp')
        self.save_to_csv(fuel_prices)
        print('Delay for 2 sec...')
        time.sleep(2)
    
    def scrape_bcp(self):
        print('Scraping BCP...')
        html_content = self.fetch_data()
        fuel_prices = self.parse_fuel_data(html_content, 'gasprice shell')
        self.save_to_csv(fuel_prices)
        print('Delay for 2 sec...')
        time.sleep(2)
    
    def scrape_esso(self):
        print('Scraping ESSO...')
        html_content = self.fetch_data()
        fuel_prices = self.parse_fuel_data(html_content, 'gasprice esso')
        self.save_to_csv(fuel_prices)
        print('Delay for 2 sec...')
        time.sleep(2)
    
    def scrape_caltex(self):
        print('Scraping CALTEX...')
        html_content = self.fetch_data()
        fuel_prices = self.parse_fuel_data(html_content, 'gasprice caltex')
        self.save_to_csv(fuel_prices)
        print('Delay for 2 sec...')
        time.sleep(2)
    
    def scrape_pt(self):
        print('Scraping PT...')
        html_content = self.fetch_data()
        fuel_prices = self.parse_fuel_data(html_content, 'gasprice pt')
        self.save_to_csv(fuel_prices)
        print('Delay for 2 sec...')
        time.sleep(2)
    
    def scrape_susco(self):
        print('Scraping SUSCO...')
        html_content = self.fetch_data()
        fuel_prices = self.parse_fuel_data(html_content, 'gasprice susco')
        self.save_to_csv(fuel_prices)
        print('Delay for 2 sec...')
        time.sleep(2)

    def run(self):
        """Main function to fetch, parse, and save data"""
        self.scrape_ptt()
        self.scrape_bcp()
        self.scrape_esso()
        self.scrape_caltex()
        self.scrape_pt()
        self.scrape_susco()
        

if __name__ == "__main__":
    scraper = FuelDataScraper(url='https://gasprice.kapook.com/gasprice.php')
    scraper.run()