## Kite Weather API

Takes a lat/lon, fetches today's max wind speed from Open-Meteo, and returns whether it's good weather to fly a kite.

## Stack

Python 3.12 · FastAPI · Open-Meteo · httpx

## Key files

- `app/conditions.py` — thresholds (15–50 km/h) and verdict logic
- `app/weather.py` — async Open-Meteo client
- `app/main.py` — `GET /kite-weather?lat=X&lon=Y`
- `tests/` — conditions, weather client, API layer

## Commands

```bash
pip3 install -r requirements.txt    # install
uvicorn app.main:app --reload       # run
pytest tests/ -v                    # test
```

## Deploy

Push to GitHub, connect on Railway or Render — no further config needed.
