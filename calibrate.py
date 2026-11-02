"""S3b: measure the intrinsic properties of the Tier-B cells and compare them with params.CELL_TARGETS.

Feature definitions follow Bezaire et al. 2016 (Appendix 1, "Experimental cell characterization"):
  input resistance  from the least hyperpolarising current step (here a fixed small step, HYP_PA);
  membrane tau      single-exponential fit to the voltage from step onset to steady state;
  rheobase          least depolarising current that makes the cell spike *during* the step (no rebound spikes).
Differences from the experiments, stated: the hyperpolarising step is -10 pA for every cell (the experiments use
the least hyperpolarised level of a 50 pA grid, so Rin of O-LM, 592 MOhm, would be measured at -50 pA there),
and the rheobase is found by bisection (continuous), while the experimental rheobase is quantised by the 50 pA grid.
Measured cells are deleted afterwards: `measure` assumes no other cell is alive in the NEURON session.
`settle_ms` > 0: the cell is first run at zero current for that long (step SETTLE_DT), the state is saved, and every
recording starts from it (needed for slow channels: the O-LM HCN has tau >= 100 ms; Bezaire's own runs settle 500 ms).
settle_ms = 0 (default) keeps the earlier protocol: initialise at -65 mV, 50 ms before the step.
"""
import numpy as np
from scipy.optimize import curve_fit

from cells import h

HYP_PA = -10.0
DELAY, DUR = 50.0, 400.0
DT = 0.025


SETTLE_DT = 10.0       # ms; large step for settling, as Bezaire's presimulation (the steady state does not depend on dt)
_SETTLED = {}          # sec name -> (SaveState, settle time), set by `measure`


def _record(sec, amp_na, dur=None, delay=DELAY, tail=50.0, rec_dt=0.1):
    """(t, v) with t relative to the start of the recording (the end of settling, if any). dur None = DUR."""
    dur = DUR if dur is None else dur
    st = h.IClamp(sec(0.5))
    t, v = h.Vector(), h.Vector()
    t.record(h._ref_t, rec_dt)
    v.record(sec(0.5)._ref_v, rec_dt)
    h.cvode_active(0)
    h.dt = DT
    h.finitialize(-65.0)
    t0 = 0.0
    if sec.name() in _SETTLED:
        ss, t0 = _SETTLED[sec.name()]
        ss.restore()
        h.t = t0
        h.frecord_init()
    st.delay, st.dur, st.amp = t0 + delay, dur, amp_na
    h.continuerun(t0 + delay + dur + tail)
    out = np.array(t) - t0, np.array(v)
    st.amp = 0.0
    return out


def _settle(sec, settle_ms):
    st = h.IClamp(sec(0.5))               # same structure as in _record, so the saved state fits
    st.amp = 0.0
    h.cvode_active(0)
    h.dt = SETTLE_DT
    h.finitialize(-65.0)
    while h.t < settle_ms - 1e-9:        # fadvance: continuerun would also step at the plotting interval
        h.fadvance()
    h.dt = DT
    ss = h.SaveState()
    ss.save()
    _SETTLED[sec.name()] = (ss, settle_ms)


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


DVDT_THRESHOLD = 28.0   # mV/ms, Bezaire 2016 threshold method #2 (used there for all cells except pyramidal)
SPIKE_V = -10.0         # mV, a spike is a crossing of this level during the step
MAX_GRID_STEPS = 12


def _spike_features(t, v):
    """Threshold (mV), threshold times (ms), amplitude and AHP (mV) of each spike in the step window."""
    sel = (t >= DELAY) & (t <= DELAY + DUR)
    t, v = t[sel], v[sel]
    dvdt = np.gradient(v, t)
    up = np.where((v[1:] >= SPIKE_V) & (v[:-1] < SPIKE_V))[0]
    out = []
    for k, i in enumerate(up):
        j = i
        while j > 0 and dvdt[j - 1] >= DVDT_THRESHOLD:      # walk back to where dV/dt first exceeded the cutoff
            j -= 1
        nxt = up[k + 1] if k + 1 < len(up) else len(v) - 1
        peak = i + int(np.argmax(v[i:nxt + 1]))
        out.append(dict(t_thr=t[j], v_thr=v[j], amp=v[peak] - v[j], ahp=v[j] - v[peak:nxt + 1].min()))
    return out


