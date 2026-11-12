"""Overview figures for docs/plasticity_up_down_model_2026-11-06.md.

1. docs/figures/plasticity_timescales_all.png (Figure 1): upscaling U1-U8 and downscaling D1-D14 on one log time
   axis. Spans are order-of-magnitude summaries of the two source documents (hippocampal_plasticity_model.md and
   hippocampal_downscaling_mechanisms.md), not fitted values; where a source gives only "hours" or "days", the end is
   our rounding. The dashed line is the 6 h behavioural window (personal communication, unverified).
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

MS, S, MIN, H, D, WK, MO, YR = 1e-3, 1.0, 60.0, 3600.0, 86400.0, 604800.0, 2.592e6, 3.156e7
PT = 0.72                       # points per pixel at dpi 100
INK, GREY, GRID = "#1A1A1A", "#6B6B6B", "#D9D8D3"
UP_FILL, UP_EDGE = "#F2C4C4", "#D0393B"
DN_FILL, DN_EDGE = "#BFD5F2", "#2F73D0"
plt.rcParams["font.family"] = ["Arial", "DejaVu Sans"]

UPSCALING = [
    ("U1 Neurotransmission", 0.5 * MS, 0.5 * S),
    ("U2 STP", 10 * MS, 1 * S),
    ("U3 Ca²⁺/kinase cascades", 1 * S, 5 * MIN),
    ("U4 AMPAR trafficking, early-LTP", 1 * MIN, 3 * H),
    ("U5 Tagging and capture", 1 * MIN, 3 * H),
    ("U6 Late-LTP, to stabilisation", 30 * MIN, 8 * H),
    ("U7 SWR replay", 40 * MS, 3 * D),
    ("U8 System consolidation", 1 * D, 10 * YR),
]
DOWNSCALING = [
    ("D1 Vesicle-pool depletion", 10 * MS, 10 * S),
    ("D2 Presynaptic GPCR inhibition", 50 * MS, 3 * H),
    ("D3 SWR-triggered NMDAR depression", 40 * MS, 3 * D),
    ("D4a NMDAR → calcineurin/PP1 LTD", 1 * S, 3 * H),
    ("D4b eCB → CB1 t-LTD", 1 * S, 3 * H),
    ("D5 PP1 depotentiation", 1 * MIN, 30 * MIN),
    ("D6 Heterosynaptic depression", 1 * MIN, 3 * H),
    ("D7 mGluR5 local-translation LTD", 1 * MIN, 1 * D),
    ("D8 GluA2 endocytosis", 1 * H, 2 * WK),
    ("D9 PRP competition", 30 * MIN, 8 * H),
    ("D10 GluN2A/2B threshold shift", 30 * MIN, 3 * D),
    ("D11 Homer1a sleep scaling", 1 * H, 8 * H),
    ("D12 CaMKIV/TNFα scaling", 4 * H, 3 * D),
    ("D13 Pruning, active forgetting", 1 * D, 6 * MO),
    ("D14 Protein turnover, UPS", 1 * H, 3 * WK),
]
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
    h = int(top + row * (len(UPSCALING) + len(DOWNSCALING) + 1.35) + 60)
    fig, ax = canvas(w, h)
    text(ax, x_label, 42, "Upscaling and downscaling overlap from 10 ms to months", 25, weight="bold")
    y_bottom = h - 58
    ax.plot([513, 1302], [112, 112], color="#B4B2A9", lw=1.5)
    for t, lab in TICKS:
        ax.plot([x_of(t)] * 2, [112, y_bottom], color=GRID, lw=1.2, zorder=0)
        text(ax, x_of(t), 92, lab, 19, colour=GREY, ha="center")
    x6 = x_of(6 * H)
    ax.plot([x6, x6], [112, y_bottom], color="#B4B2A9", lw=1.5, ls=(0, (4, 4)), zorder=1)
    text(ax, x6, y_bottom + 30, "6 h behavioural window (unverified)", 19, colour=GREY, ha="center")

    y = top - row * 0.55
    for title, rows, fill, edge in (("Upscaling", UPSCALING, UP_FILL, UP_EDGE),
                                    ("Downscaling", DOWNSCALING, DN_FILL, DN_EDGE)):
        box(ax, x_label, y - 9, x_label + 18, y + 9, fill, edge, lw=1.6, r=3)
        text(ax, x_label + 29, y, title, 23, weight="bold")
        y += row
        for label, a, b in rows:
            text(ax, x_label, y, label, 20)
            box(ax, x_of(a), y - 10.5, x_of(b), y + 10.5, fill, edge, lw=1.6, r=5)
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
