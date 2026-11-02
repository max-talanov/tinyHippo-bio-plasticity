"""S3a: verify TMSynPI (TM release + presynaptic GPCR inhibition of U) against analysis.tm_pi_terms.

Acceptance as S1: relative error of every release < 1% (expected ~1e-9, both are exact per event). With no inhibition
TMSynPI must equal TMSyn. The log terms must sum to log(amp/U). Parameters are test fixtures, not literature values.
"""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import analysis as an  # noqa: E402
import protocols as pr  # noqa: E402

STP = {"depressing": dict(U=0.5, tau_rec=800.0, tau_fac=0.0),
       "facilitating": dict(U=0.09, tau_rec=138.0, tau_fac=670.0),
       "mixed": dict(U=0.2, tau_rec=300.0, tau_fac=200.0)}
INHIB = dict(i_tonic=0.25, i_max=0.8, c=0.3, tau_r=50.0, tau_d=300.0)


def trains(seed=3):
    rng = np.random.default_rng(seed)
    # 1 ms refractoriness: release is read 2 steps after each spike, so spikes must be further apart than that
    sp = np.round((10.0 + np.cumsum(1.0 + rng.exponential(25.0, 60))) / pr.DT_FIXED) * pr.DT_FIXED
    gaba = sp[::2] + 3.0                                  # feedforward interneuron, every other spike, 3 ms later
    return sp, gaba


@pytest.mark.parametrize("name", STP)
def test_against_reference(name):
    sp, gaba = trains()
    got = pr.run_tm_pi(sp, gaba, **STP[name], **INHIB)
    ref = an.tm_pi_terms(sp, gaba, **STP[name], **INHIB)
    assert ref["iph"].max() > 0.1                         # the inhibition is actually engaged
    for k in ("amp", "u", "x", "ueff", "iph"):
        assert np.max(np.abs(got[k] - ref[k]) / np.maximum(np.abs(ref[k]), 1e-12)) < 1e-6, k


@pytest.mark.parametrize("name", STP)
def test_no_inhibition_equals_tmsyn(name):
    sp, gaba = trains()
    got = pr.run_tm_pi(sp, gaba, **STP[name])             # i_tonic = i_max = 0
    amps, _, _ = pr.run_tm(sp, **STP[name])
    assert np.max(np.abs(got["amp"] - amps) / amps) < 1e-9


def test_terms_sum_to_log_release():
    sp, gaba = trains()
    p = STP["mixed"]
    r = an.tm_pi_terms(sp, gaba, **p, **INHIB)
    total = r["fac"] + r["dep"] + r["phasic"] + r["tonic"]
    assert np.allclose(total, np.log(r["amp"] / p["U"]), atol=1e-12)
    assert (r["fac"] >= 0).all() and (r["dep"] <= 0).all() and (r["phasic"] <= 0).all()
