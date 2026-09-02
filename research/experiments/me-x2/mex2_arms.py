"""ME-X2 arms (frozen with design V1).  Every arm sees only the public instance,
its own trajectory and the remaining budget.  No arm imports the oracle.

Baselines: B0 retry, B1 threshold abstention, B2 ARFT-equivalent taxonomy,
B3 model-based diagnosis + myopic VoI, B4 MDA-style criticism -> expansion,
B5 strongest faithful federation = exact expected-cost planner + tau abstention
over the diagnostic modules, with the H-EXT-3 interface ladder (rungs 1-5).
M = ORION reference semantics: ``assess_discrepancy_locus`` (locus receipt with
the diagnostic-evaluator gate), ``route_frontier_action`` (witnessed obstruction,
lower-level disposition) and ``JumpTrigger``/``JumpProposal``/``assess_jump``/
``minimum_level`` (minimum-level policy).  Ablations and controls per protocol.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable

from orion_v2.epistemic_architecture import CapabilityContext, EpistemicAction, FrontierEpisode, FrontierObstruction, FrontierRouteStatus, route_frontier_action
from orion_v2.jump import JumpAssessment, JumpLevel, JumpProposal, JumpTrigger, TriggerKind, assess_jump, minimum_level
from orion_v2.ontic_epistemic_boundary import DiscrepancyLocus, LocusDiagnosisEvidence, LocusDiagnosisStatus, LocusHypothesis, assess_discrepancy_locus

from mex2_model import CLASSES, LOCI, RECURRENCE, Action, Intervention, Probe
from mex2_oracle import ArmView
from mex2_parents import FAILURE_PENALTY_MULTIPLIER, TAU, Abstention, ConsistencyDiagnosis, ExactPlanner, MDARule, MyopicVoI, TaxonomyClassifier, min_separating_total, uniform_mass

STOP = Action("STOP")
DECLARE_KIND = "DECLARE_CANNOT_IDENTIFY"


def _argmax_label(live: tuple[str, ...], label_of: Callable[[str], str], order: tuple[str, ...]) -> tuple[str, float]:
    mass: dict[str, float] = {}
    for c in live:
        mass[label_of(c)] = mass.get(label_of(c), 0.0) + 1.0 / len(live)
    best = max(mass, key=lambda k: (mass[k], -(order.index(k) if k in order else 10 ** 6)))
    return best, mass[best]


class Policy:
    name = "POLICY"
    designed_tables = False       # trust the scientific evaluator (ladder rungs < 5)
    use_dispositions = True       # feed intervention outcomes back into the candidate set

    def __init__(self, seed: str) -> None:
        self.seed = seed

    # registered-information helpers ------------------------------------------------------------
    def cls_of(self, view: ArmView, c: str) -> str:
        return view.inst.cause(c).obstruction_class

    def locus_of(self, view: ArmView, c: str) -> str:
        return view.inst.cause(c).locus

    def fix_of(self, view: ArmView, c: str) -> Intervention | None:
        return view.inst.min_fix(c)

    def live(self, view: ArmView) -> tuple[str, ...]:
        obs = []
        for s in view.steps:
            if s.action.kind == "PROBE":
                obs.append((view.inst.probe(s.action.target), s.outcome))
            elif s.action.kind == "INTERVENE" and self.use_dispositions:
                obs.append((view.inst.intervention(s.action.target), s.outcome))
        return ConsistencyDiagnosis.candidates(view.inst.live_ids(), obs, designed=self.designed_tables)

    def applied(self, view: ArmView) -> set[str]:
        return {s.action.target for s in view.steps if s.action.kind == "INTERVENE"}

    def declare(self, view: ArmView, live: tuple[str, ...], kind: str, target: str | None = None) -> Action:
        if not live:
            return Action(kind, target, "CANNOT_IDENTIFY", "CANNOT_IDENTIFY", 0.0)
        cls, conf = _argmax_label(live, lambda c: self.cls_of(view, c), CLASSES)
        loc, _ = _argmax_label(live, lambda c: self.locus_of(view, c), LOCI)
        return Action(kind, target, cls, loc, conf)

    def cannot_identify(self, view: ArmView, live: tuple[str, ...]) -> Action:
        classes = {self.cls_of(view, c) for c in live}; loci = {self.locus_of(view, c) for c in live}
        cls, conf = _argmax_label(live, lambda c: self.cls_of(view, c), CLASSES) if live else ("CANNOT_IDENTIFY", 0.0)
        return Action(DECLARE_KIND, None, cls if len(classes) == 1 else "CANNOT_IDENTIFY", loci.pop() if len(loci) == 1 else "CANNOT_IDENTIFY", conf if len(classes) == 1 else 0.0)

    def splits(self, view: ArmView, p: Probe, live: tuple[str, ...]) -> bool:
        f = p.designed_outcome if self.designed_tables else p.outcome
        return len({f(c) for c in live}) > 1

    def act(self, view: ArmView) -> Action:  # pragma: no cover - abstract
        raise NotImplementedError


# ---- B0 --------------------------------------------------------------------------------------------

class B0RetrySearch(Policy):
    name = "B0_RETRY_SEARCH"
    MAX_RETRIES = 3

    def act(self, view: ArmView) -> Action:
        n = len([s for s in view.steps if s.action.kind == "INTERVENE"])
        if n >= self.MAX_RETRIES:
            return STOP
        cands = sorted(view.affordable_interventions(), key=lambda i: (i.level, i.cost, i.intervention_id))
        if not cands:
            return STOP
        return Action("INTERVENE", cands[0].intervention_id, "SEARCH_INSUFFICIENT", "PROCESS_TOOL_WORKFLOW", None)


# ---- B1 --------------------------------------------------------------------------------------------

class B1UncertaintyAbstention(Policy):
    name = "B1_UNCERTAINTY_ABSTENTION"

    def act(self, view: ArmView) -> Action:
        live = self.live(view)
        ab = Abstention(TAU)
        cls, conf = ab.decide(live, lambda c: self.cls_of(view, c))
        if cls is not None:
            fixes = {self.fix_of(view, c).intervention_id for c in live if self.cls_of(view, c) == cls and self.fix_of(view, c)}
            if len(fixes) == 1:
                iv = view.inst.intervention(fixes.pop())
                if iv.cost <= view.budget_left and iv.intervention_id not in self.applied(view):
                    return self.declare(view, live, "INTERVENE", iv.intervention_id)
        probes = sorted([p for p in view.affordable_probes() if p.probe_id not in view.probes_run()], key=lambda p: (p.cost, p.probe_id))
        if probes:
            return Action("PROBE", probes[0].probe_id)
        return self.cannot_identify(view, live)


# ---- B2 --------------------------------------------------------------------------------------------

class B2FailureTaxonomy(Policy):
    name = "B2_FAILURE_TAXONOMY_DIAGNOSIS"

    def act(self, view: ArmView) -> Action:
        order = TaxonomyClassifier.escalation_order(view.inst.interventions, view.inst.pattern)
        done = self.applied(view)
        for iv in order:
            if iv.intervention_id in done or iv.cost > view.budget_left:
                continue
            cls = view.inst.apparent_class if not done else next((self.cls_of(view, c) for c in view.inst.live_ids() if self.fix_of(view, c) and self.fix_of(view, c).intervention_id == iv.intervention_id), view.inst.apparent_class)
            loc = next((self.locus_of(view, c) for c in view.inst.live_ids() if self.cls_of(view, c) == cls), "CANNOT_IDENTIFY")
            return Action("INTERVENE", iv.intervention_id, cls, loc, None)
        return STOP


# ---- B3 / B4 -----------------------------------------------------------------------------------------

class B3ModelBasedDiagnosisVoI(Policy):
    name = "B3_MODEL_BASED_DIAGNOSIS_VOI"

    def act(self, view: ArmView) -> Action:
        live = self.live(view)
        F = FAILURE_PENALTY_MULTIPLIER * float(view.inst.budget)
        voi = MyopicVoI(F)
        untried = [i for i in view.affordable_interventions() if i.intervention_id not in self.applied(view)]
        if len(live) == 1:
            fix = self.fix_of(view, live[0])
            if fix and fix.cost <= view.budget_left and fix.intervention_id not in self.applied(view):
                return self.declare(view, live, "INTERVENE", fix.intervention_id)
            return STOP
        probes = [p for p in view.affordable_probes() if p.probe_id not in view.probes_run()]
        scored = sorted(((voi.value(p, live, untried, designed=self.designed_tables), p) for p in probes), key=lambda t: (-t[0], t[1].cost, t[1].probe_id))
        if scored and scored[0][0] > 1e-9:
            return Action("PROBE", scored[0][1].probe_id)
        best, v = voi.best_act(live, untried)
        if best is not None and v < F:
            return self.declare(view, tuple(c for c in live if c in best.resolves) or live, "INTERVENE", best.intervention_id)
        return self.cannot_identify(view, live)


class B4MDAModelExpansion(B3ModelBasedDiagnosisVoI):
    name = "B4_MDA_MODEL_EXPANSION"

    def act(self, view: ArmView) -> Action:
        live = self.live(view)
        crit = MDARule.criticism_probes(view.inst.probes)
        run = view.probes_run()
        rejected = any(s.action.kind == "PROBE" and s.action.target in {p.probe_id for p in crit} and s.outcome in MDARule.REJECT for s in view.steps)
        if len(live) > 1:
            if MDARule.should_expand(live, lambda c: self.locus_of(view, c), rejected):
                for iv in sorted(view.inst.interventions, key=lambda i: (i.cost, i.intervention_id)):
                    if iv.level == 2 and iv.intervention_id not in self.applied(view) and iv.cost <= view.budget_left and any(c in iv.resolves and self.locus_of(view, c) == "EPISTEMIC_MODEL" for c in live):
                        return Action("INTERVENE", iv.intervention_id, "MODEL_FAMILY_INADEQUATE", "EPISTEMIC_MODEL", uniform_mass(live, iv.resolves))
            for p in sorted(crit, key=lambda p: p.cost):
                if p.probe_id not in run and p.cost <= view.budget_left and self.splits(view, p, live):
                    return Action("PROBE", p.probe_id)
        return super().act(view)


# ---- B5 federation ladder ---------------------------------------------------------------------------

class Federation(Policy):
    """rung 1 verdict only; 2 +candidate set; 3 +discriminator tables; 4 +disposition records; 5 +evaluator contract."""
    name = "B5_STRONGEST_FAITHFUL_PARENT_FEDERATION"
    rung = 5
    tau: float | None = TAU

    def __init__(self, seed: str) -> None:
        super().__init__(seed)
        self.designed_tables = self.rung < 5
        self.use_dispositions = self.rung >= 4

    def _greedy_probe(self, view: ArmView, live: tuple[str, ...]) -> Action | None:
        cands = sorted([p for p in view.affordable_probes() if p.probe_id not in view.probes_run() and self.splits(view, p, live)], key=lambda p: (p.cost, p.probe_id))
        return Action("PROBE", cands[0].probe_id) if cands else None

    def act(self, view: ArmView) -> Action:
        live = self.live(view)
        done = self.applied(view)
        F = FAILURE_PENALTY_MULTIPLIER * float(view.inst.budget)
        if not live:
            return STOP
        if self.rung <= 2:
            if len(live) > 1:
                pa = self._greedy_probe(view, live)
                if pa:
                    return pa
            if self.rung == 1:
                verdict, _ = _argmax_label(live, lambda c: self.cls_of(view, c), CLASSES)
                fixes = [self.fix_of(view, c) for c in live if self.cls_of(view, c) == verdict and self.fix_of(view, c)]
                fixes = sorted([f for f in fixes if f.intervention_id not in done and f.cost <= view.budget_left], key=lambda f: (f.level, f.cost, f.intervention_id))
                loc = next(self.locus_of(view, c) for c in live if self.cls_of(view, c) == verdict)
                return Action("INTERVENE", fixes[0].intervention_id, verdict, loc, None) if fixes else STOP
            # rung 2: candidate set exported -> tau gate + expected-cost choice, no planning, no feedback
            voi = MyopicVoI(F)
            adm = [i for i in view.affordable_interventions() if i.intervention_id not in done and (i.level <= 1 or uniform_mass(live, i.resolves) >= self.tau)]
            best, v = voi.best_act(live, adm)
            if best is not None and v < F:
                return self.declare(view, tuple(c for c in live if c in best.resolves) or live, "INTERVENE", best.intervention_id)
            return self.cannot_identify(view, live)
        planner = ExactPlanner(view.inst.probes, view.inst.interventions, F, tau=self.tau, designed=self.designed_tables)
        v, a = planner.value(live, frozenset(view.probes_run()), frozenset(done), view.budget_left)
        if a is None:
            return self.cannot_identify(view, live)
        if a[0] == "PROBE":
            return Action("PROBE", a[1])
        iv = view.inst.intervention(a[1])
        return self.declare(view, tuple(c for c in live if c in iv.resolves) or live, "INTERVENE", iv.intervention_id)


class B5R1(Federation):
    name = "B5_R1_VERDICT_ONLY"; rung = 1


class B5R2(Federation):
    name = "B5_R2_PLUS_CANDIDATE_SET"; rung = 2


class B5R3(Federation):
    name = "B5_R3_PLUS_DISCRIMINATOR_TABLES"; rung = 3


class B5R4(Federation):
    name = "B5_R4_PLUS_DISPOSITION_RECORDS"; rung = 4


class B5NoAbstention(Federation):
    name = "B5_NO_ABSTENTION_GATE"; rung = 5; tau = None


# ---- M ---------------------------------------------------------------------------------------------------

_CTX = CapabilityContext(("env:me-x2",), ("task:locus-diagnosis",), ("resource:registered-budget",), ("boundary:public-instance",), ("interface:registered-tables",), ("timescale:episode",), ("criterion:oracle-minimal-level",))
_LEVEL_ACTION = {0: EpistemicAction.MEASURE, 1: EpistemicAction.REASON, 2: EpistemicAction.CHANGE_MODEL, 3: EpistemicAction.CHANGE_REPRESENTATION, 4: EpistemicAction.REFORMULATE_PROBLEM, 5: EpistemicAction.BUILD_TOOL, 6: EpistemicAction.CHANGE_WORKFLOW}
_LEVEL_TRIGGER = {2: TriggerKind.MODEL_FAMILY_INADEQUACY, 3: TriggerKind.EXPRESSIVE_CEILING, 4: TriggerKind.SEMANTIC_OR_SCALE_DRIFT, 5: TriggerKind.STRUCTURAL_NONIDENTIFIABILITY, 6: TriggerKind.REPEATED_PROTECTED_RESIDUAL}
_ORION_LOCUS = {loc: DiscrepancyLocus(loc) for loc in LOCI if loc in DiscrepancyLocus.__members__}
_ORION_LOCUS["NO_MATERIAL_DISCREPANCY"] = DiscrepancyLocus.EVALUATOR_VALIDATION  # witnessed plateau is evaluator-side; the study locus vocabulary keeps NO_MATERIAL_DISCREPANCY


class MLocusMinimumEscalation(Policy):
    name = "M_ME_LOCUS_PLUS_MINIMUM_ESCALATION"
    # ablation switches
    probing = True
    gate = True
    lower_level_disposition = True
    prospective_discriminator = True
    always_escalate = False
    never_escalate = False
    max_level = 6

    def __init__(self, seed: str) -> None:
        super().__init__(seed)
        self.jump_receipts: list[dict] = []

    # --- registered semantics -------------------------------------------------------------------
    def _receipt(self, view: ArmView, live: tuple[str, ...], adequate: bool):
        all_ids = view.inst.live_ids()
        hyps = tuple(LocusHypothesis(f"h:{c}", _ORION_LOCUS[self.locus_of(view, c)], (f"w:{view.inst.symptom}",), tuple(f"d:{p.probe_id}" for p in view.inst.probes if self.splits(view, p, all_ids)) or ("d:registered-resolves",), (f"f:{c}",)) for c in all_ids)
        supported = tuple(f"h:{c}" for c in live) if len(live) == 1 else ()
        unresolved = tuple(f"h:{c}" for c in live) if len(live) > 1 else ()
        defeated = tuple(f"h:{c}" for c in all_ids if c not in live)
        ev = LocusDiagnosisEvidence((f"w:{view.inst.symptom}",), supported, defeated, unresolved, adequate)
        return assess_discrepancy_locus(hyps, ev)

    def _dispositions(self, view: ArmView, live: tuple[str, ...]) -> tuple[bool, tuple[str, ...]]:
        """Every registered lower-level (<=1) intervention must be tried or semantically excluded."""
        ids: list[str] = []; complete = True
        cheap = [i for i in view.inst.interventions if i.is_cheap]
        if not cheap:
            ids.append("disp:no-lower-level-intervention-registered")
        for i in cheap:
            if i.intervention_id in self.applied(view):
                ids.append(f"disp:tried-recurred:{i.intervention_id}")
            elif not any(c in i.resolves for c in live):
                ids.append(f"disp:semantically-excluded:{i.intervention_id}")
            elif i.cost > view.budget_left:
                ids.append(f"disp:unaffordable:{i.intervention_id}")
            else:
                complete = False
        return complete, tuple(ids)

    def _escalate(self, view: ArmView, live: tuple[str, ...], candidates: list[Intervention], declared_live: tuple[str, ...]) -> Action:
        """Route a level>=2 intervention through witnessed obstruction + Jump semantics; choose the minimum level."""
        complete, disp = self._dispositions(view, live)
        obstruction = FrontierObstruction(f"obs:{view.inst.instance_id}", view.inst.instance_id, (f"w:{view.inst.symptom}",) + tuple(f"w:{s.action.target}={s.outcome}" for s in view.steps if s.outcome is not None),
                                          tuple(f"h:{c}" for c in live), tuple(f"d:{p}" for p in view.probes_run()) or ("d:registered-resolves",), disp if complete else ())
        episode = FrontierEpisode(f"ep:{view.inst.instance_id}", view.inst.instance_id, _CTX, obstruction, tuple(EpistemicAction))
        route = route_frontier_action(episode, _LEVEL_ACTION[candidates[0].level])
        if route.status is not FrontierRouteStatus.JUMP_ASSESSMENT_REQUIRED:
            self.jump_receipts.append({"route": route.status.value})
            return None  # caller falls back (lower level unresolved)
        incumbent = JumpLevel(1 if any(i.is_cheap for i in view.inst.interventions) else 0)
        proposals = []
        for iv in candidates:
            trig = JumpTrigger(f"trig:{iv.intervention_id}", _LEVEL_TRIGGER[iv.level], incumbent, obstruction.witness_ids, disp)
            proposals.append(JumpProposal(f"prop:{iv.intervention_id}", trig, JumpLevel(iv.level), iv.kind, (f"parent:{iv.kind}",), tuple(f"corr:{c}" for c in live), ("preserve:registered-criterion",), (f"contract:resolves:{','.join(iv.resolves)}",), (f"falsifier:recurrence-after:{iv.intervention_id}",)))
        chosen = minimum_level(tuple(proposals))
        verdict = assess_jump(chosen, lower_level_sufficient=False, donor_product_ties=False)
        self.jump_receipts.append({"route": route.status.value, "jump": verdict.value, "level": int(chosen.level), "intervention": chosen.proposal_id})
        if verdict is not JumpAssessment.CANDIDATE_FOR_PROTECTED_EVALUATION:
            return None
        iv = view.inst.intervention(chosen.proposal_id[len("prop:"):])
        return self.declare(view, declared_live, "INTERVENE", iv.intervention_id)

    def _apply(self, view: ArmView, live: tuple[str, ...], fix: Intervention, declared_live: tuple[str, ...], alternatives: list[Intervention]) -> Action:
        if fix.level > self.max_level:
            return self.cannot_identify(view, live)
        if fix.level <= 1:
            return self.declare(view, declared_live, "INTERVENE", fix.intervention_id)
        cands = sorted([i for i in alternatives if i.level >= 2 and i.level <= self.max_level and i.cost <= view.budget_left and i.intervention_id not in self.applied(view)], key=lambda i: (i.level, i.cost, i.intervention_id))
        if not cands:
            return STOP
        act = self._escalate(view, live, cands, declared_live)
        return act if act is not None else self._disposition_action(view, live)

    def _disposition_action(self, view: ArmView, live: tuple[str, ...]) -> Action:
        cheap = sorted([i for i in view.inst.interventions if i.is_cheap and i.cost <= view.budget_left and i.intervention_id not in self.applied(view) and any(c in i.resolves for c in live)], key=lambda i: (i.cost, i.intervention_id))
        if cheap:
            return self.declare(view, tuple(c for c in live if c in cheap[0].resolves), "INTERVENE", cheap[0].intervention_id)
        return STOP

    # --- main loop ---------------------------------------------------------------------------------
    def _establishable(self, view: ArmView, live: tuple[str, ...], c: str) -> bool:
        """Diagnostic-evaluator adequacy for hypothesis c: from the current state, some affordable set of
        registered tests separates c from every other live hypothesis while c's minimal fix stays affordable."""
        fix = self.fix_of(view, c)
        if fix is None or fix.intervention_id in self.applied(view) or fix.cost > view.budget_left:
            return False
        rivals = tuple(d for d in live if d != c)
        if not rivals:
            return True
        probes = [p for p in view.inst.probes if p.probe_id not in view.probes_run()]
        repairs = [i for i in view.inst.interventions if i.is_cheap and i.intervention_id not in self.applied(view)]
        return min_separating_total(c, rivals, probes, repairs, fix.cost, view.budget_left, designed=self.designed_tables) is not None

    def _reachable_after(self, view: ArmView, group: tuple[str, ...], c: str, left: int, used: set[str], applied: set[str]) -> bool:
        fix = self.fix_of(view, c)
        if fix is None or fix.intervention_id in applied or fix.cost > left:
            return False
        rivals = tuple(d for d in group if d != c)
        if not rivals:
            return True
        probes = [p for p in view.inst.probes if p.probe_id not in used]
        repairs = [i for i in view.inst.interventions if i.is_cheap and i.intervention_id not in applied]
        return min_separating_total(c, rivals, probes, repairs, fix.cost, left, designed=self.designed_tables) is not None

    def _reserve_ok(self, view: ArmView, live: tuple[str, ...], cost: int, target: str, kind: str) -> bool:
        """Fail-closed resource rule (minimum-sufficient escalation on the budget): a discriminating action
        is admissible only if, under every registered outcome, every hypothesis that is establishable now
        remains establishable afterwards.  A test that would spend the episode out of reach of a warranted
        minimal intervention is not a lower-level disposition, it is a resource leak."""
        left = view.budget_left - cost
        if left < 0:
            return False
        used = set(view.probes_run()); applied = set(self.applied(view))
        if kind == "PROBE":
            p = view.inst.probe(target); used = used | {target}
            f = p.designed_outcome if self.designed_tables else p.outcome
            groups: dict[str, list[str]] = {}
            for c in live:
                groups.setdefault(f(c), []).append(c)
        else:
            iv = view.inst.intervention(target); applied = applied | {target}
            groups = {"RECURRENCE": [c for c in live if c not in iv.resolves]}  # SUCCESS ends the episode
        for g in groups.values():
            grp = tuple(g)
            for c in grp:
                if self._establishable(view, live, c) and not self._reachable_after(view, grp, c, left, used, applied):
                    return False
        return True

    def _discriminators(self, view: ArmView, live: tuple[str, ...]) -> list[tuple[int, int, str, str]]:
        out = []
        if self.probing:
            for p in view.affordable_probes():
                if p.probe_id in view.probes_run() or not self._reserve_ok(view, live, p.cost, p.probe_id, "PROBE"):
                    continue
                if self.splits(view, p, live) or not self.prospective_discriminator:
                    out.append((p.cost, 0, p.probe_id, "PROBE"))
        if self.lower_level_disposition:
            for i in view.affordable_interventions():
                if not i.is_cheap or i.intervention_id in self.applied(view) or not self._reserve_ok(view, live, i.cost, i.intervention_id, "INTERVENE"):
                    continue
                hit = [c for c in live if c in i.resolves]
                if hit and (len(hit) < len(live) or not self.prospective_discriminator):
                    out.append((i.cost, 1, i.intervention_id, "INTERVENE"))
        if not self.prospective_discriminator:
            # registered order, probes first, ignoring discrimination value
            out.sort(key=lambda t: (t[1], t[2]))
            return out
        return sorted(out)

    def act(self, view: ArmView) -> Action:
        live = self.live(view)
        if not live:
            return STOP
        unique = len(live) == 1
        fixes = {self.fix_of(view, c).intervention_id for c in live if self.fix_of(view, c)}
        common = view.inst.intervention(next(iter(fixes))) if len(fixes) == 1 and all(self.fix_of(view, c) for c in live) else None
        disc = self._discriminators(view, live)
        adequate = unique or common is not None or bool(disc)
        receipt = self._receipt(view, live, adequate)
        if unique:
            assert receipt.status is LocusDiagnosisStatus.ACTIONABLE_LOCUS_HYPOTHESIS
            fix = self.fix_of(view, live[0])
            if fix is None or fix.intervention_id in self.applied(view):
                return STOP
            if fix.cost > view.budget_left:
                return self.cannot_identify(view, live)  # resource-blocked: no admissible intervention within the registered budget
            if self.never_escalate and fix.level >= 2:
                return self.cannot_identify(view, live)
            return self._apply(view, live, fix, live, [i for i in view.inst.interventions if live[0] in i.resolves])
        if self.always_escalate:
            cands = sorted([i for i in view.affordable_interventions() if i.intervention_id not in self.applied(view) and any(c in i.resolves for c in live)], key=lambda i: (-i.level, i.cost, i.intervention_id))
            if cands:
                return self.declare(view, tuple(c for c in live if c in cands[0].resolves), "INTERVENE", cands[0].intervention_id)
            return self.cannot_identify(view, live)
        if common is not None and common.intervention_id not in self.applied(view):
            if common.cost > view.budget_left or (self.never_escalate and common.level >= 2):
                return self.cannot_identify(view, live)
            return self._apply(view, live, common, live, [i for i in view.inst.interventions if all(c in i.resolves for c in live)])
        if disc:
            cost, _, target, kind = disc[0]
            if kind == "PROBE":
                return Action("PROBE", target)
            iv = view.inst.intervention(target)
            return self.declare(view, tuple(c for c in live if c in iv.resolves), "INTERVENE", target)
        assert receipt.status is LocusDiagnosisStatus.CANNOT_IDENTIFY or not self.gate or receipt.status is LocusDiagnosisStatus.MULTIPLE_LIVE_LOCUS_HYPOTHESES
        if not self.gate:
            for c in live:  # forced attribution in registered order
                fix = self.fix_of(view, c)
                if fix and fix.cost <= view.budget_left and fix.intervention_id not in self.applied(view):
                    return self.declare(view, (c,), "INTERVENE", fix.intervention_id)
            return STOP
        if not self.lower_level_disposition:
            cands = sorted([i for i in view.affordable_interventions() if i.intervention_id not in self.applied(view) and any(c in i.resolves for c in live)], key=lambda i: (-len([c for c in live if c in i.resolves]), i.level, i.cost, i.intervention_id))
            if cands:
                return self.declare(view, tuple(c for c in live if c in cands[0].resolves), "INTERVENE", cands[0].intervention_id)
        return self.cannot_identify(view, live)


