"""Tier-B cells: one PYR (4 sections) and three one-compartment interneurons.

ALL BIOPHYSICAL VALUES HERE ARE UNVERIFIED PLACEHOLDERS (NEURON's textbook hh and generic passive values),
not literature values for CA1. The interneuron classes differ only in size. Do not quote them as CA1 properties.
Rheobase is measured with injected DC current in `rheobase()`.
"""
import math
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
    el: float = -54.3             # mV, hh leak reversal (NEURON default)
    nseg: int = 5


@dataclass(frozen=True)
class INParams:
    size: float = 15.0            # um, L = diam (morph="point" only)
    Ra: float = 100.0
    cm: float = 1.0
    gnabar: float = 0.12
    gkbar: float = 0.036
    gl: float = 3e-4
    el: float = -54.3             # mV, hh leak reversal (NEURON default)
    morph: str = "point"          # "point": one soma; "bezaire": soma + dendrites of IN_MORPH (passive)
    dend_diam_scale: float = 1.0  # multiplies every dendrite and axon diameter of IN_MORPH
    g_pas: float = 1e-4           # S/cm2, dendrites and axon
    e_pas: float = -65.0


IN_KINDS = {"pv": INParams(size=15.0), "bis": INParams(size=18.0), "olm": INParams(size=20.0)}

# Morphologies of the Bezaire et al. 2016 CA1 model (code: github.com/mbezaire/ca1, commit a8655fa, cells/class_*.hoc;
# also ModelDB 187604). These are the model's simplified morphologies, not reconstructions. Status: model value.
# Soma (L, diam) um; branches (name, L um, diam um, parent, parent end), parent None = soma. cm uF/cm2, Ra ohm cm as in
# that code. PV basket and bistratified share one morphology there: two apical trees of five sections (diameter
# 4 -> 1 um, 600 um) from soma(1) and two basal trees of three sections (2 -> 1 um, 300 um) from soma(0).
# Each tree is given by the (x, y) end points of its sections in the templates (pt3dadd; z = 0, the middle points lie
# on the line) and their diameters; the length is the distance, e.g. 199.9997 um rather than 200, so that the port
# reproduces the templates to 1e-10 mV (tests/test_s3b_bezaire_cells.py). Trees: apA = dend[0-4], apB = dend[5-9],
# baA = dend[10-12], baB = dend[13-15].
_TREES = {
    "apA": ((0, 20), (38.9418, 112.106), (77.8837, 204.212), (155.767, 388.424), (194.709, 480.531), (233.651, 572.637)),
    "apB": ((0, 20), (-38.9418, 112.106), (-77.8837, 204.212), (-155.767, 388.424), (-194.709, 480.531),
            (-233.651, 572.637)),
    "baA": ((0, 0), (-38.9418, -92.1061), (-77.8837, -184.212), (-116.826, -276.318)),
    "baB": ((0, 0), (38.9419, -92.1061), (77.8837, -184.212), (116.826, -276.318)),
}
_DIAMS = {"ap": (4.0, 3.0, 2.0, 1.5, 1.0), "ba": (2.0, 1.5, 1.0)}


def _tree(prefix, root_end):
    pts, diams = _TREES[prefix], _DIAMS[prefix[:2]]
    return tuple((f"{prefix}{i}", math.dist(pts[i], pts[i + 1]), d, None if i == 0 else f"{prefix}{i - 1}",
                  root_end if i == 0 else 1.0) for i, d in enumerate(diams))


_BASKET_LIKE = dict(soma=(20.0, 10.0), cm=1.4, Ra=100.0,
                    branches=_tree("apA", 1.0) + _tree("apB", 1.0) + _tree("baA", 0.0) + _tree("baB", 0.0))
