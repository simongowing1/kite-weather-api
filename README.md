# Kite Weather API

Is it kite weather today?

Our neighbour gave my kids an old kite. But how do I know the best day to fly it with them? 

Base URL: `https://kite-weather-api.up.railway.app`.

Interactive docs: `https://kite-weather-api.up.railway.app/docs`

## Usage

```bash
curl "https://kite-weather-api.up.railway.app/kite-weather?lat=53.3498&lon=-6.2603"
```

```json
{
  "is_kite_weather": true,
  "verdict": "Great kite weather — wind is 28.0 km/h",
  "wind_speed_kmh": 28.0,
  "conditions": {
    "min_wind_kmh": 15.0,
    "max_wind_kmh": 50.0
  },
  "location": {
    "lat": 53.3498,
    "lon": -6.2603
  }
}
```

## Kite conditions

| Parameter | Min | Max |
|---|---|---|
| Wind speed (km/h) | 15 | 50 |

Edit `api/conditions.py` to adjust the thresholds.

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/kite-weather` | Returns kite weather verdict for a lat/lon |
| GET | `/health` | Health check |

### Query parameters

| Param | Type | Required | Description |
|---|---|---|---|
| `lat` | float | yes | Latitude (-90 to 90) |
| `lon` | float | yes | Longitude (-180 to 180) |

## Local Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn api.main:app --reload
```

The API is now running at `http://localhost:8000`.

Interactive docs: `http://localhost:8000/docs`

---

## Weather data

Wind speed is sourced from [Open-Meteo](https://open-meteo.com/) — free, no API key required.
