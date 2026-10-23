"""S3a: single-synapse balance map. Balance index B(f) = R_ss(f) / U per pathway, crossover f*, U-gain dependence.

R_ss is the release fraction u+ * x- of the last pulse of a periodic train, read from TMSyn.amp in NEURON (CVODE),
and compared with the closed form (analysis.tm_amplitudes) on the identical spike times. Spike times are snapped to the
0.025 ms grid. Train length = 8 * max(tau_rec, tau_fac) of biology + 20 pulses, so the steady state is reached.
B > 1: net upscaling (facilitation wins). B < 1: net downscaling (depression wins). U gain g scales U (presynaptic
inhibition g < 1, higher [Ca2+]o or enhancers g > 1), U = min(1, g * U0).
Deterministic: no seeds. Parameters are the secondary-source values of params.py.
Usage: python run_s3a.py  -> docs/figures/s3a_balance_map.png, results/s3a_balance.csv, tables on stdout.
"""
import csv
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import brentq

import analysis as an
import protocols as pr
from params import PATHWAYS

GRID = 0.025
FREQ_FINE = np.logspace(0, np.log10(300), 25)        # gain 1
FREQ_GAIN = np.logspace(0, np.log10(300), 13)        # other gains
GAINS = (0.5, 0.75, 1.0, 1.25, 1.5)
W = 1e-3


def train(f, tau_rec, tau_fac):
    n = int(np.ceil(8 * max(tau_rec, tau_fac) * f / 1000.0)) + 20
    return np.round((10.0 + np.arange(n) * 1000.0 / f) / GRID) * GRID


def release(sp, U, D, F):
    """(neuron_release, closed_form_release) for a train."""
    a, _, _ = pr.run_tm(sp, U, D, F, w=W, tail=5.0)
    return a, an.tm_amplitudes(sp, U, D, F)


def crossover(freqs, B):
    """Highest frequency at which B crosses 1 downwards (log-linear interpolation), else None."""
    idx = [i for i in range(len(B) - 1) if B[i] >= 1.0 > B[i + 1]]
    if not idx:
        return None
    i = idx[-1]
    lf = np.log(freqs[i]) + (B[i] - 1.0) / (B[i] - B[i + 1]) * (np.log(freqs[i + 1]) - np.log(freqs[i]))
    return float(np.exp(lf))


def closed_form_B(p, f, g=1.0):
    U = min(1.0, g * p.U)
    return an.tm_amplitudes(train(f, p.tau_rec, p.tau_fac), U, p.tau_rec, p.tau_fac)[-1] / U


rows, dev_all = [], []
for name, p in PATHWAYS.items():
    for g in GAINS:
        U = min(1.0, g * p.U)
        for f in (FREQ_FINE if g == 1.0 else FREQ_GAIN):
            sp = train(f, p.tau_rec, p.tau_fac)
            a, ref = release(sp, U, p.tau_rec, p.tau_fac)
            dev = float(np.max(np.abs(a / ref - 1.0)))
            dev_all.append(dev)
            f_eff = 1000.0 / np.mean(np.diff(sp))
            rows.append(dict(pathway=name, gain=g, U=U, f_nominal=f, f_actual=f_eff, n_pulses=len(sp),
                             R_first=a[0], R_ss=a[-1], B=a[-1] / U, R_ss_closed=ref[-1], max_rel_dev=dev))
    print(f"done {name}", flush=True)

