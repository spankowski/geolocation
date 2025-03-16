# services.py
import requests
from core.config import get_settings

import aiohttp
from core.config import get_settings
import socket
from urllib.parse import urlparse


def get_ip_from_domain(domain):
    try:
        parsed_url = urlparse(domain)
        domain = parsed_url.netloc if parsed_url.netloc else parsed_url.path
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror:
        return None


def get_domain_from_ip(ip_address: str) -> str:
    try:
        domain, _, _ = socket.gethostbyaddr(ip_address)
        return domain
    except socket.herror:
        return f"No domain found for IP {ip_address}"


async def fetch_geolocation(ip: str, domain: str | None = None):
    url = f"http://api.ipstack.com/{ip}?access_key={get_settings().IPSTACK_API_KEY}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return None
            data = await response.json()
            print(data)
            return {
                "ip": data.get("ip"),
                "url": domain if domain else get_domain_from_ip(ip_address=data.get("ip")),
                "country": data.get("country_name"),
                "city": data.get("city"),
                "latitude": str(data.get("latitude")),
                "longitude": str(data.get("longitude")),
            }
