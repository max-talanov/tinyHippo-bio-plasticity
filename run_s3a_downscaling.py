"""S3a: up- vs downscaling inside STP with presynaptic GPCR inhibition (downscaling #2) added to depletion (#1).

Per spike n of a train, mod/TMSynPI.mod gives the exact split
    log(amp_n / U) = fac_n + dep_n + phasic_n + tonic_n
    fac    = log(u+/U_eff) >= 0   facilitation                                   (upscaling)
    dep    = log(x-)       <= 0   vesicle depletion, #1                          (downscaling)
    phasic = log(1 - I)    <= 0   activity-dependent A1R inhibition of U        (downscaling, #2)
    tonic  = log(1-i_ton)  <= 0   tonic A1R inhibition of U (ambient adenosine)  (downscaling, #2)
so the per-spike weight w_eff = w * amp is w * U * exp(up + down). Drive: every presynaptic spike stands for a volley of
the SC population, which releases adenosine onto the terminal with a 50 ms lag (Mitchell et al. 1993; the drive per
volley c was measured for a 1-mV-fEPSP volley, so the population must fire with this synapse). Release is read from NEURON
(TMSynPI.amp etc., fixed step 0.025 ms) and checked against analysis.tm_pi_terms on the same spike times.
Parameters: STP from params.PATHWAYS (secondary sources); inhibition from params.PRESYN_INHIB["SC_A1R"] (Mitchell et
al. 1993, rat, 34 C, 2.5 mM Ca; kinetics and c fitted here), also swept. GABA_B (#2 too) has only its maximum
(PRESYN_INHIB["SC_GABAB"]), no kinetics, and is not run. No time compression. Deterministic: no seeds.
Usage: python run_s3a_downscaling.py -> docs/figures/s3a_downscaling_profiles.png, docs/figures/s3a_downscaling_balance.png,
       results/s3a_downscaling.csv, tables on stdout.
"""
import csv
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import analysis as an
import protocols as pr
from params import PATHWAYS, PRESYN_INHIB

GRID = pr.DT_FIXED
PI = PRESYN_INHIB["SC_A1R"]
KIN = dict(tau_r=PI.tau_r, tau_d=PI.tau_d)
CONDITIONS = {                  # name -> (i_tonic, i_max, c)
    "STP only": (0.0, 0.0, 0.0),
    "+ tonic": (PI.i_tonic, 0.0, 0.0),
    "+ phasic": (0.0, PI.i_max, PI.c),
    "+ tonic + phasic": (PI.i_tonic, PI.i_max, PI.c),
}
C_SWEEP = (0.03, 0.1, PI.c, 1.0)
TONIC_SWEEP = (0.0, PI.i_tonic, 0.25, 0.5)
PATHS = ("SC_PYR", "SC_PV")    # SC terminals (SC_PV = SC_BiS, pooled fit): where A1R and GABA_B inhibition of release is described
FREQS = np.logspace(0, np.log10(300), 19)


def snap(t):
    return np.round(np.asarray(t) / GRID) * GRID


def protocols():
    out = {f"{f} Hz, 1 s": snap(10.0 + np.arange(f) * 1000.0 / f) for f in (5, 20, 40, 80)}
    # theta burst: 10 bursts of 4 spikes at 100 Hz, bursts at 5 Hz
    out["theta burst"] = snap(np.concatenate([10.0 + 200.0 * b + 10.0 * np.arange(4) for b in range(10)]))
    return out


def run(sp, path, cond):
    p = PATHWAYS[path]
    i_tonic, i_max, c = cond
    stp = dict(U=p.U, tau_rec=p.tau_rec, tau_fac=p.tau_fac)
    inh = dict(i_tonic=i_tonic, i_max=i_max, c=c, **KIN)
    gaba = sp + PI.lag
    ref = an.tm_pi_terms(sp, gaba, **stp, **inh)
    got = pr.run_tm_pi(sp, gaba, **stp, cvode=False, **inh)
    err = float(np.max(np.abs(got["amp"] - ref["amp"]) / ref["amp"]))
    return ref, err


def steady_train(f, path):
    p = PATHWAYS[path]
    n = int(np.ceil(8 * max(p.tau_rec, p.tau_fac, PI.tau_d) * f / 1000.0)) + 20
    return snap(10.0 + np.arange(n) * 1000.0 / f)