os.makedirs("results", exist_ok=True)
with open("results/s3a_balance.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

print(f"\nNEURON vs closed form, max |release ratio - 1| over {len(rows)} trains: {max(dev_all):.2e}  (criterion < 1e-2)")


def sel(name, g):
    r = sorted([x for x in rows if x["pathway"] == name and x["gain"] == g], key=lambda x: x["f_nominal"])
    return np.array([x["f_actual"] for x in r]), np.array([x["R_ss"] for x in r]), np.array([x["B"] for x in r])


print("\nB(f) = R_ss/U at gain 1 (NEURON), crossover f* (NEURON, log-linear interpolation on 25 points), and closed-form f*")
hdr_f = (1, 5, 20, 80, 200, 300)
print(f"{'pathway':9s}" + "".join(f"{f:>7d}" for f in hdr_f) + f"{'max B':>8s}{'at Hz':>8s}{'f* NEURON':>11s}{'f* closed':>11s}  class")
summary = {}
for name, p in PATHWAYS.items():
    fr, R, B = sel(name, 1.0)
    at = lambda f: B[np.argmin(np.abs(fr - f))]
    fs = crossover(fr, B)
    dense = np.logspace(0, np.log10(300), 400)
    Bc = np.array([closed_form_B(p, f) for f in dense])
    fc = crossover(dense, Bc)
    cls = "down only" if B.max() < 1.0 else ("up and down" if fs else "up throughout")
    summary[name] = (fs, fc, B.max(), fr[B.argmax()], cls)
    print(f"{name:9s}" + "".join(f"{at(f):7.2f}" for f in hdr_f) + f"{B.max():8.2f}{fr[B.argmax()]:8.1f}"
          f"{(f'{fs:.1f}' if fs else '-'):>11s}{(f'{fc:.1f}' if fc else '-'):>11s}  {cls}")

print("\nU gain: crossover f* (Hz) and absolute steady-state release R_ss at 5 / 20 / 80 / 200 Hz (NEURON)")
print(f"{'pathway':9s}{'gain':>6s}{'U':>7s}{'f*':>8s}   R_ss(5)  R_ss(20)  R_ss(80)  R_ss(200)")
for name in ("SC_PYR", "SC_PV", "PYR_OLM", "PV_PYR"):
    for g in GAINS:
        fr, R, B = sel(name, g)
        fs = crossover(fr, B)
        at = lambda f: R[np.argmin(np.abs(fr - f))]
        print(f"{name:9s}{g:6.2f}{min(1, g * PATHWAYS[name].U):7.3f}{(f'{fs:.1f}' if fs else '-'):>8s}"
              f"{at(5):9.3f}{at(20):10.3f}{at(80):10.3f}{at(200):11.3f}")

print("\nVoltage-clamp spot check (release read from the EPSC, peak minus pre-pulse current), 5 and 20 Hz, gain 1")
scale = W * 70.0
worst = 0.0
for name, p in PATHWAYS.items():
    for f in (5.0, 20.0):
        sp = train(f, p.tau_rec, p.tau_fac)
        t, i = pr.run_clamped(sp, p.U, p.tau_rec, p.tau_fac, w=W, tail=30.0)
        amp = pr.epsc_amplitudes(t, i, sp)
        ref = an.tm_amplitudes(sp, p.U, p.tau_rec, p.tau_fac) * scale
        worst = max(worst, float(np.max(np.abs(np.abs(amp) / ref - 1.0))))
print(f"max |EPSC amplitude / (w * 70 mV * release) - 1| over all 9 pathways: {worst:.2e}")

fig, ax = plt.subplots(1, 3, figsize=(15, 4.4))
col = {"SC_PYR": "#D85A30", "SC_PV": "#EF9F27", "SC_BiS": "#BA7517", "PYR_PV": "#185FA5", "PYR_BiS": "#378ADD",
       "PYR_OLM": "#534AB7", "PV_PYR": "#0F6E56", "BiS_PYR": "#1D9E75", "OLM_PYR": "#5DCAA5"}
for name in PATHWAYS:
    fr, R, B = sel(name, 1.0)
    ax[0].semilogx(fr, B, label=name, color=col[name], lw=1.6)
ax[0].axhline(1, color="k", lw=0.8, ls="--"); ax[0].set_xlabel("presynaptic rate (Hz)"); ax[0].set_ylabel("B = R_ss / U")
ax[0].set_title("Balance index (>1 up, <1 down)", fontsize=10); ax[0].legend(fontsize=7, ncol=3)
for g in GAINS:
    fr, R, B = sel("SC_PYR", g)
    ax[1].semilogx(fr, B, label=f"gain {g}", lw=1.4)
ax[1].axhline(1, color="k", lw=0.8, ls="--"); ax[1].set_xlabel("presynaptic rate (Hz)"); ax[1].set_ylabel("B")
ax[1].set_title("SC to PYR: effect of a U gain on B", fontsize=10); ax[1].legend(fontsize=8)
for g in GAINS:
    fr, R, B = sel("SC_PYR", g)
    ax[2].loglog(fr, R, label=f"gain {g}", lw=1.4)
ax[2].set_xlabel("presynaptic rate (Hz)"); ax[2].set_ylabel("steady-state release per spike")
ax[2].set_title("SC to PYR: release saturates at high rate", fontsize=10); ax[2].legend(fontsize=8)
fig.suptitle("S3a single-synapse balance map (NEURON TMSyn, secondary-source parameters)", fontsize=11)
fig.tight_layout(); fig.savefig("docs/figures/s3a_balance_map.png", dpi=130)
