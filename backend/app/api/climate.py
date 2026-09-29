from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.providers.geocoding_provider import geocoding_provider
from app.providers.climate_provider import climate_provider
from app.schemas.climate import ClimateTrendResponse, ClimateComparisonResponse

router = APIRouter(prefix="/climate", tags=["Climate"])

@router.get("/trend", response_model=ClimateTrendResponse)
async def get_climate_trend(
    city: Optional[str] = Query("Chennai"),
    start_year: int = Query(2004, ge=1980, le=2024),
    end_year: int = Query(2024, ge=1990, le=2024)
):
    geo = await geocoding_provider.search(city)
    target = geo[0] if geo else {"name": city, "latitude": 13.0827, "longitude": 80.2707}
    
    data = await climate_provider.get_climate_trends(
        lat=target["latitude"],
        lon=target["longitude"],
        location_name=target["name"],
        start_year=start_year,
        end_year=end_year
    )
    return data

@router.get("/compare", response_model=ClimateComparisonResponse)
async def compare_climates(
    location_a: str = Query("Chennai"),
    location_b: str = Query("Madurai")
):
    geo_a = await geocoding_provider.search(location_a)
    geo_b = await geocoding_provider.search(location_b)
    
    loc_a = geo_a[0] if geo_a else {"name": location_a, "latitude": 13.08, "longitude": 80.27}
    loc_b = geo_b[0] if geo_b else {"name": location_b, "latitude": 9.92, "longitude": 78.11}

    data = await climate_provider.compare_locations(loc_a, loc_b)
    return data
