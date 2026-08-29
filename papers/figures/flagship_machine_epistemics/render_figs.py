#!/usr/bin/env python3
"""Machine Epistemics flagship - Figures 1-4 production render.
Vector PDF + 200 dpi PNG. Gate contract: no color-alone distinctions,
grayscale legible, no repository terminology, NMI Perspective style."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch, Circle

INK    = "#1F2328"
SUB    = "#57606A"
RULE   = "#B9BEC6"
LIGHT  = "#EEF1F4"
ACCENT = "#2F5B8F"   # emphasis only, always redundant with a symbol/label
WHITE  = "#FFFFFF"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})
MM = 1 / 25.4

def new_ax(w_mm, h_mm):
    fig = plt.figure(figsize=(w_mm * MM, h_mm * MM))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    return fig, ax

def panel(ax, x, y, w, h, fc=LIGHT, ec=RULE, lw=0.8, rounding=1.4, ls="solid", z=1):
    p = FancyBboxPatch((x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={rounding}",
        facecolor=fc, edgecolor=ec, linewidth=lw, linestyle=ls,
        mutation_aspect=1.0, zorder=z)
    ax.add_patch(p); return p

def arrow(ax, x0, y0, x1, y1, ls="solid", lw=1.1, color=INK, ms=9, z=3):
    a = FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>",
        mutation_scale=ms, linewidth=lw, linestyle=ls, color=color,
        shrinkA=0, shrinkB=0, zorder=z)
    ax.add_patch(a); return a

def T(ax, x, y, s, size=7, color=INK, ha="left", va="center",
      weight="normal", style="normal", z=4, **kw):
    return ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va,
                   fontweight=weight, fontstyle=style, zorder=z, **kw)

AUDIT = {}

def audit(fig, ax, name):
    """Ground-truth checks: in-canvas extents + pairwise text-text collision."""
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    inv = ax.transData.inverted()
    bad = []
    boxes = []
    for t in ax.texts:
        bb = t.get_window_extent(renderer=r)
        (x0, y0), (x1, y1) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
        if x0 < -0.3 or x1 > 100.3 or y0 < -0.3 or y1 > 100.3:
            bad.append(f"OUT-OF-CANVAS [{x0:.1f},{y0:.1f}]-[{x1:.1f},{y1:.1f}] "
                       f"'{t.get_text()[:48]}'")
        boxes.append((x0, y0, x1, y1, t.get_text()))
    TOL = 0.55  # data units; overlap must exceed this in BOTH axes to count
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            ax0, ay0, ax1, ay1, atx = boxes[i]
            bx0, by0, bx1, by1, btx = boxes[j]
            ox = min(ax1, bx1) - max(ax0, bx0)
            oy = min(ay1, by1) - max(ay0, by0)
            if ox > TOL and oy > TOL:
                bad.append(f"TEXT-COLLISION ov=({ox:.1f},{oy:.1f}) "
                           f"'{atx[:32]}' <-> '{btx[:32]}'")
    AUDIT.setdefault(name, []).extend(bad)

def check_x1(fig, ax, name, artists, limit, what):
    """Right-edge constraint: listed artists must not cross `limit`."""
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    inv = ax.transData.inverted()
    for t in artists:
        bb = t.get_window_extent(renderer=r)
        (x0, y0), (x1, y1) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
        if x1 > limit:
            AUDIT.setdefault(name, []).append(
                f"{what} x1={x1:.1f} > {limit} '{t.get_text()[:48]}'")

def save(fig, name):
    audit(fig, fig.axes[0], name)
    fig.savefig(f"/tmp/figs/{name}.pdf", format="pdf")
    fig.savefig(f"/tmp/figs/{name}.png", dpi=200)
    plt.close(fig)
    print("rendered", name)

# ---------------------------------------------------------------- Figure 1
def fig1():
    fig, ax = new_ax(183, 155)
    T(ax, 1, 98.5, "Executable research episodes change scientific state, not only outputs",
      size=9.5, weight="bold")
    T(ax, 1, 94.6, "Inside one machine-mediated research episode every action passes through a typed "
      "interpretation/transition gate before any scientific commitment changes.",
      size=6.8, color=SUB)

    ytop, hh = 71.0, 19.0
    # entry state
    panel(ax, 1.0, ytop, 18.0, hh)
    T(ax, 2.2, ytop+hh-3.0, "ENTRY STATE", size=6.2, weight="bold", color=SUB)
    T(ax, 2.2, ytop+8.4, "problem &\ncriterion contract\n\nplural scientific\nstate", size=6.2)
    # actions
    panel(ax, 22.0, ytop, 23.5, hh)
    T(ax, 23.2, ytop+hh-3.0, "ADMISSIBLE ACTIONS", size=6.2, weight="bold", color=SUB)
    T(ax, 23.2, ytop+8.0, "retrieval  |  proof &\ncomputation  |  simulation\n"
      "experiment & measurement\nhuman review", size=6.2)
    # outputs
    panel(ax, 48.5, ytop+4.0, 14.5, 11.0, fc=WHITE)
    T(ax, 55.7, ytop+11.6, "OUTPUTS", size=6.2, weight="bold", color=SUB, ha="center")
    T(ax, 55.7, ytop+7.0, "observations,\ntool results", size=6.2, ha="center")
    # gate (typed) - double border + diamond glyph
    gp = panel(ax, 64.5, ytop, 20.0, hh, fc=WHITE, ec=INK, lw=1.4)
    panel(ax, 65.3, ytop+0.8, 18.4, hh-1.6, fc=WHITE, ec=INK, lw=0.7, rounding=1.1)
    T(ax, 74.5, ytop+hh-2.6, "INTERPRETATION /\nTRANSITION GATE", size=6.0,
      weight="bold", ha="center", va="top")
    T(ax, 74.5, ytop+8.4, "what changed?  subject | problem |\ncriterion | source | evidence |\n"
      "representation | evaluator | authority", size=5.8, ha="center", color=SUB)
    ax.plot([74.5], [ytop+2.4], marker="D", ms=3.4, color=ACCENT,
            markeredgecolor=INK, markeredgewidth=0.5, zorder=5, ls="none")
    # updated state + obligations
    panel(ax, 91.0, ytop, 8.0, hh, fc=LIGHT)
    T(ax, 95.0, ytop+hh-3.2, "UPDATED\nSCIENTIFIC\nSTATE", size=6.0, weight="bold", ha="center")
    T(ax, 95.0, ytop+5.2, "accepted\ncommitments,\nbounded by\ntheir warrants", size=5.7, ha="center")
    # reopened obligations tag (dashed, below gate)
    panel(ax, 77.5, ytop-9.5, 21.5, 6.6, fc=WHITE, ec=SUB, lw=0.9, ls=(0,(3,2)))
    T(ax, 88.2, ytop-6.2, "reopened obligations & history", size=6.0, ha="center")

    arrow(ax, 19.0, ytop+hh/2, 22.0, ytop+hh/2)
    arrow(ax, 45.5, ytop+hh/2+3.2, 48.5, ytop+hh/2+3.2)
    arrow(ax, 63.0, ytop+9.5, 64.5, ytop+9.5)
    # typed exits: commit (solid) / reopen (dashed)
    arrow(ax, 84.5, ytop+11.0, 91.0, ytop+11.0)
    arrow(ax, 84.5, ytop+3.4, 91.0, ytop+3.4, ls=(0,(3,2)))
    T(ax, 87.8, ytop+12.8, "commit", size=5.2, color=SUB, ha="center")
    T(ax, 87.8, ytop+1.4, "reopen", size=5.2, color=SUB, ha="center")
    arrow(ax, 74.5, ytop, 84.0, ytop-2.9, ls=(0,(3,2)), lw=0.9, ms=7)
    # contrast strip: plain workflow vs episode
    yc = 46.0
    panel(ax, 1.0, yc-9.0, 47.0, 17.5, fc=WHITE)
    T(ax, 2.6, yc+5.4, "A plain workflow ends at its output", size=6.6, weight="bold")
    panel(ax, 4.0, yc-5.6, 10.5, 6.4, fc=LIGHT, rounding=0.9)
    T(ax, 9.2, yc-2.4, "actions", size=5.9, ha="center")
    arrow(ax, 14.5, yc-2.4, 20.0, yc-2.4)
    panel(ax, 20.0, yc-5.6, 10.5, 6.4, fc=LIGHT, rounding=0.9)
    T(ax, 25.2, yc-2.4, "output", size=5.9, ha="center")
    ax.plot([33.6], [yc-2.4], marker="s", ms=5.2, color=INK, zorder=5, ls="none")
    arrow(ax, 30.5, yc-2.4, 31.9, yc-2.4)
    T(ax, 35.2, yc-2.4, "terminal claim:\nexecution succeeded", size=5.7, color=SUB)

    panel(ax, 51.0, yc-9.0, 48.0, 17.5, fc=WHITE)
    T(ax, 52.6, yc+5.4, "An episode adds a typed transition and carries obligations forward",
      size=6.6, weight="bold")
    panel(ax, 54.0, yc-5.6, 9.0, 6.4, fc=LIGHT, rounding=0.9)
    T(ax, 58.5, yc-2.4, "actions", size=5.7, ha="center")
    arrow(ax, 63.0, yc-2.4, 65.4, yc-2.4)
    panel(ax, 65.4, yc-5.6, 8.4, 6.4, fc=LIGHT, rounding=0.9)
    T(ax, 69.6, yc-2.4, "output", size=5.7, ha="center")
    arrow(ax, 73.8, yc-2.4, 76.2, yc-2.4)
    ax.plot([78.6], [yc-2.4], marker="D", ms=5.6, color=WHITE,
            markeredgecolor=INK, markeredgewidth=1.1, zorder=5, ls="none")
    arrow(ax, 80.6, yc-2.4, 83.0, yc-2.4)
    panel(ax, 83.0, yc-5.6, 9.0, 6.4, fc=LIGHT, rounding=0.9)
    T(ax, 87.5, yc-2.4, "state +\nobligations", size=5.5, ha="center")
    T(ax, 78.6, yc-7.6, "gate", size=5.7, color=SUB, ha="center")

    # four hostile examples
    ex = [
        ("1", "Execution succeeds -\nevidence link invalid",
              "genuine papers retrieved;\nclaim bound to the wrong\npassage"),
        ("2", "Provenance & replay exact -\nanalysis wrong",
              "the record is complete;\nlineage does not establish\nscientific correctness"),
        ("3", "Three validators agree -\none hidden source",
              "apparent independent\nagreement is dependent;\ncount is not independence"),
        ("4", "Local search flat -\na route is censored",
              "absence of evidence on\nsearched routes is not\nevidence of closure"),
    ]
    xs = [1.0, 26.0, 51.0, 76.0]
    T(ax, 1.0, 30.6, "Four failures of transition that local success does not detect",
      size=7.2, weight="bold")
    for (num, ttl, body), x0 in zip(ex, xs):
        panel(ax, x0, 6.0, 23.0, 21.5, fc=WHITE)
        ax.add_patch(Circle((x0+3.0, 23.6), 1.75, facecolor=INK, edgecolor=INK, zorder=5))
        T(ax, x0+3.0, 23.6, num, size=6.0, color=WHITE, ha="center", va="center",
          weight="bold", z=6)
        T(ax, x0+5.6, 23.6, ttl, size=6.1, weight="bold", va="center")
        ax.plot([x0+21.3], [23.6], marker="x", ms=6.0, color=ACCENT,
                markeredgewidth=1.6, zorder=5, ls="none")
        T(ax, x0+1.7, 13.6, body, size=5.9, color=SUB, va="center")
    T(ax, 1.0, 3.9, "Panels 1-4 are constructed test cases with known correct answers, not "
      "prevalence estimates.", size=5.8, color=SUB)
    T(ax, 1.0, 1.5, "Published anchors: provenance does not establish correctness [35, 36, 54]; "
      "dependent agreement [37]; consensus is not truth [40, 41]; censored routes [65].",
      size=5.8, color=SUB)
    save(fig, "fig1")

# ---------------------------------------------------------------- Figure 2
ROWS = [
    ("1",  "Formal learning &\ncomputational epistemology  [10]",        [1], [4]),
    ("2",  "Cybernetics, control &\nresilience engineering  [18-20]",    [],  [2, 4]),
    ("3",  "Metareasoning &\nactive learning  [15-17] †",                [2], []),
    ("4",  "Belief revision, truth\nmaintenance & diagnosis  [11-14] †‡",[3, 4], []),
    ("5",  "Formal abstraction &\nbehavioural equivalence  [24, 25]",    [5], []),
    ("6",  "Causal transportability &\nmeasurement invariance  [21, 22]",[5, 6], []),
    ("7",  "Metrology & traceability  [23]",                              [6], []),
    ("8",  "Statistical workflow\n& calibration  [27-29] ‡",             [9], [4, 8]),
    ("9",  "Software testing &\noracles  [32, 33] †",                    [4, 9], []),
    ("10", "Numerical analysis &\nvalidated computation  [30, 31]",       [],  [4, 5]),
    ("11", "Provenance &\nreproducibility  [35, 36, 54]",                [7], []),
    ("12", "Dependent evidence\nsynthesis  [34, 37]",                    [8, 9], []),
    ("13", "Assurance, argumentation\n& consensus  [38-41] †",           [8], [9, 10]),
    ("14", "Social epistemology &\nphilosophy of inquiry  [42-50]",      [10], [3, 8]),
    ("15", "Sociology of science &\nIndigenous data governance\n [51-53, 7]", [10], [6]),
    ("16", "Systematic review, metascience\n& performative evaluation\n [65, 66, 69]", [9], [11]),
    ("17", "AI for Science &\nautonomous laboratories  [1-5]",           [11], [2, 7]),
    ("18", "Epistemic control &\nspec-driven architectures  [59-61]",    [10], [7, 9]),
]
COLS = ["reliable learning & identifiability", "action & experiment selection",
        "belief dependency & revision", "diagnosis & discrimination",
        "relation & transport", "measurement & linking", "provenance & replay",
        "evidence combination", "evaluator response", "authority & permission",
        "end-to-end automation"]
KEY = ["C1 reliable learning & identifiability     C2 action & experiment "
       "selection     C3 belief dependency & revision     C4 diagnosis & discrimination",
       "C5 relation & transport     C6 measurement & linking     C7 provenance & "
       "replay     C8 evidence combination",
       "C9 evaluator response     C10 authority & permission     C11 end-to-end "
       "automation"]
GAPS = [
    ("provenance -> scientific validity",        "needs rows 9, 11, 12, 13"),
    ("relation -> downstream reuse / reopening", "needs rows 4, 5, 6"),
    ("evidence -> authority-bounded adoption",   "needs rows 12, 14, 15"),
    ("route stop -> scientific closure",         "needs rows 4, 16, 18"),
    ("local repair -> search-space escalation",  "needs rows 2, 3, 4"),
]

def fig2():
    fig, ax = new_ax(183, 158)
    T(ax, 1, 98.6, "Most component mechanisms are already owned by mature parent fields",
      size=9.5, weight="bold")
    T(ax, 1, 95.4, "Native ownership (rows) of scientific decisions (columns). The proposed "
      "field claims none\nof these columns; only the cross-row composition gaps (right) are "
      "under test.", size=6.8, color=SUB, va="top")
    # legend swatches (two rows, fully self-describing)
    lx = 1.0
    ax.add_patch(Rectangle((lx, 89.95), 1.5, 1.5, facecolor=INK, edgecolor=INK, lw=0.4))
    T(ax, lx+2.1, 90.7, "native core ownership", size=5.9, va="center")
    lx2 = lx + 22.5
    ax.add_patch(Rectangle((lx2, 89.95), 1.5, 1.5, facecolor=WHITE, edgecolor=INK,
                           lw=0.5, hatch="////"))
    T(ax, lx2+2.1, 90.7, "partial / contributing ownership", size=5.9, va="center")
    lx3 = lx2 + 30.5
    ax.plot([lx3+0.7], [90.7], marker="D", ms=4.2, color=WHITE,
            markeredgecolor=ACCENT, markeredgewidth=1.1, ls="none")
    T(ax, lx3+2.1, 90.7, "candidate composition gap (a parent composition may suffice)",
      size=5.9, va="center")
    ax.add_patch(Rectangle((lx, 87.35), 1.5, 1.5, facecolor=WHITE, edgecolor=INK,
                           lw=0.4))
    T(ax, lx+2.1, 88.1, "blank cell: not a native object of that field", size=5.9,
      va="center", color=SUB)

    m_left, colw = 30.0, 3.30
    top, rowh = 85.0, 3.92
    # column codes C1..C11 (full names in the key below the matrix)
    for j in range(11):
        cx = m_left + j*colw + colw/2
        T(ax, cx, top+1.6, f"C{j+1}", size=5.3, weight="bold", ha="center",
          va="bottom", color=SUB)
    ax.plot([m_left, m_left+11*colw], [top+1.0, top+1.0], color=RULE, lw=0.5)
    # rows
    row_labels = []
    for i, (num, label, core, part) in enumerate(ROWS):
        ry = top - i*rowh - rowh/2
        T(ax, 2.2, ry, num, size=5.6, color=SUB, va="center")
        row_labels.append(T(ax, 4.4, ry, label, size=5.2, va="center"))
        for j in range(11):
            cx0 = m_left + j*colw
            cy0 = ry - 1.32
            if (j+1) in core:
                ax.add_patch(Rectangle((cx0+0.62, cy0-0.62), 2.05, 2.05,
                             facecolor=INK, edgecolor=INK, lw=0.3))
            elif (j+1) in part:
                ax.add_patch(Rectangle((cx0+0.62, cy0-0.62), 2.05, 2.05,
                             facecolor=WHITE, edgecolor=INK, lw=0.5, hatch="////"))
        if i % 2 == 0:
            ax.add_patch(Rectangle((m_left, ry-rowh/2), 11*colw, rowh,
                         facecolor="#F7F8FA", edgecolor="none", zorder=0))
    ax.add_patch(Rectangle((m_left, top-18*rowh), 11*colw, 18*rowh,
                 facecolor="none", edgecolor=RULE, lw=0.8))
    for j in range(11):
        ax.plot([m_left+j*colw, m_left+j*colw], [top, top-18*rowh+0.4], color=RULE, lw=0.35)
    # gap panel (right)
    gx, gw = 70.5, 28.5
    gy0 = top - 18*rowh
    panel(ax, gx, gy0, gw, 18*rowh, fc=WHITE, ec=INK, lw=1.0)
    T(ax, gx+1.4, top-2.4, "CANDIDATE COMPOSITION GAPS", size=6.2, weight="bold")
    T(ax, gx+1.4, top-5.4, "each exists only where multiple\nrows must interact",
      size=5.5, color=SUB)
    for k, (gname, needs) in enumerate(GAPS):
        gy = top - 9.4 - k*6.55
        ax.plot([gx+2.3], [gy], marker="D", ms=4.6, color=WHITE,
                markeredgecolor=ACCENT, markeredgewidth=1.2, ls="none", zorder=5)
        T(ax, gx+4.6, gy, gname, size=5.6, weight="bold", va="center")
        T(ax, gx+4.6, gy-2.5, needs, size=5.5, color=SUB, va="center")
    T(ax, gx+1.4, top-44.0, "a parent composition may suffice:\nif it makes the same "
      "protected\ndecision, the field hypothesis\ncontracts", size=5.5, color=SUB,
      va="top")
    # column key (full column names)
    ky = 12.3
    for line in KEY:
        T(ax, 1.0, ky, line, size=5.4, color=SUB)
        ky -= 2.05
    # footnotes
    T(ax, 1, 5.6, "† bibliographic correction applied to this row's canonical source during "
      "the 2026-08-29 citation audit (one detail still unpinned for ref 38); see manuscript "
      "reference list.", size=5.4, color=SUB)
    T(ax, 1, 3.4, "‡ minor bibliographic fix applied (refs 12, 29).", size=5.4, color=SUB)
    T(ax, 1, 1.2, "Row sources are the manuscript's audited canonical references; no row "
      "cites an uncorrected wrong-attributed source.", size=5.4, color=SUB)
    # row labels must not run into the matrix
    check_x1(fig, ax, "fig2", row_labels, m_left - 0.4, "ROW-LABEL-OVERLAP")
    save(fig, "fig2")


# ---------------------------------------------------------------- Figure 3
QUADS = [
    ("1", "OBSERVE EPISTEMIC STATE",
     "What is distinguishable?\nWhat is structurally non-identifiable?",
     ["formal learning - identifiability & limits  [10]",
      "model-based diagnosis - discriminating tests  [14]",
      "measurement invariance - constructs across groups  [22]"],
     "apparent independent agreement\nproduced through a shared hidden source  [37, 40]",
     ["state / failure distinguishability; probe cost",
      "structural non-identifiability rate"]),
    ("2", "CONTROL & TRANSPORT TRANSITIONS",
     "What may change? What survives\ncontext change? What must reopen?",
     ["metareasoning - value of computations  [15-17] \u2020",
      "causal transportability - transport conditions  [21]",
      "abstract interpretation - sound relations  [24, 25]"],
     "an approximate transport silently inherits a\ndecision warranted only for the exact relation  [21, 24]",
     ["false / unsafe transport rate",
      "reopened-obligation precision"]),
    ("3", "ASSURE EVIDENCE & AUTHORITY",
     "Which support is independent?\nWhich evaluator stays valid?",
     ["severe testing - could the method expose the error  [34]",
      "oracle problem - what a check can reveal  [32, 33] \u2020",
      "assurance & argumentation - premises, defeaters  [38, 39] \u2020"],
     "evaluators reach consensus on a reproducible\nbut scientifically wrong computation  [35, 40]",
     ["support calibration under dependence",
      "evaluator false-pass rate"]),
    ("4", "GOVERN ESCALATION & CLOSURE",
     "Repair locally, escalate, or stop -\non what licensed evidence?",
     ["belief revision / truth maintenance - local repair,\n     selective reopening  [11-13] \u2020",
      "route-level stopping - censoring-aware stopping  [65]",
      "metascience - empirical study of evaluation  [66]"],
     "closure declared while a search route is censored  [65]",
     ["false closure rate under censored routes",
      "unnecessary refusal / over-conservatism rate"]),
]

def quad(ax, x, y, w, h, num, title, question, parents, failure, quants):
    panel(ax, x, y, w, h, fc=WHITE)
    ax.add_patch(Rectangle((x, y), w, h, facecolor="none", edgecolor=INK, lw=0.9))
    T(ax, x+1.8, y+h-3.2, num, size=7.2, weight="bold", color=ACCENT, va="center")
    T(ax, x+4.5, y+h-3.2, title, size=6.8, weight="bold", va="center")
    T(ax, x+1.8, y+h-8.8, question, size=5.6, color=SUB, va="center")
    yy = y + h - 11.8
    for p in parents:
        lines = p.count("\n") + 1
        ax.add_patch(Rectangle((x+1.9, yy-0.7), 1.4, 1.4, facecolor=INK,
                               edgecolor=INK, lw=0.3))
        T(ax, x+4.3, yy, p, size=5.8, va="center")
        yy -= 2.95 * lines
    ax.plot([x+2.6], [yy-0.5], marker="x", ms=5.4, color=ACCENT,
            markeredgewidth=1.5, zorder=5, ls="none")
    T(ax, x+4.3, yy-0.5, failure, size=5.8, va="center", color=INK)
    yy -= 2.95 * (failure.count("\n") + 1) + 2.1
    for q in quants:
        ax.plot([x+2.6], [yy], marker="D", ms=3.4, color=WHITE,
                markeredgecolor=INK, markeredgewidth=0.9, ls="none", zorder=5)
        T(ax, x+4.3, yy, q, size=5.8, va="center", color=SUB)
        yy -= 2.95

def fig3():
    fig, ax = new_ax(183, 150)
    T(ax, 1, 98.9, "Four control problems organize the research programme",
      size=9.5, weight="bold")
    T(ax, 1, 96.4, "Each problem ties mature parent methods (filled square) to an observable "
      "scientific decision,\nnames one cross-layer failure (x) and two measurable quantities "
      "(open diamond) - definitions, not measurements.", size=6.4, color=SUB, va="top")
    # center node between the two quadrant columns
    panel(ax, 45.0, 44.0, 10.0, 9.5, fc=LIGHT, ec=INK, lw=1.1)
    T(ax, 50.0, 51.5, "one bounded", size=5.9, ha="center", va="center", weight="bold")
    T(ax, 50.0, 49.0, "research", size=5.9, ha="center", va="center", weight="bold")
    T(ax, 50.0, 46.5, "episode", size=5.9, ha="center", va="center", weight="bold")
    arrow(ax, 46.5, 53.5, 43.5, 57.0, lw=0.9, ms=8)
    arrow(ax, 53.5, 53.5, 56.5, 57.0, lw=0.9, ms=8)
    arrow(ax, 46.5, 44.0, 43.5, 40.0, lw=0.9, ms=8)
    arrow(ax, 53.5, 44.0, 56.5, 40.0, lw=0.9, ms=8)
    quad(ax, 2.0, 54.0, 43.0, 37.0, *QUADS[0])
    quad(ax, 55.0, 54.0, 43.0, 37.0, *QUADS[1])
    quad(ax, 2.0, 5.5, 43.0, 37.0, *QUADS[2])
    quad(ax, 55.0, 5.5, 43.0, 37.0, *QUADS[3])
    T(ax, 1, 3.3, "\u2020 bibliographic correction applied to this row's canonical source "
      "during the 2026-08-29 citation audit (one detail still unpinned for ref 38).",
      size=5.4, color=SUB)
    T(ax, 1, 1.2, "Filled square = parent method; x = cross-layer failure mode; open diamond "
      "= measurable quantity (definition, not measurement).", size=5.4, color=SUB)
    save(fig, "fig3")


# ---------------------------------------------------------------- Figure 4
def stage(ax, x, y, w, h, head, sub):
    panel(ax, x, y, w, h, fc=LIGHT)
    T(ax, x+w/2, y+h-2.9, head, size=6.4, weight="bold", ha="center", va="center")
    T(ax, x+w/2, y+2.4, sub, size=5.9, color=SUB, ha="center", va="center")

def outcome(ax, x, y, w, h, head, sub, marker, mfc):
    panel(ax, x, y, w, h, fc=WHITE, ec=INK, lw=1.2)
    if mfc == "filled":
        ax.plot([x+4.4], [y+h-3.6], marker=marker, ms=5.4, color=ACCENT,
                markeredgecolor=INK, markeredgewidth=0.7, ls="none", zorder=6)
    else:
        ax.plot([x+4.4], [y+h-3.6], marker=marker, ms=5.4, color=WHITE,
                markeredgecolor=INK, markeredgewidth=1.0, ls="none", zorder=6)
    T(ax, x+7.6, y+h-3.6, head, size=6.3, weight="bold", va="center")
    T(ax, x+2.2, y+h-9.6, sub, size=5.9, color=SUB, va="center")

def fig4():
    fig, ax = new_ax(120, 172)
    T(ax, 2, 98.9, "What would found the field - and what would falsify it",
      size=9.0, weight="bold")
    T(ax, 2, 96.2, "A prospective comparison path. The field hypothesis strengthens only if a\n"
      "cross-domain residual survives the strongest parent composition under matched\n"
      "information; every other terminal is a legitimate scientific outcome.",
      size=6.0, color=SUB, va="top")
    bx, bw = 10.0, 80.0
    stage(ax, bx, 83.5, bw, 8.0, "NATIVE PARENT RECONSTRUCTION",
          "each parent rebuilt in its native representation; native verdicts preserved")
    arrow(ax, 50, 83.5, 50, 80.2)
    stage(ax, bx, 72.0, bw, 8.0, "STRONGEST INFORMATION-MATCHED PARENT COMPOSITION",
          "matched sources, tools, compute, human expertise, evaluator access")
    arrow(ax, 50, 72.0, 50, 68.7)
    stage(ax, bx, 60.5, bw, 8.0, "PROTECTED CROSS-DOMAIN TRANSITION CASES",
          "pre-declared cases where composition should fail - or suffice")
    arrow(ax, 50, 60.5, 50, 57.2)
    stage(ax, bx, 49.0, bw, 8.0, "INDEPENDENT EVALUATION",
          "prospective predictions only; retrospective explanations do not count")
    # fan rail
    ax.plot([50, 50], [49.0, 45.7], color=INK, lw=1.0, zorder=3)
    ax.plot([3.0, 97.0], [45.7, 45.7], color=INK, lw=1.0, zorder=3)
    arrow(ax, 27, 45.7, 27, 41.3); arrow(ax, 73, 45.7, 73, 41.3)
    ax.plot([3.0, 3.0], [45.7, 18.25], color=INK, lw=1.0, zorder=3)
    ax.plot([97.0, 97.0], [45.7, 18.25], color=INK, lw=1.0, zorder=3)
    arrow(ax, 3.0, 18.25, 5.9, 18.25); arrow(ax, 97.0, 18.25, 94.1, 18.25)
    outcome(ax, 6.0, 26.5, 42.0, 14.5, "STABLE CROSS-DOMAIN RESIDUAL",
            "field hypothesis strengthened -\nproceed to specialist sciences", "D", "filled")
    outcome(ax, 52.0, 26.5, 42.0, 14.5, "PARENT TIE / PARENT WIN",
            "integration engineering,\nnot a new science", "s", "open")
    outcome(ax, 6.0, 11.0, 42.0, 14.5, "DOMAIN-SPECIFIC ONLY",
            "return to native parent\ndisciplines", "o", "open")
    outcome(ax, 52.0, 11.0, 42.0, 14.5, "CANNOT INDEPENDENTLY\nADJUDICATE",
            "field separation unresolved", "^", "open")
    panel(ax, 3.0, 1.2, 94.0, 7.6, fc=WHITE, ec=SUB, lw=0.7, ls=(0,(3,2)))
    T(ax, 50, 7.1, "Non-compensatory gate", size=6.0, weight="bold", ha="center")
    T(ax, 50, 5.3, "critical failures - false completion, source corruption, unsafe transport,",
      size=5.6, color=SUB, ha="center", va="center")
    T(ax, 50, 3.7, "criterion drift, authority violation - cannot be bought with broader",
      size=5.6, color=SUB, ha="center", va="center")
    T(ax, 50, 2.1, "scope or higher average performance", size=5.6, color=SUB,
      ha="center", va="center")
    save(fig, "fig4")

if __name__ == "__main__":
    fig1(); fig2(); fig3(); fig4()
    total = sum(len(v) for v in AUDIT.values())
    for name in ("fig1", "fig2", "fig3", "fig4"):
        for v in AUDIT.get(name, []):
            print(f"AUDIT {name}: {v}")
    print(f"AUDIT_VIOLATIONS_TOTAL={total}")
    print("ALL RENDERED")
