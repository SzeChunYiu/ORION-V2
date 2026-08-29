# P-C E20 Pilot Result Block V1

**Use:** manuscript-ready post-result insert for P-C.  
**Evidence level:** protected valid pilot, underpowered; not confirmatory.  
**Primary evidence:** issue #45 E20 R4 native evaluation, archived at commit `647aa306260f978e0570b71016b153e9ac48d6a0`.

## Results insert — real debugging pilot

We first ran a three-task gold-blind BugsInPy pilot to test whether the complete controller could return executable repairs under the same base model and task information as simpler controls. Raw registered-test success was 1/3 for the full F2/ORION controller, 1/3 for the strongest-parent federation F0, and 2/3 for both direct generation and same-model reflection. The paired success-risk difference was 0.000 for F2 versus F0 and -0.333 for F2 versus each simpler control; all bootstrap 95% intervals spanned [-1.000, 1.000] and the exact discordant tests gave p=1.0. The pilot is therefore not evidence of F2 superiority or inferiority, but it establishes an adverse boundary that the confirmatory study must explain rather than overwrite.

All six failures across the twelve arm-task evaluations occurred before registered tests because the proposed patch could not be applied. Failure decomposition showed that artifact serialization itself was a material interface variable: F2 had two patch-application failures and SIMPLE had one. In one F2 case, the diagnosis and substantive one-line edit matched the successful direct solution but the `---`/`+++` path headers were not executable; in another, the proposed semantic edit was blocked by incorrect unified-diff hunk counts. We therefore retain raw executable success as the end-to-end primary outcome while prospectively separating syntax-only artifact validity from scientific diagnosis/edit quality in E30.

## Discussion insert — boundary and contraction rule

The pilot does not support universal activation of the full controller. On these three small debugging tasks, simpler generation and reflection produced more executable successes than F2, while F2 matched F0. This is compatible with the predeclared thesis only if larger confirmatory data show that added control structure becomes useful in strata where scientific obligations, failure diagnosis, evidence adequacy or selective reopening matter. If E30 reproduces a tie or loss to simpler controls under matched resources, the correct disposition is component contraction, parent replacement or scope restriction rather than adding more structure to preserve a universal claim.

The pilot also exposes a measurement distinction relevant to scientific-agent evaluation. A system may identify the right edit yet fail to serialize it into an executable artifact. For an end-to-end agent this is still a real failure, but mechanism attribution requires separating reasoning failure from interface failure. The confirmatory analysis therefore reports the raw outcome and a pre-frozen, arm-blind syntax-only sensitivity control; the latter cannot replace the raw primary result.

## Authority sentence

`E20` is an underpowered pilot and does not promote PC-C1 or PC-C3 to a confirmed result. P-C remains open until the frozen E30/E60 and naturalistic-domain evidence determines whether the controller improves, harms or merely redistributes the scientific quality-resource frontier.
