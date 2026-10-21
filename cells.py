"""Tier-B cells: one PYR (4 sections) and three one-compartment interneurons.

ALL BIOPHYSICAL VALUES HERE ARE UNVERIFIED PLACEHOLDERS (NEURON's textbook hh and generic passive values),
not literature values for CA1. The interneuron classes differ only in size. Do not quote them as CA1 properties.
Rheobase is measured with injected DC current in `rheobase()`.
"""
from dataclasses import dataclass

from nrn_setup import load_mechanisms

h = load_mechanisms()
h.load_file("stdrun.hoc")


@dataclass(frozen=True)
class PYRParams:
    soma_L: float = 20.0          # um
    soma_diam: float = 20.0
    basal_L: float = 200.0
    basal_diam: float = 2.0
    prox_L: float = 300.0
    prox_diam: float = 2.0
    dist_L: float = 300.0
    dist_diam: float = 1.5
    Ra: float = 100.0             # ohm cm
    cm: float = 1.0               # uF/cm2
    g_pas: float = 1e-4           # S/cm2, dendrites
    e_pas: float = -65.0
    gnabar: float = 0.12          # S/cm2, hh defaults
    gkbar: float = 0.036
    gl: float = 3e-4
    nseg: int = 5


@dataclass(frozen=True)
class INParams:
    size: float = 15.0            # um, L = diam
    Ra: float = 100.0
    cm: float = 1.0
    gnabar: float = 0.12
    gkbar: float = 0.036
    gl: float = 3e-4


IN_KINDS = {"pv": INParams(size=15.0), "bis": INParams(size=18.0), "olm": INParams(size=20.0)}


def build_pyr(p: PYRParams = PYRParams(), name="pyr"):
    soma = h.Section(name=f"{name}_soma")
    basal = h.Section(name=f"{name}_basal")
    prox = h.Section(name=f"{name}_prox")
    dist = h.Section(name=f"{name}_dist")
    for sec, L, d in ((soma, p.soma_L, p.soma_diam), (basal, p.basal_L, p.basal_diam),
                      (prox, p.prox_L, p.prox_diam), (dist, p.dist_L, p.dist_diam)):
        sec.L, sec.diam, sec.Ra, sec.cm, sec.nseg = L, d, p.Ra, p.cm, p.nseg
    basal.connect(soma(0))
    prox.connect(soma(1))
    dist.connect(prox(1))
    soma.insert("hh")
    for seg in soma:
        seg.hh.gnabar, seg.hh.gkbar, seg.hh.gl = p.gnabar, p.gkbar, p.gl
    for sec in (basal, prox, dist):
        sec.insert("pas")
        for seg in sec:
            seg.pas.g, seg.pas.e = p.g_pas, p.e_pas
    return {"soma": soma, "basal": basal, "prox": prox, "dist": dist}


def build_interneuron(kind: str):
    p = IN_KINDS[kind]
    soma = h.Section(name=f"{kind}_soma")
    soma.L = soma.diam = p.size
    soma.Ra, soma.cm = p.Ra, p.cm
    soma.insert("hh")
    for seg in soma:
        seg.hh.gnabar, seg.hh.gkbar, seg.hh.gl = p.gnabar, p.gkbar, p.gl
    return {"soma": soma}


def rheobase(sec, i_max=1.0, tol=1e-4, dur=500.0):
    """Smallest DC current (nA, 500 ms) that evokes at least one spike, by bisection. Fixed step 0.025 ms."""
    import numpy as np
    stim = h.IClamp(sec(0.5))
    stim.delay, stim.dur = 50.0, dur
    tv, vv = h.Vector(), h.Vector()
    tv.record(h._ref_t)
    vv.record(sec(0.5)._ref_v)
    h.cvode_active(0)
    h.dt = 0.025

    def spikes(i):
        stim.amp = i
        h.finitialize(-65.0)
        h.continuerun(dur + 100.0)
        v = np.array(vv)
        return bool(np.any(v > 0.0))

    lo, hi = 0.0, i_max
    if not spikes(hi):
        return None
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        lo, hi = (lo, mid) if spikes(mid) else (mid, hi)
    tv.play_remove(); vv.play_remove()
    return hi
