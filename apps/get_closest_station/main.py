from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

NWS_API_BASE_URL = "https://api.weather.gov/"

def get_closest_station(latitude, longitude):
    try:
        points_url = NWS_API_BASE_URL + '/points/' + str(latitude) + ',' + str(longitude)
        response = requests.get(points_url, timeout=5)
        points_properties = response.json()['properties']
        grid_id = points_properties.get('gridId')
        grid_x = points_properties.get('gridX')
        grid_y = points_properties.get('gridY')
    except HTTPException as e:
        raise e
    try:
        gridpoints_url = NWS_API_BASE_URL + 'gridpoints/' + str(grid_id) + '/' + str(grid_x) + ',' + str(grid_y) + '/stations'
        response = requests.get(gridpoints_url, timeout=5)
        gridpoints_features = response.json()['features']
        station_id = gridpoints_features[0]['properties'].get('stationIdentifier')
    except HTTPException as e:
        raise e
    return (station_id)

@app.get("/closest-station/{latitude},{longitude}")
async def get_station(latitude: float, longitude: float):
    """Endpoint to get weather data for a given location."""
    try:
        closest_station = get_closest_station(latitude, longitude)
        return closest_station
    except HTTPException as e:
        raise e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
