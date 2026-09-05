"""Finite registered semantic-prefix safety; no natural-language completeness claim.

The inventory is a finite language *defined by enumeration*, with a separately
registered prefix interpretation table. A sample from an open language cannot
set closed=True without a separate completeness argument. Exit 0/1/2.
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
import hashlib
import json
import sys

LIVE, DEAD, UNKNOWN = "LIVE", "DEAD", "UNKNOWN"


class CannotCheck(ValueError):
    pass


@dataclass(frozen=True, order=True)
class Claim:
    proposition: str
    polarity: str = "POSITIVE"
    quantifier: str = "ATOMIC"
    modality: str = "ASSERT"
    citation: str = "NONE"


@dataclass(frozen=True)
class Completion:
    identity: str
    tokens: tuple[str, ...]
    meaning: frozenset[Claim]


@dataclass(frozen=True)
class Inventory:
    completions: tuple[Completion, ...]
    # One registered interpretation for each prefix. Full-surface ambiguity
    # must be resolved upstream or represented conservatively before freezing.
    prefix_meanings: tuple[tuple[tuple[str, ...], frozenset[Claim]], ...]
    epoch: str
    semantics_id: str
    closed: bool = False


@dataclass(frozen=True)
class PrefixState:
    inventory_digest: str
    prefix: tuple[str, ...] = ()
    committed: frozenset[Claim] = frozenset()


@dataclass(frozen=True)
class PrefixResult:
    status: str
    state: PrefixState
    compatible: tuple[str, ...] = ()
    invariant_meaning: frozenset[Claim] = frozenset()
    reason: str = ""


def _tokens(value):
    if type(value) is not tuple or any(type(t) is not str or not t for t in value):
        raise CannotCheck("tokens must be an immutable tuple of nonempty strings")
    return value


def _meaning(value):
    if type(value) is not frozenset:
        raise CannotCheck("meaning must be an immutable set of typed claims")
    for c in value:
        if (type(c) is not Claim or type(c.proposition) is not str or not c.proposition
                or c.polarity not in ("POSITIVE", "NEGATIVE")
                or c.quantifier not in ("ATOMIC", "ALL", "SOME", "NONE", "NOT_ALL")
                or c.modality not in ("ASSERT", "POSSIBLE")
                or type(c.citation) is not str or not c.citation):
            raise CannotCheck("unresolved or malformed typed claim")
    return value


def _claim_rows(meaning):
    return [(c.proposition, c.polarity, c.quantifier, c.modality, c.citation)
            for c in sorted(meaning)]


def inventory_digest(inventory):
    """Content binding, not authority that supplied semantics is correct."""
    if type(inventory) is not Inventory:
        raise CannotCheck("registered finite inventory required")
    if any(type(s) is not str or not s for s in (inventory.epoch, inventory.semantics_id)):
        raise CannotCheck("epoch and semantic representation identities required")
    if type(inventory.closed) is not bool:
        raise CannotCheck("closure declaration must be boolean")
    if type(inventory.completions) is not tuple or type(inventory.prefix_meanings) is not tuple:
        raise CannotCheck("immutable finite inventory required")
    ids, required_prefixes, completion_rows = set(), {()}, []
    for completion in inventory.completions:
        if type(completion) is not Completion or type(completion.identity) is not str or not completion.identity:
            raise CannotCheck("invalid completion identity")
        if completion.identity in ids:
            raise CannotCheck("duplicate completion identity")
        ids.add(completion.identity)
        tokens, meaning = _tokens(completion.tokens), _meaning(completion.meaning)
        required_prefixes.update(tokens[:i] for i in range(len(tokens) + 1))
        completion_rows.append((completion.identity, tokens, _claim_rows(meaning)))
    table = {}
    for row in inventory.prefix_meanings:
        if type(row) is not tuple or len(row) != 2:
            raise CannotCheck("invalid prefix interpretation row")
        prefix, meaning = _tokens(row[0]), _meaning(row[1])
        if prefix in table:
            raise CannotCheck("duplicate prefix interpretation")
        table[prefix] = meaning
    if set(table) != required_prefixes or table.get(()) != frozenset():
        raise CannotCheck("complete registered prefix interpretation table required")
    if any(table[c.tokens] != c.meaning for c in inventory.completions):
        raise CannotCheck("full surface meaning unresolved or inconsistent")
    payload = [inventory.epoch, inventory.semantics_id, inventory.closed,
               sorted(completion_rows),
               [(p, _claim_rows(table[p])) for p in sorted(table)]]
    return hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()


def safe_prefix(inventory, state, emission, liveness, authorized, *, max_completions=10000):
    """Advance only if every intermediate emitted prefix preserves its commitments.

    A whole chunk is transactional. A rejected chunk leaves the original state.
    Already-emitted commitments cannot be removed by a later correction.
    """
    try:
        if type(state) is not PrefixState:
            raise CannotCheck("registered residual state required")
        if (type(state.inventory_digest) is not str or len(state.inventory_digest) != 64
                or any(c not in "0123456789abcdef" for c in state.inventory_digest)):
            raise CannotCheck("canonical SHA-256 inventory identity required")
        _tokens(state.prefix)
        _meaning(state.committed)
        emission = _tokens(emission)
        if type(max_completions) is not int or max_completions < 0:
            raise CannotCheck("nonnegative completion budget required")
        if type(inventory) is not Inventory or type(inventory.completions) is not tuple:
            raise CannotCheck("registered finite inventory required")
        if len(inventory.completions) > max_completions:
            raise CannotCheck("completion enumeration budget exhausted")
        actual = inventory_digest(inventory)
        if actual != state.inventory_digest:
            raise CannotCheck("inventory, semantics or epoch identity drift")
        if inventory.closed is not True:
            raise CannotCheck("completion inventory not established closed")
        if not isinstance(liveness, Mapping) or type(authorized) is not frozenset:
            raise CannotCheck("explicit warrant and authority state required")
        _meaning(authorized)
        table = dict(inventory.prefix_meanings)
        # A resumed state must retain every interpretation exposed along its
        # emitted history, even if the current interpretation changed later.
        if state.prefix not in table:
            raise CannotCheck("resumed prefix is outside the registered inventory")
        history = frozenset().union(*(table[state.prefix[:i]] for i in range(len(state.prefix) + 1)))
        if state.committed != history:
            raise CannotCheck("resumed commitment history is missing or forged")
        historical_claims = frozenset()
        for i in range(len(state.prefix) + 1):
            past = state.prefix[:i]
            past_completions = tuple(c for c in inventory.completions if c.tokens[:i] == past)
            if not past_completions:
                return PrefixResult("NO_ADMISSIBLE_COMPLETION", state, reason="registered residual language is empty")
            historical_claims |= table[past]
            if any(not historical_claims <= c.meaning for c in past_completions):
                return PrefixResult("HISTORY_CONFLICT", state, reason="resumed history passed an unsafe intermediate prefix")
        current, committed = state.prefix, state.committed
        points = ((),) if not emission else tuple((token,) for token in emission)
        for piece in points:
            current += piece
            compatible = tuple(c for c in inventory.completions if c.tokens[:len(current)] == current)
            if not compatible:
                return PrefixResult("NO_ADMISSIBLE_COMPLETION", state, reason="registered residual language is empty")
            common = frozenset.intersection(*(c.meaning for c in compatible))
            proposed = committed | table[current]
            if not committed <= common:
                return PrefixResult("HISTORY_CONFLICT", state, reason="later completion cannot erase emitted claims")
            if not proposed <= common:
                return PrefixResult("UNSAFE_SEMANTIC_VARIATION", state,
                                    tuple(c.identity for c in compatible), common,
                                    "a compatible completion changes a committed semantic field")
            for claim in proposed:
                if claim not in liveness or liveness[claim] not in (LIVE, DEAD, UNKNOWN):
                    raise CannotCheck("missing or invalid current warrant status")
                if liveness[claim] != LIVE:
                    return PrefixResult("UNSAFE_WARRANT", state, reason="committed proposition is not LIVE")
                if claim not in authorized:
                    return PrefixResult("UNSAFE_AUTHORITY", state, reason="commit authority is absent")
            committed = proposed
        new_state = PrefixState(actual, current, committed)
        return PrefixResult("SAFE_PREFIX", new_state, tuple(c.identity for c in compatible), common)
    except CannotCheck as exc:
        return PrefixResult("CANNOT_CHECK", state, reason=str(exc))


def paired_fixture(kind):
    """Constructed finite semantics; labels are fixtures, not an NLP evaluation."""
    original = Claim("treatment helps", quantifier="ALL", citation="study-A")
    variants = {
        "garden_path": Claim("treatment is the subject of a report", quantifier="ALL", citation="study-A"),
        "late_negation": Claim("treatment helps", "NEGATIVE", "ALL", "ASSERT", "study-A"),
        "quantifier_reversal": Claim("treatment helps", quantifier="SOME", citation="study-A"),
        "citation_replacement": Claim("treatment helps", quantifier="ALL", citation="study-B"),
        "correction": Claim("treatment helps", "NEGATIVE", "NONE", "ASSERT", "study-A"),
        "hedge": Claim("treatment helps", quantifier="ALL", modality="POSSIBLE", citation="study-A"),
        "no_alarm": original,
    }
    changed = variants[kind]
    completions = (Completion("keep", ("claim", "keep"), frozenset({original})),
                   Completion("revise", ("claim", "revise"), frozenset({changed})))
    table = (((), frozenset()), (("claim",), frozenset({original})),
             (("claim", "keep"), frozenset({original})),
             (("claim", "revise"), frozenset({changed})))
    inventory = Inventory(completions, table, "fixture-epoch-1", "typed-claim-v1", True)
    return inventory, original, changed


def check_meg27():
    caught = []
    for kind in ("garden_path", "late_negation", "quantifier_reversal", "citation_replacement", "correction", "hedge"):
        inventory, original, changed = paired_fixture(kind)
        state = PrefixState(inventory_digest(inventory))
        live = {original: LIVE, changed: LIVE}
        authorized = frozenset(live)
        result = safe_prefix(inventory, state, ("claim",), live, authorized)
        assert result.status == "UNSAFE_SEMANTIC_VARIATION"
        # Parent C3's existential SAT criterion accepts the 'keep' completion.
        assert any(original in c.meaning for c in inventory.completions)
        # Sending an entire safe-looking completion cannot hide an unsafe
        # intermediate token already observed by a streaming reader.
        assert safe_prefix(inventory, state, ("claim", "keep"), live, authorized).status == "UNSAFE_SEMANTIC_VARIATION"
        caught.append(kind)
    inventory, claim, _ = paired_fixture("no_alarm")
    state = PrefixState(inventory_digest(inventory))
    result = safe_prefix(inventory, state, ("claim",), {claim: LIVE}, frozenset({claim}))
    assert result.status == "SAFE_PREFIX" and result.state.committed == {claim}
    assert safe_prefix(inventory, result.state, ("keep",), {claim: LIVE}, frozenset({claim})).status == "SAFE_PREFIX"
    assert safe_prefix(inventory, state, ("claim",), {claim: UNKNOWN}, frozenset({claim})).status == "UNSAFE_WARRANT"
    assert safe_prefix(inventory, state, ("claim",), {claim: LIVE}, frozenset()).status == "UNSAFE_AUTHORITY"
    assert safe_prefix(inventory, state, ("claim",), {claim: LIVE}, frozenset({claim}), max_completions=1).status == "CANNOT_CHECK"
    return {"terminal": "SAFE_PREFIX_CRITERION", "scope": "CLOSED_FINITE_REGISTERED_SEMANTICS",
            "semantic_mutants_caught": caught, "universal_not_existential": True,
            "intermediate_prefixes_checked": True, "GENERAL_NOVELTY": "NOT_ESTABLISHED"}


def main():
    try:
        if sys.flags.optimize:
            raise CannotCheck("assertions disabled by optimized Python")
        result = check_meg27()
    except CannotCheck as exc:
        print(json.dumps({"status": "CANNOT_CHECK", "reason": str(exc)}, sort_keys=True))
        return 2
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc), "type": type(exc).__name__}, sort_keys=True))
        return 1
    print(json.dumps({"status": "PASS", "result": result}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
