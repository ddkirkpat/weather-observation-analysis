from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json
from collections import defaultdict
from datetime import datetime

app = FastAPI()

NWS_API_BASE_URL = "https://api.weather.gov/"

def get_high_low_temps_by_date(station_id):
    try:
        stations_url = NWS_API_BASE_URL + 'stations/' + str(station_id) + '/observations'
        response = requests.get(stations_url, timeout=5)
        stations_features = response.json()['features']
    except HTTPException as e:
        raise e
    temps_by_timestamp = {}
    for feature in stations_features:
        timestamp_string = feature['properties'].get('timestamp')
        temperature = feature['properties']['temperature'].get('value')
        # Added conditional due to "null" values in temperature data from NWS API
        if temperature is not None:
            temps_by_timestamp[timestamp_string] = temperature
    high_low_temperatures_by_date = defaultdict(lambda: {'high': float('-inf'), 'low': float('inf')})
    for timestamp_string, temperature in temps_by_timestamp.items():
        timestamp = datetime.strptime(timestamp_string, '%Y-%m-%dT%H:%M:%S%z')
        date = timestamp.date()
        if temperature > high_low_temperatures_by_date[date]['high']:
            high_low_temperatures_by_date[date]['high'] = temperature
        if temperature < high_low_temperatures_by_date[date]['low']:
            high_low_temperatures_by_date[date]['low'] = temperature
    high_low_temperatures_by_date_json = high_low_temperatures_by_date.dumps()
    return (high_low_temperatures_by_date_json)

@app.get("/highlowtempsbydate/{station_id}")
async def get_high_low_temps_by_date(station_id: str, high_low_temperatures_by_date: dict):
    """Endpoint to get high and low temperatures by date for a given observation station ID."""
    try:
        high_low_temperatures_by_date = dict(get_high_low_temps_by_date(station_id))
        return (high_low_temperatures_by_date)
    except HTTPException as e:
        raise e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
