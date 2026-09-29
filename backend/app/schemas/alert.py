from typing import Optional, List
from pydantic import BaseModel

class WeatherAlert(BaseModel):
    id: str
    type: str  # Heavy Rain, Extreme Heat, Cold Wave, Strong Wind, Thunderstorm, Flood Risk, Cyclone, Severe Weather
    severity: str  # Moderate, Severe, Extreme, Advisory
    classification: str  # "OFFICIAL WARNING" or "AI-GENERATED WEATHER INSIGHT"
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    start_time: str
    end_time: str
    headline: str
    description: str
    instructions: Optional[str] = None
    source: str  # e.g., "IMD (India Meteorological Department)", "Open-Meteo Threshold Engine"
    issued_at: str
    is_active: bool = True
    parameters_exceeded: Optional[dict] = None

class AlertListResponse(BaseModel):
    total: int
    alerts: List[WeatherAlert]
    monitored_region: str
    generated_at: str