class MMinusLocusDiagnosis(MLocusMinimumEscalation):
    name = "M_MINUS_LOCUS_DIAGNOSIS"; probing = False

    def live(self, view: ArmView) -> tuple[str, ...]:
        obs = [(view.inst.intervention(s.action.target), s.outcome) for s in view.steps if s.action.kind == "INTERVENE"]
        return ConsistencyDiagnosis.candidates(view.inst.live_ids(), obs)


class MLocusLabelsShuffled(MLocusMinimumEscalation):
    name = "M_LOCUS_LABELS_SHUFFLED"

    def _perm(self, view: ArmView) -> dict[str, str]:
        ids = list(view.inst.live_ids())
        rng = random.Random(f"{self.seed}|shuffle|{view.inst.instance_id}")
        for _ in range(100):
            perm = ids[:]; rng.shuffle(perm)
            if all(a != b for a, b in zip(ids, perm)):
                break
        return dict(zip(ids, perm))

    def cls_of(self, view, c):
        return view.inst.cause(self._perm(view)[c]).obstruction_class

    def locus_of(self, view, c):
        return view.inst.cause(self._perm(view)[c]).locus

    def fix_of(self, view, c):
        return view.inst.min_fix(self._perm(view)[c])


class MMinusDiagnosticEvaluatorGate(MLocusMinimumEscalation):
    name = "M_MINUS_DIAGNOSTIC_EVALUATOR_GATE"; gate = False


