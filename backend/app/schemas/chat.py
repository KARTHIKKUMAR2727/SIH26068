from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    language: Optional[str] = "en"
    location: Optional[Dict[str, Any]] = None  # name, lat, lon

class GroundedDataRecord(BaseModel):
    parameter: str
    value: Any
    unit: str
    source: str
    timestamp: str

class ChatResponse(BaseModel):
    conversation_id: str
    message_id: str
    response: str
    intent: str
    location: Optional[Dict[str, Any]] = None
    structured_weather: Optional[Dict[str, Any]] = None
    alerts: Optional[List[Dict[str, Any]]] = None
    advisories: Optional[List[Dict[str, Any]]] = None
    climate_insight: Optional[Dict[str, Any]] = None
    grounded_data: List[GroundedDataRecord] = []
    source: Dict[str, Any]
    language: str
    suggested_questions: List[str] = []
    audio_base64: Optional[str] = None
