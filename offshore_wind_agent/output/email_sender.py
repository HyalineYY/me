"""Send the generated report via email."""

import smtplib
import os
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

# Config from environment variables
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.qq.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "465"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
RECIPIENT = os.environ.get("REPORT_RECIPIENT", "1873149332@qq.com")


def send_report(html_path: str, md_path: str, items_count: int) -> bool:
    """Send the report HTML as email body with MD as attachment."""
    if not SMTP_USER or not SMTP_PASS:
        logger.error("SMTP credentials not set. Set SMTP_USER and SMTP_PASS env vars.")
        return False

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    subject = f"【海上风电行业周报】{now} - 共 {items_count} 条高价值信息"

    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = RECIPIENT

    # HTML body
    html_content = Path(html_path).read_text(encoding="utf-8")
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    # Markdown attachment
    md_content = Path(md_path).read_text(encoding="utf-8")
    attach = MIMEBase("application", "octet-stream")
    attach.set_payload(md_content.encode("utf-8"))
    encoders.encode_base64(attach)
    attach.add_header("Content-Disposition", f"attachment; filename=offshore_wind_{now}.md")
    msg.attach(attach)

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, [RECIPIENT], msg.as_string())
        logger.info("Email sent to %s", RECIPIENT)
        return True
    except Exception as e:
        logger.error("Failed to send email: %s", e)
        return False
