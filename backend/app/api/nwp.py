from fastapi import APIRouter, Query
from typing import Optional
from app.providers.geocoding_provider import geocoding_provider
from app.providers.nwp_provider import nwp_provider
from app.schemas.nwp import NWPComparisonResponse

router = APIRouter(prefix="/nwp", tags=["Numerical Weather Prediction (NWP)"])

@router.get("/run", response_model=NWPComparisonResponse)
async def get_nwp_model_runs(city: Optional[str] = Query("Chennai")):
    geo = await geocoding_provider.search(city)
    target = geo[0] if geo else {"name": city, "latitude": 13.0827, "longitude": 80.2707}
    
    data = await nwp_provider.get_model_runs(
        lat=target["latitude"],
        lon=target["longitude"],
        location_name=target["name"]
    )
    return data
