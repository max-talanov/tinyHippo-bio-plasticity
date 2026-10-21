"""S3 pilot: Tier-B circuit under a 300 ms SC volley. Activity of all cells and weight profiles of PYR synapses.

PILOT: cell biophysics and contact counts are unverified placeholders (see cells.py, circuit.py).
Usage: python run_s3_pilot.py   -> docs/figures/s3_pilot_activity.png, s3_pilot_weights.png, prints tables.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from circuit import Config, TierB, G_HAT_NS
from params import PATHWAYS

SEEDS = range(5)
CFG = dict(rate_t=5.0)
OUT = "docs/figures/"
NAMES = ["pyr", "pv", "bis", "olm"]
WIN = (200.0, 500.0)


def run(seed, stp=True):
    return TierB(Config(seed=seed, stp=stp, **CFG)).run()


def counts(c):
    return {k: int(np.sum((np.array(c.spk[k]) >= WIN[0]) & (np.array(c.spk[k]) < WIN[1]))) for k in NAMES}


def pooled(res):
    ev = np.concatenate([e for e, _, _ in res]) if res else np.array([])
    w = np.concatenate([x for _, _, x in res]) if res else np.array([])
    return ev, w


def binned(ev, w, edges):
    m, s, n = [], [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        sel = (ev >= lo) & (ev < hi)
        n.append(int(sel.sum())); m.append(w[sel].mean() if sel.any() else np.nan)
        s.append(w[sel].std() if sel.sum() > 1 else np.nan)
    return np.array(m), np.array(s), np.array(n)


# ---- 5 seeds, STP on and off ------------------------------------------------------------------------------------
print("Spike counts in the 300 ms volley (200-500 ms), mean +- SD over 5 seeds, and 1 Hz background outside")
tab = {}
for stp in (True, False):
    cs = [counts(run(s, stp)) for s in SEEDS]
    tab[stp] = cs
    print(f"STP {'on ' if stp else 'off'}: " + "  ".join(
        f"{k} {np.mean([c[k] for c in cs]):.1f}+-{np.std([c[k] for c in cs], ddof=1):.1f}" for k in NAMES)
        + f"   (per seed pyr: {[c['pyr'] for c in cs]})")

# ---- seed 0: activity figure --------------------------------------------------------------------------------------
c = run(0, True)
print("\nNEURON-vs-closed-form release fraction, max abs deviation, first synapse of each excitatory pathway:", c.amp_check())
t = np.array(c.rec["t"])
fig, ax = plt.subplots(9, 1, figsize=(10, 12), sharex=True, gridspec_kw={"height_ratios": [1]*7 + [0.8, 1.2]})
labels = [("pyr_soma", "PYR soma"), ("pyr_basal", "PYR basal (SO)"), ("pyr_prox", "PYR apical prox (SR)"),
          ("pyr_dist", "PYR apical dist (SLM)"), ("pv", "PV basket"), ("bis", "Bistratified"), ("olm", "O-LM")]
for a, (k, lab) in zip(ax[:7], labels):
    a.plot(t, np.array(c.rec[k]), lw=0.7, color="#993C1D" if k.startswith("pyr") else "#185FA5")
    a.set_ylabel("mV", fontsize=8); a.set_title(lab, fontsize=9, loc="left", pad=1)
    a.axvspan(*WIN, color="#cccccc", alpha=0.35, lw=0)
for i, k in enumerate(NAMES):
    sp = np.array(c.spk[k]); ax[7].vlines(sp, i, i + 0.8, color="#993C1D" if k == "pyr" else "#185FA5", lw=0.8)
ax[7].set_yticks([0.4, 1.4, 2.4, 3.4]); ax[7].set_yticklabels(["PYR", "PV", "BiS", "O-LM"], fontsize=8)
ax[7].axvspan(*WIN, color="#cccccc", alpha=0.35, lw=0); ax[7].set_title("spike raster", fontsize=9, loc="left", pad=1)
for k, col in (("PV_PYR", "#0C447C"), ("BiS_PYR", "#378ADD"), ("OLM_PYR", "#85B7EB")):
    ax[8].plot(t, np.array(c.rec["g_" + k]) * 1e3, lw=0.8, label=k, color=col)
ax[8].axvspan(*WIN, color="#cccccc", alpha=0.35, lw=0)
ax[8].set_ylabel("nS", fontsize=8); ax[8].set_xlabel("time (ms)"); ax[8].legend(fontsize=7, ncol=3, loc="upper right")
ax[8].set_title("inhibitory conductance onto PYR", fontsize=9, loc="left", pad=1)
fig.suptitle("Tier-B pilot, seed 0, STP on. Grey: SC volley 200-500 ms. Unverified cell biophysics.", fontsize=10)
fig.tight_layout(); fig.savefig(OUT + "s3_pilot_activity.png", dpi=130); plt.close(fig)
print("rheobase-free check: spikes seed 0", {k: len(v) for k, v in c.spk.items()})

# ---- seed 0: weight profiles ---------------------------------------------------------------------------------------
we = c.weight_events()
edges = np.arange(0, 1001, 25.0)
mid = 0.5 * (edges[:-1] + edges[1:])
panels = [("SC_PYR", "SC -> PYR apical prox (SR)", "#D85A30"), ("SC_PYR_basal", "SC -> PYR basal (SO)", "#D85A30"),
          ("T_PYR", "T -> PYR apical prox (SR), 5 Hz", "#D85A30"),
          ("PV_PYR", "PV -> PYR soma", "#378ADD"), ("BiS_PYR", "BiS -> PYR apical prox", "#378ADD"),
          ("OLM_PYR", "O-LM -> PYR apical dist", "#378ADD")]
fig, ax = plt.subplots(2, 3, figsize=(12, 6.2), sharex=True)
print("\nEffective weight w*u*x (pS) per release event, seed 0. w = ghat (x contact scale for loop pathways). For loop pathways 'first/last 50 ms' use the first/last event when the window is empty.")
print(f"{'pathway':14s}{'w (pS)':>9s}{'U':>6s}{'w*U (pS)':>10s}{'n syn':>7s}{'n ev':>7s}{'pre-volley':>12s}{'first 50 ms':>13s}{'last 50 ms':>12s}{'last/first':>11s}")
rows = {}
for a, (k, lab, col) in zip(ax.ravel(), panels):
    ev, w = pooled(we[k]); n_syn = len(we[k])
    w_nom = (c.syn[k][0]["w"]) * 1e6
    U0 = PATHWAYS["SC_PYR" if k in ("SC_PYR_basal", "T_PYR") else k].U
    w_ref = w_nom * U0
    a.axvspan(*WIN, color="#cccccc", alpha=0.35, lw=0)
    if k.endswith("PYR") and k.startswith(("PV", "BiS", "OLM")):
        a.scatter(ev, w, s=12, color=col, zorder=3)
        a.plot(ev, w, lw=0.6, color=col, alpha=0.5)
    else:
        m, s, n = binned(ev, w, edges)
        a.plot(mid, m, color=col, lw=1.5); a.fill_between(mid, m - s, m + s, color=col, alpha=0.2, lw=0)
    a.axhline(w_ref, color="k", ls="--", lw=0.7)
    a.set_title(lab, fontsize=9, loc="left"); a.set_ylabel("w·u·x (pS)", fontsize=8)
    pre = w[(ev < WIN[0])]; early = w[(ev >= WIN[0]) & (ev < WIN[0] + 50)]; late = w[(ev >= WIN[1] - 50) & (ev < WIN[1])]
    f = lambda x: np.mean(x) if len(x) else np.nan
    first = f(early) if len(early) else (w[0] if len(w) else np.nan)
    last = f(late) if len(late) else (w[-1] if len(w) else np.nan)
    rows[k] = (w_nom, n_syn, len(ev), f(pre), first, last)
    print(f"{k:14s}{w_nom:9.0f}{U0:6.2f}{w_ref:10.0f}{n_syn:7d}{len(ev):7d}{f(pre):12.1f}{first:13.1f}{last:12.1f}{last/first:11.2f}")
for a in ax[1]: a.set_xlabel("time (ms)")
fig.suptitle("Effective synaptic weight onto the PYR, seed 0, STP on. Dashed: w·U (static-control level). Mean ± SD in 25 ms bins (SC, T); events (loops).",
             fontsize=10)
fig.tight_layout(); fig.savefig(OUT + "s3_pilot_weights.png", dpi=130); plt.close(fig)

