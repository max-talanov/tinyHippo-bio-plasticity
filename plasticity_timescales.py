"""Shared time spans and colours for the plasticity timescale figures.

Used by make_fig_plasticity_overview.py (model document Fig. 1), figures/make_downscaling_timescale_axis.py and
figures/src/make_timescale_axis.py, so every process has one span, one order and one colour in all three figures.

Spans are order-of-magnitude summaries of Tables 1 and 2 in docs/plasticity_up_down_model_2026-11-06.md, not fitted values;
where a source gives only "hours" or "days", the end is our rounding. Times in seconds.
Colours: hot (amber to crimson) for upscaling, cold (teal to violet-blue) for downscaling, one per process.
"""
from matplotlib.colors import LinearSegmentedColormap, to_hex

MS, S, MIN, H, D, WK, MO, YR = 1e-3, 1.0, 60.0, 3600.0, 86400.0, 604800.0, 2.592e6, 3.156e7

# Upscaling, from Table 1 of the model document (the newer source where hippocampal_plasticity_model.md §1 differs).
# id -> (start, end, tail end or None). Tails: NMDA deactivation (U1, "hundreds of ms"), persistence after
# stabilisation (U6), recurrence of replay (U7), and the human range of system consolidation (U8).
UP_SPANS = {
    "U1": (0.5 * MS, 5 * MS, 0.5 * S),
    "U2": (10 * MS, 1 * S, None),
    "U3": (1 * S, 5 * MIN, None),
    "U4": (1 * MIN, 3 * H, None),
    "U5": (1 * MIN, 3 * H, None),
    "U6": (30 * MIN, 8 * H, 2 * WK),
    "U7": (40 * MS, 1 * D, 9 * D),
    "U8": (1 * D, 1 * MO, 10 * YR),
}
UP_ORDER = list(UP_SPANS)   # model order U1-U8, which is also roughly the order of onset

# id -> (start, end, recurring/extended tail end or None)
DOWN_SPANS = {
    "D1": (10 * MS, 10 * S, None),
    "D2": (50 * MS, 3 * H, None),
    "D3": (40 * MS, 3 * D, None),
    "D4a": (1 * S, 3 * H, None),
    "D4b": (1 * S, 3 * H, None),
    "D5": (1 * MIN, 30 * MIN, None),
    "D6": (1 * MIN, 3 * H, None),
    "D7": (1 * MIN, 1 * D, None),
    "D8": (1 * H, 2 * WK, None),
    "D9": (30 * MIN, 8 * H, None),
    "D10": (30 * MIN, 3 * D, None),
    "D11": (1 * H, 8 * H, 2 * WK),
    "D12": (4 * H, 3 * D, None),
    "D13": (1 * D, 6 * MO, 1 * YR),
    "D14": (1 * H, 3 * WK, None),
}
# Sorted by onset, then end, then id: the order of every downscaling list and figure.
DOWN_ORDER = sorted(DOWN_SPANS, key=lambda k: (DOWN_SPANS[k][0], DOWN_SPANS[k][1], k))

_HOT = LinearSegmentedColormap.from_list("hot", ["#E3A21A", "#E8731F", "#D93A26", "#A51A35", "#6E1230"])
_COLD = LinearSegmentedColormap.from_list("cold", ["#169EAE", "#2C6FD1", "#3B44B0", "#5B3E9E"])


def _ramp(cmap, n):
    return [to_hex(cmap(i / max(n - 1, 1))) for i in range(n)]


def hot(n):
    """n distinct hot colours, amber to crimson, for upscaling processes in order."""
    return _ramp(_HOT, n)


def cold(n):
    """n distinct cold colours, teal to violet-blue, for downscaling processes in order."""
    return _ramp(_COLD, n)


UP_COLOURS = dict(zip(UP_ORDER, hot(len(UP_ORDER))))
DOWN_COLOURS = dict(zip(DOWN_ORDER, cold(len(DOWN_ORDER))))


def lighten(hex_colour, amount):
    """`hex_colour` mixed with white; amount 0 keeps it, 1 gives white."""
    rgb = [int(hex_colour[i:i + 2], 16) / 255.0 for i in (1, 3, 5)]
    return to_hex([c + (1.0 - c) * amount for c in rgb])
