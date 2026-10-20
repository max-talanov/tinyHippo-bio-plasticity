"""S2 machinery: EPSC readout and TM parameter fit, checked on data with known ground truth."""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import analysis as an  # noqa: E402
import protocols as pr  # noqa: E402

W, V_HOLD, E_REV = 1e-3, -70.0, 0.0
SCALE = W * (V_HOLD - E_REV)         # nA per unit release fraction
ISIS = (20.0, 50.0, 100.0, 200.0, 500.0)
FREQS = (5.0, 10.0, 20.0, 50.0)


def protocol_trials(n_train=10):
    """Paired pulses at several ISIs plus trains at several frequencies, one independent trial each."""
    trials = [np.array([10.0, 10.0 + isi]) for isi in ISIS]
    trials += [10.0 + np.arange(n_train) * 1000.0 / f for f in FREQS]
    return trials


PARAMS = {
    "depressing": dict(U=0.5, tau_rec=800.0, tau_fac=0.0),
    "facilitating": dict(U=0.09, tau_rec=138.0, tau_fac=670.0),
    "mixed": dict(U=0.2, tau_rec=300.0, tau_fac=200.0),
}


@pytest.mark.parametrize("name", list(PARAMS))
def test_epsc_readout_matches_release_fraction(name):
    """Peak-minus-baseline EPSC amplitude = driving force * w * release fraction, to < 0.5%."""
    p = PARAMS[name]
    for sp in protocol_trials()[:7]:
        t, i = pr.run_clamped(sp, **p, w=W)
        amps = pr.epsc_amplitudes(t, i, sp)
        ref = an.tm_amplitudes(sp, **p) * abs(SCALE)
        assert np.max(np.abs(amps - ref) / ref) < 5e-3


@pytest.mark.parametrize("name", ["facilitating", "mixed"])
def test_noise_free_recovery(name):
    """Fit to NEURON-simulated EPSC amplitudes recovers the generating parameters (< 2%)."""
    p = PARAMS[name]
    trials = protocol_trials()
    obs = []
    for sp in trials:
        t, i = pr.run_clamped(sp, **p, w=W)
        obs.append(pr.epsc_amplitudes(t, i, sp))
    fit = an.fit_tm(trials, obs)
    A, U, tr, tf = fit["theta"]
    assert U == pytest.approx(p["U"], rel=2e-2)
    assert tr == pytest.approx(p["tau_rec"], rel=2e-2)
    assert tf == pytest.approx(p["tau_fac"], rel=2e-2)
    assert A == pytest.approx(abs(SCALE), rel=2e-2)
