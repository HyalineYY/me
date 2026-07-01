"""Hand-curated news items used to evaluate analyzer.py's LLM outputs.

Each item is picked to probe one specific failure mode:
- HIGH_VALUE_POLICY / LOW_VALUE_STALE: filter_item() should separate them clearly.
- SPARSE_NO_NUMBERS: the source contains no figures at all, so any number
  appearing in the generated analysis is a fabricated fact (hallucination).
- BOUNDARY_SUBJECTIVE: a borderline item used to measure run-to-run stability
  rather than "correctness", since reasonable analysts could disagree on the score.
"""

HIGH_VALUE_POLICY = {
    "title": "UK AR8 CfD Auction Brought Forward to July 2025, DESNZ Confirms",
    "source_name": "Offshore Wind Biz",
    "summary": (
        "The UK Department for Energy Security and Net Zero (DESNZ) has confirmed "
        "the Allocation Round 8 (AR8) Contracts for Difference auction will open in "
        "July 2025, two months ahead of the previously indicated September timeline. "
        "The administrative strike price for offshore wind remains under discussion, "
        "but industry sources suggest it will be set above £80/MWh."
    ),
    "raw_content": "",
}

LOW_VALUE_STALE = {
    "title": "Recap: Offshore Wind Turbine Blade Manufacturing Techniques, 2019 Overview",
    "source_name": "Generic Trade Blog",
    "summary": (
        "An old explainer article from 2019 describing generic fiberglass blade "
        "manufacturing steps, with no company names, no market data, and no "
        "connection to any current event."
    ),
    "raw_content": "",
}

SPARSE_NO_NUMBERS = {
    "title": "Developer Says Offshore Project Progressing Smoothly",
    "source_name": "Regional News Wire",
    "summary": (
        "A project developer issued a short statement saying that construction of "
        "its offshore wind farm is proceeding as planned and that the company "
        "remains in regular contact with regulators. No figures, dates, capacity, "
        "or financial terms were disclosed in the statement."
    ),
    "raw_content": "",
}

BOUNDARY_SUBJECTIVE = {
    "title": "Industry Association Notes Steady Interest in Floating Wind Concepts",
    "source_name": "Sector Newsletter",
    "summary": (
        "A regional industry association mentioned in its monthly newsletter that "
        "member companies continue to express interest in floating offshore wind "
        "concepts, without announcing any specific project, policy, or funding "
        "decision."
    ),
    "raw_content": "",
}

ALL_ITEMS = {
    "high_value_policy": HIGH_VALUE_POLICY,
    "low_value_stale": LOW_VALUE_STALE,
    "sparse_no_numbers": SPARSE_NO_NUMBERS,
    "boundary_subjective": BOUNDARY_SUBJECTIVE,
}
