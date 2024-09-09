import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

# Step 1: Fetch the HTML content from the URL
url = 'https://gasprice.kapook.com/gasprice.php'
response = requests.get(url)
if response.status_code != 200:
    raise Exception(f"Failed to load page {url}")

# Send a request to fetch the webpage content
response = requests.get(url)

# Parse the content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the target article with class "gasprice ptt"
article = soup.find('article', class_='gasprice ptt')

# Extract the header info (logo alt text and the title)
logo_alt = article.find('header').find('img')['alt']
header_title = article.find('header').find('h3').text.strip()

# Clean up the title to make it suitable as a filename
filename = header_title + '.csv'

# Get the current date in the format day-month-year
current_date = datetime.now().strftime('%d-%m-%Y')

# Extract the fuel types and prices from the list items and store them in a dictionary
fuel_prices = {}
for li in article.find_all('li'):
    fuel_type = li.find('span').text.strip()
    fuel_price = li.find('em').text.strip()
    fuel_prices[fuel_type] = fuel_price

# Check if the file exists and contains data
file_exists = os.path.exists(filename)
file_has_data = False

if file_exists:
    # Check if the file contains data
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        file_has_data = any(row for row in reader)  # Check if the file has any rows

# Open the CSV file in append mode if it has data, otherwise write mode
with open(filename, mode='a' if file_has_data else 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # If the file is empty, write the header (fuel types)
    if not file_has_data:
        writer.writerow(['วันที่'] + list(fuel_prices.keys()))

    # Append the fuel prices as a new row, with the date as the first column
    writer.writerow([current_date] + list(fuel_prices.values()))

print(f"Data saved to {filename}")