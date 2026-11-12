"""Render figures/downscaling_timescale_axis.png.

Companion to figures/timescale_axis.png (potentiation/consolidation stages):
the same log time axis (1 ms - 10 yr), showing synaptic downscaling mechanisms.
Bar spans are characteristic ranges from the references in
hippocampal_downscaling_mechanisms.md, rounded to the order of magnitude.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

MS, S, MIN, HR, DAY, WK, YR = 1e-3, 1.0, 60.0, 3600.0, 86400.0, 604800.0, 3.156e7

# (id, molecular pathway, start_s, end_s, tail_end_s or None, colour)
# Ids match the sections of hippocampal_downscaling_mechanisms.md. Rows are
# drawn in order of onset (start_s), ties broken by end_s then id, so the
# bars form a staircase like figures/timescale_axis.png.
MECHANISMS = sorted([
    ("1",  "Vesicle-pool depletion",        10 * MS, 10 * S,  None,     "#2e6fa7"),
    ("2",  "Presynaptic GPCR (A1, GABA_B)", 50 * MS, 10 * MIN, 12 * HR, "#1f8fa0"),
    ("3",  "SWR-triggered NMDAR depr.",     100 * MS, 8 * HR, 3 * DAY,  "#3f8f6a"),
    ("4a", "NMDAR → calcineurin/PP1 LTD",   10 * S,  3 * HR,  None,     "#4a8c3a"),
    ("4b", "eCB → CB1 presynaptic t-LTD",   10 * S,  3 * HR,  None,     "#5d8f34"),
    ("5",  "PP1 depotentiation (A1R)",      1 * MIN, 1 * HR,  None,     "#6f8f2e"),
    ("6",  "IP3R/calcineurin heterosyn.",   1 * MIN, 2 * HR,  None,     "#a98a2e"),
    ("7",  "mGluR5 → local translation",    5 * MIN, 1 * DAY, None,     "#c08a2a"),
    ("8",  "GluA2 endocytosis (E-LTP decay)", 30 * MIN, 4 * HR, None,   "#c4632f"),
    ("9",  "PRP competition",               30 * MIN, 8 * HR, None,     "#b5533a"),
    ("10", "GluN2A/2B threshold shift",     30 * MIN, 2 * DAY, None,    "#a64541"),
    ("11", "Homer1a–mGluR5 sleep scaling",  1 * HR,  1 * DAY, 2 * WK,   "#9a3f5c"),
    ("12", "CaMKIV/TNFα synaptic scaling",  12 * HR, 3 * DAY, None,     "#7d4a8a"),
    ("13", "Complement/microglia pruning",  1 * DAY, 5 * WK,  1 * YR,   "#5a4f86"),
    ("14", "UPS degradation / turnover",    1 * HR,  3 * WK,  None,     "#4a5a8a"),
], key=lambda m: (m[2], m[3], m[0]))

# Upscaling process drawn on top as a time reference, as in figures/timescale_axis.png:
# neurotransmission (AMPA/NMDA gating), ~0.5-5 ms per hippocampal_plasticity_model.md §1.
REFERENCE = [("U1", "Neurotransmission (ref.)", 0.5 * MS, 5 * MS, None, "#8a8f99")]

TICKS = [(1 * MS, "1 ms"), (100 * MS, "100 ms"), (1 * S, "1 s"), (1 * MIN, "1 min"),
         (1 * HR, "1 hr"), (1 * DAY, "1 day"), (1 * WK, "1 week"),
         (1 * YR, "1 year"), (10 * YR, "10 yr")]


def lighten(hex_colour, amount=0.45):
    rgb = np.array([int(hex_colour[i:i + 2], 16) for i in (1, 3, 5)]) / 255.0
    return tuple(rgb + (1.0 - rgb) * amount)


def main(out=Path(__file__).with_name("downscaling_timescale_axis.png")):
    plt.rcParams["font.family"] = "monospace"
    rows = REFERENCE + MECHANISMS
    n = len(rows)
    fig, ax = plt.subplots(figsize=(18, 0.68 * n + 1.9), dpi=100)
    x0, x1 = np.log10(0.6 * MS), np.log10(14 * YR)
    label_x = x0 - 3.6

    grid = np.arange(-3, np.log10(10 * YR) + 0.01, 0.5)
    ax.vlines(grid, 0.15, n + 0.7, color="#dddddd", lw=1.2, zorder=0)

    ax.hlines(n - len(REFERENCE) + 0.5, label_x, x1, color="#bbbbbb", lw=1, ls=(0, (4, 4)))
    for i, (mid, label, a, b, tail, colour) in enumerate(rows):
        y = n - i
        ax.plot([np.log10(a), np.log10(b)], [y, y], color=colour, lw=19,
                solid_capstyle="round", zorder=3)
        if tail:
            xs = np.arange(np.log10(b) + 0.09, np.log10(tail), 0.09)
            ax.scatter(xs, np.full_like(xs, y), s=70, color=lighten(colour), zorder=2)
        ax.text(label_x, y, f"{mid:>2} · {label}", color=colour, fontsize=15,
                va="center", ha="left")

    ax.axhline(0.15, xmin=0.0, color="#555a66", lw=2)
    for t, lab in TICKS:
        ax.plot([np.log10(t)] * 2, [0.15, 0.0], color="#555a66", lw=2)
        ax.text(np.log10(t), -0.35, lab, ha="center", va="top", fontsize=13,
                color="#333333")

    ax.scatter([label_x + 0.05, label_x + 0.2, label_x + 0.35], [-1.2] * 3,
               s=90, color="#6b6f7a", clip_on=False)
    ax.text(label_x + 0.6, -1.2, "dotted = recurring / extended tail "
            "(repeated sleep cycles, slow structural follow-through)",
            fontsize=13, color="#555a66", va="center")
    ax.text(label_x + 0.6, -1.75, "grey, above the dashed line = U1 neurotransmission, "
            "an upscaling process shown as a time reference",
            fontsize=13, color="#555a66", va="center")

    ax.set_xlim(label_x - 0.1, x1)
    ax.set_ylim(-2.1, n + 0.8)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(out, facecolor="white")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
