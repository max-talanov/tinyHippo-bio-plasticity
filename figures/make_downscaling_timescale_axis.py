"""Render figures/downscaling_timescale_axis.png.

Companion to figures/timescale_axis.png (potentiation/consolidation stages):
the same log time axis (1 ms - 10 yr), showing synaptic downscaling mechanisms.
Spans, onset order and colours come from plasticity_timescales.py, shared with the
model document's Fig. 1; each pathway has its own cold colour, and the U1
reference row is hot. Spans are order-of-magnitude summaries, not fitted values.
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from plasticity_timescales import (DOWN_COLOURS, DOWN_ORDER, DOWN_SPANS, MS, S, MIN, H, D, WK, YR,  # noqa: E402
                                   hot, lighten)

# Short pathway names; ids match the sections of hippocampal_downscaling_mechanisms.md (D4a is "4a").
LABELS = {
    "D1": "Vesicle-pool depletion", "D2": "Presynaptic GPCR (A1, GABA_B)", "D3": "SWR-triggered NMDAR depr.",
    "D4a": "NMDAR → calcineurin/PP1 LTD", "D4b": "eCB → CB1 presynaptic t-LTD", "D5": "PP1 depotentiation (A1R)",
    "D6": "IP3R/calcineurin heterosyn.", "D7": "mGluR5 → local translation",
    "D8": "GluA2 endocytosis (E-LTP decay)", "D9": "PRP competition", "D10": "GluN2A/2B threshold shift",
    "D11": "Homer1a–mGluR5 sleep scaling", "D12": "CaMKIV/TNFα synaptic scaling",
    "D13": "Complement/microglia pruning", "D14": "UPS degradation / turnover",
}
# (id, name, start_s, end_s, tail_end_s or None, colour), in onset order.
MECHANISMS = [(k[1:], LABELS[k], *DOWN_SPANS[k], DOWN_COLOURS[k]) for k in DOWN_ORDER]

# Upscaling process drawn on top as a time reference, as in figures/timescale_axis.png:
# neurotransmission (AMPA/NMDA gating), ~0.5-5 ms per hippocampal_plasticity_model.md §1.
REFERENCE = [("U1", "Neurotransmission", 0.5 * MS, 5 * MS, None, hot(2)[0])]

TICKS = [(1 * MS, "1 ms"), (100 * MS, "100 ms"), (1 * S, "1 s"), (1 * MIN, "1 min"),
         (1 * H, "1 hr"), (1 * D, "1 day"), (1 * WK, "1 week"),
         (1 * YR, "1 year"), (10 * YR, "10 yr")]


def main(out=Path(__file__).with_name("downscaling_timescale_axis.png")):
    plt.rcParams["font.family"] = "monospace"
    rows = REFERENCE + MECHANISMS
    n = len(rows)
    fig, ax = plt.subplots(figsize=(18, 0.68 * n + 2.3), dpi=100)
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
            ax.scatter(xs, np.full_like(xs, y), s=70, color=lighten(colour, 0.45), zorder=2)
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
    ax.text(label_x + 0.6, -1.75, "warm row above the dashed line = U1 neurotransmission, "
            "an upscaling process shown as a time reference",
            fontsize=13, color="#555a66", va="center")
    ax.text(label_x + 0.6, -2.3, "cold rows = downscaling pathways, one colour each, sorted by onset",
            fontsize=13, color="#555a66", va="center")

    ax.set_xlim(label_x - 0.1, x1)
    ax.set_ylim(-2.6, n + 0.8)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(out, facecolor="white")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
