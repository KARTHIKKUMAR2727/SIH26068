import asyncio

from app.engines.query_engine import query_engine
from app.providers.climate_provider import ERA5ClimateProvider
from app.providers.llm_provider import sanitize_response_text


def test_historical_range_uses_local_era5_data():
    async def run_check():
        provider = ERA5ClimateProvider()
        result = await provider.get_historical_range(13.0827, 80.2707, "2024-01-01", "2024-01-15")
        return result

    result = asyncio.run(run_check())

    assert result["records"], "Historical records should not be empty"
    assert result.get("is_demo") is False, "Historical data must come from the real ERA5 archive, not demo data"
    assert result["data_source"].lower().find("era5") >= 0


def test_multilingual_rain_query_parses_chennai_and_tomorrow():
    parsed = query_engine.parse_query("சென்னை நாளை மழை இருக்கா?", default_location="Chennai")
    assert parsed["location"] == "Chennai"
    assert parsed["intent"] in {"rainfall", "forecast"}
    assert parsed["date"] == "tomorrow"

    parsed_hi = query_engine.parse_query("चेन्नई में कल बारिश होगी?", default_location="Chennai")
    assert parsed_hi["location"] == "Chennai"
    assert parsed_hi["intent"] in {"rainfall", "forecast"}
    assert parsed_hi["date"] == "tomorrow"


def test_response_text_is_plain_and_clean_without_emoji_or_icons():
    raw = "🌤️ Current Weather for Chennai\n\n• Temperature: 31°C\n• Condition: Clear sky\n\nSource: Open-Meteo"
    cleaned = sanitize_response_text(raw)
    assert "🌤️" not in cleaned
    assert "•" not in cleaned
    assert "**" not in cleaned
    assert "Current Weather for Chennai" in cleaned
    assert "Temperature: 31°C" in cleaned


def test_forecast_response_excludes_lead_source_footer():
    raw = "Forecast for Chennai (Tomorrow). Precipitation Probability: 79%. Rain is Likely. Expected Precipitation: 0.7 mm. Sky Condition: Light drizzle. Temperature Range: Min 26.7°C / Max 35.1°C. Forecast Lead Source: Open-Meteo High-Resolution Multi-Model Forecast."
    cleaned = sanitize_response_text(raw)
    assert "Forecast Lead Source" not in cleaned
    assert "Open-Meteo High-Resolution Multi-Model Forecast" not in cleaned


def test_rain_question_gets_direct_specific_answer():
    from app.providers.llm_provider import LocalGroundedLLMProvider

    prompt = "Will it rain in Chennai tomorrow evening?"
    context = {
        "intent": "forecast",
        "target_date": "tomorrow",
        "location": {"name": "Chennai"},
        "forecast": {
            "daily": [
                {"date": "2024-01-01", "rain_probability": 20, "precipitation_sum_mm": 0.2, "temp_max": 31, "temp_min": 26, "condition": "Partly cloudy"},
                {"date": "2024-01-02", "rain_probability": 79, "precipitation_sum_mm": 0.7, "temp_max": 35.1, "temp_min": 26.7, "condition": "Light drizzle"},
            ],
            "source": {"source": "Open-Meteo"},
        },
    }

    result = asyncio.run(LocalGroundedLLMProvider().generate_response(prompt, "", context, "en"))
    assert "Yes" in result or "Likely" in result
    assert "79%" in result
    assert "Chennai" in result
    assert "tomorrow" in result.lower()


def test_translated_weather_responses_do_not_include_source_footer():
    from app.providers.language_provider import language_provider

    ta = language_provider.format_weather_response("ta", "Sivakasi", 31, 28, "Light rain", 75, 12, 94, "Open-Meteo")
    hi = language_provider.format_weather_response("hi", "Sivakasi", 31, 28, "Light rain", 75, 12, 94, "Open-Meteo")

    assert "ஆதாரம்" not in ta
    assert "source" not in ta.lower()
    assert "डेटा स्रोत" not in hi
    assert "source" not in hi.lower()