IN_MORPH = {
    "pv": _BASKET_LIKE,
    "bis": _BASKET_LIKE,
    # O-LM: two horizontal dendrites (250.3 um, 3 um) from soma(1) and an axon stub (150 um, 1.5 um) from soma(0)
    "olm": dict(soma=(20.0, 10.0), cm=1.3, Ra=150.0,
                branches=(("dA", math.hypot(177.0, 177.0), 3.0, None, 1.0), ("dB", math.hypot(177.0, 177.0), 3.0, None, 1.0),
                          ("axon", 150.0, 1.5, None, 0.0))),
}


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
        seg.hh.gnabar, seg.hh.gkbar, seg.hh.gl, seg.hh.el = p.gnabar, p.gkbar, p.gl, p.el
    for sec in (basal, prox, dist):
        sec.insert("pas")
        for seg in sec:
            seg.pas.g, seg.pas.e = p.g_pas, p.e_pas
    return {"soma": soma, "basal": basal, "prox": prox, "dist": dist}


def build_interneuron(kind: str, p: INParams = None):
    """morph="point": one soma of size p.size, cm and Ra from p. morph="bezaire": soma and branches of IN_MORPH[kind],
    with that morphology's cm and Ra; hh in the soma only, passive branches (p.g_pas, p.e_pas). Returns {"soma", "dend"}."""
    p = p or IN_KINDS[kind]
    soma = h.Section(name=f"{kind}_soma")
    dend = {}
    if p.morph == "point":
        soma.L = soma.diam = p.size
        soma.Ra, soma.cm = p.Ra, p.cm
    else:
        m = IN_MORPH[kind]
        soma.L, soma.diam = m["soma"]
        soma.Ra, soma.cm = m["Ra"], m["cm"]
        for name, L, d, parent, end in m["branches"]:
            sec = h.Section(name=f"{kind}_{name}")
            sec.L, sec.diam, sec.Ra, sec.cm = L, d * p.dend_diam_scale, m["Ra"], m["cm"]
            sec.nseg = max(1, 2 * int(L / 50.0) + 1)                # odd, about one segment per 25 um
            sec.connect(soma(end) if parent is None else dend[parent](1.0))
            sec.insert("pas")
            for seg in sec:
                seg.pas.g, seg.pas.e = p.g_pas, p.e_pas
            dend[name] = sec
    soma.insert("hh")
    for seg in soma:
        seg.hh.gnabar, seg.hh.gkbar, seg.hh.gl, seg.hh.el = p.gnabar, p.gkbar, p.gl, p.el
    return {"soma": soma, "dend": dend}


# Channel densities and passive values of the Bezaire et al. 2016 interneurons (same source and commit as IN_MORPH,
# `mechinit` and `insert_mechs` of the templates; mechanisms in mod/, see mod/BEZAIRE_CHANNELS.md). Status: model value.
# gmax in S/cm2, rm in ohm cm2. PV and bistratified: every channel in soma and dendrites with the same density
# ("all"); Ca2+ not accumulated (iconc_Ca is not inserted in those templates), cai = NEURON default, eca fixed.
# O-LM: per-section values; ena, ek are not set by that template (NEURON defaults 50 and -77 mV), nor is eh (see eh).
_BASKET_CH = dict(KvA="ch_KvA", CavN="ch_CavN", CavL="ch_CavL", KCaS="ch_KCaS", KvCaB="ch_KvCaB", Kdr="ch_Kdrfast",
                  leak="ch_leak")
BEZ_CHANNELS = {
    "pv": dict(Na="ch_Navaxonp", rm=5555.0, e_leak=-65.0, ena=55.0, ek=-90.0,
               all=dict(Na=0.15, Kdr=0.013, KvA=0.00015, CavN=0.0008, CavL=0.005, KvCaB=2e-7, KCaS=2e-6)),
    "bis": dict(Na="ch_Navbis", rm=11110.0, e_leak=-67.0, ena=55.0, ek=-90.0,
                all=dict(Na=0.07, Kdr=0.016, KvA=0.00005, CavN=0.0004, CavL=0.004, KvCaB=7e-8, KCaS=7e-7)),
    "olm": dict(Na="ch_Nav", rm=1e5, e_leak=-67.0, ena=None, ek=None,
                soma=dict(KvA=0.0165 * 0.3 * 1.5, H=0.0005, Kdr=0.0319 * 2.3, Na=0.0107),
                dend=dict(KvA=0.004 * 0.7 * 1.5, Kdr=2 * 0.023 * 2.3, Na=2 * 0.0117),
                axon=dict(Kdr=0.05104 * 2.3, Na=0.01712)),
}
_OLM_CH = dict(KvA="ch_KvAolm", H="ch_HCNolm", Kdr="ch_Kdrfast", leak="ch_leak")
BEZ_CELSIUS = 34.0
_CA_OUT, _CA_IN = 2.0, 5e-6        # mM; the PV/BiS templates' eca formula (gives about 171 mV at 34 C)


