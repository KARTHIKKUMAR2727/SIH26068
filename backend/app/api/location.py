from fastapi import APIRouter, Query
from typing import List, Dict, Any, Optional
from app.providers.geocoding_provider import geocoding_provider, INDIAN_CITIES_REGISTRY

router = APIRouter(prefix="/location", tags=["Geocoding & Location"])

@router.get("/search")
async def search_location(q: str = Query(..., min_length=1, description="Location search query")):
    results = await geocoding_provider.search(q)
    return results

@router.get("/popular")
async def get_popular_locations():
    return INDIAN_CITIES_REGISTRY[:12]

@router.get("/reverse")
async def reverse_geocode(lat: float = Query(...), lon: float = Query(...)):
    res = await geocoding_provider.reverse(lat, lon)
    return res
