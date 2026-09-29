import httpx
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

# Curated high-accuracy Indian & global locations database for fast lookup and offline resilience
INDIAN_CITIES_REGISTRY: List[Dict[str, Any]] = [
    {"name": "Chennai", "state": "Tamil Nadu", "country": "India", "latitude": 13.0827, "longitude": 80.2707},
    {"name": "Madurai", "state": "Tamil Nadu", "country": "India", "latitude": 9.9252, "longitude": 78.1198},
    {"name": "Sivakasi", "state": "Tamil Nadu", "country": "India", "latitude": 9.4533, "longitude": 77.7972},
    {"name": "Coimbatore", "state": "Tamil Nadu", "country": "India", "latitude": 11.0168, "longitude": 76.9558},
    {"name": "Tiruchirappalli", "state": "Tamil Nadu", "country": "India", "latitude": 10.7905, "longitude": 78.7047},
    {"name": "Salem", "state": "Tamil Nadu", "country": "India", "latitude": 11.6643, "longitude": 78.1460},
    {"name": "Tirunelveli", "state": "Tamil Nadu", "country": "India", "latitude": 8.7139, "longitude": 77.7567},
    {"name": "Kanyakumari", "state": "Tamil Nadu", "country": "India", "latitude": 8.0883, "longitude": 77.5385},
    {"name": "Bengaluru", "state": "Karnataka", "country": "India", "latitude": 12.9716, "longitude": 77.5946},
    {"name": "Hyderabad", "state": "Telangana", "country": "India", "latitude": 17.3850, "longitude": 78.4867},
    {"name": "Mumbai", "state": "Maharashtra", "country": "India", "latitude": 19.0760, "longitude": 72.8777},
    {"name": "Pune", "state": "Maharashtra", "country": "India", "latitude": 18.5204, "longitude": 73.8567},
    {"name": "New Delhi", "state": "Delhi", "country": "India", "latitude": 28.6139, "longitude": 77.2090},
    {"name": "Delhi", "state": "Delhi", "country": "India", "latitude": 28.6139, "longitude": 77.2090},
    {"name": "Kolkata", "state": "West Bengal", "country": "India", "latitude": 22.5726, "longitude": 88.3639},
    {"name": "Kochi", "state": "Kerala", "country": "India", "latitude": 9.9312, "longitude": 76.2673},
    {"name": "Thiruvananthapuram", "state": "Kerala", "country": "India", "latitude": 8.5241, "longitude": 76.9366},
    {"name": "Visakhapatnam", "state": "Andhra Pradesh", "country": "India", "latitude": 17.6868, "longitude": 83.2185},
    {"name": "Vijayawada", "state": "Andhra Pradesh", "country": "India", "latitude": 16.5062, "longitude": 80.6480},
    {"name": "Ahmedabad", "state": "Gujarat", "country": "India", "latitude": 23.0225, "longitude": 72.5714},
    {"name": "Jaipur", "state": "Rajasthan", "country": "India", "latitude": 26.9124, "longitude": 75.7873},
    {"name": "Lucknow", "state": "Uttar Pradesh", "country": "India", "latitude": 26.8467, "longitude": 80.9462},
    {"name": "Bhopal", "state": "Madhya Pradesh", "country": "India", "latitude": 23.2599, "longitude": 77.4126},
    {"name": "Patna", "state": "Bihar", "country": "India", "latitude": 25.5941, "longitude": 85.1376},
    {"name": "Bhubaneswar", "state": "Odisha", "country": "India", "latitude": 20.2961, "longitude": 85.8245},
    {"name": "Guwahati", "state": "Assam", "country": "India", "latitude": 26.1445, "longitude": 91.7362},
    {"name": "London", "state": "England", "country": "United Kingdom", "latitude": 51.5074, "longitude": -0.1278},
    {"name": "New York", "state": "New York", "country": "United States", "latitude": 40.7128, "longitude": -74.0060},
    {"name": "Tokyo", "state": "Tokyo", "country": "Japan", "latitude": 35.6762, "longitude": 139.6503},
    {"name": "Singapore", "state": "Singapore", "country": "Singapore", "latitude": 1.3521, "longitude": 103.8198}
]

class BaseGeocodingProvider(ABC):
    @abstractmethod
    async def search(self, query: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def reverse(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        pass


class OpenMeteoGeocodingProvider(BaseGeocodingProvider):
    def __init__(self):
        self.api_url = "https://geocoding-api.open-meteo.com/v1/search"

    async def search(self, query: str) -> List[Dict[str, Any]]:
        q = query.strip().lower()
        if not q:
            return []

        # Check local registry first for high-speed instant match
        local_matches = [
            city for city in INDIAN_CITIES_REGISTRY
            if q in city["name"].lower() or (city["state"] and q in city["state"].lower())
        ]

        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                res = await client.get(self.api_url, params={"name": query, "count": 10, "language": "en", "format": "json"})
                if res.status_code == 200:
                    data = res.json()
                    results = data.get("results", [])
                    if results:
                        formatted = []
                        for item in results:
                            formatted.append({
                                "name": item.get("name"),
                                "state": item.get("admin1"),
                                "country": item.get("country"),
                                "latitude": item.get("latitude"),
                                "longitude": item.get("longitude"),
                                "country_code": item.get("country_code"),
                                "timezone": item.get("timezone", "Asia/Kolkata")
                            })
                        return formatted
        except Exception as e:
            print(f"External geocoding error: {e}, falling back to local registry.")

        # Return local registry matches if available
        if local_matches:
            return local_matches

        # Default fallback to Chennai if nothing matched
        return [INDIAN_CITIES_REGISTRY[0]]

    async def reverse(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        # Find closest city in registry
        closest = None
        min_dist = float("inf")
        for city in INDIAN_CITIES_REGISTRY:
            dist = (city["latitude"] - lat) ** 2 + (city["longitude"] - lon) ** 2
            if dist < min_dist:
                min_dist = dist
                closest = city
        return closest or {"name": f"Location ({lat:.2f}, {lon:.2f})", "latitude": lat, "longitude": lon, "country": "India"}


geocoding_provider = OpenMeteoGeocodingProvider()
