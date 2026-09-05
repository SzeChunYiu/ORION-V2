"""Small deterministic replay, with checks active under python -O."""
import itertools
import json

from . import codecs as c
from . import semantics as s


def require(condition, message):
    if not condition:
        raise s.CannotCheck(message)


def main():
    try:
        reg = s.Registry((s.Sort("person", ("alice", "bob")),),
                         (s.Predicate("red", ("person",)), s.Predicate("likes", ("person", "person"))), "reference_v1")
        constants = (s.Term("const", "alice"), s.Term("const", "bob"))
        v0, v1 = s.Term("var", 0), s.Term("var", 1)
        formulas = [s.atom("red", t) for t in constants]
        formulas += [s.atom("likes", a, b) for a, b in itertools.product(constants, repeat=2)]
        formulas += [s.quantify(q, "person", s.quantify(p, "person", s.atom("likes", x, y)))
                     for q, p in itertools.product(("all", "some"), repeat=2)
                     for x, y in ((v0, v1), (v1, v0))]
        formulas += [s.negate(f) for f in tuple(formulas)]
        for formula in formulas:
            for encode, decode in ((c.encode_sentence, c.decode_sentence), (c.encode_functional, c.decode_functional)):
                result = decode(encode(formula, reg), reg)
                require(result.status == "UNIQUE" and result.candidates == (formula,), "codec roundtrip mismatch")
                require(s.meaning(result.candidates[0], reg) == s.meaning(formula, reg), "finite meaning mismatch")
        relation = s.Registry(reg.sorts, (reg.predicates[1],), "relation_v1")
        ae = s.quantify("all", "person", s.quantify("some", "person", s.atom("likes", v1, v0)))
        ea = s.quantify("some", "person", s.quantify("all", "person", s.atom("likes", v0, v1)))
        got_ae, got_ea = s.meaning(ae, relation), s.meaning(ea, relation)
        for mask in range(16):
            matrix = [[bool(mask & (1 << (2*x+y))) for y in range(2)] for x in range(2)]
            require(got_ae.truth_vector[mask] == all(any(row) for row in matrix), "forall-exists oracle mismatch")
            require(got_ea.truth_vector[mask] == any(all(matrix[x][y] for x in range(2)) for y in range(2)), "exists-forall oracle mismatch")
        require(got_ae != got_ea, "quantifier reversal was collapsed")
        print(json.dumps({"terminal": "FINITE_CODEC_REFERENCE_REVALIDATED", "roundtrip_formulas": len(formulas),
                          "codec_paths": 2, "independent_quantifier_worlds": 16,
                          "protected_codec_evaluation": "CANNOT_CHECK",
                          "unrestricted_language": "OPEN_RESEARCH"}, sort_keys=True))
        return 0
    except s.CannotCheck as exc:
        print(json.dumps({"terminal": "CANNOT_CHECK", "reason": str(exc)}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
