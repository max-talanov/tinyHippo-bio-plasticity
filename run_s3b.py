"""S3b: intrinsic properties of the Tier-B cells against params.CELL_TARGETS, and their calibration.

Usage:
  python run_s3b.py                 baseline: measure the current placeholder cells
  python run_s3b.py fit PYR|PV|BiS|OLM [bez|bez-noh|hh|point]   least-squares fit; writes results/s3b_<cell>.json (PYR,
      point), results/s3b_<cell>_dend.json (hh) or results/s3b_<cell>_bez[_noh].json (bez, the interneuron default)
Targets: Rin, tau_m, rheobase and resting potential (params.CELL_TARGETS). Parameters fitted:
  PYR: dendritic leak g_pas, dendrite diameter scale, soma Na/K scale, soma leak gl, e_pas and soma el;
  dendritic interneurons (default; morphology cells.IN_MORPH from Bezaire 2016): the same, but separate soma Na and K
    scales (7 parameters), rheobase searched up to 3 nA;
  point interneurons ("point"): lumped soma size (um, L = diam), leak gl, Na/K scale (gnabar, gkbar x s), el;
  Bezaire interneurons ("bez", cells.build_bezaire_interneuron, 34 C, all channels of the published model): scales on
    the published leak, Na and fast K densities, dendrite diameter scale (0.5-2), leak reversal; O-LM also the HCN
    scale, with eh from params.CHANNEL_PARAMS. "bez-noh": O-LM with HCN removed. Start: the published cell (all
    scales 1). Cells are settled for SETTLE_MS before measuring (O-LM HCN tau about 2.8 s at rest).
  "fit PYR bez": the Bezaire pyramidal cell (cells.build_bezaire_pyr), scales on leak, Na, Kdr, HCN, A-type K and
    e_pas, with the ISI target as well; writes results/s3b_PYR_bez.json.
Positive parameters on a log scale. Spike-based features use fixed step dt = 0.025 ms.
"""
import dataclasses
import json
import sys

import numpy as np
from scipy.optimize import least_squares

import calibrate as cal
from cells import BezINParams, PYRParams, IN_KINDS, build_bezaire_interneuron, build_interneuron, build_pyr, h
from params import CELL_TARGETS, CHANNEL_PARAMS

KIND = {"PV": "pv", "BiS": "bis", "OLM": "olm"}
BASE_NAK = (0.12, 0.036)


def builder(cell, x, point=False):
    """x = log parameters. Returns a zero-argument builder."""
    if cell != "PYR" and not point:
        g_pas, dscale, s_na, s_k, gl, e_pas, el = _lin(x)
        p = dataclasses.replace(IN_KINDS[KIND[cell]], morph="bezaire", g_pas=g_pas, dend_diam_scale=dscale,
                                gnabar=BASE_NAK[0] * s_na, gkbar=BASE_NAK[1] * s_k, gl=gl, e_pas=e_pas, el=el)
        return lambda: build_interneuron(KIND[cell], p)
    if cell == "PYR":
        g_pas, dscale, s, gl, e_pas, el = _lin(x)
        p = dataclasses.replace(PYRParams(), g_pas=g_pas, basal_diam=2.0 * dscale, prox_diam=2.0 * dscale,
                                dist_diam=1.5 * dscale, gnabar=BASE_NAK[0] * s, gkbar=BASE_NAK[1] * s, gl=gl,
                                e_pas=e_pas, el=el)
        return lambda: build_pyr(p)
    size, gl, s, el = _lin(x)
    p = dataclasses.replace(IN_KINDS[KIND[cell]], size=size, gl=gl, gnabar=BASE_NAK[0] * s, gkbar=BASE_NAK[1] * s, el=el)
    return lambda: build_interneuron(KIND[cell], p)


def _lin(x):
    """Parameter vector -> physical values: log parameters exponentiated, the last entries (reversals, mV) as is."""
    v = np.array(x, dtype=float)
    n_log = len(v) - (2 if len(v) >= 6 else 1)
    v[:n_log] = np.exp(v[:n_log])
    return v


