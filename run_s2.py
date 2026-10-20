"""S2 machinery run: PPR signatures from a voltage-clamped TMSyn, and fit accuracy on synthetic data.

No literature parameter set is used here (params.py has no verified numbers yet); the three
fixtures are the S1 test sets. Prints the PPR-vs-ISI table and the empirical coverage of the fit CIs.
"""
import numpy as np

import analysis as an
import protocols as pr
from tests.test_s1_tmsyn import PARAMS
from tests.test_s2_fit import ISIS, protocol_trials

W = 1e-3

print("PPR (EPSC2/EPSC1, NEURON voltage clamp, peak minus baseline) vs inter-spike interval")
print(f"{'set':13s}" + "".join(f"{int(i):>8d}ms" for i in ISIS) + "   class")
for name, p in PARAMS.items():
    ppr = []
    for isi in ISIS:
        sp = np.array([10.0, 10.0 + isi])
        t, i = pr.run_clamped(sp, **p, w=W)
        a = pr.epsc_amplitudes(t, i, sp)
        ppr.append(a[1] / a[0])
    ppr = np.array(ppr)
    cls = "facilitating" if np.all(ppr[:3] > 1) else "depressing" if np.all(ppr[:3] < 1) else "mixed"
    print(f"{name:13s}" + "".join(f"{x:10.3f}" for x in ppr) + f"   {cls}")

print("\nCoverage of the 95% CI of fit_tm on synthetic data (analytic amplitudes, 10% noise, 100 replicates)")
rng = np.random.default_rng(0)
trials = protocol_trials()
for name in ("facilitating", "mixed"):
    p = PARAMS[name]
    truth = np.array([1.0, p["U"], p["tau_rec"], p["tau_fac"]])
    clean = [an.tm_amplitudes(sp, **p) for sp in trials]
    hits = np.zeros(4)
    widths = []
    est = []
    for _ in range(100):
        obs = [c * (1 + 0.10 * rng.standard_normal(len(c))) for c in clean]
        f = an.fit_tm(trials, obs, starts=[(1.0, 0.3, 300.0, 300.0), (1.0, 0.1, 150.0, 700.0)])
        hits += np.abs(f["theta"] - truth) <= f["ci95"]
        widths.append(f["ci95"] / truth)
        est.append(f["theta"])
    est = np.array(est)
    print(f"{name:13s} coverage  A {hits[0]:.0f}%  U {hits[1]:.0f}%  tau_rec {hits[2]:.0f}%  tau_fac {hits[3]:.0f}%"
          f"   median half-width (rel. to truth) U {np.median(np.array(widths)[:, 1]):.2f}"
          f"  tau_rec {np.median(np.array(widths)[:, 2]):.2f}  tau_fac {np.median(np.array(widths)[:, 3]):.2f}")
