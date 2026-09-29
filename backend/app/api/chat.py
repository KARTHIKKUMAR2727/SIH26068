from fastapi import APIRouter, Depends, Header
from typing import Optional
from app.schemas.chat import ChatRequest, ChatResponse
from app.engines.weather_intelligence_engine import weather_intelligence_engine
from app.api.auth import get_current_user
from app.providers.llm_provider import sanitize_response_text

router = APIRouter(prefix="/chat", tags=["Conversational AI Engine"])

@router.post("", response_model=ChatResponse)
async def chat_interaction(
    chat_req: ChatRequest,
    user: Optional[dict] = Depends(get_current_user)
):
    user_id = user.get("id") if user else None
    preferred_lang = user.get("preferred_language") if user else chat_req.language or "en"
    
    result = await weather_intelligence_engine.process_chat_message(
        message=chat_req.message,
        conversation_id=chat_req.conversation_id,
        language=preferred_lang,
        user_location_hint=chat_req.location,
        user_id=user_id
    )
    if isinstance(result.get("response"), str):
        result["response"] = sanitize_response_text(result["response"])
    return result
