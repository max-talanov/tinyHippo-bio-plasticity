"""S3a: facilitation (STF, upscaling) vs depression (STD, downscaling) on every STP pathway of the Tier-B circuit.

Per spike n, release amp_n = u+_n x-_n splits exactly as
    log(amp_n / U) = fac_n + dep_n,   fac = log(u+/U) >= 0 (facilitation),   dep = log(x-) <= 0 (vesicle depletion)
(analysis.tm_pi_terms with no presynaptic inhibition), so w_eff,n = w U exp(fac_n + dep_n). T->PYR uses the SC->PYR
parameters (circuit.STP_OF). Release is computed in closed form and checked against NEURON (TMSyn.amp, CVODE) on the
same spike times. Parameters: params.PATHWAYS (secondary sources, see RESULTS.md section 3). No presynaptic inhibition
(section 11 covers it for SC). No time compression. Deterministic: no seeds.
Usage: python run_s3a_stp_all.py -> docs/figures/s3a_stp_all_{profiles,split_20Hz,split_theta,steady}.png,
       results/s3a_stp_all.csv
"""
import csv
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, LogLocator

import analysis as an
import protocols as pr
from params import PATHWAYS

GRID = pr.DT_FIXED
ORDER = ("SC_PYR", "SC_PV", "SC_BiS", "PYR_PV", "PYR_BiS", "PYR_OLM", "PV_PYR", "BiS_PYR", "OLM_PYR")
LABEL = {"SC_PYR": "SC → PYR (and T → PYR)", "SC_PV": "SC → PV", "SC_BiS": "SC → BiS", "PYR_PV": "PYR → PV",
         "PYR_BiS": "PYR → BiS", "PYR_OLM": "PYR → O-LM", "PV_PYR": "PV → PYR", "BiS_PYR": "BiS → PYR",
         "OLM_PYR": "O-LM → PYR"}
RATES = (5, 20, 80)
RATE_COLOR = {5: "tab:blue", 20: "tab:orange", 80: "tab:red"}
FREQS = np.logspace(0, np.log10(300), 25)
UP, DOWN = "tab:green", "tab:purple"
DPI = 150


def snap(t):
    return np.round(np.asarray(t) / GRID) * GRID


def periodic(f, dur=1000.0):
    return snap(10.0 + np.arange(int(round(f * dur / 1000.0))) * 1000.0 / f)


def theta_burst():
    return snap(np.concatenate([10.0 + 200.0 * b + 10.0 * np.arange(4) for b in range(10)]))


def terms(sp, name):
    p = PATHWAYS[name]
    return an.tm_pi_terms(sp, [], p.U, p.tau_rec, p.tau_fac)


def check(sp, name):
    p = PATHWAYS[name]
    amps, _, _ = pr.run_tm(sp, p.U, p.tau_rec, p.tau_fac, tail=5.0)
    return float(np.max(np.abs(amps - terms(sp, name)["amp"]) / amps))


def grid():
    fig, ax = plt.subplots(3, 3, figsize=(11, 8.5), sharex=True)
    return fig, ax.ravel()


def split_figure(sp, title, path):
    fig, ax = grid()
    x = np.arange(1, len(sp) + 1)
    for a, name in zip(ax, ORDER):
        r = terms(sp, name)
        a.bar(x, r["fac"], width=0.85, color=UP, label="facilitation (up)")
        a.bar(x, r["dep"], width=0.85, color=DOWN, label="depletion (down)")
        a.plot(x, r["fac"] + r["dep"], "k.-", ms=3, lw=0.9, label="net log(w_eff / wU)")
        a.axhline(0.0, color="0.5", lw=0.6)
        a.set_title(f"{LABEL[name]}  (U {PATHWAYS[name].U}, D {PATHWAYS[name].tau_rec:g}, F {PATHWAYS[name].tau_fac:g} ms)",
                    fontsize=9)
    for a in ax[6:]:
        a.set_xlabel("spike number")
    for a in ax[::3]:
        a.set_ylabel("log contribution")
    ax[0].legend(fontsize=7, loc="lower left")
    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(path, dpi=DPI)
    plt.close(fig)


