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

    def file_has_data(self, filename: str) -> bool:
        """Check if the file exists and contains data"""
        if not os.path.exists(filename):
            return False
        
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            return any(row for row in reader)  # Check if the file has any rows

    def save_to_csv(self, fuel_data: list):
        """Save fuel prices to a CSV file"""
        current_date = datetime.now().strftime('%d-%m-%Y')
        file_exists = self.file_has_data(self.output_filename)
        
        # Open the file in append mode if it has data, otherwise write mode
        with open(self.output_filename, mode='a' if file_exists else 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Write the header if the file is empty
            if not file_exists:
                writer.writerow(['date', 'provider', 'type', 'price'])

            # Write the data rows
            for entry in fuel_data:
                writer.writerow([current_date, entry['provider'], entry['type'], entry['price']])

        print(f"Data saved to {self.output_filename}")
    
    def scrape_ptt(self, html_content):
        print('Scraping PTT...')
        fuel_data = self.parse_fuel_data(html_content, 'gasprice ptt', 'ptt')
        self.save_to_csv(fuel_data)
        print('Delay for 2 sec...')
        time.sleep(2)
    
    def scrape_bcp(self, html_content):
        print('Scraping BCP...')
        fuel_data = self.parse_fuel_data(html_content, 'gasprice bcp', 'bcp')
        self.save_to_csv(fuel_data)
        print('Delay for 2 sec...')
        time.sleep(2)
    
    def scrape_shell(self, html_content):
        print('Scraping Shell...')
        fuel_data = self.parse_fuel_data(html_content, 'gasprice shell', 'shell')
        self.save_to_csv(fuel_data)
        print('Delay for 2 sec...')
        time.sleep(2)
    
    def scrape_esso(self, html_content):
        print('Scraping ESSO...')
        fuel_data = self.parse_fuel_data(html_content, 'gasprice esso', 'esso')
        self.save_to_csv(fuel_data)
        print('Delay for 2 sec...')
        time.sleep(2)
    
    def scrape_caltex(self, html_content):
        print('Scraping CALTEX...')
        fuel_data = self.parse_fuel_data(html_content, 'gasprice caltex', 'caltex')
        self.save_to_csv(fuel_data)
        print('Delay for 2 sec...')
        time.sleep(2)
    
    def scrape_pt(self, html_content):
        print('Scraping PT...')
        fuel_data = self.parse_fuel_data(html_content, 'gasprice pt', 'pt')
        self.save_to_csv(fuel_data)
        print('Delay for 2 sec...')
        time.sleep(2)
    
    def scrape_susco(self, html_content):
        print('Scraping SUSCO...')
        fuel_data = self.parse_fuel_data(html_content, 'gasprice susco', 'susco')
        self.save_to_csv(fuel_data)
        print('Delay for 2 sec...')
        time.sleep(2)

    def run(self):
        """Main function to fetch, parse, and save data"""
        html_content = self.fetch_data()
        self.scrape_ptt(html_content)
        self.scrape_bcp(html_content)
        self.scrape_shell(html_content)
        self.scrape_esso(html_content)
        self.scrape_caltex(html_content)
        self.scrape_pt(html_content)
        self.scrape_susco(html_content)
        

if __name__ == "__main__":
    scraper = FuelDataScraper(url='https://gasprice.kapook.com/gasprice.php', output_filename='fuels.csv')
    scraper.run()