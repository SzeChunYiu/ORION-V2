"""Data-only renderer and independent actual-text commitment eligibility gate.

The renderer receives no mutable object or callback. This is an API capability
property of this trusted function, not a sandbox for arbitrary Python plugins.
Only the separate gate sees current external evidence and protected identities.
"""
from __future__ import annotations

from dataclasses import dataclass
import re

from .codecs import decode_functional, decode_sentence, encode_functional, encode_sentence
from .semantics import (CannotCheck, Formula, identifier, meaning, registry_digest,
                        validate_formula)


@dataclass(frozen=True, slots=True)
class ShownClaim:
    formula: Formula
    marker: str                        # ASSERT, HEDGE, WITHHOLD
    citations: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class RenderView:
    registry_digest: str
    epoch: str
    claims: tuple[ShownClaim, ...]


@dataclass(frozen=True, slots=True)
class Support:
    evidence_id: str
    semantic_seed: str
    status: str                        # LIVE, UNKNOWN, DEAD
    scope: str
    world_authority: bool


@dataclass(frozen=True, slots=True)
class GateResult:
    status: str
    reason: str
    checked_claims: int = 0


def _digest(value):
    return type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def validate_view(view, registry):
    if type(view) is not RenderView or not _digest(view.registry_digest) or view.registry_digest != registry_digest(registry):
        raise CannotCheck("render view registry binding mismatch")
    if not identifier(view.epoch) or type(view.claims) is not tuple or len(view.claims) > 128:
        raise CannotCheck("immutable bounded view and epoch required")
    for claim in view.claims:
        if type(claim) is not ShownClaim or type(claim.marker) is not str or claim.marker not in ("ASSERT", "HEDGE", "WITHHOLD"):
            raise CannotCheck("typed claim and marker required")
        if type(claim.citations) is not tuple or any(not identifier(c) for c in claim.citations) or len(set(claim.citations)) != len(claim.citations):
            raise CannotCheck("unique immutable citation identities required")
        validate_formula(claim.formula, registry)


def render(view, registry, *, codec="sentence"):
    validate_view(view, registry)
    if type(codec) is not str or codec not in ("sentence", "functional"):
        raise CannotCheck("registered codec required")
    encode = encode_sentence if codec == "sentence" else encode_functional
    return "\n".join(f"{c.marker}[{','.join(c.citations)}] :: {encode(c.formula, registry)}"
                     for c in view.claims if c.marker != "WITHHOLD")


def commitment_eligibility(text, view, registry, supports, *, current_epoch,
                           scope, codec="sentence", protected_seeds=(),
                           max_worlds=4096, max_steps=2_000_000):
    """No store write. Evidence/epoch/protected identities are external premises.

ASSERT requires every cited record to be LIVE, semantically matched, in scope,
and world-authorized. HEDGE reports uncertainty, never truth: its support must
be absent or include UNKNOWN; all-DEAD and all-LIVE mislabellings are rejected.
The caller must serialize a later real commitment with its evidence snapshot.
"""
    try:
        validate_view(view, registry)
        if not identifier(current_epoch) or current_epoch != view.epoch or not identifier(scope):
            raise CannotCheck("current evidence epoch or scope mismatch")
        if type(supports) is not tuple or type(protected_seeds) is not tuple or any(not _digest(s) for s in protected_seeds):
            raise CannotCheck("immutable evidence and protected identities required")
        if type(text) is not str or len(text) > 1_048_576 or type(codec) is not str or codec not in ("sentence", "functional"):
            raise CannotCheck("bounded actual text and registered codec required")
        evidence = {}
        for support in supports:
            if (type(support) is not Support or not identifier(support.evidence_id)
                    or not _digest(support.semantic_seed) or type(support.status) is not str
                    or support.status not in ("LIVE", "UNKNOWN", "DEAD")
                    or not identifier(support.scope) or type(support.world_authority) is not bool
                    or support.evidence_id in evidence):
                raise CannotCheck("malformed or duplicate evidence record")
            evidence[support.evidence_id] = support
        expected = tuple(c for c in view.claims if c.marker != "WITHHOLD")
        lines = text.split("\n") if text else []
        if len(lines) != len(expected):
            return GateResult("REFUSED", "actual assertion inventory differs from shown plan")
        decode = decode_sentence if codec == "sentence" else decode_functional
        for i, (line, claim) in enumerate(zip(lines, expected)):
            match = re.fullmatch(r"(ASSERT|HEDGE)\[([a-z0-9_,]*)\] :: (.+)", line)
            if match is None:
                raise CannotCheck("actual surface marker/citation framing is unrecognized")
            marker, citations, body = match.groups()
            refs = tuple(citations.split(",")) if citations else ()
            if marker != claim.marker or refs != claim.citations:
                return GateResult("REFUSED", "actual marker or citations changed", i)
            parsed = decode(body, registry)
            if parsed.status != "UNIQUE":
                raise CannotCheck("actual surface is ambiguous or outside the registered grammar")
            intended = meaning(claim.formula, registry, max_worlds=max_worlds, max_steps=max_steps)
            actual = meaning(parsed.candidates[0], registry, max_worlds=max_worlds, max_steps=max_steps)
            # Compare complete semantic objects, not caller-supplied digest claims.
            if actual != intended:
                return GateResult("REFUSED", "actual surface changes finite registered meaning", i)
            if intended.seed in protected_seeds:
                return GateResult("REFUSED", "protected semantic content", i)
            records = []
            for ref in refs:
                if ref not in evidence:
                    raise CannotCheck("cited evidence record missing")
                support = evidence[ref]
                if support.semantic_seed != intended.seed or support.scope != scope:
                    return GateResult("REFUSED", "citation supports another meaning or scope", i)
                records.append(support)
            if marker == "ASSERT":
                if not records or any(r.status != "LIVE" or not r.world_authority for r in records):
                    return GateResult("REFUSED", "assertion lacks current LIVE world authority", i)
            elif records and not any(r.status == "UNKNOWN" for r in records):
                return GateResult("REFUSED", "hedge lacks registered uncertainty", i)
        return GateResult("ELIGIBLE_FOR_EXTERNAL_COMMIT", "finite semantics and current evidence checked", len(expected))
    except CannotCheck as exc:
        return GateResult("CANNOT_CHECK", str(exc))
