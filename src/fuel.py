import requests
from bs4 import BeautifulSoup
import psycopg2
from datetime import datetime
import time

class FuelDataScraper:
    def __init__(self, url: str, db_params: dict):
        self.url = url
        self.db_params = db_params
        self.conn = None
        self.cursor = None
    
    def connect_db(self):
        """Establish connection to the PostgreSQL database"""
        self.conn = psycopg2.connect(**self.db_params)
        self.cursor = self.conn.cursor()

    def close_db(self):
        """Close the database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def create_table(self):
        """Create table for storing fuel data if it doesn't exist"""
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS fuel_prices (
            id SERIAL PRIMARY KEY,
            date DATE NOT NULL,
            provider VARCHAR(50),
            type VARCHAR(50),
            price NUMERIC(10, 2)
        );
        '''
        self.cursor.execute(create_table_query)
        self.conn.commit()

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

    def save_to_db(self, fuel_data: list):
        """Save fuel prices to PostgreSQL database"""
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        insert_query = '''
        INSERT INTO fuel_prices (date, provider, type, price)
        VALUES (%s, %s, %s, %s)
        '''
        
        # Insert each row into the table
        for entry in fuel_data:
            self.cursor.execute(insert_query, (current_date, entry['provider'], entry['type'], entry['price']))
        
        self.conn.commit()
        print(f"Data saved to PostgreSQL database.")
    
    def scrape_ptt(self, html_content):
        print('Scraping PTT...')
        fuel_data = self.parse_fuel_data(html_content, 'gasprice ptt', 'ptt')
        self.save_to_db(fuel_data)
        print('Delay for 2 sec...')
        time.sleep(2)
    
    def scrape_bcp(self, html_content):
        print('Scraping BCP...')
        fuel_data = self.parse_fuel_data(html_content, 'gasprice bcp', 'bcp')
        self.save_to_db(fuel_data)
        print('Delay for 2 sec...')
        time.sleep(2)
    
    def scrape_shell(self, html_content):
        print('Scraping Shell...')
        fuel_data = self.parse_fuel_data(html_content, 'gasprice shell', 'shell')
        self.save_to_db(fuel_data)
        print('Delay for 2 sec...')
        time.sleep(2)
    
    def scrape_esso(self, html_content):
        print('Scraping ESSO...')
        fuel_data = self.parse_fuel_data(html_content, 'gasprice esso', 'esso')
        self.save_to_db(fuel_data)
        print('Delay for 2 sec...')
        time.sleep(2)
    
    def scrape_caltex(self, html_content):
        print('Scraping CALTEX...')
        fuel_data = self.parse_fuel_data(html_content, 'gasprice caltex', 'caltex')
        self.save_to_db(fuel_data)
        print('Delay for 2 sec...')
        time.sleep(2)
    
    def scrape_pt(self, html_content):
        print('Scraping PT...')
        fuel_data = self.parse_fuel_data(html_content, 'gasprice pt', 'pt')
        self.save_to_db(fuel_data)
        print('Delay for 2 sec...')
        time.sleep(2)
    
    def scrape_susco(self, html_content):
        print('Scraping SUSCO...')
        fuel_data = self.parse_fuel_data(html_content, 'gasprice susco', 'susco')
        self.save_to_db(fuel_data)
        print('Delay for 2 sec...')
        time.sleep(2)

    def run(self):
        """Main function to fetch, parse, and save data"""
        try:
            self.connect_db()
            self.create_table()
            html_content = self.fetch_data()
            self.scrape_ptt(html_content)
            self.scrape_bcp(html_content)
            self.scrape_shell(html_content)
            self.scrape_esso(html_content)
            self.scrape_caltex(html_content)
            self.scrape_pt(html_content)
            self.scrape_susco(html_content)
        finally:
            self.close_db()

if __name__ == "__main__":
    db_params = {
        'dbname': 'rsrc_db',
        'user': 'myuser',
        'password': 'mypassword',
        'host': 'localhost',
        'port': '5432'
    }
    scraper = FuelDataScraper(url='https://gasprice.kapook.com/gasprice.php', db_params=db_params)
    scraper.run()
