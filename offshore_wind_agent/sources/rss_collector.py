"""RSS feed collector — uses xml.etree.ElementTree (no feedparser dependency)."""

import logging
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from typing import Optional
import requests
from .sources_config import RSS_SOURCES

logger = logging.getLogger(__name__)

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc": "http://purl.org/dc/elements/1.1/",
}


def _text(el, *tags) -> str:
    for tag in tags:
        child = el.find(tag)
        if child is not None and child.text:
            return child.text.strip()
    return ""


def _parse_date(date_str: str) -> Optional[datetime]:
    if not date_str:
        return None
    for fmt in ("%a, %d %b %Y %H:%M:%S %z", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ"):
        try:
            return datetime.strptime(date_str.strip(), fmt).astimezone(timezone.utc)
        except Exception:
            pass
    try:
        return parsedate_to_datetime(date_str).astimezone(timezone.utc)
    except Exception:
        return None


def fetch_rss_feed(source: dict, cutoff_days: int = 7) -> list[dict]:
    cutoff = datetime.now(timezone.utc) - timedelta(days=cutoff_days)
    items = []

    headers = {"User-Agent": "OffshoreWindAgent/1.0 (+https://github.com/hyalineyy/me)"}
    try:
        resp = requests.get(source["url"], headers=headers, timeout=15)
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
    except Exception as e:
        logger.warning("Failed to fetch/parse RSS %s: %s", source["name"], e)
        return items

    # RSS 2.0
    for item_el in root.findall(".//item"):
        title = _text(item_el, "title")
        url = _text(item_el, "link")
        summary = _text(item_el, "description")
        pub_raw = _text(item_el, "pubDate", "dc:date")
        content = item_el.findtext("{http://purl.org/rss/1.0/modules/content/}encoded", "")
        pub_date = _parse_date(pub_raw)

        if pub_date and pub_date < cutoff:
            continue
        if title and url:
            items.append({
                "source_name": source["name"],
                "source_category": source["category"],
                "language": source["language"],
                "title": title,
                "url": url,
                "summary": summary,
                "raw_content": content or "",
                "published_at": pub_date.isoformat() if pub_date else None,
            })

    # Atom feeds
    for entry_el in root.findall(".//{http://www.w3.org/2005/Atom}entry"):
        title = entry_el.findtext("{http://www.w3.org/2005/Atom}title", "").strip()
        link_el = entry_el.find("{http://www.w3.org/2005/Atom}link[@rel='alternate']")
        if link_el is None:
            link_el = entry_el.find("{http://www.w3.org/2005/Atom}link")
        url = link_el.get("href", "") if link_el is not None else ""
        summary = entry_el.findtext("{http://www.w3.org/2005/Atom}summary", "").strip()
        pub_raw = entry_el.findtext("{http://www.w3.org/2005/Atom}published") or entry_el.findtext("{http://www.w3.org/2005/Atom}updated", "")
        pub_date = _parse_date(pub_raw)

        if pub_date and pub_date < cutoff:
            continue
        if title and url:
            items.append({
                "source_name": source["name"],
                "source_category": source["category"],
                "language": source["language"],
                "title": title,
                "url": url,
                "summary": summary,
                "raw_content": "",
                "published_at": pub_date.isoformat() if pub_date else None,
            })

    logger.info("Fetched %d items from %s", len(items), source["name"])
    return items


def collect_all_rss(cutoff_days: int = 7) -> list[dict]:
    all_items = []
    for source in RSS_SOURCES:
        all_items.extend(fetch_rss_feed(source, cutoff_days=cutoff_days))
    logger.info("Total RSS items: %d", len(all_items))
    return all_items
