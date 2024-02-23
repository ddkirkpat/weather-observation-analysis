import pytest
import requests
from high_low_temps_by_address import get_closest_station

# Should return the correct station ID when given valid latitude and longitude
def test_valid_latitude_longitude():
    latitude = 39.7392
    longitude = -104.9903
    expected_station_id = 'KBJC'
    result = get_closest_station(latitude, longitude)
    assert result == expected_station_id

# Should return None when given invalid latitude and longitude
def test_invalid_latitude_longitude():
    latitude = 100
    longitude = -200
    result = get_closest_station(latitude, longitude)
    assert result == None
