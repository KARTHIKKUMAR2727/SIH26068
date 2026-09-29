from typing import Dict, Any, List
from datetime import datetime, timezone

class LocationAdvisoryEngine:
    def generate_advisories(
        self,
        location_name: str,
        lat: float,
        lon: float,
        current: Dict[str, Any],
        forecast: Dict[str, Any]
    ) -> Dict[str, Any]:
        temp = current.get("temperature", {}).get("current", 28.0)
        humidity = current.get("humidity", {}).get("value", 65)
        wind_speed = current.get("wind", {}).get("speed", 12.0)
        rain_prob = current.get("precipitation", {}).get("probability", 15)

        daily = forecast.get("daily", [])
        tomorrow_rain_prob = daily[1].get("rain_probability", 20) if len(daily) > 1 else rain_prob
        tomorrow_rain_mm = daily[1].get("precipitation_sum_mm", 0.0) if len(daily) > 1 else 0.0

        # 1. Agriculture Advisory
        agri_conditions = [
            f"Ambient Temp: {temp}°C",
            f"Relative Humidity: {humidity}%",
            f"Next 24h Rain Probability: {tomorrow_rain_prob}% ({tomorrow_rain_mm} mm)",
            f"Surface Wind: {wind_speed} km/h"
        ]
        agri_recs = []
        agri_severity = "Low"

        if tomorrow_rain_mm >= 15.0 or tomorrow_rain_prob >= 65:
            agri_severity = "High"
            agri_recs.append("Postpone scheduled field irrigation and chemical pesticide/fertilizer spray operations to avoid wash-off.")
            agri_recs.append("Ensure proper drainage in low-lying paddies and cash-crop fields to prevent root waterlogging.")
        elif wind_speed > 25.0:
            agri_severity = "Moderate"
            agri_recs.append("Avoid foliar chemical spray due to high droplet drift risk under current wind speeds.")
            agri_recs.append("Provide staking or earthing-up support for tall standing crops (sugarcane, banana).")
        elif humidity > 80 and temp > 28.0:
            agri_severity = "Moderate"
            agri_recs.append("Warm and humid conditions favor fungal blast/sheath blight. Monitor crops closely.")
            agri_recs.append("Irrigation may proceed during early morning hours.")
        else:
            agri_recs.append("Weather conditions are favorable for routine fertilizer application and crop weeding.")
            agri_recs.append("Standard irrigation schedule may continue normally.")

        agri_advisory = {
            "category": "Agriculture",
            "severity_level": agri_severity,
            "headline": "Favorable Field Conditions" if agri_severity == "Low" else ("Precipitation Caution for Farmers" if agri_severity == "High" else "Moderate Weather Influence"),
            "key_conditions": agri_conditions,
            "actionable_recommendations": agri_recs,
            "disclaimer": "Agricultural recommendations are contextual decision-support guidelines and should be correlated with local Krishi Vigyan Kendra (KVK) crop stage recommendations."
        }

        # 2. Travel Advisory
        travel_conditions = [
            f"Surface Temperature: {temp}°C",
            f"Wind: {wind_speed} km/h",
            f"Precipitation Risk: {tomorrow_rain_prob}%"
        ]
        travel_recs = []
        travel_severity = "Low"

        if tomorrow_rain_prob >= 60 or tomorrow_rain_mm >= 25.0:
            travel_severity = "High"
            travel_recs.append("Allow extra travel time due to anticipated urban waterlogging and wet road conditions.")
            travel_recs.append("Maintain increased following distances to avoid hydroplaning on highways.")
        elif temp >= 38.0:
            travel_severity = "Moderate"
            travel_recs.append("High midday heat index. Carry sufficient drinking water and check vehicle tire pressure.")
        else:
            travel_recs.append("Normal highway and city transit conditions with good atmospheric visibility.")

        travel_advisory = {
            "category": "Travel",
            "severity_level": travel_severity,
            "headline": "Normal Transit Conditions" if travel_severity == "Low" else "Travel Delay Advisory",
            "key_conditions": travel_conditions,
            "actionable_recommendations": travel_recs,
            "disclaimer": "Commuters must follow official highway and traffic police advisories during severe weather events."
        }

        # 3. Marine Advisory
        marine_conditions = [
            f"Coastal Wind: {wind_speed} km/h",
            f"Estimated Sea State: {'Squally' if wind_speed > 35 else ('Moderate' if wind_speed > 20 else 'Slight')}",
            f"Barometric Pressure: {current.get('pressure', {}).get('value', 1012.0)} hPa"
        ]
        marine_recs = []
        marine_severity = "Low"

        if wind_speed >= 40.0:
            marine_severity = "High"
            marine_recs.append("Fishermen are strongly advised NOT to venture into open sea. Squally winds exceeding 40 km/h.")
            marine_recs.append("Secure small craft and fishing trawlers at designated coastal harbors.")
        elif wind_speed >= 25.0:
            marine_severity = "Moderate"
            marine_recs.append("Small craft operators should exercise caution in offshore waters due to choppy seas.")
        else:
            marine_recs.append("Safe for inshore and offshore coastal fishing operations. Sea state is calm to slight.")

        marine_advisory = {
            "category": "Marine",
            "severity_level": marine_severity,
            "headline": "Calm Sea Operations" if marine_severity == "Low" else "Marine Caution / Squally Winds",
            "key_conditions": marine_conditions,
            "actionable_recommendations": marine_recs,
            "disclaimer": "Official marine warnings are governed by the India Meteorological Department (IMD) and INCOIS ocean bulletins."
        }

        # 4. Aviation Advisory
        aviation_conditions = [
            f"Surface Wind: {wind_speed} km/h ({round(wind_speed * 0.539957, 1)} knots)",
            f"Visibility: {current.get('visibility', {}).get('value', 10.0)} km",
            f"Surface Pressure: {current.get('pressure', {}).get('value', 1012.0)} hPa (QNH estimate)"
        ]
        aviation_recs = [
            "Meteorological briefing only: Verify official ICAO METAR/TAF with aerodrome control.",
            f"Visual flight conditions (VMC) supported by {current.get('visibility', {}).get('value', 10.0)} km visibility."
        ]
        aviation_advisory = {
            "category": "Aviation",
            "severity_level": "Low",
            "headline": "VMC Conditions Indicated",
            "key_conditions": aviation_conditions,
            "actionable_recommendations": aviation_recs,
            "disclaimer": "This platform provides meteorological general insights only and is strictly NOT an operational flight dispatch or official METAR/TAF service."
        }

        return {
            "location": location_name,
            "latitude": lat,
            "longitude": lon,
            "current_temp": temp,
            "rain_probability": rain_prob,
            "wind_speed": wind_speed,
            "humidity": humidity,
            "advisories": {
                "Agriculture": agri_advisory,
                "Travel": travel_advisory,
                "Marine": marine_advisory,
                "Aviation": aviation_advisory
            },
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "data_source": current.get("source", {}).get("source", "Meteorological Multi-Sensor NWP Analysis")
        }

advisory_engine = LocationAdvisoryEngine()
