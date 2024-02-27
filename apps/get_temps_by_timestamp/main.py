from fastapi import FastAPI, HTTPException
import requests
import json
from collections import defaultdict
from datetime import datetime

app = FastAPI()

NWS_API_BASE_URL = "https://api.weather.gov/"

def temps_by_timestamp(station_id):
    try:
        stations_url = NWS_API_BASE_URL + 'stations/' + str(station_id) + '/observations'
        response = requests.get(stations_url, timeout=5)
        stations_features = response.json()['features']
    except HTTPException as e:
        raise e
    temperatures_by_timestamp = {}
    for feature in stations_features:
        timestamp_string = feature['properties'].get('timestamp')
        temperature = feature['properties']['temperature'].get('value')
        # Added conditional due to "null" values in temperature data from NWS API
        if temperature is not None:
            temperatures_by_timestamp[timestamp_string] = temperature
    return (temperatures_by_timestamp)

@app.get("/tempsbytimestamp/{station_id}")
async def get_temps_by_timestamp(station_id: str):
    """Endpoint to get temperatures by timestamp for a given observation station ID."""
    try:
        temperatures_by_timestamp = temps_by_timestamp(station_id)
        return (temperatures_by_timestamp)
    except HTTPException as e:
        raise e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
