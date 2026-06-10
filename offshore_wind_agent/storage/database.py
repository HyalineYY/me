"""SQLite storage for collected items — prevents duplicate processing."""

import sqlite3
import hashlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).parent.parent / "data" / "offshore_wind.db"


def _conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    """Create tables if they don't exist."""
    with _conn() as con:
        con.executescript("""
            CREATE TABLE IF NOT EXISTS raw_items (
                id          TEXT PRIMARY KEY,
                source_name TEXT,
                category    TEXT,
                language    TEXT,
                title       TEXT,
                url         TEXT UNIQUE,
                summary     TEXT,
                raw_content TEXT,
                published_at TEXT,
                collected_at TEXT,
                processed   INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS processed_items (
                id              TEXT PRIMARY KEY,
                raw_id          TEXT REFERENCES raw_items(id),
                title_cn        TEXT,
                core_content    TEXT,
                impact_analysis TEXT,
                value_score     INTEGER,
                tags            TEXT,
                processed_at    TEXT
            );

            CREATE TABLE IF NOT EXISTS report_runs (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                run_at      TEXT,
                items_count INTEGER,
                report_path TEXT,
                email_sent  INTEGER DEFAULT 0
            );
        """)
    logger.info("Database initialised at %s", DB_PATH)


def url_to_id(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:16]


def is_seen(url: str) -> bool:
    with _conn() as con:
        row = con.execute("SELECT 1 FROM raw_items WHERE url=?", (url,)).fetchone()
        return row is not None


def save_raw_items(items: list[dict]) -> list[dict]:
    """Insert new items, skip duplicates. Returns only newly inserted items."""
    new_items = []
    with _conn() as con:
        for item in items:
            url = item.get("url", "")
            if not url:
                continue
            item_id = url_to_id(url)
            try:
                con.execute(
                    """INSERT INTO raw_items
                       (id, source_name, category, language, title, url,
                        summary, raw_content, published_at, collected_at)
                       VALUES (?,?,?,?,?,?,?,?,?,?)""",
                    (
                        item_id,
                        item.get("source_name", ""),
                        item.get("source_category", ""),
                        item.get("language", "en"),
                        item.get("title", ""),
                        url,
                        item.get("summary", ""),
                        item.get("raw_content", ""),
                        item.get("published_at"),
                        datetime.now(timezone.utc).isoformat(),
                    ),
                )
                item["id"] = item_id
                new_items.append(item)
            except sqlite3.IntegrityError:
                pass  # duplicate URL
    logger.info("Saved %d new items (skipped %d duplicates)", len(new_items), len(items) - len(new_items))
    return new_items


def save_processed_item(raw_id: str, analysis: dict):
    with _conn() as con:
        con.execute(
            """INSERT OR REPLACE INTO processed_items
               (id, raw_id, title_cn, core_content, impact_analysis,
                value_score, tags, processed_at)
               VALUES (?,?,?,?,?,?,?,?)""",
            (
                url_to_id(raw_id + "_proc"),
                raw_id,
                analysis.get("title_cn", ""),
                analysis.get("core_content", ""),
                analysis.get("impact_analysis", ""),
                analysis.get("value_score", 0),
                json.dumps(analysis.get("tags", []), ensure_ascii=False),
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        con.execute("UPDATE raw_items SET processed=1 WHERE id=?", (raw_id,))


def get_processed_items_for_report(min_score: int = 3) -> list[dict]:
    """Fetch processed items above min_score that haven't been in a report yet."""
    with _conn() as con:
        rows = con.execute(
            """SELECT p.*, r.title, r.url, r.source_name, r.published_at, r.language
               FROM processed_items p
               JOIN raw_items r ON r.id = p.raw_id
               WHERE p.value_score >= ?
               ORDER BY p.value_score DESC, r.published_at DESC""",
            (min_score,),
        ).fetchall()
    return [dict(row) for row in rows]


def save_report_run(items_count: int, report_path: str, email_sent: bool = False):
    with _conn() as con:
        con.execute(
            "INSERT INTO report_runs (run_at, items_count, report_path, email_sent) VALUES (?,?,?,?)",
            (datetime.now(timezone.utc).isoformat(), items_count, report_path, int(email_sent)),
        )
