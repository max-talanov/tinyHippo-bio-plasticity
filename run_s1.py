"""S1: verify TMSyn against the closed-form TM solution; print the worst-case errors."""
import numpy as np

import analysis as an
import protocols as pr
from tests.test_s1_tmsyn import PARAMS, T1, T2, W, irregular, periodic

rows = []
for name, p in PARAMS.items():
    trains = {f"{f} Hz x{n}": periodic(f, n) for f in (5, 20, 50) for n in (2, 20)}
    trains["irregular x30"] = irregular()
    for label, sp in trains.items():
        res = {}
        for mode, cv in (("cvode", True), ("fixed", False)):
            amps, t, g = pr.run_tm(sp, **p, w=W, tau1=T1, tau2=T2, cvode=cv)
            ref = an.tm_amplitudes(sp, **p)
            g_ref = an.tm_conductance(t, sp, ref, W, T1, T2)
            res[mode] = (np.max(np.abs(amps - ref) / ref),
                         np.max(np.abs(g - g_ref)) / np.max(g_ref), g, t)
        n = min(len(res["cvode"][2]), len(res["fixed"][2]))
        cf = np.max(np.abs(res["cvode"][2][:n] - res["fixed"][2][:n])) / np.max(res["fixed"][2][:n])
        rows.append((name, label, res["cvode"][0], res["fixed"][0],
                     res["cvode"][1], res["fixed"][1], cf))

print(f"{'params':13s}{'train':15s}{'amp cvode':>11s}{'amp fixed':>11s}{'g cvode':>10s}{'g fixed':>10s}{'cvode-fixed':>12s}")
for r in rows:
    print(f"{r[0]:13s}{r[1]:15s}{r[2]:11.1e}{r[3]:11.1e}{r[4]:10.1e}{r[5]:10.1e}{r[6]:12.1e}")
print("\nworst case over all rows:")
for k, lab in zip(range(2, 7), ("amp cvode", "amp fixed", "g cvode", "g fixed", "cvode vs fixed")):
    print(f"  {lab:15s}{max(r[k] for r in rows):.2e}")
