"""Generate structured HTML and Markdown reports from analyzed items."""

from datetime import datetime, timezone
from pathlib import Path

REPORT_DIR = Path(__file__).parent.parent / "reports"


def generate_report(items: list[dict]) -> tuple[str, str]:
    """
    Generate both Markdown and HTML reports.
    Returns (markdown_path, html_path).
    """
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")

    md_path = REPORT_DIR / f"offshore_wind_{ts}.md"
    html_path = REPORT_DIR / f"offshore_wind_{ts}.html"

    md_content = _build_markdown(items)
    html_content = _build_html(items, md_content)

    md_path.write_text(md_content, encoding="utf-8")
    html_path.write_text(html_content, encoding="utf-8")

    return str(md_path), str(html_path)


def _build_markdown(items: list[dict]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# 海上风电行业动态周报",
        f"",
        f"**生成时间：** {now}",
        f"**信息条数：** {len(items)} 条",
        f"",
        "---",
        "",
    ]

    # Group by category
    categories = {
        "industry_org": "🌐 行业组织与报告",
        "government": "🏛️ 政府政策与监管",
        "company_ir": "🏢 主要公司动态",
        "news_media": "📰 行业新闻",
        "news_media_cn": "📰 国内行业新闻",
        "search": "🔍 搜索聚合",
    }

    grouped: dict[str, list] = {}
    for item in items:
        cat = item.get("source_category", "search")
        grouped.setdefault(cat, []).append(item)

    for cat_key, cat_label in categories.items():
        cat_items = grouped.get(cat_key, [])
        if not cat_items:
            continue

        lines.append(f"## {cat_label}")
        lines.append("")

        for item in sorted(cat_items, key=lambda x: x.get("analysis", {}).get("value_score", 0), reverse=True):
            a = item.get("analysis", {})
            title_cn = a.get("title_cn") or item.get("title", "")
            orig_title = item.get("title", "")
            url = item.get("url", "#")
            core = a.get("core_content", item.get("summary", ""))
            impact = a.get("impact_analysis", "")
            value_note = a.get("value_note", "")
            score = a.get("value_score", "—")
            tags = a.get("tags", [])
            pub = item.get("published_at", "")[:10] if item.get("published_at") else ""
            source = item.get("source_name", "")

            lines += [
                f"### {title_cn}",
                f"",
                f"**原标题：** {orig_title}",
                f"**来源：** {source}　**发布日期：** {pub}　**价值评分：** {'⭐' * int(score) if isinstance(score, int) else score}",
                f"",
                f"**核心内容：**",
                f"{core}",
                f"",
                f"**影响分析：**",
                f"{impact}",
                f"",
            ]
            if value_note:
                lines.append(f"**参考价值：** {value_note}")
                lines.append("")
            if tags:
                lines.append(f"**标签：** {' · '.join(f'`{t}`' for t in tags)}")
                lines.append("")
            lines.append(f"🔗 [查看原文]({url})")
            lines.append("")
            lines.append("---")
            lines.append("")

    lines += [
        "## 声明",
        "",
        "本报告由自动化信息采集系统生成，内容来源于公开信息，仅供参考，不构成投资建议。",
        "",
    ]

    return "\n".join(lines)


def _build_html(items: list[dict], md_source: str) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    count = len(items)

    rows = []
    for item in sorted(items, key=lambda x: x.get("analysis", {}).get("value_score", 0), reverse=True):
        a = item.get("analysis", {})
        score = a.get("value_score", 0)
        stars = "⭐" * int(score) if isinstance(score, int) else ""
        title_cn = a.get("title_cn") or item.get("title", "")
        orig_title = item.get("title", "")
        url = item.get("url", "#")
        core = a.get("core_content", item.get("summary", "")).replace("\n", "<br>")
        impact = a.get("impact_analysis", "").replace("\n", "<br>")
        value_note = a.get("value_note", "")
        tags = a.get("tags", [])
        pub = item.get("published_at", "")[:10] if item.get("published_at") else ""
        source = item.get("source_name", "")
        tag_html = " ".join(f'<span class="tag">{t}</span>' for t in tags)

        rows.append(f"""
        <div class="card">
          <div class="card-header">
            <span class="score">{stars}</span>
            <h3>{title_cn}</h3>
            <div class="meta">来源：{source} &nbsp;|&nbsp; 发布：{pub}</div>
            <div class="orig-title">原标题：<a href="{url}" target="_blank">{orig_title}</a></div>
          </div>
          <div class="card-body">
            <p><strong>核心内容</strong><br>{core}</p>
            <p><strong>影响分析</strong><br>{impact}</p>
            {"<p><strong>参考价值：</strong>" + value_note + "</p>" if value_note else ""}
            <div class="tags">{tag_html}</div>
          </div>
          <div class="card-footer">
            <a href="{url}" target="_blank">🔗 查看原文</a>
          </div>
        </div>
        """)

    body = "\n".join(rows)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>海上风电行业动态周报 - {now}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: #f4f6f8; color: #333; margin: 0; padding: 20px; }}
    .header {{ background: linear-gradient(135deg, #0066cc, #00a86b);
               color: white; padding: 30px; border-radius: 12px; margin-bottom: 24px; }}
    .header h1 {{ margin: 0 0 8px; font-size: 24px; }}
    .header p {{ margin: 0; opacity: 0.9; font-size: 14px; }}
    .card {{ background: white; border-radius: 10px; margin-bottom: 20px;
             box-shadow: 0 2px 8px rgba(0,0,0,.08); overflow: hidden; }}
    .card-header {{ padding: 16px 20px 10px; border-bottom: 1px solid #eee; }}
    .card-header h3 {{ margin: 4px 0 8px; font-size: 18px; color: #1a1a2e; }}
    .score {{ font-size: 14px; }}
    .meta {{ font-size: 12px; color: #888; }}
    .orig-title {{ font-size: 12px; color: #666; margin-top: 4px; }}
    .orig-title a {{ color: #0066cc; text-decoration: none; }}
    .card-body {{ padding: 16px 20px; }}
    .card-body p {{ margin: 0 0 12px; line-height: 1.7; font-size: 14px; }}
    .tags {{ display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }}
    .tag {{ background: #e8f4f8; color: #0066cc; padding: 2px 10px;
            border-radius: 20px; font-size: 12px; }}
    .card-footer {{ padding: 10px 20px; background: #fafafa; border-top: 1px solid #eee; }}
    .card-footer a {{ color: #0066cc; font-size: 13px; text-decoration: none; }}
    .disclaimer {{ font-size: 12px; color: #999; text-align: center; margin-top: 30px; }}
  </style>
</head>
<body>
  <div class="header">
    <h1>🌊 海上风电行业动态周报</h1>
    <p>生成时间：{now} &nbsp;|&nbsp; 本期 {count} 条高价值信息</p>
  </div>
  {body}
  <p class="disclaimer">本报告由自动化信息采集系统生成，内容来源于公开信息，仅供参考，不构成投资建议。</p>
</body>
</html>"""
