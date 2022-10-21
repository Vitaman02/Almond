import aiohttp

async def get_host_usage(url: str) -> dict:
    """Get the current CPU, MEM and disk usage"""

    async with aiohttp.ClientSession() as session:
        resp = await session.get(url)
        data = await resp.json()
    return data
