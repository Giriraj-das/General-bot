import aiohttp

from config import settings


async def get_weather(latitude: str, longitude: str):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;\q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'current': 'temperature_2m,precipitation,relative_humidity_2m,rain,wind_direction_10m,wind_speed_10m',
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=settings.weather.url,
            headers=headers,
            params=params,
            timeout=aiohttp.ClientTimeout(total=3),
        ) as response:
            return await response.json()
