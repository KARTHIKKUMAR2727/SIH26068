from typing import Dict, Any, List
from datetime import datetime, timezone
import io
import csv

class WeatherReportEngine:
    def generate_daily_report(self, location_name: str, current: Dict[str, Any], forecast: Dict[str, Any], alerts: List[Dict[str, Any]]) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        temp = current.get("temperature", {})
        daily = forecast.get("daily", [])
        today_f = daily[0] if daily else {}

        summary = (
            f"Daily meteorological summary for {location_name}: Today recorded a current temperature of {temp.get('current')}°C "
            f"(feels like {temp.get('feels_like')}°C) with {current.get('condition')}. Humidity was {current.get('humidity', {}).get('value')}% "
            f"with winds sustained at {current.get('wind', {}).get('speed')} km/h. "
            f"Precipitation probability is {today_f.get('rain_probability', 0)}% with {today_f.get('precipitation_sum_mm', 0.0)} mm expected."
        )

        return {
            "report_id": f"REP-DAILY-{now.strftime('%Y%m%d%H%M')}",
            "type": "Daily Weather Report",
            "location": location_name,
            "period": now.strftime("%Y-%m-%d"),
            "generated_at": now.isoformat(),
            "summary": summary,
            "observations": {
                "temperature": f"{temp.get('current')}°C",
                "feels_like": f"{temp.get('feels_like')}°C",
                "max_temp": f"{today_f.get('temp_max', temp.get('current'))}°C",
                "min_temp": f"{today_f.get('temp_min', temp.get('current'))}°C",
                "humidity": f"{current.get('humidity', {}).get('value')}%",
                "wind": f"{current.get('wind', {}).get('speed')} km/h",
                "pressure": f"{current.get('pressure', {}).get('value')} hPa",
                "condition": current.get("condition")
            },
            "active_alerts_count": len(alerts),
            "alerts": alerts,
            "sources": [current.get("source", {}).get("source", "Open-Meteo WMO Network")]
        }

    def export_csv(self, report_data: Dict[str, Any]) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Report Title", report_data.get("type")])
        writer.writerow(["Location", report_data.get("location")])
        writer.writerow(["Generated Timestamp", report_data.get("generated_at")])
        writer.writerow([])
        writer.writerow(["Parameter", "Value"])
        for k, v in report_data.get("observations", {}).items():
            writer.writerow([k.replace("_", " ").title(), v])
        return output.getvalue()

report_engine = WeatherReportEngine()
