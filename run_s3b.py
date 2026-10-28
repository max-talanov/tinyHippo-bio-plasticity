"""S3b: intrinsic properties of the Tier-B cells against params.CELL_TARGETS, and their calibration.

Usage:
  python run_s3b.py                 baseline: measure the current placeholder cells
  python run_s3b.py fit PYR|PV|BiS|OLM   least-squares fit of three cell parameters; writes results/s3b_<cell>.json
Targets: Rin, tau_m, rheobase and resting potential (params.CELL_TARGETS). Parameters fitted: interneurons: lumped soma
size (um, L = diam), leak gl, Na/K scale (gnabar, gkbar x s), hh leak reversal el; PYR: dendritic leak g_pas, dendritic
diameter scale (all three dendrites), soma Na/K scale, soma leak gl, e_pas and soma el. Positive parameters on a log scale.
Starting point: the placeholder values of cells.py. Spike-based features use fixed step dt = 0.025 ms.
"""
import dataclasses
import json
import sys

import numpy as np
from scipy.optimize import least_squares

import calibrate as cal
from cells import INParams, PYRParams, IN_KINDS, build_interneuron, build_pyr
from params import CELL_TARGETS

KIND = {"PV": "pv", "BiS": "bis", "OLM": "olm"}
BASE_NAK = (0.12, 0.036)


def builder(cell, x):
    """x = log parameters. Returns a zero-argument builder."""
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
    n_log = 4 if len(v) == 6 else 3
    v[:n_log] = np.exp(v[:n_log])
    return v


def x0(cell):
    """Start vector: log of the positive parameters, then reversal potentials (mV)."""
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


def describe(cell, x):
    v = _lin(x)
    return (dict(g_pas=v[0], dend_diam_scale=v[1], nak_scale=v[2], soma_gl=v[3], e_pas=v[4], el=v[5]) if cell == "PYR"
            else dict(size_um=v[0], gl=v[1], nak_scale=v[2], el=v[3]))


def fit(cell):
    target = CELL_TARGETS[cell]
    log = []

    def res(x):
        try:
            m = cal.measure(builder(cell, x), rheobase_tol_na=1e-3)
        except Exception as e:                                   # a failed exponential fit or integration
            m = {"r_in": None, "tau_m": None, "rheobase": None}
        r = cal.residuals(m, target)
        log.append((describe(cell, x), m, float(np.sum(r ** 2))))
        return r

    if cell == "PYR":
        lo = np.concatenate([np.log([1e-7, 0.05, 0.02, 1e-6]), [-90.0, -90.0]])
        hi = np.concatenate([np.log([1e-2, 40.0, 50.0, 1e-3]), [-40.0, -40.0]])
    else:
        lo = np.concatenate([np.log([5.0, 1e-6, 0.02]), [-90.0]])
        hi = np.concatenate([np.log([300.0, 1e-3, 50.0]), [-40.0]])
    starts = [x0(cell)] + ([x0_from_target(cell)] if cell != "PYR" else [])
    sols = [least_squares(res, s, bounds=(lo, hi), diff_step=0.05, max_nfev=80, x_scale=1.0) for s in starts]
    sol = min(sols, key=lambda s: np.sum(s.fun ** 2))
    final = cal.measure(builder(cell, sol.x))
    out = dict(cell=cell, params=describe(cell, sol.x), measured=final, start=describe(cell, x0(cell)),
               residuals=cal.residuals(final, target).tolist(), sum_sq=float(np.sum(sol.fun ** 2)),
               n_evals=len(log), status=int(sol.status), start_sum_sq=[float(np.sum(s.fun ** 2)) for s in sols],
               target={k: getattr(target, t) for k, t in cal.FEATURES})
    with open(f"results/s3b_{cell}.json", "w") as fh:
        json.dump(out, fh, indent=1)
    return out


def baseline():
    print(f"{'cell':5s}{'Rin MOhm':>20s}{'tau_m ms':>22s}{'rheobase pA':>24s}    (measured | target mean +- SD)")
    for k in CELL_TARGETS:
        m, t = cal.measure(builder(k, x0(k))), CELL_TARGETS[k]
        print(f"{k:5s}{m['r_in']:10.1f} |{t.r_in_mohm[0]:6.1f}+-{t.r_in_mohm[1]:5.1f}"
              f"{m['tau_m']:10.2f} |{t.tau_m_ms[0]:5.1f}+-{t.tau_m_ms[1]:4.1f}"
              f"{m['rheobase']:11.1f} |{t.rheobase_pa[0]:6.1f}+-{t.rheobase_pa[1]:5.1f}")


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "fit":
        r = fit(sys.argv[2])
        print(json.dumps(r, indent=1))
    else:
        baseline()
