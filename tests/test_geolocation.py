import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import AsyncMock, patch
from endpoints.geolocation.models import (
    Geolocation,
)
from endpoints.geolocation.models import (
    GeolocationCreate,
)
from services.geolocation import fetch_geolocation

VALID_IP = "142.250.75.14"
VALID_URL = "google.com"
SAMPLE_GEO_DATA = {
    "ip": VALID_IP,
    "country": "United States",
    "region": "California",
    "city": "Mountain View",
    "latitude": "37.386",
    "longitude": "-122.0838",
}


@pytest.mark.asyncio
async def test_add_geolocation_with_ip_success(
    client, override_get_async_db, mock_db_session
):
    with patch(
        "endpoints.geolocation.api.fetch_geolocation",
        new_callable=AsyncMock,
        return_value=SAMPLE_GEO_DATA,
    ) as mock_fetch:
        mock_db_session.add.return_value = None
        mock_db_session.commit.return_value = None
        mock_db_session.refresh.side_effect = lambda x: setattr(x, "id", 1)

        from services.geolocation import fetch_geolocation

        response = client.post("/api/v1/geolocation/", json={"ip": VALID_IP})

        assert response.status_code == 200, (
            f"Failed with status {response.status_code}: {response.json()}"
        )
        assert response.json()["ip"] == VALID_IP
        mock_fetch.assert_called_once_with(ip=VALID_IP, domain=None)


@pytest.fixture(autouse=True)
def cleanup():
    yield
    app.dependency_overrides.clear()
