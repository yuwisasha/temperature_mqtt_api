from typing import Any

from httpx import AsyncClient, URL, RequestError


async def get_temperature(url: URL) -> dict[str, Any]:
    """Get data from temperature API"""

    async with AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            response_json = response.json()
            return response_json
        raise RequestError(
            message=f"Request failed with status code: {response.status_code}"
        )


async def get_stations_temperature(
    stations: set[str], response: dict[str, Any]
) -> list[dict[str, Any]]:
    """Get temperature for stations from STATION_ID list"""

    try:
        return [
            item
            for item in response["items"][0]["readings"]
            if item["station_id"] in stations
        ]
    except KeyError as e:
        raise KeyError("Invalid response format: missing required keys") from e


async def get_api_info(response: dict[str, Any]) -> dict[str, str]:
    """Get API status"""

    return response.get("api_info")
