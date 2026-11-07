"""S3a: B(f) = R_ss / U at exact rates, and the A1R windows with and without tonic inhibition.

run_s3a.py runs NEURON on a 25-point rate grid, so its "5 / 20 / 80 / 200 Hz" columns are the nearest grid
rates (5.28, 21.97, 72.08, 186.51 Hz). This script evaluates the closed form at the rates themselves. The
closed form matches NEURON to 3e-11 on that grid (RESULTS §5). Deterministic: no seeds, no NEURON, no time
compression.
"""
import numpy as np
from scipy.optimize import brentq

import analysis as an
from params import PATHWAYS, PRESYN_INHIB

ROWS = (("SC → PYR", "SC_PYR"), ("SC → PV, BiS", "SC_PV"), ("PYR → O-LM", "PYR_OLM"), ("PYR → PV, BiS", "PYR_PV"),
        ("PV → PYR", "PV_PYR"), ("BiS → PYR", "BiS_PYR"), ("O-LM → PYR", "OLM_PYR"))
DENSE = np.geomspace(1.0, 300.0, 6000)
A1R_RATES = np.geomspace(1.0, 40.0, 400)


def r_ss(p, f, gain=1.0):
    """Steady-state release u+ x- of a periodic train at rate f (Hz), closed form."""
    U, d = gain * p.U, 1000.0 / f
    e_fac, e_rec = np.exp(-d / p.tau_fac), np.exp(-d / p.tau_rec)
    u_plus = U / (1.0 - (1.0 - U) * e_fac)
    return u_plus * (1.0 - e_rec) / (1.0 - (1.0 - u_plus) * e_rec)


def balance(p, f, gain=1.0):
    return r_ss(p, f, gain) / (gain * p.U)


def crossover(p, gain=1.0):
    """Rate at which B falls through 1, or None for a down-only pathway."""
    b = balance(p, DENSE, gain) - 1.0
    idx = np.where((b[:-1] > 0) & (b[1:] <= 0))[0]
    return brentq(lambda f: balance(p, f, gain) - 1.0, DENSE[idx[-1]], DENSE[idx[-1] + 1]) if len(idx) else None


def a1r_balance(p, f, i_tonic):
    """B at rate f with A1R inhibition: one volley per spike after the lag, on a train long enough to settle."""
    a = PRESYN_INHIB["SC_A1R"]
    d = 1000.0 / f
    spikes = np.arange(int(max(6000.0 / d, 50))) * d
    terms = an.tm_pi_terms(spikes, spikes + a.lag, p.U, p.tau_rec, p.tau_fac, i_tonic, a.i_max, a.c, a.tau_r, a.tau_d)
    return terms["amp"][-1] / p.U


print("B(f) at exact rates; last column checks 20 Hz against a recursive train (analysis.tm_amplitudes)")
print(f"{'pathway':15s}{'5 Hz':>7s}{'20 Hz':>7s}{'80 Hz':>7s}{'max B':>7s}{'at Hz':>7s}{'f* Hz':>7s}{'|train-closed|':>16s}")
for label, key in ROWS:
    p = PATHWAYS[key]
    b = balance(p, DENSE)
    i = b.argmax()
    f_star = crossover(p)
    train = an.tm_amplitudes(np.arange(4000) * 50.0, p.U, p.tau_rec, p.tau_fac)[-1] / p.U
    star = f"{f_star:.1f}" if f_star else "none"
    print(f"{label:15s}{balance(p, 5.0):7.2f}{balance(p, 20.0):7.2f}{balance(p, 80.0):7.2f}"
          f"{b[i]:7.2f}{DENSE[i]:7.1f}{star:>7s}{abs(train - balance(p, 20.0)):16.1e}")

sc = PATHWAYS["SC_PYR"]
print("\nSC → PYR U gain 0.5 / 1 / 1.5")
print("  f*:", [round(crossover(sc, g), 1) for g in (0.5, 1.0, 1.5)])
print("  R_ss at 200 Hz:", [round(float(r_ss(sc, 200.0, g)), 4) for g in (0.5, 1.0, 1.5)])

print("\nA1R inhibition (PRESYN_INHIB['SC_A1R'], c per spike: assumes the SC fibres fire together)")
for name, i_tonic in (("phasic only", 0.0), ("phasic + tonic", PRESYN_INHIB["SC_A1R"].i_tonic)):
    for label, key in (("SC → PYR", "SC_PYR"), ("SC → PV, BiS", "SC_PV")):
        b = np.array([a1r_balance(PATHWAYS[key], f, i_tonic) for f in A1R_RATES])
        i = b.argmax()
        cross = [round(float(A1R_RATES[j + 1]), 1) for j in range(len(b) - 1) if b[j] > 1.0 >= b[j + 1]]
        print(f"  {name:15s}{label:14s} max B {b[i]:.2f} at {A1R_RATES[i]:.1f} Hz; down-crossing {cross or 'none'}")
