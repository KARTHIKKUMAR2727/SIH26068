from typing import Dict, Any

METEOROLOGICAL_DICTIONARY: Dict[str, Dict[str, str]] = {
    "ta": {  # Tamil
        "current_weather": "தற்போதைய வானிலை",
        "temperature": "வெப்பநிலை",
        "feels_like": "உணரப்படும் வெப்பநிலை",
        "humidity": "ஈரப்பதம்",
        "wind": "காற்று வேகம்",
        "pressure": "வளிமண்டல அழுத்தம்",
        "rain_probability": "மழைக்கான வாய்ப்பு",
        "precipitation": "மழை அளவு",
        "condition": "வானிலை நிலை",
        "alert": "வானிலை எச்சரிக்கை",
        "forecast": "வானிலை முன்னறிவிப்பு",
        "tomorrow": "நாளை",
        "advisory": "பரிந்துரை",
        "clear_sky": "தெளிவான வானம்",
        "heavy_rain": "கனமழை",
        "thunderstorm": "இடி மின்னலுடன் கூடிய மழை",
        "heatwave": "வெப்ப அலை",
        "source": "தகவல் ஆதாரம்",
        "official_warning": "அதிகாரப்பூர்வ எச்சரிக்கை",
        "ai_insight": "AI வானிலை நுண்ணறிவு"
    },
    "hi": {  # Hindi
        "current_weather": "वर्तमान मौसम",
        "temperature": "तापमान",
        "feels_like": "महसूस होने वाला तापमान",
        "humidity": "नमी (आर्द्रता)",
        "wind": "हवा की गति",
        "pressure": "वायुमंडलीय दबाव",
        "rain_probability": "बारिश की संभावना",
        "precipitation": "वर्षा",
        "condition": "मौसम की स्थिति",
        "alert": "मौसम चेतावनी",
        "forecast": "मौसम पूर्वानुमान",
        "tomorrow": "कल",
        "advisory": "परामर्श",
        "clear_sky": "साफ आसमान",
        "heavy_rain": "भारी बारिश",
        "thunderstorm": "गरज के साथ बारिश",
        "heatwave": "लू (हीटवेव)",
        "source": "डेटा स्रोत",
        "official_warning": "आधिकारिक चेतावनी",
        "ai_insight": "एआई मौसम अंतर्दृष्टि"
    },
    "te": {  # Telugu
        "current_weather": "ప్రస్తుత వాతావరణం",
        "temperature": "ఉష్ణోగ్రత",
        "feels_like": "అనిపించే ఉష్ణోగ్రత",
        "humidity": "తేమ",
        "wind": "గాలి వేగం",
        "pressure": "పీడనం",
        "rain_probability": "వర్ష సూచన సంభావ్యత",
        "precipitation": "వర్షపాతం",
        "condition": "వాతావరణ పరిస్థితి",
        "alert": "వాతావరణ హెచ్చరిక",
        "forecast": "వాతావరణ అంచనా",
        "tomorrow": "రేపు",
        "advisory": "సలహా",
        "clear_sky": "నిర్మలమైన ఆకాశం",
        "heavy_rain": "భారీ వర్షం",
        "thunderstorm": "ఉరుములతో కూడిన వర్షం",
        "heatwave": "వడగాల్పులు",
        "source": "సమాచార మూలం",
        "official_warning": "అధికారిక హెచ్చరిక",
        "ai_insight": "AI వాతావరణ విశ్లేషణ"
    },
    "ml": {  # Malayalam
        "current_weather": "നിലവിലെ കാലാവസ്ഥ",
        "temperature": "താപനില",
        "feels_like": "അനുഭവപ്പെടുന്ന ചൂട്",
        "humidity": "ആർദ്രത",
        "wind": "കാറ്റിന്റെ വേഗത",
        "pressure": "വായു മർദ്ദം",
        "rain_probability": "മഴ സാധ്യത",
        "precipitation": "മഴയുടെ അളവ്",
        "condition": "കാലാവസ്ഥാവസ്ഥ",
        "alert": "കാലാവസ്ഥ മുന്നറിയിപ്പ്",
        "forecast": "കാലാവസ്ഥാ പ്രവചനം",
        "tomorrow": "നാളെ",
        "advisory": "നിർദ്ദേശം",
        "clear_sky": "തെളിഞ്ഞ ആകാശം",
        "heavy_rain": "കനത്ത മഴ",
        "thunderstorm": "ഇടിമിന്നലോട് കൂടിയ മഴ",
        "heatwave": "ഉഷ്ണതരംഗം",
        "source": "വിവര സ്രോതസ്സ്",
        "official_warning": "ഔദ്യോഗിക മുന്നറിയിപ്പ്",
        "ai_insight": "AI കാലാവസ്ഥ ഉൾക്കാഴ്ച"
    },
    "kn": {  # Kannada
        "current_weather": "ಪ್ರಸ್ತುತ ಹವಾಮಾನ",
        "temperature": "ತಾಪಮಾನ",
        "feels_like": "ಅನುಭವವಾಗುವ ತಾಪಮಾನ",
        "humidity": "ಆರ್ದ್ರತೆ",
        "wind": "ಗಾಳಿಯ ವೇಗ",
        "pressure": "ವಾತಾವರಣದ ಒತ್ತಡ",
        "rain_probability": "ಮಳೆಯ ಸಂಭವನೀಯತೆ",
        "precipitation": "ಮಳೆ ಪ್ರಮಾಣ",
        "condition": "ಹವಾಮಾನ ಸ್ಥಿತಿ",
        "alert": "ಹವಾಮಾನ ಎಚ್ಚರಿಕೆ",
        "forecast": "ಹವಾಮಾನ ಮುನ್ಸೂಚನೆ",
        "tomorrow": "ನಾಳೆ",
        "advisory": "ಸಲಹೆ",
        "clear_sky": "ಸ್ವಚ್ಛ ಆಕಾಶ",
        "heavy_rain": "ಭಾರೀ ಮಳೆ",
        "thunderstorm": "ಗುಡುಗು ಸಹಿತ ಮಳೆ",
        "heatwave": "ಬಿಸಿಗಾಳಿ",
        "source": "ಮಾಹಿತಿ ಮೂಲ",
        "official_warning": "ಅಧಿಕೃತ ಎಚ್ಚರಿಕೆ",
        "ai_insight": "AI ಹವಾಮಾನ ಒಳನೋಟ"
    },
    "bn": {  # Bengali
        "current_weather": "বর্তমান আবহাওয়া",
        "temperature": "তাপমাত্রা",
        "feels_like": "অনুভূত তাপমাত্রা",
        "humidity": "আর্দ্রতা",
        "wind": "বাতাসের গতি",
        "pressure": "বায়ুচাপ",
        "rain_probability": "বৃষ্টির সম্ভাবনা",
        "precipitation": "বৃষ্টিপাত",
        "condition": "আবহাওয়ার অবস্থা",
        "alert": "আবহাওয়া সতর্কতা",
        "forecast": "আবহাওয়ার পূর্বাভাস",
        "tomorrow": "আগামীকাল",
        "advisory": "পরামর্শ",
        "clear_sky": "পরিষ্কার আকাশ",
        "heavy_rain": "ভারী বৃষ্টি",
        "thunderstorm": "বজ্রবিদ্যুৎ সহ বৃষ্টি",
        "heatwave": "দাবদাহ",
        "source": "উৎস",
        "official_warning": "সরকারী সতর্কতা",
        "ai_insight": "এআই আবহাওয়া অন্তর্দৃষ্টি"
    },
    "mr": {  # Marathi
        "current_weather": "सध्याचे हवामान",
        "temperature": "तापमान",
        "feels_like": "जाणवणारे तापमान",
        "humidity": "हवेतील आर्द्रता",
        "wind": "वाऱ्याचा वेग",
        "pressure": "हवेचा दाब",
        "rain_probability": "पावसाची शक्यता",
        "precipitation": "पाऊस",
        "condition": "हवामानाची स्थिती",
        "alert": "हवामान इशारा",
        "forecast": "हवामान अंदाज",
        "tomorrow": "उद्या",
        "advisory": "सल्ला",
        "clear_sky": "निरभ्र आकाश",
        "heavy_rain": "मुसळधार पाऊस",
        "thunderstorm": "वादळी पाऊस",
        "heatwave": "उष्णतेची लाट",
        "source": "माहिती स्रोत",
        "official_warning": "अधिकृत इशारा",
        "ai_insight": "एआय हवामान निरीक्षण"
    },
    "en": {
        "current_weather": "Current Weather",
        "temperature": "Temperature",
        "feels_like": "Feels like",
        "humidity": "Humidity",
        "wind": "Wind",
        "pressure": "Pressure",
        "rain_probability": "Rain Probability",
        "precipitation": "Precipitation",
        "condition": "Condition",
        "alert": "Weather Alert",
        "forecast": "Forecast",
        "tomorrow": "Tomorrow",
        "advisory": "Advisory",
        "clear_sky": "Clear Sky",
        "heavy_rain": "Heavy Rain",
        "thunderstorm": "Thunderstorm",
        "heatwave": "Heatwave",
        "source": "Data Source",
        "official_warning": "Official Warning",
        "ai_insight": "AI Weather Insight"
    }
}

