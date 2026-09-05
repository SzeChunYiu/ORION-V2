"""Finite calibration for the #202 F4 time-bounded invariance correction.

Registered binary-program transducers; no architecture comparison or novelty.
Exit 0 PASS; 1 a checked consequence fails; 2 CANNOT_CHECK outside this model.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import json


class CannotCheck(ValueError):
    pass


def natural(value, label, *, positive=False):
    if type(value) is not int or value < int(positive):
        raise CannotCheck(label + " must be an exact registered natural number")
    return value


@dataclass(frozen=True)
class Run:
    output: str
    description_bits: int
    ticks: int


def run(machine, program, *, output_cap=128):
    """Charge decoding, one output-write tick per bit, and explicit padding.

    0w emits literal binary w. 1bin(n) emits n zeros; bin(n) is canonical
    and nonempty. A charges 2n extra padding ticks; B charges none.
    The two machines have identical semantics on every valid program.
    """
    natural(output_cap, "output cap", positive=True)
    if machine not in ("A", "B"):
        raise CannotCheck("unregistered transducer")
    if type(program) is not str or len(program) < 2 or any(c not in "01" for c in program):
        raise CannotCheck("nonempty registered binary program required")
    if len(program) > output_cap + 1:
        raise CannotCheck("program exceeds registered materialization cap")
    if program[0] == "0":
        word = program[1:]
        padding = 0
    else:
        if program[1] != "1":
            raise CannotCheck("run length must have canonical positive binary encoding")
        n = int(program[1:], 2)
        if n > output_cap:
            raise CannotCheck("output exceeds registered materialization cap")
        word = "0" * n
        padding = 2 * n if machine == "A" else 0
    # All work counted by this abstract transducer's explicitly declared meter.
    # Python wall time, allocation and host decoding are not these machine ticks.
    decode_ticks = sum(1 for _ in program)
    write_ticks = sum(1 for _ in word)
    delay_ticks = sum(1 for _ in range(padding))
    return Run(word, len(program), decode_ticks + write_ticks + delay_ticks)


def programs_for_zero_word(n, *, output_cap=128):
    natural(n, "target length", positive=True)
    natural(output_cap, "output cap", positive=True)
    if n > output_cap:
        raise CannotCheck("target outside registered finite inventory")
    # These are all programs for this output under the two-mode grammar.
    return ("0" + "0" * n, "1" + format(n, "b"))


def minimum_bits(machine, n, time_bound, *, output_cap=128):
    natural(time_bound, "time bound")
    candidates = [run(machine, p, output_cap=output_cap)
                  for p in programs_for_zero_word(n, output_cap=output_cap)]
    feasible = [r.description_bits for r in candidates if r.ticks <= time_bound]
    return min(feasible) if feasible else None


def compiler_contract(source, target, source_programs, target_programs, *,
                      length_overhead, time_factor, output_cap=128):
    natural(length_overhead, "length overhead")
    natural(time_factor, "time factor", positive=True)
    if (type(source_programs) not in (tuple, list)
            or type(target_programs) not in (tuple, list)
            or not source_programs or len(source_programs) != len(target_programs)):
        raise CannotCheck("complete materialized paired compiler inventory required")
    for p, compiled in zip(source_programs, target_programs):
        a = run(source, p, output_cap=output_cap)
        b = run(target, compiled, output_cap=output_cap)
        if (a.output != b.output
                or b.description_bits > a.description_bits + length_overhead
                or b.ticks > time_factor * a.ticks):
            return False
    return True


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def calibrate(n_max=128):
    natural(n_max, "calibration size", positive=True)
    if n_max > 128:
        raise CannotCheck("registered calibration cap is 128")
    checked = violations = 0
    for n in range(1, n_max + 1):
        programs = programs_for_zero_word(n)
        for source, target in (("A", "B"), ("B", "A")):
            require(compiler_contract(source, target, programs, programs,
                                      length_overhead=0, time_factor=3),
                    "identity compiler does not satisfy its registered contract")
            t = 2*n + 1
            source_min = minimum_bits(source, n, t)
            target_min = minimum_bits(target, n, 3*t)
            require(source_min is not None and target_min is not None,
                    "registered target unexpectedly infeasible")
            require(target_min <= source_min, "directional compiler inequality failed")
            checked += len(programs)
        t = 2*n + 1
        a = minimum_bits("A", n, t)
        b = minimum_bits("B", n, 3*t)
        require(a == n+1 and b == 1+n.bit_length(),
                "complete two-mode optimum disagrees with the written witness")
        violations += int(abs(a-b) > 0)
    # Actual mutants: wrong compiled output and a false no-slowdown claim.
    require(not compiler_contract("A", "B", ("110",), ("111",),
                                  length_overhead=0, time_factor=3),
            "changed-output compiler mutant was not caught")
    require(not compiler_contract("B", "A", ("11",), ("11",),
                                  length_overhead=0, time_factor=1),
            "unearned factor-one runtime mutant was not caught")
    cap = n_max
    return {
        "terminal": "SCOPED_COMPILER_BOUND_CORRECTION_CALIBRATED",
        "registered_target_lengths": n_max,
        "directional_program_checks": checked,
        "absolute_bound_zero_overhead_violations": violations,
        "largest_registered_witness": {
            "n": cap, "source_time": 2*cap+1, "target_time": 3*(2*cap+1),
            "source_bits": cap+1, "target_bits": 1+cap.bit_length(),
            "gap": cap-cap.bit_length(), "compiler_description_overhead": 0,
            "both_runtime_factors": 3,
        },
        "changed_output_mutant_caught": True,
        "unearned_runtime_factor_mutant_caught": True,
        "unbounded_proof": "WRITTEN_ARGUMENT_ONLY",
        "old_F1_F3_outcomes_regenerated": False,
        "architecture_comparison": "NOT_PERFORMED",
        "independent_external_review": "NOT_OBTAINED",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-max", type=int, default=128)
    args = parser.parse_args(argv)
    try:
        result = calibrate(args.n_max)
    except CannotCheck as exc:
        print(json.dumps({"terminal": "CANNOT_CHECK", "reason": str(exc)}))
        return 2
    except AssertionError as exc:
        print(json.dumps({"terminal": "FAIL", "reason": str(exc)}))
        return 1
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

