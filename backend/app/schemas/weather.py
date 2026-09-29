from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class LocationInfo(BaseModel):
    name: str
    latitude: float
    longitude: float
    country: Optional[str] = "India"
    state: Optional[str] = None
    district: Optional[str] = None

class SourceMetadata(BaseModel):
    source: str
    retrieved_at: str
    forecast_model: Optional[str] = "ECMWF/GFS Multi-Model"
    forecast_time: Optional[str] = None
    data_type: str = "observation"  # observation, forecast, reanalysis, nwp
    is_demo: bool = False

class CurrentWeatherResponse(BaseModel):
    location: LocationInfo
    temperature: Dict[str, Any]  # current, feels_like, min, max, unit
    humidity: Dict[str, Any]     # value, unit
    wind: Dict[str, Any]         # speed, direction, gust, unit
    pressure: Dict[str, Any]     # value, unit
    visibility: Dict[str, Any]   # value, unit
    precipitation: Dict[str, Any]# current, probability, unit
    condition: str
    condition_code: int
    uv_index: Optional[float] = 0.0
    air_quality_index: Optional[int] = 45
    timestamp: str
    source: SourceMetadata

class HourlyForecastItem(BaseModel):
    time: str
    temperature: float
    feels_like: float
    rain_probability: int
    precipitation_mm: float
    humidity: int
    wind_speed: float
    wind_direction: int
    cloud_cover: int
    condition: str
    pressure: float

class DailyForecastItem(BaseModel):
    date: str
    temp_max: float
    temp_min: float
    rain_probability: int
    precipitation_sum_mm: float
    humidity_mean: int
    wind_speed_max: float
    condition: str
    sunrise: Optional[str] = None
    sunset: Optional[str] = None
    uv_index_max: Optional[float] = None

class ForecastResponse(BaseModel):
    location: LocationInfo
    hourly: List[HourlyForecastItem]
    daily: List[DailyForecastItem]
    source: SourceMetadata