def x0(cell, point=False):
    """Start vector: log of the positive parameters, then reversal potentials (mV)."""
    if cell != "PYR" and not point:
        return x0_dend(cell)
    if cell == "PYR":
        p = PYRParams()
        return np.concatenate([np.log([p.g_pas, 1.0, 1.0, p.gl]), [p.e_pas, p.el]])
    p = IN_KINDS[KIND[cell]]
    return np.concatenate([np.log([p.size, p.gl, 1.0]), [p.el]])


def x0_from_target(cell):
    """Interneuron start derived from the targets: C = tau/Rin sets the lumped area (cm = 1 uF/cm2), then gl = 1/(Rin*A)."""
    t = CELL_TARGETS[cell]
    c_pf = t.tau_m_ms[0] / t.r_in_mohm[0] * 1e3            # ms / MOhm = nF -> pF
    area_cm2 = c_pf * 1e-6 / 1.0                            # pF / (uF/cm2) -> cm2 (1 pF = 1e-6 uF)
    size = float(np.sqrt(area_cm2 * 1e8 / np.pi))           # cm2 -> um2, L = diam, area = pi d^2
    gl = 1.0 / (t.r_in_mohm[0] * 1e6 * area_cm2)
    return np.concatenate([np.log([size, gl, 0.1]), [-55.0]])


def x0_dend(cell, nak=1.0):
    """Dendritic interneuron start: g_pas from the target Rin and the membrane area of the Bezaire morphology,
    g_pas = 1 / (Rin * A); resting reversals at the target RMP."""
    t = CELL_TARGETS[cell]
    c = builder(cell, np.concatenate([np.log([1e-4, 1.0, 1.0, 1.0, 1e-4]), [-65.0, -65.0]]))()
    area_cm2 = sum(seg.area() for sec in [c["soma"], *c["dend"].values()] for seg in sec) * 1e-8
    for sec in list(h.allsec()):
        h.delete_section(sec=sec)
    g_pas = 1.0 / (t.r_in_mohm[0] * 1e6 * area_cm2)
    return np.concatenate([np.log([g_pas, 1.0, nak, nak, g_pas]), [t.rmp_mv[0], t.rmp_mv[0]]])


def describe(cell, x, point=False):
    v = _lin(x)
    if cell != "PYR" and point:
        return dict(size_um=v[0], gl=v[1], nak_scale=v[2], el=v[3])
    if cell == "PYR":
        return dict(g_pas=v[0], dend_diam_scale=v[1], nak_scale=v[2], soma_gl=v[3], e_pas=v[4], el=v[5])
    return dict(g_pas=v[0], dend_diam_scale=v[1], na_scale=v[2], k_scale=v[3], soma_gl=v[4], e_pas=v[5], el=v[6])


def fit(cell, point=False):
    target = CELL_TARGETS[cell]
    log = []
    six = cell == "PYR" or not point
    i_max = 3.0 if cell != "PYR" and not point else 1.0           # dendritic cells: search rheobase up to 3 nA

    def res(x):
        try:
            m = cal.measure(builder(cell, x, point), rheobase_tol_na=1e-3, i_max_na=i_max)
        except Exception as e:                                   # a failed exponential fit or integration
            m = {"r_in": None, "tau_m": None, "rheobase": None}
        r = cal.residuals(m, target)
        log.append((describe(cell, x, point), m, float(np.sum(r ** 2))))
        return r

    if cell == "PYR":
        lo = np.concatenate([np.log([1e-7, 0.05, 0.02, 1e-6]), [-90.0, -90.0]])
        hi = np.concatenate([np.log([1e-2, 40.0, 50.0, 1e-3]), [-40.0, -40.0]])
        starts = [x0(cell)]
    elif six:
        # diameter scale bounded to 0.5-2: the morphology is kept close to the Bezaire one
        lo = np.concatenate([np.log([1e-7, 0.5, 0.02, 0.02, 1e-6]), [-90.0, -90.0]])
        hi = np.concatenate([np.log([1e-2, 2.0, 50.0, 50.0, 1e-2]), [-40.0, -40.0]])
        starts = [x0_dend(cell, 1.0), x0_dend(cell, 0.1)]
    else:
        lo = np.concatenate([np.log([5.0, 1e-6, 0.02]), [-90.0]])
        hi = np.concatenate([np.log([300.0, 1e-3, 50.0]), [-40.0]])
        starts = [x0(cell, True), x0_from_target(cell)]
    sols = [least_squares(res, s, bounds=(lo, hi), diff_step=0.05, max_nfev=80, x_scale=1.0) for s in starts]
    sol = min(sols, key=lambda s: np.sum(s.fun ** 2))
    final = cal.measure(builder(cell, sol.x, point), i_max_na=i_max)
    out = dict(cell=cell, morph="point" if point and cell != "PYR" else ("pyr" if cell == "PYR" else "bezaire"),
               params=describe(cell, sol.x, point), measured=final,
               starts=[describe(cell, s, point) for s in starts],
               residuals=cal.residuals(final, target).tolist(), sum_sq=float(np.sum(sol.fun ** 2)),
               n_evals=len(log), status=int(sol.status), start_sum_sq=[float(np.sum(s.fun ** 2)) for s in sols],
               target={k: getattr(target, t) for k, t in cal.FEATURES})
    suffix = "_dend" if cell != "PYR" and not point else ""
    with open(f"results/s3b_{cell}{suffix}.json", "w") as fh:
        json.dump(out, fh, indent=1)
    return out


