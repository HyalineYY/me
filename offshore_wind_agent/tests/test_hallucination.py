"""Hallucination checks: does the generated analysis introduce facts not in the source?

Two complementary techniques:
1. Rule-based number-grounding: extract every number token from the source
   text and from the generated text; any number in the output that doesn't
   appear in the input is a strong signal of a fabricated statistic. Cheap,
   deterministic, no extra API call.
2. LLM-as-judge: ask a model (ideally a stronger/different model than the one
   under test) to compare source vs. generated analysis and flag unsupported
   claims in structured JSON. Catches fabrications that aren't numeric
   (invented company names, invented causal claims, etc).
"""

import json
import re

import pytest

NUMBER_RE = re.compile(r"\d[\d,.]*")

JUDGE_SYSTEM = """你是一名严格的事实核查员。给定"原文"和"分析"，判断"分析"中是否包含任何原文未提及、
无法从原文合理推断的具体事实（数字、日期、公司名、金额、百分比等）。
仅输出JSON，不要有其他文字：
{"has_unsupported_claims": true/false, "unsupported_claims": ["..."]}"""


def _numbers_in(text: str) -> set:
    return set(NUMBER_RE.findall(text or ""))


def _judge_grounding(judge_client, source_text: str, analysis_text: str) -> dict:
    msg = judge_client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=400,
        system=JUDGE_SYSTEM,
        messages=[{"role": "user", "content": f"原文：\n{source_text}\n\n分析：\n{analysis_text}"}],
    )
    raw = msg.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw)


@pytest.mark.llm
def test_no_fabricated_numbers_when_source_has_none():
    from processing.analyzer import analyze_item
    from tests.golden_dataset import SPARSE_NO_NUMBERS

    analysis = analyze_item(SPARSE_NO_NUMBERS)
    source_numbers = _numbers_in(SPARSE_NO_NUMBERS["summary"])
    output_text = analysis["core_content"] + " " + analysis["impact_analysis"]
    output_numbers = _numbers_in(output_text)

    fabricated = output_numbers - source_numbers
    assert not fabricated, (
        f"analysis invented numbers not present in source: {fabricated}\n"
        f"output: {output_text!r}"
    )


@pytest.mark.llm
def test_llm_judge_finds_no_unsupported_claims(judge_client):
    from processing.analyzer import analyze_item
    from tests.golden_dataset import HIGH_VALUE_POLICY

    analysis = analyze_item(HIGH_VALUE_POLICY)
    analysis_text = f"{analysis['core_content']}\n{analysis['impact_analysis']}"
    verdict = _judge_grounding(judge_client, HIGH_VALUE_POLICY["summary"], analysis_text)

    assert not verdict.get("has_unsupported_claims", True), (
        f"judge flagged unsupported claims: {verdict.get('unsupported_claims')}"
    )


@pytest.mark.llm
def test_comparison_analysis_does_not_invent_history_when_none_given():
    """compare_with_history() should return an empty string rather than
    fabricating a comparison when no historical context is passed in."""
    from processing.analyzer import compare_with_history
    from tests.golden_dataset import HIGH_VALUE_POLICY

    result = compare_with_history(HIGH_VALUE_POLICY, historical_context="")
    assert result == ""
