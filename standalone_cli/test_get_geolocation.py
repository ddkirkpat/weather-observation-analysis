import pytest
import requests
from archive.high_low_temps_by_address import get_geolocation

# Given a valid US address, it should return the latitude and longitude of the address
def test_valid_address(mocker):
    # Mock the requests.get() function to return a predefined response
    mocker.patch('requests.get')
    requests.get.return_value.json.return_value = {
        'result': {
            'addressMatches': [
                {
                    'coordinates': {
                        'y': 39.7392,
                        'x': -104.9903
                    }
                }
            ]
        }
    }
    # Call the code under test
    result = get_geolocation('1701 Wynkoop St. Denver, CO')
    # Assert the result is the expected latitude and longitude
    assert result == (39.7392, -104.9903)
    # Assert that requests.get() was called with the correct URL and parameters
    requests.get.assert_called_once_with('https://geocoding.geo.census.gov/geocoder/locations/onelineaddress', {
        'address': '1701 Wynkoop St. Denver, CO',
        'benchmark': 'Public_AR_Current',
        'format': 'json'
    })

# Given an invalid US address, it should raise an exception
def test_invalid_address(mocker):
    # Mock the requests.get() function to return a predefined response with no address matches
    mocker.patch('requests.get')
    requests.get.return_value.json.return_value = {
        'result': {
            'addressMatches': []
        }
    }   
    # Call the code under test
    with pytest.raises(Exception):
        get_geolocation('Invalid Address')
    
    # Assert that requests.get() was called with the correct URL and parameters
    requests.get.assert_called_once_with('https://geocoding.geo.census.gov/geocoder/locations/onelineaddress', {
        'address': 'Invalid Address',
        'benchmark': 'Public_AR_Current',
        'format': 'json'
    })
