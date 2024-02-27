from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

US_CENSUS_GEOCODING_SERVICES_API_URL = "https://geocoding.geo.census.gov/geocoder"

def get_latitude_longitude(address):
    try:
        base_url = US_CENSUS_GEOCODING_SERVICES_API_URL
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
    except HTTPException as e:
        raise e
    return (latitude, longitude)

@app.get("/geolocate/{address}")
async def get_geolocation(address: str):
    """Endpoint to get GeoLocation for a given US address."""
    try:
        latitude, longitude = get_latitude_longitude(address)
        return (latitude, longitude)
    except HTTPException as e:
        raise e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
