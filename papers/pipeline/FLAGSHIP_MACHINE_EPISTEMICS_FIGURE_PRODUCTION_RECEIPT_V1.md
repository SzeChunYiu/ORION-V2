# Figure Production Receipt V1 — Machine Epistemics Perspective (flagship)

**Agent:** D (wave6-contraction-closure figure gate) · **Date:** 2026-08-29
**Inputs:** `/tmp/figplan.md` (frozen plan), `/tmp/FIGURE_CLAIM_BINDING_V1.md` (stages 1–2),
`/tmp/FLAGSHIP_SENTENCE_LEVEL_CITATION_AUDIT_V1.md`, `/tmp/genealogy.md`, V8 manuscript.
**Renderer:** `/tmp/figs/render_figs.py` (matplotlib, vector PDF + 200 dpi PNG, pdf.fonttype 42).
**No repository files were edited.**

---

## Terminal counters

| Counter | Value |
|---|---|
| FIGURE_CLAIM_BINDING | **COMPLETE_62_OF_62** (fig1 10 + fig2 18 + fig3 24 + fig4 10) |
| UNBOUND_ELEMENTS_TOTAL | **0** |
| QUANTITATIVE_UNPUBLISHED_ELEMENTS | **0** (no numbers, effect sizes, or unpublished ORION-V2 results in any figure) |
| TABLE1_ROWS_VERDICTED | **17** (13 clean, 3 † rows, overlapping ‡ notes; 0 rows citing an uncorrected WRONG source) |
| STAGE2_DISCLAIMER_COMPLIANCE | **PASS** — every †/‡-carrying parent label in figs 2–3 renders with its marker and an in-figure footnote explaining it |
| FIGURES_RENDERED | **4** (fig1–fig4, PDF + PNG each) |
| AUDIT_VIOLATIONS_TOTAL | **0** (programmatic: out-of-canvas, right-edge, pairwise text collision; plus targeted panel-containment probes) |
| EVERY_SURFACE_REVIEW fig1 | **PASS** |
| EVERY_SURFACE_REVIEW fig2 | **PASS** |
| EVERY_SURFACE_REVIEW fig3 | **PASS** |
| EVERY_SURFACE_REVIEW fig4 | **PASS** (after one real fix, re-verified) |
| GRAYSCALE_LEGINIBILITY fig1–fig4 | **PASS** (per-figure verdicts below) |
| JARGON_SCAN fig1–fig4 | **PASS** — zero repository/project terms; public vocabulary only ("Machine Epistemics", parent field names, "parent federation / interfield theories / absorptive supertheory / domain federation") |

---

## Per-figure status

### Figure 1 — One bounded research episode (183 × 155 mm)
- **Claim binding:** 10 elements → 6 BOUND, 4 CONCEPTUAL_ONLY, 0 UNBOUND. Constructed test cases
  (panels 1–4) are labelled as constructed in the in-figure footnote; published anchors cited by number.
- **Render:** `fig1.pdf` / `fig1.png` (1440×1220). Clean audit.
- **Surfaces reviewed:** full figure (fresh-path vision pass), gate-panel zoom, footnote zoom (viewed
  inline), grayscale copy, programmatic extents for every text artist.
- **Grayscale:** PASS — "fully interpretable in grayscale; no element relies on color alone" (filled vs
  open marks, solid vs dashed arrows, x glyphs all survive conversion).
- **Micro-typography:** three vision claims from the full-figure pass were **adjudicated FALSE by the
  extents probe** and closed (see QA-method note): gate title is two lines with 5 u clearance inside
  its panel; "reopen" label clears the adjacent box by 1.63 u; footnotes end at x=78.7 with ~21 u of
  white space. The zoomed views confirm.
- **Advisory (non-blocking), dispositioned:** smallest glyphs (typed-gate diamond vs plain-workflow
  square) distinguishable only on close inspection — they never serve as a discriminating pair and the
  contrast strip labels them; footer ink is the secondary token used figure-wide (contrast 6.39:1 on
  white, above the 4.5:1 AA floor).

### Figure 2 — Parent-field ownership matrix (183 × 158 mm)
- **Claim binding:** 18 rows BOUND; 5 gap entries CONCEPTUAL with BOUND parents; no quantitative content.
- **Stage 2:** rows 3/9/13 carry †, rows 4/8 carry ‡ (row 4 both); in-figure footnotes explain both
  markers and state that no row cites an uncorrected wrong-attributed source. Verdict: PASS.
- **Render:** `fig2.pdf` / `fig2.png` (1440×1244). One layout fix during production (subtitle/legend
  collision → 2-line subtitle + 2-row legend), re-audited clean.
- **Surfaces reviewed:** full figure (fresh-path vision pass, 10 checks: codes C1–C11, legend, 18 row
  labels, gap names with ASCII "->" arrows + needs-lines, contracting note, column key, 3 footnotes,
  zero jargon), grayscale copy.