@dataclass(frozen=True)
class BezINParams:
    """Scale factors on the Bezaire densities (1 = the published cell). k_scale multiplies the fast delayed rectifier
    only; h_scale the O-LM HCN. e_leak None = source value. eh: HCN reversal (mV); None leaves the ion default, which is
    what the published O-LM template runs with (0 mV, because ch_HCNolm READs eh and the template never sets it)."""
    leak_scale: float = 1.0
    na_scale: float = 1.0
    k_scale: float = 1.0
    h_scale: float = 1.0
    dend_diam_scale: float = 1.0
    e_leak: float = None
    eh: float = None


def _bez_nseg(L, diam):
    """Bezaire's set_nseg (d_lambda 0.1 at 100 Hz), evaluated, as in the templates, before Ra and cm are set
    (NEURON defaults Ra 35.4 ohm cm, cm 1 uF/cm2)."""
    lam = 1e5 * math.sqrt(diam / (4 * math.pi * 100.0 * 35.4 * 1.0))
    return int((L / (0.1 * lam) + 0.9) / 2) * 2 + 1


def build_bezaire_interneuron(kind: str, p: BezINParams = BezINParams()):
    """Bezaire 2016 interneuron: morphology IN_MORPH[kind], channels BEZ_CHANNELS[kind] times the scales of p.
    Sets h.celsius = 34 (global, as the templates do). Returns {"soma", "dend"}."""
    h.celsius = BEZ_CELSIUS
    m, ch = IN_MORPH[kind], BEZ_CHANNELS[kind]
    soma = h.Section(name=f"{kind}_soma")
    soma.L, soma.diam = m["soma"]
    secs, dend = {"soma": soma}, {}
    for name, L, d, parent, end in m["branches"]:
        sec = h.Section(name=f"{kind}_{name}")
        sec.L, sec.diam = L, d * p.dend_diam_scale
        sec.connect(soma(end) if parent is None else dend[parent](1.0))
        dend[name] = secs[name] = sec
    scale = dict(Na=p.na_scale, Kdr=p.k_scale, H=p.h_scale)
    e_leak = ch["e_leak"] if p.e_leak is None else p.e_leak
    for name, sec in secs.items():
        sec.nseg = _bez_nseg(sec.L, sec.diam)
        sec.Ra, sec.cm = m["Ra"], m["cm"]
        if kind == "olm":
            group = "soma" if name == "soma" else ("axon" if name == "axon" else "dend")
            dens, names = ch[group], dict(_OLM_CH, Na=ch["Na"])
        else:
            dens, names = ch["all"], dict(_BASKET_CH, Na=ch["Na"])
        for key, g in list(dens.items()) + [("leak", 1.0 / ch["rm"] * p.leak_scale)]:
            mech = names[key]
            sec.insert(mech)
            for seg in sec:
                setattr(getattr(seg, mech), "gmax", g * scale.get(key, 1.0))
        for seg in sec:
            seg.ch_leak.e = e_leak
        if ch["ena"] is not None:
            sec.ena, sec.ek = ch["ena"], ch["ek"]
        if kind != "olm":
            sec.eca = 8.314 * (273.15 + BEZ_CELSIUS) / (2 * 9.649e4) * math.log(_CA_OUT / _CA_IN) * 1000
        elif name == "soma" and p.eh is not None:
            sec.eh = p.eh
    return {"soma": soma, "dend": dend}


