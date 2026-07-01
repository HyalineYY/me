"""Run-to-run stability checks: same input, multiple LLM calls, bounded variance.

An agent that scores/labels news is only useful if repeated runs on the same
input don't flip-flop. These tests call the real model N times (small N to
keep cost down) and assert the *spread* of outputs stays within a tolerance,
rather than asserting a single exact value.
"""

import pytest

N_RUNS = 5


def _tag_jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


@pytest.mark.llm
def test_filter_score_is_stable_across_repeated_calls():
    from processing.analyzer import filter_item
    from tests.golden_dataset import HIGH_VALUE_POLICY

    scores = [filter_item(HIGH_VALUE_POLICY) for _ in range(N_RUNS)]
    assert max(scores) - min(scores) <= 1, f"filter score spread too wide across runs: {scores}"


@pytest.mark.llm
def test_value_score_is_stable_across_repeated_calls():
    from processing.analyzer import analyze_item
    from tests.golden_dataset import BOUNDARY_SUBJECTIVE

    scores = [analyze_item(BOUNDARY_SUBJECTIVE)["value_score"] for _ in range(N_RUNS)]
    assert max(scores) - min(scores) <= 1, f"value_score spread too wide across runs: {scores}"


@pytest.mark.llm
def test_tags_are_reasonably_consistent_across_repeated_calls():
    from processing.analyzer import analyze_item
    from tests.golden_dataset import HIGH_VALUE_POLICY

    tag_sets = [set(analyze_item(HIGH_VALUE_POLICY)["tags"]) for _ in range(N_RUNS)]
    baseline = tag_sets[0]
    similarities = [_tag_jaccard(baseline, s) for s in tag_sets[1:]]
    avg_similarity = sum(similarities) / len(similarities)
    assert avg_similarity >= 0.3, f"tags vary too much across runs: {tag_sets}"


@pytest.mark.llm
def test_json_output_parses_every_run():
    """analyze_item() falls back to a '分析失败' stub on a JSON parse error;
    across repeated calls that fallback should never trigger for a well-formed input."""
    from processing.analyzer import analyze_item
    from tests.golden_dataset import HIGH_VALUE_POLICY

    results = [analyze_item(HIGH_VALUE_POLICY) for _ in range(N_RUNS)]
    parse_failures = [r for r in results if r["impact_analysis"] == "分析失败"]
    assert not parse_failures, f"{len(parse_failures)}/{N_RUNS} runs hit the JSON-parse-failure fallback"
