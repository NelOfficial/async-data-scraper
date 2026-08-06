import asyncio
import logging
from typing import List, Dict, Any, Optional
import aiohttp
from config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class AsyncFetcher:
    def __init__(self, max_concurrent_requests: int = settings.MAX_CONCURRENT_REQUESTS, timeout_seconds: int = settings.TIMEOUT_SECONDS):
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)
        self.timeout = aiohttp.ClientTimeout(total=timeout_seconds)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*"
        }

    async def fetch_url(self, session: aiohttp.ClientSession, url: str) -> Optional[Dict[str, Any]]:
        async with self.semaphore:
            try:
                async with session.get(url, timeout=self.timeout) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 429:
                        logging.warning(f"rate-limi on {url}")
                        return None
                    else:
                        logging.warning(f"access err {url}: status {response.status}")
                        return None
            except asyncio.TimeoutError:
                logging.error(f"timeout {url}")
                return None
            except Exception as e:
                logging.error(f"requiest err {url}: {str(e)}")
                return None

    async def fetch_all(self, urls: List[str]) -> List[Optional[Dict[str, Any]]]:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            tasks = [self.fetch_url(session, url) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return results


async def main():
    test_urls = [f"https://jsonplaceholder.typicode.com/posts/{i}" for i in range(1, 11)]

    fetcher = AsyncFetcher(max_concurrent_requests=3, timeout_seconds=5)
    logging.info("starting...")
    
    data = await fetcher.fetch_all(test_urls)
    
    # фильтруем успешные ответы
    valid_data = [item for item in data if isinstance(item, dict)]
    logging.info(f"objs successfully collected: {len(valid_data)} from {len(test_urls)}")
    
    # вывод первого объекта для проверки структуры
    if valid_data:
        print("object example:", valid_data[0])

if __name__ == "__main__":
    asyncio.run(main())