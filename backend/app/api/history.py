from fastapi import APIRouter, Query
from typing import Optional
from app.providers.geocoding_provider import geocoding_provider
from app.providers.climate_provider import climate_provider

router = APIRouter(prefix="/history", tags=["Historical Weather"])

@router.get("")
async def get_historical_weather(
    city: Optional[str] = Query("Chennai"),
    start_date: str = Query("2024-07-01"),
    end_date: str = Query("2024-07-31")
):
    geo = await geocoding_provider.search(city)
    target = geo[0] if geo else {"name": city, "latitude": 13.0827, "longitude": 80.2707}
    data = await climate_provider.get_historical_range(
        lat=target["latitude"],
        lon=target["longitude"],
        start_date=start_date,
        end_date=end_date
    )
    return {"location": target["name"], **data}