SETTLE_MS = 20000.0


def bez_builder(cell, x, with_h=True):
    """x = [log leak, log diameter, log Na, log K, (log HCN, O-LM with_h only), leak reversal mV]."""
    v = np.array(x, dtype=float)
    v[:-1] = np.exp(v[:-1])
    kw = dict(leak_scale=v[0], dend_diam_scale=v[1], na_scale=v[2], k_scale=v[3], e_leak=v[-1])
    if cell == "OLM":
        kw.update(h_scale=v[4] if with_h else 0.0, eh=CHANNEL_PARAMS["OLM_eh"].value)
    p = BezINParams(**kw)
    return lambda: build_bezaire_interneuron(KIND[cell], p)


def bez_describe(cell, x, with_h=True):
    v = np.array(x, dtype=float)
    v[:-1] = np.exp(v[:-1])
    d = dict(leak_scale=v[0], dend_diam_scale=v[1], na_scale=v[2], k_scale=v[3], e_leak=v[-1])
    if cell == "OLM":
        d.update(h_scale=v[4] if with_h else 0.0, eh=CHANNEL_PARAMS["OLM_eh"].value)
    return d


def fit_bez(cell, with_h=True):
    from cells import BEZ_CHANNELS
    target = CELL_TARGETS[cell]
    n_log = 5 if cell == "OLM" and with_h else 4
    x_start = np.concatenate([np.zeros(n_log), [BEZ_CHANNELS[KIND[cell]]["e_leak"]]])
    lo = np.concatenate([np.log([0.05, 0.5, 0.1, 0.1, 0.05][:n_log]), [-90.0]])
    hi = np.concatenate([np.log([20.0, 2.0, 10.0, 10.0, 20.0][:n_log]), [-40.0]])
    log = []
    meas = lambda x: cal.measure(bez_builder(cell, x, with_h), rheobase_tol_na=1e-3, i_max_na=3.0, settle_ms=SETTLE_MS)

    def res(x):
        try:
            m = meas(x)
        except Exception:
            m = {"r_in": None, "tau_m": None, "rheobase": None}
        r = cal.residuals(m, target)
        log.append((bez_describe(cell, x, with_h), m, float(np.sum(r ** 2))))
        return r

    published = meas(x_start)
    sol = least_squares(res, x_start, bounds=(lo, hi), diff_step=0.05, max_nfev=80, x_scale=1.0)
    final = meas(sol.x)
    out = dict(cell=cell, morph="bezaire", channels="bezaire" + ("" if with_h else "-noh"), celsius=34.0,
               settle_ms=SETTLE_MS, params=bez_describe(cell, sol.x, with_h), measured=final,
               published=dict(params=bez_describe(cell, x_start, with_h), measured=published,
                              residuals=cal.residuals(published, target).tolist()),
               residuals=cal.residuals(final, target).tolist(), sum_sq=float(np.sum(sol.fun ** 2)),
               n_evals=len(log), status=int(sol.status),
               target={k: getattr(target, t) for k, t in cal.FEATURES})
    with open(f"results/s3b_{cell}_bez{'' if with_h else '_noh'}.json", "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    return out


def fit_bez_pyr(h_bounds=(0.1, 10.0), out_path="results/s3b_PYR_bez.json"):
    """Bezaire 2016 pyramidal cell (cells.build_bezaire_pyr): scales on the published leak, Na, Kdr, HCN and A-type K
    densities (each 0.1-10 except HCN in h_bounds, gradients kept) and e_pas; targets Rin, tau_m, rheobase, RMP and
    ISI (Bezaire grid)."""
    from cells import BezPYRParams, build_bezaire_pyr
    target = CELL_TARGETS["PYR"]
    names = ("leak_scale", "na_scale", "k_scale", "h_scale", "ka_scale")
    x_start = np.concatenate([np.zeros(len(names)), [-66.0]])
    lo = np.concatenate([np.log(np.full(len(names), 0.1)), [-90.0]])
    hi = np.concatenate([np.log(np.full(len(names), 10.0)), [-50.0]])
    ih = names.index("h_scale")
    lo[ih], hi[ih] = np.log(h_bounds[0]), np.log(h_bounds[1])
    describe_x = lambda x: dict(zip(names, np.exp(x[:-1]).tolist()), e_pas=float(x[-1]))
    meas = lambda x: cal.measure(lambda: build_bezaire_pyr(BezPYRParams(**describe_x(x))), rheobase_tol_na=1e-3,
                                 i_max_na=3.0, settle_ms=SETTLE_MS, grid_pa=target.grid_pa)
    log = []

    def res(x):
        try:
            m = meas(x)
        except Exception:
            m = {"r_in": None, "tau_m": None, "rheobase": None, "isi": None}
        r = cal.residuals(m, target)
        log.append((describe_x(x), m, float(np.sum(r ** 2))))
        print(len(log), describe_x(x), np.round(r, 2), flush=True)
        return r

    published = meas(x_start)
    sol = least_squares(res, x_start, bounds=(lo, hi), diff_step=0.05, max_nfev=60, x_scale=1.0)
    final = meas(sol.x)
    out = dict(cell="PYR", morph="bezaire poolosyncell", channels="bezaire", celsius=34.0, settle_ms=SETTLE_MS,
               h_bounds=list(h_bounds),
               params=describe_x(sol.x), measured=final,
               published=dict(params=describe_x(x_start), measured=published,
                              residuals=cal.residuals(published, target).tolist()),
               residuals=cal.residuals(final, target).tolist(), sum_sq=float(np.sum(sol.fun ** 2)),
               n_evals=len(log), status=int(sol.status))
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    return out


def baseline():
    print(f"{'cell':5s}{'Rin MOhm':>20s}{'tau_m ms':>22s}{'rheobase pA':>24s}    (measured | target mean +- SD)")
    for k in CELL_TARGETS:
        m, t = cal.measure(builder(k, x0(k, True), True)), CELL_TARGETS[k]
        print(f"{k:5s}{m['r_in']:10.1f} |{t.r_in_mohm[0]:6.1f}+-{t.r_in_mohm[1]:5.1f}"
              f"{m['tau_m']:10.2f} |{t.tau_m_ms[0]:5.1f}+-{t.tau_m_ms[1]:4.1f}"
              f"{m['rheobase']:11.1f} |{t.rheobase_pa[0]:6.1f}+-{t.rheobase_pa[1]:5.1f}")


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "fit":
        cell, mode = sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else ("bez" if sys.argv[2] != "PYR" else "")
        if cell == "PYR" and mode == "bez":
            r = fit_bez_pyr()
        elif cell == "PYR" and mode == "bez-hbound":      # HCN held near the published density
            r = fit_bez_pyr(h_bounds=(0.5, 2.0), out_path="results/s3b_PYR_bez_hbound.json")
        elif mode in ("bez", "bez-noh"):
            r = fit_bez(cell, with_h=mode == "bez")
        else:
            r = fit(cell, point=mode == "point")
        print(json.dumps(r, indent=1))
    else:
        baseline()
