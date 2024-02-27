import pytest
import requests
from datetime import datetime
from archive.high_low_temps_by_address import get_high_low_temps_by_day

# Should return a dictionary with high and low temperatures for each day
def test_return_high_low_temps(mocker):
    # Mock the response from the API
    mocker.patch('requests.get')
    response_mock = mocker.Mock()
    response_mock.json.return_value = {
        'features': [
            {
                'properties': {
                    'timestamp': '2022-01-01T00:00:00+00:00',
                    'temperature': {'value': 10}
                }
            },
            {
                'properties': {
                    'timestamp': '2022-01-01T06:00:00+00:00',
                    'temperature': {'value': 20}
                }
            },
            {
                'properties': {
                    'timestamp': '2022-01-01T12:00:00+00:00',
                    'temperature': {'value': 5}
                }
            },
            {
                'properties': {
                    'timestamp': '2022-01-02T00:00:00+00:00',
                    'temperature': {'value': 15}
                }
            },
            {
                'properties': {
                    'timestamp': '2022-01-02T06:00:00+00:00',
                    'temperature': {'value': 5}
                }
            },
            {
                'properties': {
                    'timestamp': '2022-01-02T12:00:00+00:00',
                    'temperature': {'value': 10}
                }
            }
        ]
    }
    requests.get.return_value = response_mock
    # Call the function under test
    result = get_high_low_temps_by_day('station_id')
    # Assert the expected high and low temperatures for each day
    expected_result = {
        datetime.strptime('2022-01-01', '%Y-%m-%d').date(): {'high': 20, 'low': 5},
        datetime.strptime('2022-01-02', '%Y-%m-%d').date(): {'high': 15, 'low': 5}
        }
    assert result == expected_result

# Should return an empty dictionary when no temperature readings are available
def test_return_empty_dict_no_readings(mocker):
    # Mock the response from the API
    mocker.patch('requests.get')
    response_mock = mocker.Mock()
    response_mock.json.return_value = {'features': []}
    requests.get.return_value = response_mock
    # Call the function under test
    result = get_high_low_temps_by_day('station_id')
    # Assert that the result is an empty dictionary
    assert result == {}
