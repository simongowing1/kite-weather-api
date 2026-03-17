from pathlib import Path

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel

from api.conditions import CONDITIONS, assess
from api.weather import fetch_max_wind_speed

_VIEWER_HTML = (Path(__file__).parent / "viewer.html").read_text()

app = FastAPI(
    title="Kite Weather API",
    description="Is it kite weather at your location today?",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
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


@app.get("/viewer", response_class=HTMLResponse)
async def viewer():
    return HTMLResponse(content=_VIEWER_HTML)


@app.get("/kite-weather/here", response_class=HTMLResponse)
async def kite_weather_here():
    return RedirectResponse(url="/viewer?here=1")


@app.get("/health")
async def health():
    return {"status": "ok"}
