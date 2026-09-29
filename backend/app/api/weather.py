from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.providers.geocoding_provider import geocoding_provider
from app.providers.weather_provider import get_weather_provider
from app.schemas.weather import CurrentWeatherResponse

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/current", response_model=CurrentWeatherResponse)
async def get_current_weather(
    city: Optional[str] = Query(None, description="City or district name (e.g., Chennai, Sivakasi)"),
    latitude: Optional[float] = Query(None, description="Geographical latitude"),
    longitude: Optional[float] = Query(None, description="Geographical longitude")
):
    lat = latitude
    lon = longitude
    loc_name = city or "Chennai"

    if lat is None or lon is None:
        geo_results = await geocoding_provider.search(loc_name)
        if not geo_results:
            raise HTTPException(status_code=404, detail=f"Location '{loc_name}' could not be resolved.")
        target = geo_results[0]
        lat = target["latitude"]
        lon = target["longitude"]
        loc_name = target["name"]
    else:
        rev = await geocoding_provider.reverse(lat, lon)
        if rev:
            loc_name = rev.get("name", f"Location ({lat:.2f}, {lon:.2f})")

    provider = get_weather_provider()
    data = await provider.get_current_weather(lat, lon, loc_name)
    return data
