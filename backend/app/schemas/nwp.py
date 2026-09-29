from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class NWPLeadTimeStep(BaseModel):
    lead_time_hours: int  # 6, 12, 24, 48, 72
    forecast_timestamp: str
    temperature: float
    precipitation: float
    wind_speed: float
    pressure: float
    cloud_cover: int

class NWPModelRun(BaseModel):
    model_name: str  # "GFS (Global Forecast System)", "ECMWF IFS", "ICON Global"
    run_cycle: str  # "00Z", "06Z", "12Z", "18Z"
    run_timestamp: str
    resolution_km: float
    provider_source: str
    lead_times: List[NWPLeadTimeStep]

class NWPComparisonResponse(BaseModel):
    location: str
    latitude: float
    longitude: float
    models: List[NWPModelRun]
    ensemble_spread: Dict[str, Any]  # min, max, mean, spread_category
    generated_at: str
