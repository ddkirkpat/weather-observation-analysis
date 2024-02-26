
import requests
from requests.exceptions import HTTPError
import json
from collections import defaultdict
from datetime import datetime
from tabulate import tabulate

def get_geolocation(address):
    try:
        base_url = 'https://geocoding.geo.census.gov/geocoder'
        return_type = '/locations'
        search_type = '/onelineaddress'
        url = base_url + return_type + search_type
        params = {
            'address': address,
            'benchmark': 'Public_AR_Current',
            'format': 'json'
        }
        response = requests.get(url, params, timeout=5)
        matches = response.json()['result']['addressMatches']
        if len(matches) != 0:
            latitude = matches[0]['coordinates']['y']
            longitude = matches[0]['coordinates']['x']
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    return (latitude, longitude)

def get_closest_station(latitude, longitude):
    try:
        points_url = 'https://api.weather.gov/points/' + str(latitude) + ',' + str(longitude)
        response = requests.get(points_url, timeout=5)
        points_properties = response.json()['properties']
        grid_id = points_properties.get('gridId')
        grid_x = points_properties.get('gridX')
        grid_y = points_properties.get('gridY')
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    try:
        gridpoints_url = 'https://api.weather.gov/gridpoints/' + str(grid_id) + '/' + str(grid_x) + ',' + str(grid_y) + '/stations'
        response = requests.get(gridpoints_url, timeout=5)
        gridpoints_features = response.json()['features']
        station_id = gridpoints_features[0]['properties'].get('stationIdentifier')
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    return (station_id)
    
def get_high_low_temps_by_day(station_id):
    try:
        stations_url = 'https://api.weather.gov/stations/' + str(station_id) + '/observations'
        response = requests.get(stations_url, timeout=5)
        stations_features = response.json()['features']
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    temps_by_timestamp = {}
    for f in range(len(stations_features)):
        timestamp_string = stations_features[f]['properties'].get('timestamp')
        temperature = stations_features[f]['properties']['temperature'].get('value')
        # Added conditional due to "null" values in temperature data from NWS API
        if temperature != None:
            temps_by_timestamp[timestamp_string] = temperature
    high_low_temperatures_by_date = defaultdict(lambda: {'high': float('-inf'), 'low': float('inf')})
    for timestamp_string, temperature in temps_by_timestamp.items():
        timestamp = datetime.strptime(timestamp_string, '%Y-%m-%dT%H:%M:%S%z')
        date = timestamp.date()
        if temperature > high_low_temperatures_by_date[date]['high']:
            high_low_temperatures_by_date[date]['high'] = temperature
        if temperature < high_low_temperatures_by_date[date]['low']:
            high_low_temperatures_by_date[date]['low'] = temperature
    return high_low_temperatures_by_date

if __name__ == '__main__':
    #address = str(input('Please enter a US address (ex. 1701 Wynkoop St. Denver, CO): ').strip())
    address = str(input('Please enter either a US address, City, or Postal Zipcode (ex. 1701 Wynkoop St. Denver, CO): ').strip())
    latitude, longitude = get_geolocation(address)
    station_id = get_closest_station(latitude, longitude)
    results = get_high_low_temps_by_day(station_id)
    print(tabulate(results.items(), headers=['Date','Temperatures (C)']))
