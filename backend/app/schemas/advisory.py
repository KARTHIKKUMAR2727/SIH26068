from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class AdvisoryItem(BaseModel):
    category: str  # Agriculture, Travel, Marine, Aviation
    severity_level: str  # Low, Moderate, High, Caution
    headline: str
    key_conditions: List[str]
    actionable_recommendations: List[str]
    disclaimer: str

class AdvisoryResponse(BaseModel):
    location: str
    latitude: float
    longitude: float
    current_temp: float
    rain_probability: int
    wind_speed: float
    humidity: int
    advisories: Dict[str, AdvisoryItem]
    generated_at: str
    data_source: str
