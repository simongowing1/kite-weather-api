import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Kite Weather API"
    assert "kite-weather" in body["endpoints"]
    assert "health" in body["endpoints"]


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_kite_weather_good_conditions():
    with patch("app.main.fetch_max_wind_speed", new=AsyncMock(return_value=28.0)):
        response = client.get("/kite-weather?lat=53.35&lon=-6.26")

    assert response.status_code == 200
    body = response.json()
    assert body["is_kite_weather"] is True
    assert body["wind_speed_kmh"] == 28.0
    assert body["location"] == {"lat": 53.35, "lon": -6.26}
    assert "Great kite weather" in body["verdict"]


def test_kite_weather_too_calm():
    with patch("app.main.fetch_max_wind_speed", new=AsyncMock(return_value=5.0)):
        response = client.get("/kite-weather?lat=53.35&lon=-6.26")

    assert response.status_code == 200
    body = response.json()
    assert body["is_kite_weather"] is False
    assert "Too calm" in body["verdict"]


def test_kite_weather_too_strong():
    with patch("app.main.fetch_max_wind_speed", new=AsyncMock(return_value=80.0)):
        response = client.get("/kite-weather?lat=53.35&lon=-6.26")

    assert response.status_code == 200
    body = response.json()
    assert body["is_kite_weather"] is False
    assert "Too strong" in body["verdict"]


def test_missing_params():
    response = client.get("/kite-weather")
    assert response.status_code == 422


def test_invalid_lat():
    response = client.get("/kite-weather?lat=999&lon=0")
    assert response.status_code == 422


def test_invalid_lon():
    response = client.get("/kite-weather?lat=0&lon=999")
    assert response.status_code == 422


def test_weather_fetch_failure_returns_502():
    with patch("app.main.fetch_max_wind_speed", new=AsyncMock(side_effect=Exception("API down"))):
        response = client.get("/kite-weather?lat=53.35&lon=-6.26")

    assert response.status_code == 502
    assert "Failed to fetch weather data" in response.json()["detail"]
