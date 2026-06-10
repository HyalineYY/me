"""
Offshore Wind Energy Intelligence Agent
=======================================
Orchestrates: collect → deduplicate → filter → analyze → report → email
"""

import logging
import os
import sys
from datetime import datetime, timezone

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("offshore_wind_agent")


def run(dry_run: bool = False, min_score: int = 3, cutoff_days: int = 7):
    from storage.database import init_db, save_raw_items, save_processed_item, get_processed_items_for_report, save_report_run
    from sources.rss_collector import collect_all_rss
    from sources.web_scraper import collect_scraped_sources, collect_google_news
    from processing.analyzer import batch_filter_and_analyze
    from output.report_generator import generate_report
    from output.email_sender import send_report

    logger.info("=" * 60)
    logger.info("Offshore Wind Agent starting — %s", datetime.now(timezone.utc).isoformat())
    logger.info("=" * 60)

    # ── 1. Init DB ──────────────────────────────────────────────
    init_db()

    # ── 2. Collect ───────────────────────────────────────────────
    logger.info("Step 1/5: Collecting from information sources...")
    raw_items = []
    raw_items += collect_all_rss(cutoff_days=cutoff_days)
    raw_items += collect_scraped_sources()
    raw_items += collect_google_news()
    logger.info("Collected %d raw items total", len(raw_items))

    # ── 3. Deduplicate & save ────────────────────────────────────
    logger.info("Step 2/5: Deduplicating...")
    new_items = save_raw_items(raw_items)
    logger.info("%d new (unseen) items", len(new_items))

    if not new_items:
        logger.info("No new items to process. Exiting.")
        return

    # ── 4. Filter + Analyze ──────────────────────────────────────
    logger.info("Step 3/5: LLM filtering and analysis...")
    if dry_run:
        logger.info("[dry_run] Skipping LLM analysis")
        analyzed = [dict(item, analysis={"title_cn": item["title"], "core_content": item.get("summary", ""),
                                          "impact_analysis": "dry_run", "value_note": "", "tags": [], "value_score": 3})
                    for item in new_items]
    else:
        analyzed = batch_filter_and_analyze(new_items, min_filter_score=min_score)

    # Save analysis results
    for item in analyzed:
        if "id" in item and "analysis" in item:
            save_processed_item(item["id"], item["analysis"])

    # ── 5. Retrieve all high-value processed items ───────────────
    all_report_items = get_processed_items_for_report(min_score=min_score)
    # Merge analysis fields into report item structure
    report_items = []
    for row in all_report_items:
        import json
        row["analysis"] = {
            "title_cn": row.get("title_cn", row.get("title", "")),
            "core_content": row.get("core_content", ""),
            "impact_analysis": row.get("impact_analysis", ""),
            "value_note": "",
            "tags": json.loads(row.get("tags", "[]")),
            "value_score": row.get("value_score", 3),
        }
        report_items.append(row)

    if not report_items:
        logger.info("No high-value items to report. Exiting.")
        return

    # ── 6. Generate report ───────────────────────────────────────
    logger.info("Step 4/5: Generating report (%d items)...", len(report_items))
    md_path, html_path = generate_report(report_items)
    logger.info("Report saved: %s", html_path)

    # ── 7. Send email ────────────────────────────────────────────
    logger.info("Step 5/5: Sending email...")
    email_sent = False
    if not dry_run:
        email_sent = send_report(html_path, md_path, len(report_items))

    save_report_run(len(report_items), html_path, email_sent)

    logger.info("=" * 60)
    logger.info("Done. Report: %s | Email sent: %s", html_path, email_sent)
    logger.info("=" * 60)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Offshore Wind Intelligence Agent")
    parser.add_argument("--dry-run", action="store_true", help="Skip LLM calls and email")
    parser.add_argument("--min-score", type=int, default=3, help="Minimum value score to include (1-5)")
    parser.add_argument("--days", type=int, default=7, help="Collect items from last N days")
    args = parser.parse_args()

    run(dry_run=args.dry_run, min_score=args.min_score, cutoff_days=args.days)
