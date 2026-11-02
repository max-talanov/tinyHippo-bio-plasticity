"""S3b: cells.build_bezaire_interneuron against the original Bezaire et al. 2016 hoc templates (reference/bezaire2016).

Both cells get the same current steps (a hyperpolarising step and a suprathreshold one), fixed dt = 0.025 ms, 34 C,
same initialisation. Acceptance: the soma voltage traces agree within 0.01 mV everywhere and the spike counts are equal.
Observed: O-LM 2e-10 mV; PV 2e-3 and bistratified 7e-4 mV during spiking (3e-8 mV subthreshold). The PV/BiS templates
define the geometry by 3-D points; with the template's own section lengths copied in, the port agrees to 6e-11 mV, so the
rest is geometry rounding (probably the single-precision 3-D points), amplified over the spikes.
"""
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from cells import BezINParams, build_bezaire_interneuron, h  # noqa: E402

TEMPLATES = {"pv": "pvbasketcell", "bis": "bistratifiedcell", "olm": "olmcell"}
_loaded = False


def _template(kind):
    global _loaded
    if not _loaded:
        h("numCellTypes = 0")          # stubs for the network globals the templates declare `external`
        h("objref cellType[1]")
        for name in TEMPLATES.values():
            h.load_file(str(ROOT / "reference" / "bezaire2016" / f"class_{name}.hoc"))
        _loaded = True
    return getattr(h, TEMPLATES[kind])(0, 0, 0)


def _run(sec, amp_na, t_stop=400.0):
    st = h.IClamp(sec(0.5))
    st.delay, st.dur, st.amp = 100.0, 200.0, amp_na
    v = h.Vector()
    v.record(sec(0.5)._ref_v)
    h.cvode_active(0)
    h.dt = 0.025
    h.celsius = 34.0
    h.finitialize(-65.0)
    h.continuerun(t_stop)
    return np.array(v)


@pytest.mark.parametrize("kind", ["pv", "bis", "olm"])
@pytest.mark.parametrize("amp_na", [-0.05, 0.5])
def test_port_matches_template(kind, amp_na):
    ref = _template(kind)
    v_ref = _run(ref.soma[0], amp_na)
    del ref
    for sec in list(h.allsec()):
        h.delete_section(sec=sec)
    port = build_bezaire_interneuron(kind, BezINParams())
    v_port = _run(port["soma"], amp_na)
    for sec in list(h.allsec()):
        h.delete_section(sec=sec)
    spikes = lambda v: int(np.sum((v[1:] > 0) & (v[:-1] <= 0)))
    assert spikes(v_port) == spikes(v_ref)
    assert np.max(np.abs(v_port - v_ref)) < 0.01
