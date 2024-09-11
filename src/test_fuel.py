import pytest
from unittest.mock import patch, mock_open, MagicMock
from fuel import FuelDataScraper
import os
import requests
from datetime import datetime

# Mocking the requests.get to return a custom HTML
@patch('fuel.requests.get')
def test_fetch_data(mock_get):
    scraper = FuelDataScraper(url="http://example.com")
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'<html></html>'
    mock_get.return_value = mock_response
    
    content = scraper.fetch_data()
    assert content == b'<html></html>'
    mock_get.assert_called_once_with("http://example.com")

# Test the parse_fuel_data method
def test_parse_fuel_data():
    html_content = """
    <article class="gasprice ptt">
        <li>
            <span>Diesel</span>
            <em>29.99</em>
        </li>
        <li>
            <span>Petrol</span>
            <em>35.59</em>
        </li>
    </article>
    """
    scraper = FuelDataScraper(url="http://example.com")
    result = scraper.parse_fuel_data(html_content, "gasprice ptt", "ptt")
    
    assert result == [
        {"provider": "ptt", "type": "Diesel", "price": 29.99},
        {"provider": "ptt", "type": "Petrol", "price": 35.59}
    ]

# Mocking the os.path.exists function and testing file_has_data
@patch('fuel.os.path.exists')
@patch('fuel.open', new_callable=mock_open, read_data="date,provider,type,price\n")
def test_file_has_data(mock_open, mock_exists):
    scraper = FuelDataScraper(url="http://example.com")
    
    # Simulate the file existing
    mock_exists.return_value = True
    result = scraper.file_has_data('test.csv')
    
    assert result is True
    mock_open.assert_called_once_with('test.csv', 'r', encoding='utf-8')

# Mocking the open function to test save_to_csv
@patch('fuel.open', new_callable=mock_open)
@patch('fuel.FuelDataScraper.file_has_data')
@patch('fuel.datetime')
def test_save_to_csv(mock_datetime, mock_file_has_data, mock_open):
    scraper = FuelDataScraper(url="http://example.com", output_filename='test.csv')
    
    # Mock the current date
    mock_datetime.now.return_value.strftime.return_value = '01-01-2023'
    
    # Simulate that the file does not already exist
    mock_file_has_data.return_value = False
    
    # Define the fuel data to save
    fuel_data = [
        {"provider": "ptt", "type": "Diesel", "price": 29.99},
        {"provider": "ptt", "type": "Petrol", "price": 35.59}
    ]
    
    # Call save_to_csv
    scraper.save_to_csv(fuel_data)
    
    # Assert that the file was opened in write mode
    mock_open.assert_called_once_with('test.csv', mode='w', newline='', encoding='utf-8')


# Test the run method by mocking all the relevant components
@patch('fuel.FuelDataScraper.fetch_data')
@patch('fuel.FuelDataScraper.scrape_ptt')
@patch('fuel.FuelDataScraper.scrape_bcp')
@patch('fuel.FuelDataScraper.scrape_shell')
@patch('fuel.FuelDataScraper.scrape_esso')
@patch('fuel.FuelDataScraper.scrape_caltex')
@patch('fuel.FuelDataScraper.scrape_pt')
@patch('fuel.FuelDataScraper.scrape_susco')
def test_run(mock_susco, mock_pt, mock_caltex, mock_esso, mock_shell, mock_bcp, mock_ptt, mock_fetch_data):
    scraper = FuelDataScraper(url="http://example.com")
    
    # Mock the HTML content
    mock_fetch_data.return_value = '<html></html>'
    
    # Run the method
    scraper.run()
    
    # Assert that all scrape methods were called
    mock_ptt.assert_called_once_with('<html></html>')
    mock_bcp.assert_called_once_with('<html></html>')
    mock_shell.assert_called_once_with('<html></html>')
    mock_esso.assert_called_once_with('<html></html>')
    mock_caltex.assert_called_once_with('<html></html>')
    mock_pt.assert_called_once_with('<html></html>')
    mock_susco.assert_called_once_with('<html></html>')
