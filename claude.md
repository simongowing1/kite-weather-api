## Kite Weather API

Takes a user's lat/lon, fetches today's max wind speed from Open-Meteo, compares it against kite-flying thresholds, and returns a verdict.

## Stack

Python 3.11+ · FastAPI · Open-Meteo (free, no API key) · httpx

## Files

- `conditions.py` — kite thresholds (15–50 km/h) and comparison logic
- `weather.py` — async Open-Meteo client
- `main.py` — FastAPI app, single `GET /kite-weather?lat=X&lon=Y` endpoint
- `requirements.txt` — fastapi, uvicorn, httpx

## Run

```bash
pip3 install -r requirements.txt
uvicorn main:app --reload
```
