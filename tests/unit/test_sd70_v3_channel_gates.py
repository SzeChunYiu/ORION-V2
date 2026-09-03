"""SD70-V3: the gates added over V2 must actually fire, and must not cry wolf.

Every test asserts BOTH directions: the clean case is reported clean, and the
broken case is reported broken. A gate only validated on the failing case is
how a checker ends up raising a false alarm on its first real run.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

V3 = Path(__file__).resolve().parents[2] / "research" / "experiments" / "sd70-v3"
if str(V3) not in sys.path:
    sys.path.insert(0, str(V3))

import sd70v3_channel as CH  # noqa: E402
import sd70v3_model_arm as MA  # noqa: E402

DESIGN = json.loads((V3 / "SD70_V3_EXECUTION_DESIGN_V1.json").read_text(encoding="utf-8"))
CONTRACT = DESIGN["channel_contract"]


def _obs(canary: str, *, input_tokens=13600, output_tokens=30, reasoning=0,
         comp="2911", slugs=None, observable=True, ok=True, token="OK"):
    return {
        "canary": canary,
        "prompt_sha256": CH.canary_prompt_hashes()[canary],
        "prompt_bytes": len(CH.CANARY_PROMPTS[canary].encode()),
        "dispatch_ok": ok,
        "answer": {"token": token, "note": ""} if ok else None,
        "usage": {"input_tokens": input_tokens, "output_tokens": output_tokens,
                  "reasoning_output_tokens": reasoning, "cached_input_tokens": 0,
                  "total_tokens": input_tokens + output_tokens,
                  "usage_source": "TURN_COMPLETED_USAGE", "turn_completed": True, "turn_failed": False},
        "channel_observation": {
            "observable": observable,
            "gpt_5_5_comp_hash": comp if observable else None,
            "served_slugs_prefix": (slugs if slugs is not None else CONTRACT["expected_served_slugs_prefix"]) if observable else None,
        },
    }


def _measurement(**kw):
    return {"observations": [_obs(c, **kw) for c in sorted(CH.CANARY_PROMPTS)]}


# --------------------------------------------------------------------------
# channel contract: three-valued, and UNOBSERVABLE is never OK
# --------------------------------------------------------------------------

def test_clean_channel_is_ok_and_every_check_has_a_nonzero_denominator():
    v = CH.verdict(_measurement(), _measurement(), CONTRACT)
    assert v["verdict"] == CH.CONTRACT_OK
    assert v["checks"], "no checks ran at all"
    for c in v["checks"]:
        assert c["denominator"] > 0, f"{c['check']} reported a verdict over an empty denominator"


def test_comp_hash_change_is_drift_not_ok():
    v = CH.verdict(_measurement(), _measurement(comp="9999"), CONTRACT)
    assert v["verdict"] == CH.CONTRACT_DRIFT
    assert "comp_hash_matches_frozen" in v["failed_checks"]


def test_served_slug_list_change_is_drift():
    v = CH.verdict(_measurement(), _measurement(slugs=["gpt-5.5"]), CONTRACT)
    assert v["verdict"] == CH.CONTRACT_DRIFT


def test_unobservable_manifest_is_not_reported_as_ok():
    """The scrape depends on a CLI decode failure. If the server is fixed the
    scrape goes silent -- that must never read as 'contract verified'."""
    v = CH.verdict(_measurement(observable=False), _measurement(observable=False), CONTRACT)
    assert v["verdict"] == CH.CONTRACT_UNOBSERVABLE
    assert v["verdict"] != CH.CONTRACT_OK
    assert v["unobservable"]


def test_canary_dispatch_failure_is_its_own_verdict():
    v = CH.verdict(_measurement(), _measurement(ok=False), CONTRACT)
    assert v["verdict"] == CH.CONTRACT_FAILED


def test_e30_r12_style_reasoning_blowup_is_detected():
    """The concrete failure this gate exists for: an identical frozen prompt
    whose output budget is silently consumed by a reasoning block."""
    v = CH.verdict(_measurement(output_tokens=30, reasoning=0),
                   _measurement(output_tokens=6000, reasoning=5900), CONTRACT)
    assert v["verdict"] == CH.CONTRACT_DRIFT
    assert "canary_token_behaviour_stable" in v["failed_checks"]


def test_within_band_jitter_does_not_cry_wolf():
    """Calibrated jitter must NOT fire; a gate that alarms on normal variation
    gets switched off before it ever catches anything."""
    v = CH.verdict(_measurement(input_tokens=13593, output_tokens=31, reasoning=0),
                   _measurement(input_tokens=14875, output_tokens=49, reasoning=16), CONTRACT)
    assert v["verdict"] == CH.CONTRACT_OK


def test_canary_prompts_are_byte_frozen_against_the_design():
    assert CH.canary_prompt_hashes() == CONTRACT["canary_prompt_sha256"]


# --------------------------------------------------------------------------
# per-envelope usage parsing
# --------------------------------------------------------------------------

def test_turn_completed_usage_is_read_explicitly_including_reasoning_tokens():
    stream = "\n".join([
        json.dumps({"type": "thread.started", "thread_id": "t"}),
        json.dumps({"type": "turn.started"}),
        json.dumps({"type": "turn.completed", "usage": {"input_tokens": 13581, "cached_input_tokens": 2432,
                                                        "output_tokens": 61, "reasoning_output_tokens": 24}}),
    ])
    u = MA.parse_events(stream)
    assert u["usage_source"] == "TURN_COMPLETED_USAGE"
    assert u["cached_input_tokens"] == 2432, "V2's recursive scan silently dropped this field"
    assert u["reasoning_output_tokens"] == 24, "V2's recursive scan silently dropped this field"
    assert u["turn_completed"] is True


def test_absent_usage_is_marked_absent_not_zero():
    u = MA.parse_events(json.dumps({"type": "turn.started"}))
    assert u["usage_source"] == "ABSENT"
    assert u["input_tokens"] is None, "an unmeasured token count must be None, never 0"


def test_channel_scrape_reports_unobservable_when_the_body_is_absent():
    c = MA.parse_channel_observation("some stderr with no models manifest")
    assert c["observable"] is False
    assert c["gpt_5_5_comp_hash"] is None


def test_channel_scrape_reads_comp_hash_and_slugs_from_a_real_body():
    raw = (V3 / "provenance" / "CHANNEL_PROBE_OBSERVATION_V1.json")
    expected = json.loads(raw.read_text(encoding="utf-8"))
    body = ('ERROR ...: body: {"models":[{"slug":"gpt-5.5","context_window":272000,'
            '"comp_hash":"2911","display_name":"GPT-5.5"},{"slug":"gpt-5.4"}]}')
    c = MA.parse_channel_observation(body)
    assert c["observable"] is True
    assert c["gpt_5_5_comp_hash"] == expected["gpt_5_5_manifest"]["comp_hash"]
    assert c["served_slugs_prefix"][0] == "gpt-5.5"


# --------------------------------------------------------------------------
# the design's own registered constants
# --------------------------------------------------------------------------

def test_model_is_the_one_actually_reachable_under_the_pinned_cli():
    assert DESIGN["model_arms"]["model"] == "gpt-5.5"
    prov = DESIGN["provenance"]["block_evidence"]
    assert prov["gpt_5_5"]["exit_code"] == 0 and prov["gpt_5_5"]["turn_completed"] is True
    assert prov["gpt_5_6_terra"]["http_status"] == 400
    assert prov["gpt_5_6_terra"]["absent_from_served_manifest"] is True


def test_v3_does_not_claim_to_be_an_edit_of_v2_and_spends_no_v2_authorization():
    rel = DESIGN["relationship_to_sd70_v2"]
    assert rel["is_an_edit_of_v2"] is False
    assert rel["v2_authorization_spent"] is False
    assert rel["v2_expectation_status"] == "UNOBSERVED"
    assert DESIGN["seed_commitment"]["seed_sha256"] != DESIGN["seed_commitment"]["sd70_v2_seed_sha256_not_reused"]


def test_design_grants_no_authority():
    for k, v in DESIGN["authority"].items():
        assert v is False, f"{k} must be false"


def test_comparator_is_the_stronger_of_parent_and_federation_on_development():
    c = DESIGN["comparator"]
    acc = c["development_exact_accuracy"]
    assert max(acc.values()) == acc["STRONGEST_GENERATOR_FAITHFUL_PARENT (MAXMARGIN_PARENT)"]
    assert c["selected"].startswith("STRONGEST_GENERATOR_FAITHFUL_PARENT")


def test_reasoning_is_declared_enabled_not_disabled():
    """default_reasoning_summary 'none' suppresses SUMMARIES; reasoning still runs."""
    rb = DESIGN["channel_contract"]["request_body"]
    assert rb["reasoning_enabled"] is True
    assert rb["reasoning_summaries_emitted"] is False
