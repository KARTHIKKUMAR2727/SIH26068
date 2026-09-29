from fastapi import APIRouter, Query, Response
from typing import Optional
from app.providers.geocoding_provider import geocoding_provider
from app.providers.weather_provider import get_weather_provider
from app.providers.alert_provider import alert_provider
from app.engines.report_engine import report_engine

router = APIRouter(prefix="/reports", tags=["Reports & Export"])

@router.get("/generate")
async def generate_report(city: Optional[str] = Query("Chennai"), report_type: str = Query("daily")):
    geo = await geocoding_provider.search(city)
    target = geo[0] if geo else {"name": city, "latitude": 13.0827, "longitude": 80.2707}

    prov = get_weather_provider()
    curr = await prov.get_current_weather(target["latitude"], target["longitude"], target["name"])
    f = await prov.get_forecast(target["latitude"], target["longitude"], target["name"])
    alerts = await alert_provider.get_alerts_for_location(target["latitude"], target["longitude"], target["name"], curr, f)

    rep = report_engine.generate_daily_report(target["name"], curr, f, alerts)
    return rep

@router.get("/export/csv")
async def export_report_csv(city: Optional[str] = Query("Chennai")):
    rep = await generate_report(city, "daily")
    csv_text = report_engine.export_csv(rep)
    return Response(
        content=csv_text,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=WeatherGPT_Report_{city}.csv"}
    )
