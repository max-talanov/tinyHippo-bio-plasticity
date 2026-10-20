"""S0: NEURON installs, NMODL compiles, Exp2Syn and an event-driven mechanism run."""
import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from nrn_setup import load_mechanisms  # noqa: E402

h = load_mechanisms()
h.load_file("stdrun.hoc")


def _soma():
    soma = h.Section(name="soma")
    soma.L = soma.diam = 20.0
    soma.insert("pas")
    soma.g_pas = 1.0 / 20000.0   # membrane tau = 20 ms with cm = 1 uF/cm2 -> 20 ms
    soma.e_pas = -65.0
    return soma


def _run(tstop, cvode):
    h.cvode_active(1 if cvode else 0)
    if cvode:
        h.CVode().atol(1e-8)   # default atol = 1e-3 is too coarse for small state variables
    else:
        h.dt = 0.025
    h.finitialize(-65.0)
    h.continuerun(tstop)


@pytest.mark.parametrize("cvode", [True, False])
def test_exp2syn_epsp(cvode):
    soma = _soma()
    syn = h.Exp2Syn(soma(0.5))
    syn.tau1, syn.tau2, syn.e = 0.5, 3.0, 0.0
    stim = h.NetStim()
    stim.number, stim.start, stim.noise = 1, 5.0, 0
    nc = h.NetCon(stim, syn)
    nc.weight[0], nc.delay = 0.001, 0.0
    t, v = h.Vector().record(h._ref_t), h.Vector().record(soma(0.5)._ref_v)
    _run(300.0, cvode)
    peak = max(v) + 65.0
    t_peak = t[list(v).index(max(v))]
    assert 0.05 < peak < 20.0
    assert 5.0 < t_peak < 15.0
    assert abs(v[-1] + 65.0) < 1e-2        # back to rest


@pytest.mark.parametrize("cvode", [True, False])
def test_event_jump_and_decay(cvode):
    soma = _soma()
    pp = h.S0Check(soma(0.5))
    pp.tau = 20.0
    stim = h.NetStim()
    stim.number, stim.start, stim.noise = 1, 5.0, 0
    nc = h.NetCon(stim, pp)
    nc.weight[0], nc.delay = 1.0, 0.0
    tv, xv = h.Vector().record(h._ref_t), h.Vector().record(pp._ref_x)
    _run(60.0, cvode)
    t = list(tv)
    for probe in (10.0, 25.0, 45.0):
        i = min(range(len(t)), key=lambda k: abs(t[k] - probe))
        expected = math.exp(-(t[i] - 5.0) / 20.0)
        assert abs(xv[i] - expected) / expected < 2e-2