- **Grayscale:** PASS — solid vs hatched vs blank vs diamond fully distinguishable without color; † vs ‡
  distinguishable.

### Figure 3 — Four control problems quadrant map (183 × 150 mm)
- **Claim binding:** 24 elements → 16 BOUND, 8 CONCEPTUAL_ONLY, 0 UNBOUND. Failure examples are
  conceptual instances of published distinctions, each with published anchors.
- **Stage 2:** quadrants 2/3/4 parent lines carry † ([15–17], [32,33], [38,39], [11–13]); **fix applied
  during review:** fig3 previously had no in-figure † footnote and no glyph legend (flagged
  independently by the grayscale pass). Added two footnote lines mirroring fig2's wording plus an
  explicit glyph legend ("Filled square = parent method; x = cross-layer failure mode; open diamond =
  measurable quantity (definition, not measurement)"). Extents-verified (in canvas, clear of the
  quadrant row by ≥1.7 u, 1.07 u line gap) and visually confirmed via inline zoom.
- **Render:** `fig3.pdf` / `fig3.png` (1440×1181). Re-rendered after the fix; audit clean.
- **Surfaces reviewed:** full figure (fresh-path vision pass: 3/1/2 marks per quadrant, 2-line subtitle
  clear, central episode box + 4 arrows, daggers render, zero jargon), grayscale copy, footnote zoom.
- **Grayscale:** PASS — squares/x-glyphs/open-diamonds "three clearly different marks"; daggers survive
  conversion.

### Figure 4 — Founding-vs-falsification decision path (120 × 172 mm)
- **Claim binding:** 10 elements, all conceptual schematic steps with published anchors, 0 UNBOUND.
- **Render:** `fig4.pdf` / `fig4.png` (944×1354). **One real defect found and fixed:** the
  "CANNOT INDEPENDENTLY ADJUDICATE" title grazed its box border (0.08 u ≈ 0.1 mm clearance,
  vision claim confirmed by the extents probe) → wrapped to two lines; post-fix clearance 11.65 u.
  Re-rendered; zoom re-verified ("two lines, fully readable, well clear of the right border"; open
  triangle marker visible; caption separated). All four outcome titles now clear by ≥3.4 u.
- **Surfaces reviewed:** full figure (fresh-path vision pass: 4 stages, 4 outcomes, dashed gate box
  contents inside), outcome-box zoom, grayscale copy.
- **Grayscale:** PASS — all six outcome-marker pairs distinguishable by shape alone (◆ □ ○ △), each
  redundant with its text label; dashed gate border clearly dashed.

---

## QA method and adjudication record

- **Evidence hierarchy for micro-typography:** programmatic extents probe (matplotlib
  `get_window_extent` → data units vs panel borders) > high-zoom crops > full-figure vision. At 200 dpi,
  6 pt text is ~8 px tall and full-figure vision produced three hallucinated geometry claims on fig1
  and one true one on fig4; each was settled by the probe, not by re-asking vision.
- **Vision false positives closed (fig1):** (a) gate title "clipped" — actually 2 lines, 5 u clear;
  (b) "reopen" clipped by box — 1.63 u clear; (c) footnote "[6" truncated — text ends at x=78.7.
- **Vision true positive fixed (fig4):** adjudicate-title border graze (0.08 u) → wrapped, re-verified.
- **Vision flag dismissed with evidence (fig1 gate zoom):** "bounded by their warrants" near panel top
  — crop artifact; probe shows the block centered in the updated-state panel with 0.49 u side, 2.98 u
  bottom, 11.6 u top clearance.
- **Accessibility hard rules honoured:** no distinction carried by color alone anywhere (the validated
  blue #2F5B8F vs gray #57606A pair fails the normal-vision ΔE floor, so it is used only as
  emphasis, always redundant with a glyph); legends locally intelligible (fig2 in-figure legend +
  footnotes; fig3 glyph-legend footnote; fig4 per-outcome labels; fig1 contrast strip + footnotes);
  arrows drawn as ASCII "->"; ink tokens: INK 15.80:1, SUB 6.39:1 on white.
- **Cache discipline:** review copies use unique basenames (`gray_*_v4/v5`, `zoom_*_v4/v1`) because any
  basename containing "figN" collides with a stale CDN cache path.

## Deliverables (all in /tmp, uncommitted by design)

| Artifact | Path |
|---|---|
| Claim binding (stages 1+2) | `/tmp/FIGURE_CLAIM_BINDING_V1.md` |
| This receipt | `/tmp/FIGURE_PRODUCTION_RECEIPT_V1.md` |
| Renderer (single source) | `/tmp/figs/render_figs.py` |
| Figure PDFs | `/tmp/figs/fig1.pdf`, `fig2.pdf`, `fig3.pdf`, `fig4.pdf` |
| Figure PNGs (200 dpi) | `/tmp/figs/fig1.png` … `fig4.png` |

FIGURE_GATE = **CLOSED**.
