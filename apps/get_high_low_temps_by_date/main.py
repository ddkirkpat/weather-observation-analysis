from fastapi import FastAPI, HTTPException

import json
from collections import defaultdict
from datetime import datetime

app = FastAPI()

def parse_high_low_temps_by_date(temperatures_by_timestamp)):
    high_low_temperatures_by_date = defaultdict(lambda: {'high': float('-inf'), 'low': float('inf')})
    for timestamp_string, temperature in temps_by_timestamp.items():
        timestamp = datetime.strptime(timestamp_string, '%Y-%m-%dT%H:%M:%S%z')
        date = timestamp.date()
        if temperature > high_low_temperatures_by_date[date]['high']:
            high_low_temperatures_by_date[date]['high'] = temperature
        if temperature < high_low_temperatures_by_date[date]['low']:
            high_low_temperatures_by_date[date]['low'] = temperature
    high_low_temperatures_by_date_json = json.dumps(high_low_temperatures_by_date)
    print(high_low_temperatures_by_date_json)
    return (high_low_temperatures_by_date_json)

@app.get("/highlowtempsbydate/{station_id}")
async def parse_high_low_temps_by_date(temperatures_by_timestamp: dict):
    """Endpoint to get high and low temperatures by date for a given observation station ID."""
    try:
        high_low_temperatures_by_date = parse_high_low_temps_by_date(station_id)
        return (high_low_temperatures_by_date))
    except HTTPException as e:
        raise e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
