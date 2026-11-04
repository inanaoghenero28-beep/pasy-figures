"""Figures 1-3 of the manuscript "Performance Modeling for Isolated Industrial
Operations: A Data Envelopment Analysis Framework" (Inana, O.).

Every result and setting shown is read from the two result files written by the PASy
run: runs/paper_results.json and runs/baseline_s42/daily_classified.csv. That
includes the test days, quartile thresholds, AHP weights, design settings, variable
roles and day counts.

The only values set here are three descriptions of the input data, which the result
files do not contain: the date of the lost-time incident (Y6 = 0 on that day in
AGGREGATED_DAILY_REPORTS), the wording of the test-day legend, and the dry-season
months. They are listed under "Input-data descriptions" below.

Usage: python make_figures.py RUNS_DIR OUT_DIR
"""
import json, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mp
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

# ---- Input-data descriptions (not results) ---------------------------------------
LTI_DATES = ["2025-06-27"]          # days with Y6 = 0 (lost-time incident) in the input data
EVENT_LABEL = "Three largest unplanned-downtime days"   # test days are the largest Y4 (downtime) days
DRY_MONTHS = [1, 2, 3, 10, 11, 12]  # dry season in the dataset description (Appendix B)

BASELINE = "baseline_s42"
DAILY = None
FAIL, LTI = None, None

W_IN = 6.85  # 174 mm, Springer full width
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.labelsize": 9,
    "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 8,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": "#E0E0E0", "grid.linewidth": 0.5,
    "ps.fonttype": 42, "pdf.fonttype": 42,
})
COL = {1: "#C62828", 2: "#EF6C00", 3: "#2E7D32", 4: "#1565C0"}
LAB = {1: "Q1 Low", 2: "Q2 Below Average", 3: "Q3 Above Average", 4: "Q4 High"}


