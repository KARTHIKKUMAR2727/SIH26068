import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone, timedelta

SUPPORTED_INTENTS = [
    "current_weather",
    "forecast",
    "rainfall",
    "temperature",
    "wind",
    "humidity",
    "pressure",
    "air_quality",
    "weather_alert",
    "cyclone",
    "historical_weather",
    "climate_analysis",
    "comparison",
    "agriculture_advisory",
    "travel_advisory",
    "marine_advisory",
    "aviation_weather",
    "location_search",
    "general_weather_question"
]

class NaturalLanguageQueryEngine:
    def __init__(self):
        # Known Indian cities and regions for fast entity extraction
        self.known_locations = [
            "chennai", "madurai", "sivakasi", "coimbatore", "tiruchirappalli", "trichy",
            "salem", "tirunelveli", "kanyakumari", "tamil nadu", "bengaluru", "bangalore",
            "hyderabad", "mumbai", "pune", "delhi", "new delhi", "kolkata", "kochi",
            "cochin", "thiruvananthapuram", "trivandrum", "kerala", "visakhapatnam",
            "vizag", "vijayawada", "ahmedabad", "jaipur", "lucknow", "bhopal", "patna",
            "சென்னை", "மதுரை", "சிவகாசி", "கோயம்புத்தூர்", "திருச்சி", "சேலம்",
            "திருநெல்வேலி", "கன்னியாகுமரி", "தமிழ்நாடு", "பெங்களூர்", "ஹைதராபாத்",
            "மும்பை", "புனே", "டெல்லி", "கொல்கத்தா", "கோச்சி", "திருவனந்தபுரம்",
            "విజాగ్", "విశాఖపట్టణం", "విజయవాడ", "చెన్నై", "బెంగళూరు", "హైదరాబాదు",
            "ముంబై", "పూణే", "న్యూ ఢిల్లీ", "కొల్కతా", "కోయిచ్", "తిరువనంతపురం",
            "चेन्नई", "मदुरै", "कोयंबटूर", "तिरुच्चिरापल्ली", "बेंगलुरु", "हैदराबाद",
            "मुंबई", "पुणे", "दिल्ली", "कोलकाता", "कोच्चि", "तिरुवनंतपुरम"
        ]
        self.location_aliases = {
            "சென்னை": "Chennai",
            "சென்ன": "Chennai",
            "மதுரை": "Madurai",
            "சிவகாசி": "Sivakasi",
            "கோயம்புத்தூர்": "Coimbatore",
            "திருச்சி": "Tiruchirappalli",
            "சேலம்": "Salem",
            "திருநெல்வேலி": "Tirunelveli",
            "கன்னியாகுமரி": "Kanyakumari",
            "தமிழ்நாடு": "Tamil Nadu",
            "பெங்களூர்": "Bengaluru",
            "கோச்சி": "Kochi",
            "மும்பை": "Mumbai",
            "புனே": "Pune",
            "டெல்லி": "Delhi",
            "கொல்கத்தா": "Kolkata",
            "திருவனந்தபுரம்": "Thiruvananthapuram",
            "చెన్నై": "Chennai",
            "బెంగళూరు": "Bengaluru",
            "హైదరాబాదు": "Hyderabad",
            "ముంబై": "Mumbai",
            "పూణే": "Pune",
            "కొల్కతా": "Kolkata",
            "చెన్నయ": "Chennai",
            "चेन्नई": "Chennai",
            "मुंबई": "Mumbai",
            "दिल्ली": "Delhi",
            "कोलकाता": "Kolkata",
            "कोच्चि": "Kochi",
            "बेंगलुरु": "Bengaluru",
            "हैदराबाद": "Hyderabad",
            "मदुरै": "Madurai",
        }
        self.time_aliases = {
            "நாளை": "tomorrow",
            "இன்று": "today",
            "மறுநாள்": "day after tomorrow",
            "कल": "tomorrow",
            "आज": "today",
            "होगा": "future",
            "వేపు": "tomorrow",
            "రేపు": "tomorrow",
            "నేడు": "today",
            "ఈ వారం": "week",
        }
        self.rain_keywords = [
            "rain", "raining", "rainfall", "precipitation", "shower", "drizzle", "downpour",
            "மழை", "மழை இருக்கா", "மழை வருமா", "மழை பெய்யுமா", "வானிலை", "பொழிவு",
            "बारिश", "बरसात", "गर्मी", "अच्छा मौसम", "भारी बारिश", "गर्मी",
            "వర్షం", "వర్ష సూచన", "వర్షం అవుతుందా", "మంచు", "వాతావరణం",
            "മഴ", "മഴയോ", "മഴക്കாலം", "മഴവെള്ളം", "കാലാവസ്ഥ",
            "ಮಳೆ", "ಮಳೆ ಬರುತ್ತೆ", "ಮಳೆಯಾಗುತ್ತಾ", "ಹವಾಮಾನ",
            "বৃষ্টি", "বৃষ্টির", "আবহাওয়া"
        ]

    def parse_query(self, text: str, default_location: Optional[str] = None) -> Dict[str, Any]:
        text_lower = text.lower().strip()

        # 1. Extract Location
        extracted_location = None
        extracted_secondary_location = None

        # Check for comparison (e.g., "compare chennai and madurai" or "between chennai and madurai")
        comp_match = re.search(r'(?:compare|between)\s+([a-z\s\u0900-\u097F\u0B00-\u0B7F\u0C00-\u0C7F\u0B80-\u0BFF]+?)\s+(?:and|with|to)\s+([a-z\s\u0900-\u097F\u0B00-\u0B7F\u0C00-\u0C7F\u0B80-\u0BFF\?]+)', text_lower)
        if comp_match:
            loc1 = comp_match.group(1).strip()
            loc2 = re.sub(r'[\?\.,!]', '', comp_match.group(2)).strip()
            loc2 = loc2.split(" tomorrow")[0].split(" today")[0].split(" this week")[0].strip()
            extracted_location = self.location_aliases.get(loc1, loc1.title())
            extracted_secondary_location = self.location_aliases.get(loc2, loc2.title())

        if not extracted_location:
            for loc in self.known_locations:
                pattern = r'\b' + re.escape(loc) + r'\b'
                if re.search(pattern, text_lower):
                    extracted_location = self.location_aliases.get(loc, loc.title())
                    break

        # Fallback to default location or Chennai
        if not extracted_location:
            extracted_location = default_location or "Chennai"

        # 2. Extract Temporal Dimensions (Date & Time Period)
        date_entity = "today"
        time_period = "current"
        for key, value in self.time_aliases.items():
            if key in text_lower:
                date_entity = value
                break

        if date_entity == "today" and ("day after tomorrow" in text_lower or "மறுநாள்" in text_lower or "दो दिन बाद" in text_lower):
            date_entity = "day after tomorrow"
        elif date_entity == "today" and ("tomorrow" in text_lower or "நாளை" in text_lower or "कल" in text_lower or "రేపు" in text_lower):
            date_entity = "tomorrow"
        elif "yesterday" in text_lower:
            date_entity = "yesterday"
        elif "this week" in text_lower or "next week" in text_lower or "வாரம்" in text_lower or "सप्ताह" in text_lower:
            date_entity = "week"
        elif "last year" in text_lower or "last july" in text_lower or "20 years" in text_lower or "past" in text_lower:
            date_entity = "historical"

        if "morning" in text_lower:
            time_period = "morning"
        elif "afternoon" in text_lower:
            time_period = "afternoon"
        elif "evening" in text_lower or "6 pm" in text_lower or "night" in text_lower:
            time_period = "evening"

        # 3. Detect Intent and Meteorological Variables
        intent = "general_weather_question"
        variables: List[str] = []

        rain_signal = any(w in text_lower for w in ["rain", "raining", "rainfall", "precipitation", "shower", "drizzle", "downpour"] + ["மழை", "மழை இருக்கா", "பொழிவு", "பொழிவு வருமா", "बारिश", "बरसात", "वर्षा", "वृष्टि", "వర్షం", "మഴ", "ಮಳೆ", "ಬৃষ্টি"])
        if extracted_secondary_location or "compare" in text_lower or "comparison" in text_lower:
            intent = "comparison"
            variables.extend(["temperature", "precipitation", "wind"])

        elif any(w in text_lower for w in ["cyclone", "depression", "storm", "typhoon"]):
            intent = "cyclone"
            variables.append("wind")

        elif rain_signal:
            intent = "rainfall" if date_entity == "today" else "forecast"
            variables.append("precipitation")

        elif any(w in text_lower for w in ["alert", "warning", "bulletin", "severe", "danger", "hazard"]):
            intent = "weather_alert"

        elif any(w in text_lower for w in ["farmer", "farming", "crop", "agriculture", "irrigation", "spray"]):
            intent = "agriculture_advisory"

        elif any(w in text_lower for w in ["travel", "driving", "flight", "road", "trip"]):
            intent = "travel_advisory"

        elif any(w in text_lower for w in ["marine", "fisherman", "fishermen", "sea", "wave", "ocean", "coastal"]):
            intent = "marine_advisory"

        elif any(w in text_lower for w in ["aviation", "pilot", "runway", "crosswind", "turbul"]):
            intent = "aviation_weather"

        elif any(w in text_lower for w in ["hotter", "colder", "trend", "20 years", "climate", "global warming", "last 20", "hottest year"]):
            intent = "climate_analysis"
            variables.append("temperature")

        elif any(w in text_lower for w in ["last july", "historical", "last month", "last year", "in 20", "what was the rainfall"]):
            intent = "historical_weather"
            variables.append("precipitation")

        elif any(w in text_lower for w in ["wind", "gust", "breeze"]):
            intent = "wind"
            variables.append("wind")

        elif any(w in text_lower for w in ["temp", "temperature", "heat", "hot", "cold"]):
            intent = "temperature"
            variables.append("temperature")

        elif any(w in text_lower for w in ["humidity", "humid", "moisture"]):
            intent = "humidity"
            variables.append("humidity")

        elif any(w in text_lower for w in ["pressure", "barometer", "hpa"]):
            intent = "pressure"
            variables.append("pressure")

        elif any(w in text_lower for w in ["air quality", "aqi", "pollution"]):
            intent = "air_quality"

        elif any(w in text_lower for w in ["tomorrow", "week", "forecast", "future", "upcoming", "day after"]):
            intent = "forecast"
            variables.extend(["temperature", "precipitation"])

        elif any(w in text_lower for w in ["current", "now", "today", "weather"]):
            intent = "current_weather"
            variables.extend(["temperature", "humidity", "wind", "precipitation"])

        return {
            "intent": intent,
            "location": extracted_location,
            "secondary_location": extracted_secondary_location,
            "date": date_entity,
            "time_period": time_period,
            "variables": variables,
            "raw_query": text
        }

query_engine = NaturalLanguageQueryEngine()