def main():
    os.makedirs("docs/figures", exist_ok=True)
    os.makedirs("results", exist_ok=True)
    rows, max_err = [], 0.0

    # 1. per-spike weight w_eff / (w U) in 1 s trains at 5, 20, 80 Hz
    fig, ax = plt.subplots(3, 3, figsize=(11, 8.5), sharex=True)
    ax = ax.ravel()
    for a, name in zip(ax, ORDER):
        for f in RATES:
            sp = periodic(f)
            r = terms(sp, name)
            max_err = max(max_err, check(sp, name))
            a.plot(sp - sp[0], r["amp"] / PATHWAYS[name].U, ".-", ms=2.5, lw=0.9, color=RATE_COLOR[f], label=f"{f} Hz")
            rows.append(dict(part="train_1s", path=name, rate_hz=f, n=len(sp),
                             mean_w_rel=float(np.mean(r["amp"])) / PATHWAYS[name].U,
                             last_w_rel=float(r["amp"][-1]) / PATHWAYS[name].U,
                             sum_fac=float(np.sum(r["fac"])), sum_dep=float(np.sum(r["dep"]))))
        a.axhline(1.0, color="0.5", lw=0.6)
        a.set_yscale("log")
        a.yaxis.set_major_locator(LogLocator(subs=(1.0, 2.0, 5.0)))
        a.yaxis.set_minor_formatter(FuncFormatter(lambda *_: ""))
        a.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:g}"))
        a.set_title(LABEL[name], fontsize=9)
    for a in ax[6:]:
        a.set_xlabel("time in train (ms)")
    for a in ax[::3]:
        a.set_ylabel("w_eff / (w U)")
    ax[0].legend(fontsize=8)
    fig.suptitle("Per-spike weight in 1 s trains (1 = first spike; >1 net facilitation, <1 net depression)")
    fig.tight_layout()
    fig.savefig("docs/figures/s3a_stp_all_profiles.png", dpi=DPI)
    plt.close(fig)

    # 2, 3. up/down split per spike at 20 Hz and in a theta burst
    split_figure(periodic(20), "Up/down split per spike, 20 Hz for 1 s", "docs/figures/s3a_stp_all_split_20Hz.png")
    split_figure(theta_burst(), "Up/down split per spike, theta burst (10 bursts of 4 at 100 Hz, 5 Hz)",
                 "docs/figures/s3a_stp_all_split_theta.png")
    for name in ORDER:
        max_err = max(max_err, check(theta_burst(), name))

    # 4. steady state vs rate: facilitation, depletion and net, last spike of a long periodic train
    fig, ax = grid()
    for a, name in zip(ax, ORDER):
        p = PATHWAYS[name]
        fac, dep = [], []
        for f in FREQS:
            n = int(np.ceil(8 * max(p.tau_rec, p.tau_fac) * f / 1000.0)) + 20
            r = terms(snap(10.0 + np.arange(n) * 1000.0 / f), name)
            fac.append(r["fac"][-1])
            dep.append(r["dep"][-1])
        fac, dep = np.array(fac), np.array(dep)
        net = fac + dep
        a.fill_between(FREQS, 0, fac, color=UP, alpha=0.5, label="facilitation (up)")
        a.fill_between(FREQS, 0, dep, color=DOWN, alpha=0.5, label="depletion (down)")
        a.plot(FREQS, net, "k-", lw=1.2, label="net")
        a.axhline(0.0, color="0.5", lw=0.6)
        a.set_xscale("log")
        cross = np.where((net[:-1] >= 0) & (net[1:] < 0))[0]
        f_star = None
        if len(cross):
            i = cross[-1]
            lf = np.log(FREQS)
            f_star = float(np.exp(lf[i] + net[i] / (net[i] - net[i + 1]) * (lf[i + 1] - lf[i])))
            a.axvline(f_star, color="k", ls=":", lw=0.8)
        a.set_title(f"{LABEL[name]}" + (f"  f* = {f_star:.1f} Hz" if f_star else "  no crossover"), fontsize=9)
        rows.append(dict(part="steady", path=name, f_star_hz=f_star, max_net=float(net.max()),
                         f_max_net=float(FREQS[np.argmax(net)]),
                         **{f"net_{f:.3g}Hz": float(v) for f, v in zip(FREQS, net)}))
    for a in ax[6:]:
        a.set_xlabel("rate (Hz)")
    for a in ax[::3]:
        a.set_ylabel("log(R_ss / U)")
    ax[0].legend(fontsize=7, loc="lower left")
    fig.suptitle("Steady state vs rate: up (facilitation) and down (depletion) terms; net > 0 = net upscaling")
    fig.tight_layout()
    fig.savefig("docs/figures/s3a_stp_all_steady.png", dpi=DPI)
    plt.close(fig)

    keys = sorted({k for r in rows for k in r}, key=lambda k: (k not in rows[0], k))
    with open("results/s3a_stp_all.csv", "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=keys, lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)

    print("1 s trains: mean w_eff/(wU) | last spike | sum fac | sum dep")
    for r in rows:
        if r["part"] == "train_1s":
            print(f"  {r['path']:8s} {r['rate_hz']:3d} Hz  {r['mean_w_rel']:5.2f} | {r['last_w_rel']:5.2f} | "
                  f"{r['sum_fac']:7.2f} | {r['sum_dep']:8.2f}")
    print("steady state: f* (net up -> net down), max net factor")
    for r in rows:
        if r["part"] == "steady":
            fs = "none" if r["f_star_hz"] is None else f"{r['f_star_hz']:.1f} Hz"
            print(f"  {r['path']:8s} f* {fs:9s} max exp(net) {np.exp(r['max_net']):.2f} at {r['f_max_net']:.1f} Hz")
    print(f"NEURON vs closed form, max relative release difference: {max_err:.1e}")


if __name__ == "__main__":
    main()
