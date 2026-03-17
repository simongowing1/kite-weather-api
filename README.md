# Kite Weather

Is it kite weather today?

Our neighbour gave my kids an old kite. But how do I know the best day to fly it with them?

Base URL: `https://kite-weather-api.up.railway.app`.

Interactive docs: `https://kite-weather-api.up.railway.app/docs`

- **`api/`** — FastAPI backend that fetches today's max wind speed from [Open-Meteo](https://open-meteo.com/) and returns a kite weather verdict
- **`viewer/`** — Next.js frontend with an animated speedometer UI

The viewer runs independently and proxies API calls to the FastAPI backend.

---

## Running locally

**API** (port 8000)
```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
```

**Viewer** (port 3000)
```bash
cd viewer && npm install
npm run dev
```

Open `http://localhost:3000` — or go straight to `http://localhost:3000?here=1` to use your current location.

---

## API

Base URL (deployed): `https://kite-weather-api.up.railway.app`

### Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/kite-weather?lat=X&lon=Y` | Kite weather verdict |
| GET | `/viewer` | Legacy HTML speedometer |
| GET | `/kite-weather/here` | Redirects to legacy viewer with geolocation |
| GET | `/health` | Health check |

### Example

```bash
curl "https://kite-weather-api.up.railway.app/kite-weather?lat=53.3498&lon=-6.2603"
```

```json
{
  "is_kite_weather": true,
  "verdict": "Great kite weather — wind is 28.0 km/h",
  "wind_speed_kmh": 28.0,
  "conditions": { "min_wind_kmh": 15.0, "max_wind_kmh": 50.0 },
  "location": { "lat": 53.3498, "lon": -6.2603 }
}
```

Interactive docs: `http://localhost:8000/docs`

---

## Kite conditions

| Parameter | Min | Max |
|---|---|---|
| Wind speed (km/h) | 15 | 50 |

Edit `api/conditions.py` to adjust the thresholds.

---

## Deploy

Two services on Railway or Render:

1. **API** — root directory, start command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
2. **Viewer** — `viewer/` directory, set env var `API_URL=<deployed API URL>`
