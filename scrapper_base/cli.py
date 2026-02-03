from __future__ import annotations

import argparse
import asyncio

from scrapper_base.pipeline import ScrapePipeline
from scrapper_base.registry import available_sites, build_scraper
from scrapper_base.storage import JsonlStorage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scrapper Base Médicale")
    parser.add_argument(
        "--site",
        action="append",
        required=True,
        help="Site à scraper (ex: ansm, has, theriaque, drugbank, vidal)",
    )
    parser.add_argument(
        "--output",
        default="output/data.jsonl",
        help="Chemin de sortie JSONL",
    )
    parser.add_argument(
        "--list-sites",
        action="store_true",
        help="Afficher les sites disponibles",
    )
    return parser


async def run_scrapers(sites: list[str], output: str) -> None:
    scrapers = [build_scraper(site) for site in sites]
    pipeline = ScrapePipeline(scrapers)
    results = await pipeline.run()
    storage = JsonlStorage(output)
    for site_name, items in results.items():
        tagged = [dict(item, source=site_name) for item in items]
        storage.write(tagged)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.list_sites:
        print("\n".join(available_sites()))
        return

    asyncio.run(run_scrapers(args.site, args.output))


if __name__ == "__main__":
    main()

