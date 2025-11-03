from typing import List, Dict, Optional
import asyncio, aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import async_timeout

DEFAULT_HEADERS = {"User-Agent": "webscraper-work-sample/1.0 (+https://github.com/yourname)"}

async def fetch_url(session: ClientSession, url: str, timeout: int = 10) -> Optional[str]:
    try:
        async with async_timeout.timeout(timeout):
            async with session.get(url) as resp:
                resp.raise_for_status()
                return await resp.text()
    except:
        return None

def parse_title_and_links(html: str) -> Dict:
    soup = BeautifulSoup(html, "lxml")
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    links = [a["href"] for a in soup.find_all("a", href=True)]
    return {"title": title, "links": links}

async def scrape(urls: List[str], concurrency: int = 5, timeout: int = 10, retries: int = 2) -> List[Dict]:
    connector = aiohttp.TCPConnector(limit_per_host=concurrency)
    results = []
    async with aiohttp.ClientSession(headers=DEFAULT_HEADERS, connector=connector) as session:
        sem = asyncio.Semaphore(concurrency)
        async def _worker(u: str):
            for _ in range(retries + 1):
                async with sem:
                    html = await fetch_url(session, u, timeout)
                if html:
                    parsed = parse_title_and_links(html)
                    parsed["url"] = u
                    return parsed
                await asyncio.sleep(1)
            return {"url": u, "title": "", "links": []}
        tasks = [asyncio.create_task(_worker(u)) for u in urls]
        for t in asyncio.as_completed(tasks):
            results.append(await t)
    return results