class MMinusLowerLevelDisposition(MLocusMinimumEscalation):
    name = "M_MINUS_LOWER_LEVEL_DISPOSITION"; lower_level_disposition = False


class MMinusProspectiveDiscriminator(MLocusMinimumEscalation):
    name = "M_MINUS_PROSPECTIVE_DISCRIMINATOR"; prospective_discriminator = False


class MAlwaysEscalateWhenStuck(MLocusMinimumEscalation):
    name = "M_ALWAYS_ESCALATE_WHEN_STUCK"; always_escalate = True


class MNeverEscalate(MLocusMinimumEscalation):
    name = "M_NEVER_ESCALATE"; never_escalate = True; max_level = 1


# ---- controls ------------------------------------------------------------------------------------------------

class CRandomPolicy(Policy):
    name = "C_RANDOM_POLICY"

    def act(self, view: ArmView) -> Action:
        rng = random.Random(f"{self.seed}|random|{view.inst.instance_id}|{len(view.steps)}")
        opts: list[Action] = [Action(DECLARE_KIND, None, rng.choice(CLASSES), rng.choice(LOCI), rng.random()), STOP]
        opts += [Action("PROBE", p.probe_id) for p in view.affordable_probes() if p.probe_id not in view.probes_run()]
        opts += [Action("INTERVENE", i.intervention_id, rng.choice(CLASSES), rng.choice(LOCI), rng.random()) for i in view.affordable_interventions() if i.intervention_id not in self.applied(view)]
        return rng.choice(opts)


