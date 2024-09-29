import pytest
from unittest.mock import call, patch, MagicMock, mock_open
from app.services.fuel_service import FuelDataService

# Mocking external dependencies
@pytest.fixture
def mock_fuel_service():
    with patch("app.services.fuel_service.DatabaseContext") as MockDBContext, \
         patch("app.services.fuel_service.FuelRepository") as MockFuelRepo, \
         patch("app.services.fuel_service.requests.get") as MockRequestsGet:
        
        # Setup Mock Database and Repo
        mock_db = MockDBContext.return_value
        mock_repo = MockFuelRepo.return_value
        
        # Create an instance of the service
        service = FuelDataService()
        yield service, mock_db, mock_repo, MockRequestsGet

# Test when debug=True (mock file read operation)
@patch("builtins.open", new_callable=mock_open, read_data="<html>Sample HTML file content</html>")
@patch("app.services.fuel_service.debug", True)  # Mock the debug flag
def test_fetch_data_debug_true(mock_file, mock_fuel_service):
    service, _, _, _ = mock_fuel_service  # Get the service instance from the fixture

    # Call the fetch_data method
    result = service.fetch_data()

    # Check that the file open method was called with the correct path
    mock_file.assert_called_once_with('./raw/gasprice.html', 'r', encoding='utf-8')

    # Validate the content returned from the method
    assert result == "<html>Sample HTML file content</html>"

# Test when debug=False (mock network request)
@patch("app.services.fuel_service.debug", False)  # Mock the debug flag
def test_fetch_data_debug_false(mock_fuel_service):
    service, _, _, mock_requests_get = mock_fuel_service  # Get the service and mocks from the fixture

    # Mock a successful network response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"<html>Sample HTML content from URL</html>"
    mock_requests_get.return_value = mock_response

    # Call the fetch_data method
    result = service.fetch_data()

    # Ensure requests.get was called with the correct URL
    mock_requests_get.assert_called_once_with(service.url)

    # Validate the content returned from the method
    assert result == b"<html>Sample HTML content from URL</html>"

# Test the fetch_data method
def test_fetch_data_success(mock_fuel_service):
    # Checking for common HTML elements
    def is_html(s):
        common_html_elements = ['<html>', '<body>', '<head>', '</html>', '</body>', '</head>']
        for element in common_html_elements:
            if element in s:
                return True
        return False
    service, _, _, mock_requests_get = mock_fuel_service

    # Mock a successful response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"<html>Sample HTML content</html>"
    mock_requests_get.return_value = mock_response

    result = service.fetch_data()

    assert is_html(result)

# Test when debug=False with a failure in the network request
@patch("app.services.fuel_service.debug", False)  # Mock the debug flag
def test_fetch_data_debug_false_failure(mock_fuel_service):
    service, _, _, mock_requests_get = mock_fuel_service  # Get the service and mocks from the fixture

    # Mock a failed network response
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_requests_get.return_value = mock_response

    # Expect an exception to be raised due to the failed request
    with pytest.raises(Exception, match="Failed to load page"):
        service.fetch_data()

    # Ensure requests.get was called
    mock_requests_get.assert_called_once_with(service.url)

# Test the parse_fuel_data method
def test_parse_fuel_data(mock_fuel_service):
    service, _, _, _ = mock_fuel_service

    # Sample HTML snippet to parse
    html_content = '''
    <article class="gasprice ptt">
        <ul>
            <li><span>Diesel</span><em>30.25</em></li>
            <li><span>Gasoline</span><em>33.50</em></li>
        </ul>
    </article>
    '''
    
    # Call the method
    result = service.parse_fuel_data(html_content, "gasprice ptt", "ptt")

    # Expected result
    expected_result = [
        {"provider": "ptt", "type": "Diesel", "price": 30.25},
        {"provider": "ptt", "type": "Gasoline", "price": 33.50}
    ]
    
    assert result == expected_result

# Test saving fuel data
def test_save_fuel_data(mock_fuel_service):
    service, _, mock_repo, _ = mock_fuel_service

    # Sample data to save
    fuel_data = [
        {"provider": "ptt", "type": "Diesel", "price": 30.25},
        {"provider": "ptt", "type": "Gasoline", "price": 33.50}
    ]

    # Call the method
    service.save_fuel_data(fuel_data, "ptt")

    # Ensure the repo's insert_fuel_data was called with the correct arguments
    mock_repo.insert_fuel_data.assert_called_once_with(fuel_data, "ptt")

# Test the run method (end-to-end test with mocked dependencies)
@patch("app.services.fuel_service.debug", False)  # Ensure debug=False
def test_run(mock_fuel_service, mocker):
    service, mock_db, mock_repo, mock_requests_get = mock_fuel_service

    # Mock fetch_data
    html_content = b'''
    <article class="gasprice ptt">
        <ul>
            <li><span>Diesel</span><em>30.25</em></li>
            <li><span>Gasoline</span><em>33.50</em></li>
        </ul>
    </article>
    '''
    mocker.patch.object(service, 'fetch_data', return_value=html_content)

    # Mock parse_fuel_data
    fuel_data = [
        {"provider": "ptt", "type": "Diesel", "price": 30.25},
        {"provider": "ptt", "type": "Gasoline", "price": 33.50}
    ]
    mocker.patch.object(service, 'parse_fuel_data', return_value=fuel_data)

    # Call the run method
    result = service.run()

    # Verify the database connection was established
    mock_db.connect.assert_called_once()

    # Verify that the fuel table creation method was called
    mock_repo.create_fuel_table.assert_called_once()

    # Verify that the insert method was called with the expected parsed data
    expected_calls = [
        call(fuel_data, "ptt"),
        call(fuel_data, "bcp"),
        call(fuel_data, "shell"),
        call(fuel_data, "esso"),
        call(fuel_data, "caltex"),
        call(fuel_data, "pt"),
        call(fuel_data, "susco"),
    ]
    mock_repo.insert_fuel_data.assert_has_calls(expected_calls)

    # Check that the final result matches the expected data
    assert len(result) == 14