class LanguageProvider:
    SUPPORTED_LANGUAGES = {
        "en": "English",
        "ta": "தமிழ் (Tamil)",
        "hi": "हिन्दी (Hindi)",
        "te": "తెలుగు (Telugu)",
        "ml": "മലയാളം (Malayalam)",
        "kn": "ಕನ್ನಡ (Kannada)",
        "bn": "বাংলা (Bengali)",
        "mr": "मराठी (Marathi)"
    }

    @classmethod
    def get_term(cls, lang: str, key: str) -> str:
        lang_dict = METEOROLOGICAL_DICTIONARY.get(lang.lower(), METEOROLOGICAL_DICTIONARY["en"])
        return lang_dict.get(key, METEOROLOGICAL_DICTIONARY["en"].get(key, key))

    @classmethod
    def format_weather_response(cls, lang: str, loc_name: str, temp: float, feels: float, condition: str, humidity: int, wind: float, rain_prob: int, source_name: str) -> str:
        lang = lang.lower()
        t = lambda k: cls.get_term(lang, k)

        if lang == "ta":
            return (
                f"{loc_name} - {t('current_weather')}\n\n"
                f"{t('temperature')}: {temp}°C ({t('feels_like')}: {feels}°C)\n"
                f"{t('condition')}: {condition}\n"
                f"{t('humidity')}: {humidity}%\n"
                f"{t('wind')}: {wind} km/h\n"
                f"{t('rain_probability')}: {rain_prob}%"
            )
        elif lang == "hi":
            return (
                f"{loc_name} - {t('current_weather')}\n\n"
                f"{t('temperature')}: {temp}°C ({t('feels_like')}: {feels}°C)\n"
                f"{t('condition')}: {condition}\n"
                f"{t('humidity')}: {humidity}%\n"
                f"{t('wind')}: {wind} km/h\n"
                f"{t('rain_probability')}: {rain_prob}%"
            )
        elif lang == "te":
            return (
                f"{loc_name} - {t('current_weather')}\n\n"
                f"{t('temperature')}: {temp}°C ({t('feels_like')}: {feels}°C)\n"
                f"{t('condition')}: {condition}\n"
                f"{t('humidity')}: {humidity}%\n"
                f"{t('wind')}: {wind} km/h\n"
                f"{t('rain_probability')}: {rain_prob}%"
            )
        elif lang == "ml":
            return (
                f"{loc_name} - {t('current_weather')}\n\n"
                f"{t('temperature')}: {temp}°C ({t('feels_like')}: {feels}°C)\n"
                f"{t('condition')}: {condition}\n"
                f"{t('humidity')}: {humidity}%\n"
                f"{t('wind')}: {wind} km/h\n"
                f"{t('rain_probability')}: {rain_prob}%"
            )
        elif lang == "kn":
            return (
                f"{loc_name} - {t('current_weather')}\n\n"
                f"{t('temperature')}: {temp}°C ({t('feels_like')}: {feels}°C)\n"
                f"{t('condition')}: {condition}\n"
                f"{t('humidity')}: {humidity}%\n"
                f"{t('wind')}: {wind} km/h\n"
                f"{t('rain_probability')}: {rain_prob}%"
            )
        elif lang == "bn":
            return (
                f"{loc_name} - {t('current_weather')}\n\n"
                f"{t('temperature')}: {temp}°C ({t('feels_like')}: {feels}°C)\n"
                f"{t('condition')}: {condition}\n"
                f"{t('humidity')}: {humidity}%\n"
                f"{t('wind')}: {wind} km/h\n"
                f"{t('rain_probability')}: {rain_prob}%"
            )
        elif lang == "mr":
            return (
                f"{loc_name} - {t('current_weather')}\n\n"
                f"{t('temperature')}: {temp}°C ({t('feels_like')}: {feels}°C)\n"
                f"{t('condition')}: {condition}\n"
                f"{t('humidity')}: {humidity}%\n"
                f"{t('wind')}: {wind} km/h\n"
                f"{t('rain_probability')}: {rain_prob}%"
            )
        else:
            return (
                f"{loc_name} - Current Weather\n\n"
                f"Temperature: {temp}°C (Feels like: {feels}°C)\n"
                f"Condition: {condition}\n"
                f"Humidity: {humidity}%\n"
                f"Wind: {wind} km/h\n"
                f"Rain Probability: {rain_prob}%"
            )

language_provider = LanguageProvider()