# Interneurons chosen for Tier B (project owner, 2026-10-29; RESULTS.md section 8): the published PV basket cell, the published
# O-LM cell with its HCN at the Maccaferri & McBain reversal (params.CHANNEL_PARAMS["OLM_eh"]; the template runs it at
# 0 mV), and the bistratified refit of results/s3b_BiS_bez.json (all scales within 20% of the published cell).
TIER_B_IN = {
    "pv": BezINParams(),
    "bis": BezINParams(leak_scale=1.1819891919785726, dend_diam_scale=0.8850160316274004, na_scale=1.0039523391884928,
                       k_scale=1.0123475444828103, e_leak=-65.32734812473224),
    "olm": BezINParams(eh=-32.9),
}


@dataclass(frozen=True)
class BezPYRParams:
    """Scale factors on the Bezaire 2016 pyramidal cell (1 = published). Each multiplies the published per-segment
    densities, so the dendritic gradients (HCN, A-type K) are kept. na_scale: ch_Navp and the axonal ch_Navaxonp;
    k_scale: ch_Kdrp; h_scale: ch_HCNp; leak_scale: pas everywhere. e_pas None = published (Vrest = -66 mV)."""
    leak_scale: float = 1.0
    na_scale: float = 1.0
    k_scale: float = 1.0
    h_scale: float = 1.0
    ka_scale: float = 1.0
    e_pas: float = None


_PYR_TEMPLATE_LOADED = False


def build_bezaire_pyr(p: BezPYRParams = BezPYRParams()):
    """The Bezaire et al. 2016 CA1 pyramidal cell (class_poolosyncell: reconstructed morphology of 202 sections, Poolos-type
    channels, 34 C), run from the original template in reference/bezaire2016 with stubs for its network globals, then
    rescaled by p. Returns {"soma": soma[5] (the widest somatic section, Bezaire's distance origin), "basal", "prox"
    (stratum radiatum), "dist" (lacunosum-moleculare): lists of sections, "obj": the template object (keep it: the
    sections die with it)}. Sets h.celsius = 34."""
    global _PYR_TEMPLATE_LOADED
    from pathlib import Path
    if not _PYR_TEMPLATE_LOADED:
        if not hasattr(h, "numCellTypes"):
            h("numCellTypes = 0")
            h("objref cellType[1]")
        h.load_file(str(Path(__file__).resolve().parent / "reference" / "bezaire2016" / "class_poolosyncell.hoc"))
        _PYR_TEMPLATE_LOADED = True
    c = h.poolosyncell(0, 0, 0)
    scale = (("pas", "g", p.leak_scale), ("ch_Navp", "gmax", p.na_scale), ("ch_Navaxonp", "gmax", p.na_scale),
             ("ch_Kdrp", "gmax", p.k_scale), ("ch_HCNp", "gmax", p.h_scale), ("ch_KvAproxp", "gmax", p.ka_scale),
             ("ch_KvAdistp", "gmax", p.ka_scale))
    for sec in c.all:
        for mech, var, k in scale:
            if k != 1.0 and h.ismembrane(mech, sec=sec):
                for seg in sec:
                    m = getattr(seg, mech)
                    setattr(m, var, getattr(m, var) * k)
        if p.e_pas is not None:
            for seg in sec:
                seg.pas.e = p.e_pas
    return {"soma": c.soma[5], "basal": list(c.basal_list), "prox": list(c.rad_list), "dist": list(c.lm_list), "obj": c}


# Pyramidal cell chosen for Tier B (project owner, 2026-10-29; RESULTS.md section 9): the refit of results/s3b_PYR_bez.json
# (HCN free in 0.1-10; it went to 0.10). The HCN-bounded refit (results/s3b_PYR_bez_hbound.json) is the alternative.
TIER_B_PYR = BezPYRParams(leak_scale=0.2984330424660662, na_scale=0.6917122427493793, k_scale=1.463347813259006,
                          h_scale=0.10421089695367888, ka_scale=1.5655610162767035, e_pas=-75.17728451329069)


def rheobase(sec, i_max=1.0, tol=1e-4, dur=500.0):
    """Smallest DC current (nA, 500 ms) that evokes at least one spike, by bisection. Fixed step 0.025 ms.

    Keep a reference to every section of the cell while measuring: `rheobase(build_pyr()["soma"])` drops the dict, NEURON
    deletes the unreferenced dendrites and the result is a soma-only cell. `calibrate.measure` does this correctly."""
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
