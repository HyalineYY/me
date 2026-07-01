"""Shared fixtures for the model-quality test suite.

Tests marked `@pytest.mark.llm` make real Anthropic API calls and are skipped
automatically when ANTHROPIC_API_KEY is not set, so the suite still runs (and
still checks report formatting / schema logic) in environments without a key.
"""

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

HAS_API_KEY = bool(os.environ.get("ANTHROPIC_API_KEY"))


def pytest_configure(config):
    config.addinivalue_line("markers", "llm: needs ANTHROPIC_API_KEY, makes real API calls")


def pytest_collection_modifyitems(config, items):
    if HAS_API_KEY:
        return
    skip_llm = pytest.mark.skip(reason="ANTHROPIC_API_KEY not set")
    for item in items:
        if "llm" in item.keywords:
            item.add_marker(skip_llm)


@pytest.fixture(scope="session")
def judge_client():
    from anthropic import Anthropic

    return Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
