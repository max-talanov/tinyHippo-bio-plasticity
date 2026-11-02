"""S3b: calibrate._spike_features on a synthetic trace with known threshold times, threshold, amplitude and AHP.

Each spike: rest at -60 mV, a ramp at 10 mV/ms (below the 28 mV/ms cutoff) to -40 mV, a 100 mV/ms upstroke to +30 mV, a
fall to -65 mV (AHP 25 mV below threshold), then recovery to -60. Spikes every 50 ms inside the step window.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import calibrate as cal  # noqa: E402


def synthetic(spike_starts, dt=0.025):
    t = np.arange(0.0, cal.DELAY + cal.DUR + 50.0, dt)
    v = np.full_like(t, -60.0)
    for t0 in spike_starts:
        seg = [(t0, -60.0), (t0 + 2.0, -40.0), (t0 + 2.7, 30.0), (t0 + 4.0, -65.0), (t0 + 20.0, -60.0)]
        for (ta, va), (tb, vb) in zip(seg[:-1], seg[1:]):
            sel = (t >= ta) & (t < tb)
            v[sel] = va + (vb - va) * (t[sel] - ta) / (tb - ta)
    return t, v


def test_spike_features():
    starts = cal.DELAY + 10.0 + 50.0 * np.arange(4)
    sp = cal._spike_features(*synthetic(starts))
    assert len(sp) == 4
    assert np.allclose(np.diff([s["t_thr"] for s in sp]), 50.0, atol=0.05)
    assert all(abs(s["v_thr"] - (-40.0)) < 1.0 for s in sp)
    assert all(abs(s["amp"] - 70.0) < 1.0 for s in sp)
    assert all(abs(s["ahp"] - 25.0) < 1.0 for s in sp)


def test_spikes_outside_step_ignored():
    sp = cal._spike_features(*synthetic([10.0, cal.DELAY + cal.DUR + 5.0]))
    assert sp == []
