from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel

from app.conditions import CONDITIONS, assess
from app.weather import fetch_max_wind_speed

app = FastAPI(
    title="Kite Weather API",
    description="Is it kite weather at your location today?",
    version="0.1.0",
)


class ConditionsModel(BaseModel):
    min_wind_kmh: float
    max_wind_kmh: float


class LocationModel(BaseModel):
    lat: float
    lon: float


class KiteWeatherResponse(BaseModel):
    is_kite_weather: bool
    verdict: str
    wind_speed_kmh: float
    conditions: ConditionsModel
    location: LocationModel


@app.get("/")
async def root():
    return {
        "name": "Kite Weather API",
        "description": "Is it kite weather at your location today?",
        "endpoints": {
            "kite-weather": "/kite-weather",
            "health": "/health",
        },
    }


@app.get("/kite-weather", response_model=KiteWeatherResponse)
async def kite_weather(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lon: float = Query(..., description="Longitude", ge=-180, le=180),
):
    try:
        wind_speed = await fetch_max_wind_speed(lat, lon)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch weather data: {e}")

    is_kite, verdict = assess(wind_speed)

    return KiteWeatherResponse(
        is_kite_weather=is_kite,
        verdict=verdict,
        wind_speed_kmh=wind_speed,
        conditions=ConditionsModel(
            min_wind_kmh=CONDITIONS.min_wind_kmh,
            max_wind_kmh=CONDITIONS.max_wind_kmh,
        ),
        location=LocationModel(lat=lat, lon=lon),
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
