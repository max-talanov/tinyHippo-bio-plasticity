"""Overview figures for docs/plasticity_up_down_model_2026-11-06.md.

1. docs/figures/plasticity_timescales_all.png (Figure 1): upscaling U1-U8 and downscaling D1-D14 on one log time
   axis, one colour per process (hot for upscaling, cold for downscaling). Downscaling spans, order and colours come
   from plasticity_timescales.py, as do the upscaling spans; downscaling rows are sorted by onset. Spans are order-of-magnitude summaries, not fitted
   values. The dashed line is the 6 h behavioural window (personal communication, unverified).
2. docs/figures/plasticity_combination_chain.png (Figure 2): the chain of model states with the processes that raise
   (left) or lower (right) each one.
Both were first drawn by hand; this script redraws them so they can be regenerated. No data, no seeds.
Usage: python make_fig_plasticity_overview.py
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch

from plasticity_timescales import (DOWN_COLOURS, DOWN_ORDER, DOWN_SPANS, UP_COLOURS, UP_ORDER, UP_SPANS, MS, S, MIN,
                                   H, D, MO, YR, cold, hot, lighten)

PT = 0.72                       # points per pixel at dpi 100
INK, GREY, GRID = "#1A1A1A", "#6B6B6B", "#D9D8D3"
UP_EDGE, DN_EDGE = "#D0393B", "#2F73D0"   # Figure 2 box outlines
plt.rcParams["font.family"] = ["Arial", "DejaVu Sans"]

UP_LABELS = {
    "U1": "Neurotransmission", "U2": "STP", "U3": "Ca²⁺/kinase cascades", "U4": "AMPAR trafficking, early-LTP",
    "U5": "Tagging and capture", "U6": "Late-LTP, to stabilisation", "U7": "SWR replay",
    "U8": "System consolidation",
}
DOWN_LABELS = {
    "D1": "Vesicle-pool depletion", "D2": "Presynaptic GPCR inhibition",
    "D3": "SWR-triggered NMDAR depression", "D4a": "NMDAR → calcineurin/PP1 LTD", "D4b": "eCB → CB1 t-LTD",
    "D5": "PP1 depotentiation", "D6": "Heterosynaptic depression", "D7": "mGluR5 local-translation LTD",
    "D8": "GluA2 endocytosis", "D9": "PRP competition", "D10": "GluN2A/2B threshold shift",
    "D11": "Homer1a sleep scaling", "D12": "CaMKIV/TNFα scaling", "D13": "Pruning, active forgetting",
    "D14": "Protein turnover, UPS",
}
# (label, start, end, tail end or None, colour): upscaling in model order with hot colours; downscaling sorted by
# onset with cold colours. Spans, order and colours all come from plasticity_timescales.py.
UP_ROWS = [(f"{k} {UP_LABELS[k]}", *UP_SPANS[k], UP_COLOURS[k]) for k in UP_ORDER]
DOWN_ROWS = [(f"{k} {DOWN_LABELS[k]}", *DOWN_SPANS[k], DOWN_COLOURS[k]) for k in DOWN_ORDER]
TICKS = [(MS, "1 ms"), (S, "1 s"), (MIN, "1 min"), (H, "1 h"), (D, "1 d"), (MO, "1 mo"), (YR, "1 yr"),
         (10 * YR, "10 yr")]


def canvas(w, h):
    fig = plt.figure(figsize=(w / 100, h / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(h, 0)
    ax.axis("off")
    return fig, ax


def text(ax, x, y, s, px, colour=INK, weight="normal", ha="left"):
    ax.text(x, y, s, fontsize=px * PT, color=colour, fontweight=weight, ha=ha, va="center")


def box(ax, x0, y0, x1, y1, fill, edge, lw=1.6, r=12):
    ax.add_patch(FancyBboxPatch((x0, y0), x1 - x0, y1 - y0, boxstyle=f"round,pad=0,rounding_size={r}",
                                facecolor=fill, edgecolor=edge, linewidth=lw))


def timescales(out="docs/figures/plasticity_timescales_all.png"):
    w, row, x_label = 1344, 35.4, 42
    x_of = lambda t: 765 + 63 * np.log10(t)      # 63 px per decade, 1 s at x = 765
    top = 150
    h = int(top + row * (len(UP_ROWS) + len(DOWN_ROWS) + 1.35) + 60)
    fig, ax = canvas(w, h)
    text(ax, x_label, 42, "Upscaling and downscaling overlap from milliseconds to years", 25, weight="bold")
    y_bottom = h - 58
    ax.plot([513, 1302], [112, 112], color="#B4B2A9", lw=1.5)
    for t, lab in TICKS:
        ax.plot([x_of(t)] * 2, [112, y_bottom], color=GRID, lw=1.2, zorder=0)
        text(ax, x_of(t), 92, lab, 19, colour=GREY, ha="center")
    x6 = x_of(6 * H)
    ax.plot([x6, x6], [112, y_bottom], color="#B4B2A9", lw=1.5, ls=(0, (4, 4)), zorder=1)
    text(ax, x6, y_bottom + 30, "6 h behavioural window (unverified)", 19, colour=GREY, ha="center")
    text(ax, x_label, y_bottom + 30, "dotted = extended or recurring tail", 19, colour=GREY)

    y = top - row * 0.55
    for title, rows, key in (("Upscaling", UP_ROWS, hot(3)[1]), ("Downscaling", DOWN_ROWS, cold(3)[1])):
        box(ax, x_label, y - 9, x_label + 18, y + 9, lighten(key, 0.55), key, lw=1.6, r=3)
        text(ax, x_label + 29, y, title, 23, weight="bold")
        y += row
        for label, a, b, tail, colour in rows:
            text(ax, x_label, y, label, 20)
            if tail:
                xs = np.arange(x_of(b) + 9, x_of(tail), 9)
                ax.scatter(xs, np.full_like(xs, y), s=16, color=lighten(colour, 0.35), zorder=2, lw=0)
            box(ax, x_of(a), y - 10.5, x_of(b), y + 10.5, lighten(colour, 0.55), colour, lw=1.6, r=5)
            y += row
        y += row * 0.35
    fig.savefig(out, dpi=100, facecolor="white")
    plt.close(fig)
    print(f"wrote {out}")


LEFT = [
    ("More release", ["U2 STP: u rises per spike"], ["Decays with τ_fac"]),
    ("Calcium signal", ["U1 NMDAR opens on depolarisation", "U3 Ca²⁺/kinase cascades"], []),
    ("Tag set", ["U5 Coincident dendritic spike", "U4 AMPAR trafficking, early-LTP"], []),
    ("PRP supply", ["U5 Strong input, dopamine D1/D5", "U6 Protein synthesis on"], []),
    ("Weight stored", ["U5, U6 Capture, late-LTP", "U7 Replay drives capture"], []),
]
MIDDLE = [
    ("Release per spike", ["A = u · x"], ["Verified in NEURON"]),
    ("Segment signal", ["V_seg, then g_Ca(V_seg)"], ["Planned, S4–S5"]),
    ("Tag T", ["Lasts under 3 h unless captured"], ["Planned, S4"]),
    ("Capture gate", ["h(P), from the PRP pool P"], ["Planned, S4"]),
    ("Captured weight w_cap", ["Does not decay with τ_tag", "Turns over with τ_turn (D14)"],
     ["Planned, S4; turnover proposed"]),
]
RIGHT = [
    ("Less release", ["D1 Vesicle depletion", "D2 Presynaptic GPCR (A1R)", "D4b Endocannabinoid t-LTD"], []),
    ("Weaker or shifted signal", ["D4a NMDAR → phosphatase LTD", "D10 GluN2A/2B threshold shift"], []),
    ("Tag lost", ["D8 GluA2 removal (passive)", "D5 PP1 depotentiation (reset)"], []),
    ("PRPs limited", ["D9 Competition for PRPs", "D7 mGluR5 local translation",
                      "D14 Degraded constraint (UPS)"], []),
    ("Weight lowered or removed", ["D3 Ripple-triggered depression", "D6 Heterosynaptic depression",
                                   "D11 Homer1a sleep scaling", "D12 CaMKIV/TNFα scaling",
                                   "D13 Pruning, forgetting", "D14 Protein turnover (UPS)"], []),
]


def chain(out="docs/figures/plasticity_combination_chain.png"):
    w, line = 1344, 28
    cols = {"L": (42, 414), "M": (478, 866), "R": (930, 1302)}
    heights = [44 + line * max(len(a) + len(b) for _, a, b in (LEFT[i], MIDDLE[i], RIGHT[i])) + 16
               for i in range(len(LEFT))]
    gap, y0 = 42, 134
    h = int(y0 + sum(heights) + gap * (len(heights) - 1) + 42 + 86 + 48)
    fig, ax = canvas(w, h)
    text(ax, 42, 44, "Every level of the synapse has its own upward and downward processes", 25, weight="bold")
    for key, lab in (("L", "Upscaling"), ("M", "Model state"), ("R", "Downscaling")):
        x0, x1 = cols[key]
        text(ax, (x0 + x1) / 2, 98, lab, 22, weight="bold", ha="center")
    arrow = dict(arrowstyle="-|>", color="#B4B2A9", lw=1.6, mutation_scale=16, shrinkA=0, shrinkB=0)

    y = y0
    for i, hgt in enumerate(heights):
        yc = y + hgt / 2
        for key, (title, body, note), fill, edge, lw in (
                ("L", LEFT[i], "#FDF3F2", UP_EDGE, 1.8),
                ("M", MIDDLE[i], "#E3F3E0" if i == 0 else "#FAFAF8", "#2DA52D" if i == 0 else "#C8C6BE",
                 3.0 if i == 0 else 1.8),
                ("R", RIGHT[i], "#EEF4FD", DN_EDGE, 1.8)):
            x0, x1 = cols[key]
            box(ax, x0, y, x1, y + hgt, fill, edge, lw=lw)
            lines = [(title, INK, "bold")] + [(s, INK, "normal") for s in body] + [(s, GREY, "normal") for s in note]
            if key == "M":
                ty = yc - line * (len(lines) - 1) / 2
                for k, (s, c, wt) in enumerate(lines):
                    text(ax, (x0 + x1) / 2, ty + k * line, s, 22 if k == 0 else 20, colour=c, weight=wt,
                         ha="center")
            else:
                for k, (s, c, wt) in enumerate(lines):
                    text(ax, x0 + 22, y + 36 + k * line, s, 22 if k == 0 else 20, colour=c, weight=wt)
        ax.annotate("", xy=(cols["M"][0], yc), xytext=(cols["L"][1], yc), arrowprops=arrow)
        ax.annotate("", xy=(cols["M"][1], yc), xytext=(cols["R"][0], yc), arrowprops=arrow)
        y_next = y + hgt + gap
        ax.annotate("", xy=(672, y_next if i < len(heights) - 1 else y + hgt + 42), xytext=(672, y + hgt),
                    arrowprops=arrow)
        y = y_next
    yb = y - gap + 42
    box(ax, 372, yb, 972, yb + 86, "#EDEDEB", "#C8C6BE", lw=1.8)
    text(ax, 672, yb + 43, "Next spike: stored weight × release", 22, weight="bold", ha="center")
    fig.savefig(out, dpi=100, facecolor="white")
    plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    timescales()
    chain()
