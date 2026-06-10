"""Web scraper for sources without RSS feeds."""

import logging
import hashlib
from datetime import datetime, timezone
import requests
from bs4 import BeautifulSoup
from .sources_config import SCRAPE_SOURCES, GOOGLE_NEWS_QUERIES

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def scrape_page(source: dict) -> list[dict]:
    """Scrape news items from a single web page."""
    items = []
    try:
        resp = requests.get(source["url"], headers=HEADERS, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        logger.warning("Failed to scrape %s: %s", source["name"], e)
        return items

    elements = soup.select(source["selector"])
    for el in elements[:20]:
        title_el = el.find(["h1", "h2", "h3", "h4", "a"])
        link_el = el.find("a", href=True)

        title = title_el.get_text(strip=True) if title_el else ""
        url = link_el["href"] if link_el else ""
        if url and not url.startswith("http"):
            from urllib.parse import urljoin
            url = urljoin(source["url"], url)

        summary_el = el.find("p")
        summary = summary_el.get_text(strip=True) if summary_el else ""

        if title and url:
            items.append({
                "source_name": source["name"],
                "source_category": source["category"],
                "language": source["language"],
                "title": title,
                "url": url,
                "summary": summary,
                "published_at": datetime.now(timezone.utc).isoformat(),
                "raw_content": "",
            })

    logger.info("Scraped %d items from %s", len(items), source["name"])
    return items


def search_google_news(query: str) -> list[dict]:
    """Search Google News RSS for a query."""
    import urllib.parse
    encoded = urllib.parse.quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded}&hl=en-US&gl=US&ceid=US:en"

    import xml.etree.ElementTree as ET
    try:
        resp = requests.get(rss_url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        content = resp.content
        # Google News sometimes returns HTML — detect and skip
        if b"<html" in content[:200].lower():
            logger.warning("Google News returned HTML (blocked) for query: %s", query)
            return []
        root = ET.fromstring(content)
    except Exception as e:
        logger.warning("Google News search failed for '%s': %s", query, e)
        return []

    items = []
    for item_el in root.findall(".//item")[:10]:
        title = (item_el.findtext("title") or "").strip()
        url = (item_el.findtext("link") or "").strip()
        summary = (item_el.findtext("description") or "").strip()
        if title and url:
            items.append({
                "source_name": f"Google News: {query}",
                "source_category": "search",
                "language": "en",
                "title": title,
                "url": url,
                "summary": summary,
                "published_at": None,
                "raw_content": "",
            })
    return items


def collect_scraped_sources() -> list[dict]:
    """Collect from all scrape targets."""
    all_items = []
    for source in SCRAPE_SOURCES:
        all_items.extend(scrape_page(source))
    return all_items


def collect_google_news() -> list[dict]:
    """Collect Google News results for all configured queries."""
    all_items = []
    for query in GOOGLE_NEWS_QUERIES:
        all_items.extend(search_google_news(query))
    logger.info("Google News collected %d items", len(all_items))
    return all_items
