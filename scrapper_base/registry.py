from __future__ import annotations

from typing import Callable

from scrapper_base.scrapers.ansm import AnsmScraper
from scrapper_base.scrapers.drugbank import DrugBankScraper
from scrapper_base.scrapers.has import HasScraper
from scrapper_base.scrapers.theriaque import TheriaqueScraper
from scrapper_base.scrapers.vidal import VidalScraper

SCRAPER_REGISTRY: dict[str, Callable[[], object]] = {
    "ansm": AnsmScraper,
    "has": HasScraper,
    "theriaque": TheriaqueScraper,
    "drugbank": DrugBankScraper,
    "vidal": VidalScraper,
}


def available_sites() -> list[str]:
    return sorted(SCRAPER_REGISTRY.keys())


def build_scraper(site: str):
    if site not in SCRAPER_REGISTRY:
        raise ValueError(f"Site inconnu: {site}")
    return SCRAPER_REGISTRY[site]()

