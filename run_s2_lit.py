"""S2 on the literature parameter set (params.py): PPR sign test per pathway and fit identifiability.

PPR comes from the NEURON voltage clamp (EPSC2/EPSC1) and is compared with the closed-form TM value.
The fit step cannot use real recordings (none supplied), so it is a round trip: noisy amplitudes generated
from each pathway's parameters under the S2 protocol are fitted back, which shows how tightly 50 amplitudes
at 10% noise constrain U, tau_rec, tau_fac. It does not validate the literature values.
"""
import numpy as np

import analysis as an
import protocols as pr
from params import PATHWAYS
from tests.test_s2_fit import ISIS, protocol_trials

W = 1e-3
N_REP = 100
SEED = 0

print("PPR per pathway, NEURON clamp (closed form in brackets), literature parameters")
print(f"{'pathway':9s}{'expected':>13s}" + "".join(f"{int(i):>15d}ms" for i in ISIS) + "   sign test")
max_dev = 0.0
for name, p in PATHWAYS.items():
    kw = dict(U=p.U, tau_rec=p.tau_rec, tau_fac=p.tau_fac)
    ppr, ppr_cf = [], []
    for isi in ISIS:
        sp = np.array([10.0, 10.0 + isi])
        t, i = pr.run_clamped(sp, **kw, w=W)
        a = pr.epsc_amplitudes(t, i, sp)
        ppr.append(a[1] / a[0])
        c = an.tm_amplitudes(sp, **kw)
        ppr_cf.append(c[1] / c[0])
    ppr, ppr_cf = np.array(ppr), np.array(ppr_cf)
    max_dev = max(max_dev, np.max(np.abs(ppr / ppr_cf - 1)))
    obs = "facilitating" if np.all(ppr[:3] > 1) else "depressing" if np.all(ppr[:3] < 1) else "mixed"
    ok = "PASS" if obs == p.expected_class else f"FAIL (observed {obs})"
    print(f"{name:9s}{p.expected_class:>13s}" + "".join(f"{a:8.3f} ({b:5.3f})" for a, b in zip(ppr, ppr_cf)) + f"   {ok}")
print(f"max |NEURON/closed-form - 1| over all PPR values: {max_dev:.2e}")

print(f"\nRound-trip fit, 10% amplitude noise, {N_REP} replicates, seed {SEED}")
print(f"{'pathway':9s}{'param':>9s}{'truth':>9s}{'median est':>12s}{'median CI half-width/truth':>28s}{'coverage':>10s}")
rng = np.random.default_rng(SEED)
trials = protocol_trials()
for name, p in PATHWAYS.items():
    kw = dict(U=p.U, tau_rec=p.tau_rec, tau_fac=p.tau_fac)
    truth = np.array([1.0, p.U, p.tau_rec, p.tau_fac])
    clean = [an.tm_amplitudes(sp, **kw) for sp in trials]
    est, wid, hit, bad = [], [], np.zeros(4), 0
    for _ in range(N_REP):
        obs = [c * (1 + 0.10 * rng.standard_normal(len(c))) for c in clean]
        try:
            f = an.fit_tm(trials, obs, starts=[(1.0, 0.3, 300.0, 300.0), (1.0, 0.1, 150.0, 700.0)])
        except Exception:
            bad += 1
            continue
        est.append(f["theta"]); wid.append(f["ci95"] / truth); hit += np.abs(f["theta"] - truth) <= f["ci95"]
    est, wid = np.array(est), np.array(wid)
    n = len(est)
    for k, lab in enumerate(("A", "U", "tau_rec", "tau_fac")):
        print(f"{name if k == 0 else '':9s}{lab:>9s}{truth[k]:9.3g}{np.median(est[:, k]):12.3g}"
              f"{np.median(wid[:, k]):28.2f}{100 * hit[k] / n:9.0f}%")
    if bad:
        print(f"{'':9s}  {bad} of {N_REP} fits failed")
