# services.py
import requests
from core.config import get_settings

def fetch_geolocation(ip_or_url: str):
    url = f"http://api.ipstack.com/{ip_or_url}?access_key={get_settings().IPSTACK_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    return {
        "ip": data.get("ip"),
        "url": ip_or_url if "." in ip_or_url else None,
        "country": data.get("country_name"),
        "city": data.get("city"),
        "latitude": str(data.get("latitude")),
        "longitude": str(data.get("longitude")),
    }