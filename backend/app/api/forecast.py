from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.providers.geocoding_provider import geocoding_provider
from app.providers.weather_provider import get_weather_provider
from app.schemas.weather import ForecastResponse

router = APIRouter(prefix="/forecast", tags=["Forecast"])

@router.get("", response_model=ForecastResponse)
async def get_forecast(
    city: Optional[str] = Query(None, description="City or district name"),
    latitude: Optional[float] = Query(None, description="Latitude"),
    longitude: Optional[float] = Query(None, description="Longitude")
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

    provider = get_weather_provider()
    data = await provider.get_forecast(lat, lon, loc_name)
    return data

@router.get("/hourly")
async def get_hourly_forecast(city: Optional[str] = Query(None), latitude: Optional[float] = None, longitude: Optional[float] = None):
    full_f = await get_forecast(city, latitude, longitude)
    return {"location": full_f.location, "hourly": full_f.hourly, "source": full_f.source}

@router.get("/daily")
async def get_daily_forecast(city: Optional[str] = Query(None), latitude: Optional[float] = None, longitude: Optional[float] = None):
    full_f = await get_forecast(city, latitude, longitude)
    return {"location": full_f.location, "daily": full_f.daily, "source": full_f.source}
