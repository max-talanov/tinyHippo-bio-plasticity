"""Regenerate figures/timescale_axis.png (model Fig. 1).

Bar extents are the time constants of hippocampal_plasticity_model.md §1 (seconds, log axis).
Solid bar = characteristic duration; dotted tail = persistence after stabilization (row 6),
recurrence (row 7) or the human range beyond the rodent one (row 8).
Brackets on the right mark the two kinds of consolidation (model §1, terminology).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

MIN, HR, DAY, WK, YR = 60.0, 3600.0, 86400.0, 7 * 86400.0, 365.25 * 86400.0
# (label, colour, bar start, bar end, tail end or None), times in s
ROWS = [
    ("Neurotransmission",        "#2e6fa7", 4e-4, 6e-3, None),
    ("STP (AMPA/NMDA)",          "#1e8fa0", 8e-3, 1.3, None),
    ("Ca²⁺ / kinase cascades",   "#4c8c3b", 0.75, 5 * MIN, None),
    ("AMPAR trafficking, E-LTP", "#ad8a2e", 1 * MIN, 3 * HR, None),
    ("Tagging & capture",        "#c1642f", 1 * MIN, 4 * HR, None),
    ("Transcription, L-LTP",     "#c1642f", 30 * MIN, 8 * HR, 14 * DAY),
    ("SWR replay",               "#a6433f", 0.1, 1 * DAY, 9 * DAY),
    ("System consolidation",     "#6b4a8a", 0.7 * DAY, 30 * DAY, 10 * YR),
]
TICKS = [(1e-3, "1 ms"), (0.1, "100 ms"), (1, "1 s"), (MIN, "1 min"), (HR, "1 hr"),
         (DAY, "1 day"), (WK, "1 week"), (YR, "1 year"), (10 * YR, "10 yr")]
GRID = [1e-3, 1e-2, 0.1, 1, 10, MIN, 600, HR, 10 * HR, DAY, WK, 30 * DAY, YR, 10 * YR]

plt.rcParams["font.family"] = "DejaVu Sans Mono"
fig = plt.figure(figsize=(18, 8), dpi=100)
ax = fig.add_axes([0.25, 0.17, 0.59, 0.80])
ax.set_xscale("log")
ax.set_xlim(1.5e-4, 2e9)
ax.set_ylim(len(ROWS) - 0.4, -0.8)
for g in GRID:
    ax.axvline(g, color="#dddddd", lw=1.2, zorder=0, ymax=0.97)
for i, (lab, col, a, b, tail) in enumerate(ROWS):
    if tail:
        ax.plot([b, tail], [i, i], ls=(0, (0.1, 2.2)), lw=9, color=col, alpha=0.55,
                dash_capstyle="round")
    ax.plot([a, b], [i, i], lw=22, color=col, solid_capstyle="round")
    y_fig = 0.17 + 0.80 * (len(ROWS) - 0.4 - i) / (len(ROWS) - 0.4 + 0.8)
    fig.text(0.012, y_fig, f"{i + 1} · {lab}", color=col, fontsize=17, va="center", ha="left")


def bracket(i0, i1, text, col):
    x = 1.012
    ax.plot([x, x + 0.006, x + 0.006, x], [i0 - 0.3, i0 - 0.3, i1 + 0.3, i1 + 0.3],
            transform=ax.get_yaxis_transform(), color=col, lw=2, clip_on=False)
    ax.text(x + 0.014, (i0 + i1) / 2, text, transform=ax.get_yaxis_transform(), color=col,
            fontsize=13, va="center", ha="left", clip_on=False)


bracket(4, 5, "cellular\nconsolidation\n(synaptic correlate,\nhypothesised;\n~0–6 h)", "#c1642f")
bracket(7, 7, "system\nconsolidation\n(days–years)", "#6b4a8a")

ax.set_yticks([])
ax.set_xticks([t for t, _ in TICKS], [l for _, l in TICKS], fontsize=14, color="#444")
ax.minorticks_off()
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#484c5e")
ax.spines["bottom"].set_linewidth(2)
fig.text(0.012, 0.03, "●●●  dotted = persistence after stabilization (row 6), recurrence (row 7), "
         "human range (row 8)", fontsize=15, color="#757886")
out = Path(__file__).resolve().parents[1] / "timescale_axis.png"
fig.savefig(out, facecolor="white")
print(out)
