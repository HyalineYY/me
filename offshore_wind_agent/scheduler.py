"""
Simple scheduler to run the agent on a weekly schedule.
Usage:
  python scheduler.py                    # Run once immediately
  python scheduler.py --schedule weekly  # Run every Monday 08:00 UTC
  python scheduler.py --schedule daily   # Run every day 08:00 UTC
"""

import schedule
import time
import logging
import argparse
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("scheduler")


def job():
    from main import run
    try:
        run()
    except Exception as e:
        logger.error("Agent run failed: %s", e, exc_info=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--schedule", choices=["daily", "weekly", "once"], default="once")
    args = parser.parse_args()

    if args.schedule == "once":
        job()
        sys.exit(0)
    elif args.schedule == "daily":
        schedule.every().day.at("08:00").do(job)
        logger.info("Scheduler running: daily at 08:00 UTC")
    elif args.schedule == "weekly":
        schedule.every().monday.at("08:00").do(job)
        logger.info("Scheduler running: every Monday at 08:00 UTC")

    while True:
        schedule.run_pending()
        time.sleep(60)
