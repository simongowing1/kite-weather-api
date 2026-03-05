import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock, patch

from weather import fetch_max_wind_speed

VALID_RESPONSE = {
    "daily": {
        "windspeed_10m_max": [28.5]
    }
}


@pytest.mark.asyncio
async def test_returns_wind_speed():
    mock_response = MagicMock()
    mock_response.json.return_value = VALID_RESPONSE
    mock_response.raise_for_status = MagicMock()

    with patch("weather.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client_cls.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client_cls.return_value.__aexit__ = AsyncMock(return_value=False)

        result = await fetch_max_wind_speed(53.35, -6.26)

    assert result == 28.5


@pytest.mark.asyncio
async def test_raises_on_http_error():
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "500", request=MagicMock(), response=MagicMock()
    )

    with patch("weather.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client_cls.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client_cls.return_value.__aexit__ = AsyncMock(return_value=False)

        with pytest.raises(httpx.HTTPStatusError):
            await fetch_max_wind_speed(53.35, -6.26)


@pytest.mark.asyncio
async def test_raises_on_malformed_response():
    mock_response = MagicMock()
    mock_response.json.return_value = {"unexpected": "data"}
    mock_response.raise_for_status = MagicMock()

    with patch("weather.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client_cls.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client_cls.return_value.__aexit__ = AsyncMock(return_value=False)

        with pytest.raises(ValueError, match="Unexpected response structure"):
            await fetch_max_wind_speed(53.35, -6.26)