class CNeverIntervene(Policy):
    name = "C_NEVER_INTERVENE"

    def act(self, view: ArmView) -> Action:
        return Action(DECLARE_KIND, None, "CANNOT_IDENTIFY", "CANNOT_IDENTIFY", 0.0)


# ---- registry ---------------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class ArmSpec:
    name: str
    factory: type
    budget_multiplier: float = 1.0
    group: str = "baseline"


def arm_specs() -> list[ArmSpec]:
    return [
        ArmSpec(B0RetrySearch.name, B0RetrySearch), ArmSpec(B1UncertaintyAbstention.name, B1UncertaintyAbstention), ArmSpec(B2FailureTaxonomy.name, B2FailureTaxonomy),
        ArmSpec(B3ModelBasedDiagnosisVoI.name, B3ModelBasedDiagnosisVoI), ArmSpec("B3_EQUAL_EXTRA_SEARCH_1_5X", B3ModelBasedDiagnosisVoI, 1.5, "control"), ArmSpec(B4MDAModelExpansion.name, B4MDAModelExpansion),
        ArmSpec(B5R1.name, B5R1, group="ladder"), ArmSpec(B5R2.name, B5R2, group="ladder"), ArmSpec(B5R3.name, B5R3, group="ladder"), ArmSpec(B5R4.name, B5R4, group="ladder"), ArmSpec(Federation.name, Federation, group="ladder"),
        ArmSpec(B5NoAbstention.name, B5NoAbstention, group="federation-variant"),
        ArmSpec(MLocusMinimumEscalation.name, MLocusMinimumEscalation, group="M"),
        ArmSpec(MMinusLocusDiagnosis.name, MMinusLocusDiagnosis, group="ablation"), ArmSpec(MLocusLabelsShuffled.name, MLocusLabelsShuffled, group="ablation"), ArmSpec(MMinusDiagnosticEvaluatorGate.name, MMinusDiagnosticEvaluatorGate, group="ablation"),
        ArmSpec(MMinusLowerLevelDisposition.name, MMinusLowerLevelDisposition, group="ablation"), ArmSpec(MMinusProspectiveDiscriminator.name, MMinusProspectiveDiscriminator, group="ablation"),
        ArmSpec(MAlwaysEscalateWhenStuck.name, MAlwaysEscalateWhenStuck, group="ablation"), ArmSpec(MNeverEscalate.name, MNeverEscalate, group="ablation"),
        ArmSpec(CRandomPolicy.name, CRandomPolicy, group="control"), ArmSpec(CNeverIntervene.name, CNeverIntervene, group="control"),
    ]


def make_policy(spec: ArmSpec, seed: str) -> Policy:
    pol = spec.factory(seed)
    pol.name = spec.name
    return pol
