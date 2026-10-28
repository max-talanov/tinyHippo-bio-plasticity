"""S3b: measure the intrinsic properties of the Tier-B cells and compare them with params.CELL_TARGETS.

Feature definitions follow Bezaire et al. 2016 (Appendix 1, "Experimental cell characterization"):
  input resistance  from the least hyperpolarising current step (here a fixed small step, HYP_PA);
  membrane tau      single-exponential fit to the voltage from step onset to steady state;
  rheobase          least depolarising current that makes the cell spike *during* the step (no rebound spikes).
Differences from the experiments, stated: the hyperpolarising step is -10 pA for every cell (the experiments use
the least hyperpolarised level of a 50 pA grid, so Rin of O-LM, 592 MOhm, would be measured at -50 pA there),
and the rheobase is found by bisection (continuous), while the experimental rheobase is quantised by the 50 pA grid.
Measured cells are deleted afterwards: `measure` assumes no other cell is alive in the NEURON session.
"""
import numpy as np
from scipy.optimize import curve_fit

from cells import h

HYP_PA = -10.0
DELAY, DUR = 50.0, 400.0
DT = 0.025


def _record(sec, amp_na, dur=DUR, delay=DELAY, tail=50.0):
    st = h.IClamp(sec(0.5))
    st.delay, st.dur, st.amp = delay, dur, amp_na
    t, v = h.Vector(), h.Vector()
    t.record(h._ref_t, 0.1)
    v.record(sec(0.5)._ref_v, 0.1)
    h.cvode_active(0)
    h.dt = DT
    h.finitialize(-65.0)
    h.continuerun(delay + dur + tail)
    out = np.array(t), np.array(v)
    st.amp = 0.0
    return out


def input_resistance_and_tau(sec):
    """(v_rest mV, Rin MOhm, tau ms) from a small hyperpolarising step."""
    amp = HYP_PA * 1e-3
    t, v = _record(sec, amp)
    v0 = v[(t > DELAY - 20) & (t < DELAY)].mean()
    vss = v[(t > DELAY + DUR - 50) & (t < DELAY + DUR)].mean()
    sel = (t >= DELAY) & (t <= DELAY + DUR)
    ts, vs = t[sel] - DELAY, v[sel]
    f = lambda x, tau: vss + (v0 - vss) * np.exp(-x / tau)
    tau = curve_fit(f, ts, vs, p0=(10.0,), bounds=(0.05, 500.0))[0][0]
    return v0, (vss - v0) / amp, tau


def rheobase(sec, i_max_na=1.0, tol_na=5e-4):
    """Least DC current (pA) for >= 1 spike (v > 0 mV) during the 400 ms step; None if i_max does not make it spike."""
    def spikes(i):
        t, v = _record(sec, i)
        return bool(np.any(v[(t >= DELAY) & (t <= DELAY + DUR)] > 0.0))
    lo, hi = 0.0, i_max_na
    if not spikes(hi):
        return None
    while hi - lo > tol_na:
        mid = 0.5 * (lo + hi)
        lo, hi = (lo, mid) if spikes(mid) else (mid, hi)
    return hi * 1e3


def measure(build, rheobase_tol_na=5e-4):
    """Build a cell with `build()` (returns dict with 'soma'), measure it, delete it."""
    cell = build()
    soma = cell["soma"]
    v0, rin, tau = input_resistance_and_tau(soma)
    rheo = rheobase(soma, tol_na=rheobase_tol_na)
    for sec in list(h.allsec()):
        h.delete_section(sec=sec)
    return {"v_rest": v0, "r_in": rin, "tau_m": tau, "rheobase": rheo}


REL_FLOOR = 0.10        # tolerance floor: 10% of the target mean
RMP_FLOOR_MV = 2.0      # resting potential: linear difference in mV, tolerance max(SD, 2 mV)
NO_SPIKE_PENALTY = 10.0  # residual when no current up to 1 nA makes the cell spike
FEATURES = (("r_in", "r_in_mohm"), ("tau_m", "tau_m_ms"), ("rheobase", "rheobase_pa"))


def residuals(measured, target):
    """Residual vector of one cell: log ratio of each measured feature to its target mean, in units of a tolerance.

    residual_k = ln(measured_k / mean_k) / max(sd_k / mean_k, REL_FLOOR)

    * log ratio: the cells start 15-90x off in tau_m; a linear z-score would make those features swamp the others and
      give a badly conditioned fit, and a 10x too high and 10x too low error should cost the same;
    * tolerance = max(experimental relative SD, 10%): about one experimental SD where it is known, but never below 10%
      (O-LM rheobase 20 +- 0 pA from 3 cells on a 50 pA grid has SD 0, and the bistratified tau_m SD of 5% would demand
      more precision than the measurement has). A residual of 1 is then roughly "one SD off", and Bezaire/Migliore
      accept a cell within 2 SD;
    * rheobase None (no spike up to 1 nA): fixed penalty, so the optimiser is pushed back to cells that spike;
    * resting potential (when the target has one): (measured - mean) / max(SD, 2 mV), linear because the value is
      negative and a log ratio is meaningless; the 2 mV floor stops the 1.2 mV SDs from over-constraining.
    """
    out = []
    for key, tkey in FEATURES:
        mean, sd = getattr(target, tkey)
        x = measured.get(key)
        if x is None or not np.isfinite(x) or x <= 0:
            out.append(NO_SPIKE_PENALTY)
            continue
        out.append(np.log(x / mean) / max(sd / mean, REL_FLOOR))
    if getattr(target, "rmp_mv", None) is not None:
        mean, sd = target.rmp_mv
        x = measured.get("v_rest")
        out.append(NO_SPIKE_PENALTY if x is None or not np.isfinite(x) else (x - mean) / max(sd, RMP_FLOOR_MV))
    return np.array(out)
