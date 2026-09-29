from fastapi import APIRouter, Query
from typing import Optional
from app.providers.geocoding_provider import geocoding_provider
from app.providers.weather_provider import get_weather_provider
from app.engines.advisory_engine import advisory_engine
from app.schemas.advisory import AdvisoryResponse

router = APIRouter(prefix="/advisory", tags=["Advisories"])

@router.get("", response_model=AdvisoryResponse)
async def get_advisories(city: Optional[str] = Query("Chennai")):
    geo = await geocoding_provider.search(city)
    target = geo[0] if geo else {"name": city, "latitude": 13.0827, "longitude": 80.2707}

    prov = get_weather_provider()
    curr = await prov.get_current_weather(target["latitude"], target["longitude"], target["name"])
    f = await prov.get_forecast(target["latitude"], target["longitude"], target["name"])

    data = advisory_engine.generate_advisories(
        location_name=target["name"],
        lat=target["latitude"],
        lon=target["longitude"],
        current=curr,
        forecast=f
    )
    return data