def firing(sec, grid_pa, rheobase_pa, i_max_na=1.0):
    """Bezaire's firing features on the experimental current grid (first level, step) in pA: the least depolarised
    level >= the (continuous) rheobase at which the cell fires >= 2 spikes in the 400 ms step ("spiked regularly" is
    not defined in the source; >= 2 spikes is the minimum for an interval); ISI = mean interval between threshold
    times, threshold / amplitude / AHP = mean over the first three spikes. Also the grid rheobase and the sag at the most
    hyperpolarised grid level (steady state minus minimum)."""
    first, step = grid_pa
    out = dict(isi=None, isi_level_pa=None, grid_rheobase=None, threshold=None, spike_amp=None, ahp=None)
    t, v = _record(sec, first * 1e-3)
    sel = (t >= DELAY) & (t <= DELAY + DUR)
    out["sag"] = float(v[(t > DELAY + DUR - 50) & (t < DELAY + DUR)].mean() - v[sel].min())
    if rheobase_pa is None:
        return out
    k0 = int(np.ceil((rheobase_pa - first) / step - 1e-9))
    for k in range(k0, k0 + MAX_GRID_STEPS):
        level = first + k * step
        if level * 1e-3 > i_max_na:
            break
        t, v = _record(sec, level * 1e-3, rec_dt=DT)
        sp = _spike_features(t, v)
        if sp and out["grid_rheobase"] is None:
            out["grid_rheobase"] = level
        if len(sp) >= 2:
            f3 = sp[:3]
            out.update(isi=float(np.mean(np.diff([s["t_thr"] for s in sp]))), isi_level_pa=level,
                       threshold=float(np.mean([s["v_thr"] for s in f3])), spike_amp=float(np.mean([s["amp"] for s in f3])),
                       ahp=float(np.mean([s["ahp"] for s in f3[:-1]] if len(f3) > 1 else [f3[0]["ahp"]])))
            break
    return out


def measure(build, rheobase_tol_na=5e-4, i_max_na=1.0, settle_ms=0.0, grid_pa=None):
    """Build a cell with `build()` (returns dict with 'soma'), measure it, delete it. With grid_pa (first level, step;
    params.CellTarget.grid_pa) also the firing features of `firing`."""
    cell = build()
    soma = cell["soma"]
    if settle_ms > 0:
        _settle(soma, settle_ms)
    try:
        v0, rin, tau = input_resistance_and_tau(soma)
        rheo = rheobase(soma, i_max_na=i_max_na, tol_na=rheobase_tol_na)
        out = {"v_rest": v0, "r_in": rin, "tau_m": tau, "rheobase": rheo}
        if grid_pa is not None:
            out.update(firing(soma, grid_pa, rheo, i_max_na))
    finally:
        _SETTLED.clear()
    cell.clear()
    soma = None
    for sec in list(h.allsec()):
        h.delete_section(sec=sec)
    return out


REL_FLOOR = 0.10        # tolerance floor: 10% of the target mean
RMP_FLOOR_MV = 2.0      # resting potential: linear difference in mV, tolerance max(SD, 2 mV)
NO_SPIKE_PENALTY = 10.0  # residual when no current up to i_max (default 1 nA) makes the cell spike
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
      negative and a log ratio is meaningless; the 2 mV floor stops the 1.2 mV SDs from over-constraining;
    * ISI (when measured with `firing` and the target has one): log ratio as above; penalty if the cell never fires
      two spikes on the grid. Order: [Rin, tau, rheobase, RMP, ISI].
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
    if "isi" in measured and getattr(target, "isi_ms", None) is not None:
        mean, sd = target.isi_ms
        x = measured["isi"]
        out.append(NO_SPIKE_PENALTY if x is None or x <= 0 else np.log(x / mean) / max(sd / mean, REL_FLOOR))
    return np.array(out)
