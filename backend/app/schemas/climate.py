from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class YearlyClimatePoint(BaseModel):
    year: int
    mean_temp: float
    max_temp: float
    min_temp: float
    total_rainfall_mm: float
    temp_anomaly: float
    rainfall_anomaly: float

class ClimateTrendResponse(BaseModel):
    location: str
    latitude: float
    longitude: float
    start_year: int
    end_year: int
    baseline_period: str
    baseline_mean_temp: float
    baseline_annual_rainfall_mm: float
    temperature_trend_per_decade: float
    annual_data: List[YearlyClimatePoint]
    status: str
    anomaly_category: str  # "Below Normal", "Near Normal", "Above Normal"
    dry_days_average: int
    heavy_rainfall_days_average: int
    data_source: str
    methodology: str

class LocationComparisonItem(BaseModel):
    parameter: str
    location_a_value: Any
    location_b_value: Any
    unit: str
    difference: Optional[str] = None

class ClimateComparisonResponse(BaseModel):
    location_a: str
    location_b: str
    comparison_type: str  # "climate_baseline" or "current_forecast"
    parameters: List[LocationComparisonItem]
    ai_summary: str
    generated_at: str
