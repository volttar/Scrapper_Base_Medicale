from __future__ import annotations

from typing import Any

from scrapper_base.config import RateLimit, SiteConfig
from scrapper_base.fetcher import AsyncFetcher
from scrapper_base.parsers.common import parse_basic_page
from scrapper_base.scrapers.base import BaseScraper


class AnsmScraper(BaseScraper):
    name = "ansm"

    def __init__(self) -> None:
        super().__init__(
            SiteConfig(
                name=self.name,
                base_url="https://ansm.sante.fr",
                rate_limit=RateLimit(requests_per_second=0.5),
            )
        )

    def start_urls(self) -> list[str]:
        return ["https://ansm.sante.fr"]

    async def scrape(self, fetcher: AsyncFetcher) -> list[dict[str, Any]]:
        results = []
        async for response in fetcher.fetch_many(self.start_urls()):
            results.append(parse_basic_page(response.content, response.url))
        return results

