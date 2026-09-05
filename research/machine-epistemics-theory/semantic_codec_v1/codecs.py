"""Two separate bounded grammar codecs sharing only typed AST semantics.

Sentence codec: recursive descent over whitespace/punctuation tokens.
Functional codec: character-cursor parser over a distinct prefix grammar.
Neither decoder consults an encoder, roundtrip lookup table, or gold answer.
"""
from __future__ import annotations

from dataclasses import dataclass
import itertools
import re

from .semantics import (CannotCheck, Formula, Term, atom, conjunction, negate,
                        positive, quantify, validate_formula, validate_registry)


@dataclass(frozen=True, slots=True)
class ParseResult:
    status: str
    candidates: tuple[Formula, ...] = ()
    reason: str = ""


def _term_text(t):
    return "@" + str(t.value) if t.kind == "var" else t.value


def encode_sentence(formula, registry):
    validate_formula(formula, registry)

    def emit(f):
        if f.op == "atom":
            terms = [_term_text(t) for t in f.terms]
            return f"{terms[0]} is {f.name}" if len(terms) == 1 else f"{terms[0]} {f.name} {terms[1]}"
        if f.op == "not":
            return "it is false that ( " + emit(f.children[0]) + " )"
        if f.op == "and":
            return "( " + emit(f.children[0]) + " ) and ( " + emit(f.children[1]) + " )"
        return ("every" if f.op == "all" else "some") + f" {f.name} : ( " + emit(f.children[0]) + " )"
    return emit(formula)


def decode_sentence(text, registry, *, max_candidates=128, max_chars=8192):
    try:
        validate_registry(registry)
        if not positive(max_candidates) or not positive(max_chars) or type(text) is not str or len(text) > max_chars:
            raise CannotCheck("invalid surface or parser budget")
        # Full coverage check rejects silently ignored punctuation/control text.
        pattern = r"@[0-9]+|[a-z][a-z0-9_]*|[():]"
        tokens = re.findall(pattern, text)
        if re.sub(r"\s+", "", text) != "".join(tokens):
            raise CannotCheck("surface outside registered sentence grammar")
        at = 0

        def take(expected=None):
            nonlocal at
            if at >= len(tokens) or (expected is not None and tokens[at] != expected):
                raise CannotCheck("incomplete or malformed sentence")
            token = tokens[at]
            at += 1
            return token

        def term():
            token = take()
            return Term("var", int(token[1:])) if token.startswith("@") else Term("const", token)

        def bounded(items):
            result = []
            for item in items:
                if item not in result:
                    result.append(item)
                if len(result) > max_candidates:
                    raise CannotCheck("ambiguity inventory budget exhausted")
            return tuple(result)

        def parse(depth=0):
            if depth > 24 or at >= len(tokens):
                raise CannotCheck("sentence nesting budget exhausted or missing phrase")
            lead = tokens[at]
            if lead in ("every", "some"):
                kind = "all" if take() == "every" else "some"
                sort = take()
                take(":")
                take("(")
                bodies = parse(depth + 1)
                take(")")
                return bounded(quantify(kind, sort, body) for body in bodies)
            if lead == "it":
                for word in ("it", "is", "false", "that", "("):
                    take(word)
                bodies = parse(depth + 1)
                take(")")
                return bounded(negate(body) for body in bodies)
            if lead == "(":
                take("(")
                left = parse(depth + 1)
                for word in (")", "and", "("):
                    take(word)
                right = parse(depth + 1)
                take(")")
                return bounded(conjunction(a, b) for a, b in itertools.product(left, right))
            first = term()
            relation = take()
            if relation == "is":
                word, args = take(), (first,)
            else:
                word, args = relation, (first, term())
            options = bounded(atom(p.name, *args) for p in registry.predicates
                              if len(p.sorts) == len(args) and word in (p.name,) + p.aliases)
            if not options:
                raise CannotCheck("unregistered predicate spelling")
            return options

        candidates = parse()
        if at != len(tokens):
            raise CannotCheck("trailing unparsed surface")
        # Type constraints may eliminate a parse; ranking never eliminates one.
        valid = []
        for candidate in candidates:
            try:
                validate_formula(candidate, registry)
                valid.append(candidate)
            except CannotCheck:
                continue
        if not valid:
            raise CannotCheck("no well-typed closed reading")
        return ParseResult("UNIQUE" if len(valid) == 1 else "AMBIGUOUS", tuple(valid))
    except (CannotCheck, ValueError) as exc:
        return ParseResult("CANNOT_CHECK", reason=str(exc))


def encode_functional(formula, registry):
    validate_formula(formula, registry)

    def emit(f):
        if f.op == "atom":
            return f.name + "(" + ",".join(_term_text(t) for t in f.terms) + ")"
        if f.op == "not":
            return "neg{" + emit(f.children[0]) + "}"
        if f.op == "and":
            return "conj{" + ";".join(emit(c) for c in f.children) + "}"
        return f.op + "[" + f.name + "]{" + emit(f.children[0]) + "}"
    return emit(formula)


def decode_functional(text, registry, *, max_chars=8192):
    try:
        validate_registry(registry)
        if not positive(max_chars) or type(text) is not str or len(text) > max_chars:
            raise CannotCheck("invalid functional surface or budget")
        cursor = 0

        def consume(literal):
            nonlocal cursor
            if not text.startswith(literal, cursor):
                raise CannotCheck("functional grammar delimiter mismatch")
            cursor += len(literal)

        def name():
            nonlocal cursor
            match = re.match(r"[a-z][a-z0-9_]*", text[cursor:])
            if match is None:
                raise CannotCheck("functional identifier required")
            cursor += len(match.group())
            return match.group()

        def argument():
            nonlocal cursor
            if cursor < len(text) and text[cursor] == "@":
                cursor += 1
                match = re.match(r"[0-9]+", text[cursor:])
                if match is None:
                    raise CannotCheck("variable index required")
                cursor += len(match.group())
                return Term("var", int(match.group()))
            return Term("const", name())

        def formula(depth=0):
            if depth > 24:
                raise CannotCheck("functional nesting budget exhausted")
            operator = name()
            if operator in ("all", "some") and text[cursor:cursor + 1] == "[":
                consume("[")
                sort = name()
                consume("]{")
                body = formula(depth + 1)
                consume("}")
                return quantify(operator, sort, body)
            if operator in ("neg", "conj") and text[cursor:cursor + 1] == "{":
                consume("{")
                left = formula(depth + 1)
                if operator == "conj":
                    consume(";")
                    right = formula(depth + 1)
                consume("}")
                return negate(left) if operator == "neg" else conjunction(left, right)
            consume("(")
            args = [argument()]
            if text[cursor:cursor + 1] == ",":
                consume(",")
                args.append(argument())
            consume(")")
            return atom(operator, *args)

        result = formula()
        if cursor != len(text):
            raise CannotCheck("trailing functional surface")
        validate_formula(result, registry)
        return ParseResult("UNIQUE", (result,))
    except (CannotCheck, ValueError) as exc:
        return ParseResult("CANNOT_CHECK", reason=str(exc))
