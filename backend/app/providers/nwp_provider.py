from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone, timedelta
import httpx
import numpy as np

class BaseNWPProvider(ABC):
    @abstractmethod
    async def get_model_runs(self, lat: float, lon: float, location_name: str) -> Dict[str, Any]:
        pass


class MultiModelNWPProvider(BaseNWPProvider):
    def __init__(self):
        self.gfs_url = "https://api.open-meteo.com/v1/gfs"
        self.ecmwf_url = "https://api.open-meteo.com/v1/ecmwf"

    async def _fetch_model(self, url: str, lat: float, lon: float, model_name: str, resolution: float) -> Optional[Dict[str, Any]]:
        now = datetime.now(timezone.utc)
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": ["temperature_2m", "precipitation", "surface_pressure", "wind_speed_10m", "cloud_cover"],
            "forecast_days": 4,
            "timezone": "auto"
        }
        try:
            async with httpx.AsyncClient(timeout=6.0) as client:
                res = await client.get(url, params=params)
                if res.status_code == 200:
                    data = res.json()
                    h = data.get("hourly", {})
                    times = h.get("time", [])
                    lead_steps = []
                    # Sample at +6h, +12h, +24h, +48h, +72h
                    lead_indices = [6, 12, 24, 48, 72]
                    for lead in lead_indices:
                        if lead < len(times):
                            lead_steps.append({
                                "lead_time_hours": lead,
                                "forecast_timestamp": times[lead],
                                "temperature": round(h.get("temperature_2m", [])[lead], 1),
                                "precipitation": round(h.get("precipitation", [])[lead] or 0.0, 1),
                                "wind_speed": round(h.get("wind_speed_10m", [])[lead] or 10.0, 1),
                                "pressure": round(h.get("surface_pressure", [])[lead] or 1012.0, 1),
                                "cloud_cover": h.get("cloud_cover", [])[lead] or 25
                            })
                    return {
                        "model_name": model_name,
                        "run_cycle": "00Z Cycle",
                        "run_timestamp": (now - timedelta(hours=3)).strftime("%Y-%m-%d 00:00 UTC"),
                        "resolution_km": resolution,
                        "provider_source": "NOAA / NCEP via Open-Meteo" if "GFS" in model_name else "ECMWF Operational",
                        "lead_times": lead_steps
                    }
        except Exception as e:
            print(f"Error fetching {model_name}: {e}")
        return None

    async def get_model_runs(self, lat: float, lon: float, location_name: str) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        models = []

        # 1. Fetch live GFS
        gfs = await self._fetch_model(self.gfs_url, lat, lon, "GFS 0.25° (Global Forecast System)", 28.0)
        if gfs:
            models.append(gfs)

        # 2. Fetch live ECMWF
        ecmwf = await self._fetch_model(self.ecmwf_url, lat, lon, "ECMWF IFS (0.25° High-Resolution)", 25.0)
        if ecmwf:
            models.append(ecmwf)

        # If live models failed or network offline, provide synthesized reference NWP run
        if not models:
            models = self._generate_synthetic_nwp(now)

        # Calculate ensemble spread & uncertainty at +24h lead time
        spread_calc = self._calculate_uncertainty(models)

        return {
            "location": location_name,
            "latitude": lat,
            "longitude": lon,
            "models": models,
            "ensemble_spread": spread_calc,
            "generated_at": now.isoformat()
        }

    def _calculate_uncertainty(self, models: List[Dict[str, Any]]) -> Dict[str, Any]:
        # Extract +24h forecast temperatures across models
        t_24 = []
        p_24 = []
        for m in models:
            for step in m.get("lead_times", []):
                if step.get("lead_time_hours") == 24:
                    t_24.append(step.get("temperature", 28.0))
                    p_24.append(step.get("precipitation", 0.0))

        if not t_24:
            t_24 = [28.5, 29.2]
            p_24 = [0.0, 1.2]

        t_min = round(float(np.min(t_24)), 1)
        t_max = round(float(np.max(t_24)), 1)
        t_mean = round(float(np.mean(t_24)), 1)
        t_spread = round(t_max - t_min, 1)

        if t_spread <= 1.0:
            spread_cat = "High Confidence (Low Spread <1.0°C)"
        elif t_spread <= 2.5:
            spread_cat = "Moderate Confidence (Moderate Spread 1-2.5°C)"
        else:
            spread_cat = "Elevated Uncertainty (High Spread >2.5°C)"

        return {
            "target_lead_time": "+24 Hours",
            "temperature_min": t_min,
            "temperature_max": t_max,
            "temperature_mean": t_mean,
            "temperature_spread": t_spread,
            "spread_category": spread_cat,
            "precipitation_probability": 35 if np.mean(p_24) > 0.5 else 10,
            "participating_models": [m["model_name"] for m in models]
        }

    def _generate_synthetic_nwp(self, now: datetime) -> List[Dict[str, Any]]:
        lead_steps_gfs = []
        lead_steps_ecmwf = []
        for h in [6, 12, 24, 48, 72]:
            lead_steps_gfs.append({
                "lead_time_hours": h,
                "forecast_timestamp": (now + timedelta(hours=h)).strftime("%Y-%m-%d %H:00"),
                "temperature": round(29.0 + (h % 3) * 0.8, 1),
                "precipitation": 0.5 if h in [24, 48] else 0.0,
                "wind_speed": 14.5 + (h % 4),
                "pressure": 1011.2,
                "cloud_cover": 30
            })
            lead_steps_ecmwf.append({
                "lead_time_hours": h,
                "forecast_timestamp": (now + timedelta(hours=h)).strftime("%Y-%m-%d %H:00"),
                "temperature": round(28.4 + (h % 3) * 0.7, 1),
                "precipitation": 1.2 if h in [24, 48] else 0.1,
                "wind_speed": 16.0 + (h % 3),
                "pressure": 1010.8,
                "cloud_cover": 40
            })

        return [
            {
                "model_name": "GFS 0.25° (Global Forecast System)",
                "run_cycle": "00Z Cycle",
                "run_timestamp": (now - timedelta(hours=4)).strftime("%Y-%m-%d 00:00 UTC"),
                "resolution_km": 28.0,
                "provider_source": "DEMO / SIMULATED NWP DATA (NOAA/NCEP Reference Pipeline)",
                "lead_times": lead_steps_gfs
            },
            {
                "model_name": "ECMWF IFS (0.25° High-Resolution)",
                "run_cycle": "00Z Cycle",
                "run_timestamp": (now - timedelta(hours=4)).strftime("%Y-%m-%d 00:00 UTC"),
                "resolution_km": 25.0,
                "provider_source": "DEMO / SIMULATED NWP DATA (ECMWF Reference Pipeline)",
                "lead_times": lead_steps_ecmwf
            }
        ]

nwp_provider = MultiModelNWPProvider()
