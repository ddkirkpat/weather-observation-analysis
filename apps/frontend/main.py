from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json
from collections import defaultdict
from datetime import datetime

class Data(BaseModel):
    latitude: float
    longitude: float
    station_id: str
    temps_by_timestamp: dict

app = FastAPI()

def get_temperature_report_for_address(address, data: Data):
    return

@app.get("/gettemperaturereport/{address}")
async def get_temperature_report(address: str):
    """Endpoint to get temperatures by timestamp for a given observation station ID."""
    try:
        return ("Where is my report?")
    except HTTPException as e:
        raise e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)