"""LLM-based analysis of offshore wind news items using Claude API."""

import json
import logging
import os
from anthropic import Anthropic

logger = logging.getLogger(__name__)

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

FILTER_SYSTEM = """你是一位专注于海上风电行业的资深研究分析师。
你的任务是判断一条新闻是否对海上风电行业研究有价值。

有价值的信息包括但不限于：
- 行业政策（补贴政策、招标制度、审批流程变化）
- 重大项目进展（中标、FID、开工、并网）
- 主要公司业绩、订单、财务相关披露
- 行业数据（装机量、招标量、价格指数）
- 行业报告与预测
- 供应链重大事件（涨价、断供、新技术）
- 市场情绪相关事件（融资、破产、并购）

低价值信息：
- 纯技术文章无市场影响
- 与海上风电无直接关联
- 超过7天的旧信息

打分1-5：1=无价值，3=有一定参考价值，5=高度相关且有市场影响"""

ANALYZE_SYSTEM = """你是一位专注于海上风电行业的资深研究分析师，擅长分析信息对行业发展、业绩、估值、市场情绪的影响。

分析要求：
1. 提炼核心内容（2-3句话，中文）
2. 分析对行业的影响（政策/业绩/估值/情绪维度），如有历史对比需指出变化方向
3. 给出参考价值说明
4. 提取关键标签

必须以JSON格式输出，不要有其他文字：
{
  "title_cn": "中文标题（简洁）",
  "core_content": "核心内容（2-3句话）",
  "impact_analysis": "对行业的影响分析，包含：影响维度（政策/业绩/估值/情绪），影响方向（利好/利空/中性），影响程度（重大/一般/轻微），简要说明",
  "value_note": "参考价值说明（1句话）",
  "tags": ["标签1", "标签2"],
  "value_score": 4
}"""


def filter_item(item: dict) -> int:
    """Quick filter: return value score 1-5."""
    text = f"标题：{item.get('title', '')}\n摘要：{item.get('summary', '')}"
    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=50,
            system=FILTER_SYSTEM,
            messages=[{"role": "user", "content": f"请为以下新闻打分（只输出1个数字1-5）：\n\n{text}"}],
        )
        score_text = msg.content[0].text.strip()
        return int(score_text[0]) if score_text else 1
    except Exception as e:
        logger.warning("Filter failed for '%s': %s", item.get("title", ""), e)
        return 1


def analyze_item(item: dict) -> dict:
    """Deep analysis of a single item."""
    text = (
        f"标题：{item.get('title', '')}\n"
        f"来源：{item.get('source_name', '')}\n"
        f"摘要：{item.get('summary', '')}\n"
        f"正文节选：{item.get('raw_content', '')[:500]}"
    )
    try:
        msg = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=800,
            system=ANALYZE_SYSTEM,
            messages=[{"role": "user", "content": f"请分析以下海上风电行业信息：\n\n{text}"}],
        )
        raw = msg.content[0].text.strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw)
    except Exception as e:
        logger.warning("Analysis failed for '%s': %s", item.get("title", ""), e)
        return {
            "title_cn": item.get("title", ""),
            "core_content": item.get("summary", ""),
            "impact_analysis": "分析失败",
            "value_note": "",
            "tags": [],
            "value_score": 2,
        }


def compare_with_history(new_item: dict, historical_context: str) -> str:
    """Generate comparison analysis when similar historical items exist."""
    if not historical_context:
        return ""
    prompt = (
        f"新信息：\n{new_item.get('title', '')}\n{new_item.get('core_content', '')}\n\n"
        f"历史背景：\n{historical_context}\n\n"
        "请分析新旧信息的变化，说明进展方向（提前/延迟/超预期/低于预期等）及对行业的意义。"
        "用2-3句话回答，中文。"
    )
    try:
        msg = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text.strip()
    except Exception:
        return ""


def batch_filter_and_analyze(items: list[dict], min_filter_score: int = 3) -> list[dict]:
    """Filter then deeply analyze items above threshold."""
    results = []
    logger.info("Filtering %d items...", len(items))

    for item in items:
        score = filter_item(item)
        if score < min_filter_score:
            logger.debug("Skipped low-score item: %s (score=%d)", item.get("title", ""), score)
            continue

        logger.info("Analyzing: %s", item.get("title", ""))
        analysis = analyze_item(item)
        analysis["value_score"] = max(analysis.get("value_score", score), score)
        item["analysis"] = analysis
        results.append(item)

    logger.info("Kept %d/%d items after filtering", len(results), len(items))
    return results