def save(fig, out, name):
    for ext in ("eps", "png", "pdf"):
        fig.savefig(f"{out}/{name}.{ext}", dpi=300 if ext == "png" else None,
                    bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------- Figure 1
def var_list(vs):
    """X1, X2, X3 -> 'X1–X3' (three or more consecutive), otherwise listed."""
    out, i = [], 0
    while i < len(vs):
        j = i
        while (j + 1 < len(vs) and vs[j + 1][0] == vs[i][0]
               and int(vs[j + 1][1:]) == int(vs[j][1:]) + 1):
            j += 1
        out.append(f"{vs[i]}–{vs[j]}" if j - i >= 2 else ", ".join(vs[i:j + 1]))
        i = j + 1
    return ", ".join(out)


def fig1(R, out):
    w = R["meta"]["ahp_weights"]
    cr = R["meta"]["ahp_consistency"]["CR"]
    c = R["meta"]["config"]
    # warm-up = the W - 1 days before the first steady-state day
    first = DAILY.DATE.min()
    d0, d1 = first - pd.Timedelta(days=c["window"] - 1), first - pd.Timedelta(days=1)
    wu = (f"{d0.day}–{d1.day} {d1:%b}" if (d0.month, d0.year) == (d1.month, d1.year)
          else f"{d0.day} {d0:%b}–{d1.day} {d1:%b}")
    # undesirable outputs = output variables (Y...) placed on the DEA input side
    und = [v for v in R["meta"]["dea_inputs"] if v.startswith("Y")]
    ins = [v for v in R["meta"]["dea_inputs"] if v not in und]
    roles = (f"inputs: {var_list(ins)} and undesirable\n{var_list(und)}; outputs: {var_list(R['meta']['dea_outputs'])}"
             if und else f"inputs: {var_list(ins)}\noutputs: {var_list(R['meta']['dea_outputs'])}")
    pct = lambda x: f"{x * 100:g}%"
    fig, ax = plt.subplots(figsize=(W_IN, 7.4))
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")

    def box(x, y, w_, h, title, body, fc):
        ax.add_patch(mp.FancyBboxPatch((x, y), w_, h, boxstyle="round,pad=0.6",
                                       fc=fc, ec="#37474F", lw=0.8))
        ax.text(x + w_ / 2, y + h - 2.2, title, ha="center", va="top",
                fontsize=8.5, fontweight="bold", color="#212121")
        ax.text(x + w_ / 2, y + h - 6.0, body, ha="center", va="top",
                fontsize=7.2, color="#37474F", linespacing=1.35)

    def arr(x1, y1, x2, y2):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color="#37474F", lw=0.9,
                                    shrinkA=0, shrinkB=0))

    E, S, F, D, O = "#FFF3E0", "#F3E5F5", "#E8F5E9", "#FCE4EC", "#ECEFF1"
    # row 1: inputs (y 86-98)
    box(2, 86, 44, 11, "Observed facility data",
        "One real DMU per day (X1–X10, Y1–Y10)\nY5 rescored as accuracy: 100 − |Y5 − 100|", "#E3F2FD")
    box(54, 86, 44, 11, "Expert configuration",
        "PRISM domain and CIV rating per variable\nAHP pairwise matrix (C, I, V)", E)
    # row 2 (y 70-81)
    box(54, 70, 44, 11, "AHP weights",
        f"wC = {w['C']:.4f}   wI = {w['I']:.4f}   wV = {w['V']:.4f}\nconsistency ratio = {cr:.3f}", E)
    box(2, 70, 44, 11, "Rating factor per variable",
        f"Beta(α, β) fitted on the warm-up days\n({wu}); r = {c['r_min']:.2f} + {c['r_max'] - c['r_min']:.2f}·R, once", S)
    # row 3 (y 54-65)
    box(20, 54, 60, 11, "CIV multiplier and perturbation band",
        "M = wC·C + wI·I + wV·V        band = [1 − M·r, 1 + M·r]", E)
    # row 4 (y 38-49)
    box(2, 35, 44, 14, "Synthetic peer generation",
        f"{c['n_synth']} peers per day\nvalue = baseline × U(band)\nzero baseline stays zero", S)
    box(54, 35, 44, 14, "Feasibility checks",
        f"1. physical caps\n2. individual deviation ≤ {pct(c['max_ind_dev'])}\n"
        f"3. mean deviation ≤ {pct(c['max_agg_dev'])}   (resample ≤ {c['max_attempts']}×)", F)
    # row 5 (y 22-33)
    box(20, 19.5, 60, 11, "Rolling reference set",
        f"{c['window']} days × (1 real + {c['n_synth']} synthetic) = {c['T']:,} DMUs\n"
        "focal DMU = the current day's real observation", S)
    # row 6 (y 3-17)
    box(2, 3, 44, 14, "Bounded CCR DEA (CRS)",
        roles + "\nθU, θL and θG = √(θU·θL)", D)
    box(54, 3, 44, 14, "Annual quartile classification",
        f"thresholds: Q25, Q50, Q75 of the\n{R['headline']['n_steady']} steady-state θG values\n"
        "Low | Below Avg. | Above Avg. | High", O)

    arr(24, 85.4, 24, 81.6)       # data -> rating factor
    arr(76, 85.4, 76, 81.6)       # expert -> AHP
    arr(24, 69.4, 36, 65.6)       # r -> band
    arr(76, 69.4, 64, 65.6)       # weights -> band
    arr(36, 53.4, 24, 49.6)       # band -> generation
    arr(46.6, 43.5, 53.4, 43.5)   # generation -> checks
    arr(76, 34.4, 62, 31.1)       # checks -> reference set
    arr(38, 18.9, 24, 17.6)       # reference set -> DEA
    arr(46.6, 10, 53.4, 10)       # DEA -> classification
    # resample loop
    ax.annotate("", xy=(46.6, 41), xytext=(53.4, 41),
                arrowprops=dict(arrowstyle="-|>", color="#B71C1C", lw=0.8, ls="--"))
    ax.text(50, 39.6, "reject", ha="center", va="top", fontsize=7, color="#B71C1C", style="italic")
    save(fig, out, "Fig1")