def main():
    os.makedirs("results", exist_ok=True)
    os.makedirs("docs/figures", exist_ok=True)
    rows, max_err = [], 0.0
    prot = protocols()

    # 1. per-spike weight profiles and their up/down split, SC -> PYR
    profiles = {}
    for pname, sp in prot.items():
        for cname, cond in CONDITIONS.items():
            r, err = run(sp, "SC_PYR", cond)
            max_err = max(max_err, err)
            profiles[pname, cname] = (sp, r)
            up = float(np.sum(r["fac"]))
            down = {k: float(np.sum(r[k])) for k in ("dep", "phasic", "tonic")}
            rows.append(dict(part="profile", path="SC_PYR", protocol=pname, condition=cname, c=cond[2],
                             i_tonic=cond[0], n=len(sp), mean_w_rel=float(np.mean(r["amp"])) / PATHWAYS["SC_PYR"].U,
                             up_fac=up, down_dep=down["dep"], down_phasic=down["phasic"], down_tonic=down["tonic"],
                             err=err))

    print("SC->PYR, per train: mean w_eff/(w U) and summed log terms (up | down: depletion, phasic, tonic); "
          "up share = up / (up + |down|)")
    for r in rows:
        tot_down = r["down_dep"] + r["down_phasic"] + r["down_tonic"]
        print(f"  {r['protocol']:13s} {r['condition']:17s} w/wU {r['mean_w_rel']:5.2f}   up {r['up_fac']:6.2f} | "
              f"{r['down_dep']:6.2f} {r['down_phasic']:6.2f} {r['down_tonic']:6.2f}   "
              f"up share {r['up_fac'] / (r['up_fac'] - tot_down):4.2f}")

    # 2. steady-state balance B(f) = amp_ss / U (nominal U) and crossover f*, sweeps of c and i_tonic
    def b_curve(path, cond):
        nonlocal max_err
        B = []
        for f in FREQS:
            r, err = run(steady_train(f, path), path, cond)
            max_err = max(max_err, err)
            B.append(r["amp"][-1] / PATHWAYS[path].U)
        return np.array(B)

    def f_star(B):
        idx = np.where((B[:-1] >= 1.0) & (B[1:] < 1.0))[0]
        if len(idx) == 0:
            return None
        i = idx[-1]
        lf = np.log(FREQS)
        return float(np.exp(lf[i] + (1.0 - B[i]) / (B[i + 1] - B[i]) * (lf[i + 1] - lf[i])))

    curves = {}
    sweep = [("c", c, (0.0, PI.i_max, c)) for c in (0.0,) + C_SWEEP] + \
            [("i_tonic", it, (it, 0.0, 0.0)) for it in TONIC_SWEEP[1:]]
    print("\nSteady-state balance B(f) = R_ss / U (U = nominal, no inhibition); f* where B falls through 1")
    for path in PATHS:
        for kind, val, cond in sweep:
            B = b_curve(path, cond)
            curves[path, kind, val] = B
            fs = f_star(B)
            rows.append(dict(part="balance", path=path, condition=f"{kind}={val}", c=cond[2], i_tonic=cond[0],
                             f_star=fs, B_max=float(B.max()), f_Bmax=float(FREQS[np.argmax(B)]),
                             **{f"B_{int(round(f))}Hz": float(b) for f, b in zip(FREQS, B)}))
            print(f"  {path:7s} {kind:7s}={val:<6} max B {B.max():5.2f} at {FREQS[np.argmax(B)]:6.1f} Hz   "
                  f"f* {'none' if fs is None else f'{fs:6.1f}'}")
    print(f"\nNEURON vs closed form, max relative release difference over all trains: {max_err:.1e}")

    keys = sorted({k for r in rows for k in r}, key=lambda k: (k not in rows[0], k))
    with open("results/s3a_downscaling.csv", "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=keys)
        wr.writeheader()
        wr.writerows(rows)

    # figure 1: profiles
    names = list(prot)
    fig, ax = plt.subplots(2, len(names), figsize=(4.0 * len(names), 7.0), sharey="row")
    colors = dict(zip(CONDITIONS, ("k", "tab:blue", "tab:orange", "tab:red")))
    for j, pname in enumerate(names):
        for cname in CONDITIONS:
            sp, r = profiles[pname, cname]
            ax[0, j].plot(sp, r["amp"] / PATHWAYS["SC_PYR"].U, ".-", ms=3, lw=0.8, color=colors[cname], label=cname)
        ax[0, j].axhline(1.0, color="0.6", lw=0.6)
        ax[0, j].set_title(pname)
        sp, r = profiles[pname, "+ tonic + phasic"]
        x = np.arange(len(sp)) + 1
        ax[1, j].bar(x, r["fac"], color="tab:green", width=0.9, label="facilitation (up)")
        bottom = np.zeros(len(sp))
        for k, col, lab in (("dep", "tab:purple", "depletion #1"), ("phasic", "tab:orange", "phasic A1R #2"),
                            ("tonic", "tab:blue", "tonic A1R #2")):
            ax[1, j].bar(x, r[k], bottom=bottom, color=col, width=0.9, label=lab)
            bottom += r[k]
        net = r["fac"] + r["dep"] + r["phasic"] + r["tonic"]
        ax[1, j].plot(x, net, "k.-", ms=3, lw=0.8, label="net = log(w_eff / wU)")
        ax[1, j].axhline(0.0, color="0.6", lw=0.6)
        ax[1, j].set_xlabel("spike number")
    ax[0, 0].set_ylabel("w_eff / (w U)  (SC→PYR)")
    ax[1, 0].set_ylabel("log contribution, + tonic + phasic")
    ax[0, 0].legend(fontsize=7)
    ax[1, 0].legend(fontsize=7)
    fig.suptitle("SC→PYR: per-spike weight and its up/down split (A1R inhibition: Mitchell et al. 1993, fitted)")
    fig.tight_layout()
    fig.savefig("docs/figures/s3a_downscaling_profiles.png", dpi=130)

    # figure 2: balance curves
    fig, ax = plt.subplots(1, len(PATHS) * 2, figsize=(16, 4.2), sharey=True)
    for j, path in enumerate(PATHS):
        for kind, vals, a in (("c", (0.0,) + C_SWEEP, ax[2 * j]), ("i_tonic", TONIC_SWEEP, ax[2 * j + 1])):
            for k, v in enumerate(vals):
                B = curves.get((path, kind, v), curves[path, "c", 0.0])
                a.semilogx(FREQS, B, "o-", ms=3, color=plt.cm.viridis(k / max(1, len(vals) - 1)), label=f"{kind} {v}")
            a.axhline(1.0, color="0.6", lw=0.6)
            a.set_title(f"{path}: sweep {kind}")
            a.set_xlabel("rate (Hz)")
            a.legend(fontsize=7)
    ax[0].set_ylabel("B = R_ss / U")
    fig.tight_layout()
    fig.savefig("docs/figures/s3a_downscaling_balance.png", dpi=130)


if __name__ == "__main__":
    main()
