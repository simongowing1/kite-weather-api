import httpx

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


async def fetch_max_wind_speed(lat: float, lon: float) -> float:
    """Fetches today's maximum wind speed (km/h) at 10m for the given coordinates."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "windspeed_10m_max",
        "wind_speed_unit": "kmh",
        "forecast_days": 1,
        "timezone": "auto",
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(OPEN_METEO_URL, params=params)
        response.raise_for_status()

    data = response.json()

    try:
        wind_speed = data["daily"]["windspeed_10m_max"][0]
    except (KeyError, IndexError) as e:
        raise ValueError(f"Unexpected response structure from Open-Meteo: {e}") from e

    return float(wind_speed)
