"""Output-quality checks: schema, completeness, and language of analyzer output.

These run in two layers:
- Offline (no API key needed): validate the pre-written demo analyses match the
  schema the rest of the pipeline (database.py, report_generator.py) expects,
  so a schema drift is caught even without burning API calls.
- Online (@pytest.mark.llm): validate that *live* Claude output also matches
  the schema and meets basic completeness/language bars.
"""

import re

import pytest

REQUIRED_FIELDS = {"title_cn", "core_content", "impact_analysis", "value_note", "tags", "value_score"}
CJK_RE = re.compile(r"[一-鿿]")


def assert_schema(analysis: dict):
    missing = REQUIRED_FIELDS - analysis.keys()
    assert not missing, f"missing fields: {missing}"
    assert isinstance(analysis["value_score"], int)
    assert 1 <= analysis["value_score"] <= 5
    assert isinstance(analysis["tags"], list) and all(isinstance(t, str) for t in analysis["tags"])
    assert isinstance(analysis["title_cn"], str) and analysis["title_cn"].strip()
    assert isinstance(analysis["core_content"], str) and analysis["core_content"].strip()


def assert_chinese_output(analysis: dict):
    for field in ("title_cn", "core_content", "impact_analysis"):
        text = analysis[field]
        assert CJK_RE.search(text), f"{field} has no Chinese characters: {text!r}"


def test_demo_dataset_matches_schema():
    from demo_data import DEMO_ITEMS

    assert DEMO_ITEMS, "demo dataset is empty"
    for item in DEMO_ITEMS:
        assert_schema(item["analysis"])
        assert_chinese_output(item["analysis"])


@pytest.mark.llm
def test_live_analysis_matches_schema_and_is_not_a_failure_fallback():
    from processing.analyzer import analyze_item
    from tests.golden_dataset import HIGH_VALUE_POLICY

    analysis = analyze_item(HIGH_VALUE_POLICY)
    assert_schema(analysis)
    assert_chinese_output(analysis)
    assert analysis["impact_analysis"] != "分析失败"


@pytest.mark.llm
def test_filter_separates_high_and_low_value_items():
    from processing.analyzer import filter_item
    from tests.golden_dataset import HIGH_VALUE_POLICY, LOW_VALUE_STALE

    high_score = filter_item(HIGH_VALUE_POLICY)
    low_score = filter_item(LOW_VALUE_STALE)
    assert high_score >= 4, f"expected clearly high-value item to score >=4, got {high_score}"
    assert low_score <= 2, f"expected stale/irrelevant item to score <=2, got {low_score}"


@pytest.mark.llm
def test_core_content_is_two_to_three_sentences():
    from processing.analyzer import analyze_item
    from tests.golden_dataset import HIGH_VALUE_POLICY

    analysis = analyze_item(HIGH_VALUE_POLICY)
    sentence_count = len(re.findall(r"[。！？]", analysis["core_content"]))
    assert 1 <= sentence_count <= 4, (
        f"core_content should be ~2-3 sentences, found {sentence_count}: {analysis['core_content']!r}"
    )