# ---------------------------------------------------------------- Figure 2
def fig2(R, d, out):
    q = R["quartiles_A"]
    fig, ax = plt.subplots(figsize=(W_IN, 3.6))
    for k in (1, 2, 3, 4):
        x = d[d.class_A == k]
        ax.scatter(x.DATE, x.theta_G, s=9, c=COL[k], lw=0, label=LAB[k], zorder=3)
    ax.plot(d.DATE, d.theta_G, color="#9E9E9E", lw=0.4, zorder=2)
    for v, name in ((q["Q25"], "Q25"), (q["Q50"], "Q50"), (q["Q75"], "Q75")):
        ax.axhline(v, color="#616161", lw=0.7, ls="--", zorder=1)
    ax.axhline(1.0, color="black", lw=0.8, zorder=1)
    for f in FAIL:
        ax.axvline(f, color="#6D1B1B", lw=1.2, ls=":", zorder=1)
    for t in LTI:
        ax.axvline(t, color="#6A1B9A", lw=1.1, ls="-.", zorder=1)
    ax.set_ylabel("Geometric efficiency θG")
    ax.set_xlim(d.DATE.min() - pd.Timedelta(days=3), d.DATE.max() + pd.Timedelta(days=3))
    ax.xaxis.set_major_locator(matplotlib.dates.MonthLocator())
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%b"))
    # threshold labels inside the axes, left edge, no overlap with legend
    for v, name in ((q["Q25"], "Q25"), (q["Q50"], "Q50"), (q["Q75"], "Q75")):
        ax.annotate(f"{name} = {v:.4f}", xy=(1.0, v), xycoords=("axes fraction", "data"),
                    xytext=(4, 0), textcoords="offset points", fontsize=7, va="center",
                    ha="left", color="#424242", annotation_clip=False)
    h = [Line2D([], [], marker="o", ls="", color=COL[k], ms=4, label=LAB[k]) for k in (1, 2, 3, 4)]
    h += [Line2D([], [], color="#6D1B1B", ls=":", label=EVENT_LABEL)]
    if len(LTI):
        lab = "LTI (" + ", ".join(t.strftime("%d %b").lstrip("0") for t in LTI) + ")"
        if all(t in set(FAIL) for t in LTI):
            lab = lab[:-1] + ", also one of these days)"
        h += [Line2D([], [], color="#6A1B9A", ls="-.", label=lab)]
    ax.legend(handles=h, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.12), frameon=False)
    save(fig, out, "Fig2")


# ---------------------------------------------------------------- Figure 3
def fig3(R, d, out):
    q = R["quartiles_A"]
    d = d.copy(); d["m"] = d.DATE.dt.month
    months = sorted(d.m.unique())
    data = [d[d.m == m].theta_G.values for m in months]
    dry = set(DRY_MONTHS) if DRY_MONTHS else None
    fill = lambda m: "#E0E0E0" if dry is None else "#BBDEFB" if m in dry else "#C8E6C9"
    MIN_BOX = 5   # months with fewer days are drawn as points, not as a box plot
    big = [(m, x) for m, x in zip(months, data) if len(x) >= MIN_BOX]
    fig, ax = plt.subplots(figsize=(W_IN, 3.6))
    bp = ax.boxplot([x for _, x in big], positions=[m for m, _ in big], widths=0.6,
                    patch_artist=True, medianprops=dict(color="black", lw=1),
                    flierprops=dict(marker="o", ms=3, mfc="none", mec="#616161"))
    for (m, _), b in zip(big, bp["boxes"]):
        b.set_facecolor(fill(m))
        b.set_edgecolor("#37474F")
    for m, x in zip(months, data):
        if len(x) < MIN_BOX:
            ax.scatter([m] * len(x), x, s=16, c=fill(m), edgecolors="#37474F", lw=0.8, zorder=3)
    ax.axhline(R["headline"]["theta_G"]["mean"], color="#C62828", lw=1)
    for v in (q["Q25"], q["Q50"], q["Q75"]):
        ax.axhline(v, color="#616161", lw=0.7, ls="--")
    ax.set_xticks(months)
    ax.set_xlim(min(months) - 0.6, max(months) + 0.6)
    ax.set_xticklabels([f"{pd.Timestamp(2000, m, 1):%b}\nn={len(x)}" for m, x in zip(months, data)])
    ax.set_ylabel("Geometric efficiency θG")
    h = ([mp.Patch(fc="#BBDEFB", ec="#37474F", label="Dry season"),
          mp.Patch(fc="#C8E6C9", ec="#37474F", label="Wet season")] if dry is not None else [])
    h += [Line2D([], [], color="#C62828", label=f"Annual mean = {R['headline']['theta_G']['mean']:.4f}"),
         Line2D([], [], color="#616161", ls="--", label="Annual quartiles Q25, Q50, Q75")]
    ax.legend(handles=h, ncol=len(h), loc="upper center", bbox_to_anchor=(0.5, -0.2), frameon=False)
    save(fig, out, "Fig3")



def main(runs, out):
    global DAILY, FAIL, LTI
    os.makedirs(out, exist_ok=True)
    R = json.load(open(f"{runs}/paper_results.json"))
    d = pd.read_csv(f"{runs}/{BASELINE}/daily_classified.csv", parse_dates=["DATE"])
    DAILY = d
    FAIL = pd.to_datetime(R["test_days"]["dates"])
    lti = pd.to_datetime(LTI_DATES)
    LTI = pd.to_datetime(sorted(t for t in lti if t in set(d.DATE)))
    fig1(R, out); fig2(R, d, out); fig3(R, d, out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
