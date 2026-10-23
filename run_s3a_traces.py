"""S3a companion: synaptic conductance traces and per-spike weight profiles of each pathway under regular trains.

Single synapse, naive start (u = 0, x = 1), periodic trains at 5, 20 and 80 Hz for 1 s, nominal peak conductance g-hat
of circuit.G_HAT_NS (SC and T conductances are unverified assumptions; PYR<->interneuron without the contact scale K).
Conductance g(t) = B - A of TMSyn (the quantity a PYR or interneuron membrane sees); per-spike weight = g-hat * u+ * x-.
Usage: python run_s3a_traces.py -> docs/figures/s3a_conductance_traces.png, s3a_weight_profiles.png
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import analysis as an
import protocols as pr
from circuit import G_HAT_NS
from params import PATHWAYS

RATES = (5.0, 20.0, 80.0)
GRID = 0.025
GHAT = {"SC_PYR": G_HAT_NS["SC_PYR"], "SC_PV": G_HAT_NS["SC_PV"], "SC_BiS": G_HAT_NS["SC_BiS"],
        "PYR_PV": G_HAT_NS["PYR_PV"], "PYR_BiS": G_HAT_NS["PYR_BiS"], "PYR_OLM": G_HAT_NS["PYR_OLM"],
        "PV_PYR": G_HAT_NS["PV_PYR"], "BiS_PYR": G_HAT_NS["BiS_PYR"], "OLM_PYR": G_HAT_NS["OLM_PYR"]}
EXC = {"SC_PYR", "SC_PV", "SC_BiS", "PYR_PV", "PYR_BiS", "PYR_OLM"}


def train(f, dur=1000.0):
    n = int(dur * f / 1000.0)
    return np.round((10.0 + np.arange(n) * 1000.0 / f) / GRID) * GRID


def run(name, f):
    p = PATHWAYS[name]
    sp = train(f)
    amps, t, g = pr.run_tm(sp, p.U, p.tau_rec, p.tau_fac, w=GHAT[name] * 1e-3, tail=30.0)   # g in uS
    ref = an.tm_amplitudes(sp, p.U, p.tau_rec, p.tau_fac)
    assert np.max(np.abs(amps / ref - 1)) < 1e-6
    return sp, amps, t, g * 1e3                                                          # nS


# ---- conductance traces: one up-then-down, one strongly up, one down-only pathway --------------------------------
rows = ["SC_PYR", "PYR_OLM", "PV_PYR"]
titles = {"SC_PYR": "SC → PYR (up, then down)", "PYR_OLM": "PYR → O-LM (strong up)", "PV_PYR": "PV → PYR (down only)"}
fig, ax = plt.subplots(3, 3, figsize=(13, 7.5), sharex="col")
for i, name in enumerate(rows):
    col = "#D85A30" if name in EXC else "#378ADD"
    for j, f in enumerate(RATES):
        sp, amps, t, g = run(name, f)
        ax[i, j].plot(t - 10.0, g, color=col, lw=0.9)
        ax[i, j].set_xlim(0, 1000 if f < 80 else 400)
        if i == 0:
            ax[i, j].set_title(f"{int(f)} Hz", fontsize=10)
        if j == 0:
            ax[i, j].set_ylabel(titles[name] + "\ng (nS)", fontsize=8)
        if i == 2:
            ax[i, j].set_xlabel("time since first spike (ms)")
fig.suptitle("S3a: synaptic conductance of a single synapse under regular trains (TMSyn in NEURON, naive start). "
             "80 Hz shown for 400 ms.", fontsize=10)
fig.tight_layout(); fig.savefig("docs/figures/s3a_conductance_traces.png", dpi=130); plt.close(fig)

# ---- weight profiles: effective weight per spike, all pathways ---------------------------------------------------
fig, ax = plt.subplots(3, 3, figsize=(13, 8.5), sharex=False)
colr = {5.0: "#0C447C", 20.0: "#D85A30", 80.0: "#3B6D11"}
print(f"{'pathway':9s}{'g-hat (pS)':>11s}  weight per spike, first / spike 5 / spike 10 / last (pS) at 5, 20, 80 Hz")
for a, name in zip(ax.ravel(), PATHWAYS):
    line = f"{name:9s}{GHAT[name] * 1e3:11.0f}  "
    for f in RATES:
        sp, amps, t, g = run(name, f)
        w = amps * GHAT[name] * 1e3
        a.plot(sp - 10.0, w, "o-", ms=3, lw=0.8, color=colr[f], label=f"{int(f)} Hz")
        k = lambda i: w[min(i, len(w) - 1)]
        line += f"[{k(0):6.0f} {k(4):6.0f} {k(9):6.0f} {w[-1]:6.0f}]  "
    print(line)
    a.axhline(PATHWAYS[name].U * GHAT[name] * 1e3, color="k", lw=0.7, ls="--")
    a.set_xscale("symlog", linthresh=20); a.set_title(name.replace("_", " → "), fontsize=9, loc="left")
    a.set_ylabel("w·u·x (pS)", fontsize=8); a.set_xlabel("time since first spike (ms)", fontsize=8)
ax[0, 0].legend(fontsize=7)
fig.suptitle("S3a: effective weight w·u·x per spike during 1 s regular trains (dashed: first-spike weight ĝ·U). Unitary ĝ.",
             fontsize=10)
fig.tight_layout(); fig.savefig("docs/figures/s3a_weight_profiles.png", dpi=130); plt.close(fig)
