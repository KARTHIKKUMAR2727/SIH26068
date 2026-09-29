from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime, timezone
from app.providers.geocoding_provider import geocoding_provider
from app.providers.weather_provider import get_weather_provider
from app.providers.alert_provider import alert_provider
from app.schemas.alert import AlertListResponse

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("", response_model=AlertListResponse)
async def get_alerts(
    city: Optional[str] = Query("Chennai", description="City or State name"),
    latitude: Optional[float] = None,
    longitude: Optional[float] = None
):
    lat = latitude or 13.0827
    lon = longitude or 80.2707
    loc_name = city or "Chennai"

    if latitude is None or longitude is None:
        geo = await geocoding_provider.search(loc_name)
        if geo:
            lat = geo[0]["latitude"]
            lon = geo[0]["longitude"]
            loc_name = geo[0]["name"]

    w_prov = get_weather_provider()
    curr = await w_prov.get_current_weather(lat, lon, loc_name)
    forecast = await w_prov.get_forecast(lat, lon, loc_name)

    alerts = await alert_provider.get_alerts_for_location(lat, lon, loc_name, curr, forecast)

    return AlertListResponse(
        total=len(alerts),
        alerts=alerts,
        monitored_region=loc_name,
        generated_at=datetime.now(timezone.utc).isoformat()
    )
