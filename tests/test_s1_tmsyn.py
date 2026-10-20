"""S1: verify TMSyn against the closed-form Tsodyks-Markram solution.

Acceptance (docs/plan.md): relative error of every event amplitude and of the
conductance trace < 1%; CVODE and fixed dt = 25 us agree within 2%.
The parameter sets below are test fixtures, not literature values.
"""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import analysis as an  # noqa: E402
import protocols as pr  # noqa: E402

PARAMS = {
    "depressing": dict(U=0.5, tau_rec=800.0, tau_fac=0.0),
    "facilitating": dict(U=0.09, tau_rec=138.0, tau_fac=670.0),
    "mixed": dict(U=0.2, tau_rec=300.0, tau_fac=200.0),
}
W = 1e-3
T1, T2 = 0.5, 3.0


def periodic(freq, n, t0=10.0):
    return t0 + np.arange(n) * 1000.0 / freq


def irregular(seed=1, n=30, mean_isi=40.0):
    rng = np.random.default_rng(seed)
    t = 10.0 + np.cumsum(rng.exponential(mean_isi, n))
    return np.round(t / pr.DT_FIXED) * pr.DT_FIXED      # on the fixed-step grid


def check(spikes, p, cvode):
    amps, t, g = pr.run_tm(spikes, **p, w=W, tau1=T1, tau2=T2, cvode=cvode)
    ref = an.tm_amplitudes(spikes, **p)
    g_ref = an.tm_conductance(t, spikes, ref, W, T1, T2)
    return amps, ref, g, g_ref


@pytest.mark.parametrize("cvode", [True, False])
@pytest.mark.parametrize("n", [2, 20])
@pytest.mark.parametrize("freq", [5, 20, 50])
@pytest.mark.parametrize("name", list(PARAMS))
def test_periodic_trains(name, freq, n, cvode):
    amps, ref, g, g_ref = check(periodic(freq, n), PARAMS[name], cvode)
    assert np.max(np.abs(amps - ref) / ref) < 1e-2
    assert np.max(np.abs(g - g_ref)) / np.max(g_ref) < 1e-2


@pytest.mark.parametrize("cvode", [True, False])
@pytest.mark.parametrize("name", list(PARAMS))
def test_irregular_train(name, cvode):
    amps, ref, g, g_ref = check(irregular(), PARAMS[name], cvode)
    assert np.max(np.abs(amps - ref) / ref) < 1e-2
    assert np.max(np.abs(g - g_ref)) / np.max(g_ref) < 1e-2


@pytest.mark.parametrize("name", list(PARAMS))
def test_cvode_vs_fixed_step(name):
    sp = periodic(50, 20)
    _, t_c, g_c = pr.run_tm(sp, **PARAMS[name], w=W, tau1=T1, tau2=T2, cvode=True)
    _, t_f, g_f = pr.run_tm(sp, **PARAMS[name], w=W, tau1=T1, tau2=T2, cvode=False)
    n = min(len(g_c), len(g_f))             # the last sample can differ by one
    assert np.allclose(t_c[:n], t_f[:n])
    g_c, g_f = g_c[:n], g_f[:n]
    assert np.max(np.abs(g_c - g_f)) / np.max(g_f) < 2e-2


@pytest.mark.parametrize("name", list(PARAMS))
def test_reference_matches_ode_integration(name):
    sp = irregular(seed=3)
    a = an.tm_amplitudes(sp, **PARAMS[name])
    b = an.tm_amplitudes_ode(sp, **PARAMS[name])
    assert np.max(np.abs(a - b) / a) < 1e-6


@pytest.mark.parametrize("freq", [5, 20, 50])
def test_steady_state_closed_form(freq):
    p = PARAMS["depressing"]
    amps, *_ = pr.run_tm(periodic(freq, 40), **p, w=W, tau1=T1, tau2=T2, cvode=True)
    expected = an.tm_steady_state_amplitude(p["U"], p["tau_rec"], 1000.0 / freq)
    assert abs(amps[-1] - expected) / expected < 1e-3


def test_single_event_peak_equals_weight():
    amps, t, g = pr.run_tm(np.array([10.0]), **PARAMS["depressing"], w=W, tau1=T1, tau2=T2)
    assert amps[0] == pytest.approx(PARAMS["depressing"]["U"], rel=1e-12)   # u+ = U, x- = 1
    assert np.max(g) == pytest.approx(W * PARAMS["depressing"]["U"], rel=1e-2)
