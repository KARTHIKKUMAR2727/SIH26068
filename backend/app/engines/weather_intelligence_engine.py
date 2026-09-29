import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from app.providers.geocoding_provider import geocoding_provider
from app.providers.weather_provider import get_weather_provider
from app.providers.alert_provider import alert_provider
from app.providers.climate_provider import climate_provider
from app.providers.nwp_provider import nwp_provider
from app.providers.llm_provider import get_llm_provider
from app.providers.language_provider import language_provider
from app.engines.query_engine import query_engine
from app.engines.validation_engine import validation_engine
from app.engines.advisory_engine import advisory_engine
from app.core.database import get_collection

class WeatherIntelligenceEngine:
    def __init__(self):
        self.conversations_col = get_collection("conversations")
        self.messages_col = get_collection("messages")

    async def process_chat_message(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        language: str = "en",
        user_location_hint: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        conversation_id = conversation_id or str(uuid.uuid4())

        # 1. Retrieve Conversation History for Multi-turn Context
        prev_location = None
        if conversation_id:
            recent_msgs = await self.messages_col.find({"conversation_id": conversation_id}, limit=6)
            for m in reversed(recent_msgs):
                if m.get("location_name"):
                    prev_location = m.get("location_name")
                    break

        # 2. Extract Intent and Entities from Natural Language Query
        parsed = query_engine.parse_query(message, default_location=prev_location or (user_location_hint.get("name") if user_location_hint else "Chennai"))
        target_location_name = parsed["location"]
        target_date = parsed["date"]
        intent = parsed["intent"]

        # 3. Resolve Geographical Coordinates via Geocoding Provider
        geo_results = await geocoding_provider.search(target_location_name)
        active_geo = geo_results[0] if geo_results else {
            "name": target_location_name,
            "latitude": 13.0827,
            "longitude": 80.2707,
            "country": "India"
        }
        lat = active_geo.get("latitude", 13.0827)
        lon = active_geo.get("longitude", 80.2707)

        # 4. Retrieve Ground-Truth Meteorological Data
        weather_provider = get_weather_provider()
        current_weather = await weather_provider.get_current_weather(lat, lon, active_geo["name"])
        forecast = await weather_provider.get_forecast(lat, lon, active_geo["name"])
        active_alerts = await alert_provider.get_alerts_for_location(lat, lon, active_geo["name"], current_weather, forecast)
        climate_data = await climate_provider.get_climate_trends(lat, lon, active_geo["name"])
        advisories_data = advisory_engine.generate_advisories(active_geo["name"], lat, lon, current_weather, forecast)

        # Handle secondary location for comparison queries
        comparison_data = None
        if parsed.get("secondary_location"):
            sec_geo_results = await geocoding_provider.search(parsed["secondary_location"])
            sec_geo = sec_geo_results[0] if sec_geo_results else {"name": parsed["secondary_location"], "latitude": 9.9252, "longitude": 78.1198}
            comparison_data = await climate_provider.compare_locations(active_geo, sec_geo)

        # 5. Build Explicit Grounded Data Records for Numerical Verification
        grounded_records = []
        t_val = current_weather.get("temperature", {}).get("current")
        if t_val is not None:
            grounded_records.append({"parameter": "current_temperature", "value": t_val, "unit": "°C", "source": current_weather["source"]["source"], "timestamp": current_weather["timestamp"]})
        
        hum_val = current_weather.get("humidity", {}).get("value")
        if hum_val is not None:
            grounded_records.append({"parameter": "humidity", "value": hum_val, "unit": "%", "source": current_weather["source"]["source"], "timestamp": current_weather["timestamp"]})
        
        wind_val = current_weather.get("wind", {}).get("speed")
        if wind_val is not None:
            grounded_records.append({"parameter": "wind_speed", "value": wind_val, "unit": "km/h", "source": current_weather["source"]["source"], "timestamp": current_weather["timestamp"]})

        # Forecast grounded records
        daily = forecast.get("daily", [])
        if len(daily) > 1:
            tomorrow = daily[1]
            grounded_records.append({"parameter": "tomorrow_rain_prob", "value": tomorrow.get("rain_probability"), "unit": "%", "source": forecast["source"]["source"], "timestamp": tomorrow.get("date")})
            grounded_records.append({"parameter": "tomorrow_precipitation_mm", "value": tomorrow.get("precipitation_sum_mm"), "unit": "mm", "source": forecast["source"]["source"], "timestamp": tomorrow.get("date")})
            grounded_records.append({"parameter": "tomorrow_temp_max", "value": tomorrow.get("temp_max"), "unit": "°C", "source": forecast["source"]["source"], "timestamp": tomorrow.get("date")})
            grounded_records.append({"parameter": "tomorrow_temp_min", "value": tomorrow.get("temp_min"), "unit": "°C", "source": forecast["source"]["source"], "timestamp": tomorrow.get("date")})

        # 6. Construct LLM Context
        grounded_context = {
            "intent": intent,
            "target_date": target_date,
            "location": active_geo,
            "current_weather": current_weather,
            "forecast": forecast,
            "alerts": active_alerts,
            "climate": climate_data,
            "advisories": advisories_data["advisories"],
            "comparison": comparison_data,
            "grounded_records": grounded_records
        }

        # 7. Generate Response via LLM Provider
        system_instruction = (
            "You are WeatherGPT, a professional meteorological intelligence conversational AI platform. "
            "CRITICAL RULES:\n"
            "1. You MUST NOT invent, guess, or hallucinate any weather numbers or dates.\n"
            "2. Every numerical value (temperature, rain probability, wind, pressure) MUST come strictly from the provided GROUNDED METEOROLOGICAL CONTEXT.\n"
            "3. Clearly identify whether data is an observation, forecast, model output, or official warning.\n"
            "4. Clearly attribute data sources.\n"
            "5. Respond in the requested language."
        )

        llm_provider = get_llm_provider()
        ai_response_text = await llm_provider.generate_response(
            prompt=message,
            system_instruction=system_instruction,
            grounded_context=grounded_context,
            language=language
        )

        # 8. Anti-Hallucination & Numerical Grounding Validation
        is_valid, validation_issues = validation_engine.validate(
            response_text=ai_response_text,
            grounded_data=grounded_records,
            expected_location=active_geo["name"]
        )

        # 9. Smart Suggested Follow-up Questions
        suggested = [
            f"Will it rain in {active_geo['name']} tomorrow?",
            f"Show 7-day forecast for {active_geo['name']}",
            f"Are there any severe weather alerts near {active_geo['name']}?",
            f"What is the 20-year temperature trend for {active_geo['name']}?"
        ]

        # 10. Persist to Database / Memory
        msg_id = str(uuid.uuid4())
        await self.messages_col.insert_one({
            "message_id": msg_id,
            "conversation_id": conversation_id,
            "user_id": user_id,
            "role": "user",
            "content": message,
            "location_name": active_geo["name"],
            "created_at": now.isoformat()
        })
        await self.messages_col.insert_one({
            "message_id": str(uuid.uuid4()),
            "conversation_id": conversation_id,
            "user_id": user_id,
            "role": "assistant",
            "content": ai_response_text,
            "intent": intent,
            "location_name": active_geo["name"],
            "data_sources": [current_weather["source"]["source"]],
            "created_at": now.isoformat()
        })

        return {
            "conversation_id": conversation_id,
            "message_id": msg_id,
            "response": ai_response_text,
            "intent": intent,
            "location": active_geo,
            "structured_weather": current_weather,
            "forecast": forecast,
            "alerts": active_alerts,
            "advisories": list(advisories_data["advisories"].values()),
            "climate_insight": climate_data,
            "grounded_data": grounded_records,
            "source": current_weather["source"],
            "language": language,
            "suggested_questions": suggested,
            "validation_passed": is_valid,
            "validation_notes": validation_issues
        }

weather_intelligence_engine = WeatherIntelligenceEngine()
