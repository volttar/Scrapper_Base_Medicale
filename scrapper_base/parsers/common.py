from __future__ import annotations

from bs4 import BeautifulSoup


def parse_basic_page(html: bytes, url: str) -> dict[str, str | list[str]]:
    soup = BeautifulSoup(html, "lxml")
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    links = [a.get("href") for a in soup.select("a[href]")]
    return {
        "url": url,
        "title": title,
        "links": [link for link in links if link],
    }

