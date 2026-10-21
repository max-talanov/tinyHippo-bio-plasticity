"""Tier-B circuit (PYR + PV basket + bistratified + O-LM) with Tsodyks-Markram synapses. PILOT.

Sources: STP (U, D, F) from params.PATHWAYS (secondary sources); peak conductances g-hat from Ecker et al. 2019
Table 1 (PC->PVBC 3, PC->BS 1.4, PC->SOM+ 0.85, PVBC->PC 1.75, BS->PC 2.4, SOM+->PC 1.3 nS; rat CA1, 2 mM Ca,
Ecker model at 34 C); reversal 0 mV (excitatory) and -80 mV (inhibitory) as assumed in Ecker.
UNVERIFIED ASSUMPTIONS (free scaling factors, reported in every result):
  * SC->PYR and T->PYR g-hat = 0.6 nS (the PC->PC value; Ecker has no SC pathway); SC->interneuron g-hat = the
    PC->interneuron value of the same target.
  * contact counts N_*: one PYR stands for a population, so N synapses (each with its own resource pool) carry
    the SC drive and a single pool with weight K * g-hat carries each PYR<->interneuron projection.
  * NetCon delay 1 ms on PYR<->interneuron projections. AMPA only (no NMDA) in this pilot. tau1/tau2 = 0.5/3 ms
    (AMPA) and 0.5/8 ms (GABA_A) are placeholders.
"""
from dataclasses import dataclass, field

import numpy as np

import analysis as an
from cells import build_interneuron, build_pyr, h
from params import PATHWAYS

E_EXC, E_INH = 0.0, -80.0
G_HAT_NS = {"SC_PYR": 0.6, "T_PYR": 0.6, "SC_PV": 3.0, "SC_BiS": 1.4,
            "PYR_PV": 3.0, "PYR_BiS": 1.4, "PYR_OLM": 0.85,
            "PV_PYR": 1.75, "BiS_PYR": 2.4, "OLM_PYR": 1.3}
# STP for the tagged T pathway is that of SC->PYR (plan §2).
STP_OF = {"T_PYR": "SC_PYR", "SC_PYR_basal": "SC_PYR"}


@dataclass
class Config:
    n_sc_prox: int = 600          # SC synapses on apical prox (SR)
    n_sc_basal: int = 300         # SC synapses on basal (SO)
    n_t: int = 300                # T-pathway synapses on apical prox
    n_sc_int: int = 40            # SC synapses per interneuron
    k_pyr_int: float = 10.0       # contact scaling of each PYR -> interneuron projection
    k_int_pyr: float = 5.0        # contact scaling of each interneuron -> PYR projection
    rate_bg: float = 1.0          # Hz per SC fibre outside the volley
    rate_volley: float = 20.0     # Hz per SC fibre during the volley
    t_volley: tuple = (200.0, 500.0)
    rate_t: float = 0.0           # Hz per T fibre (0: T silent); T fires only when `t_events` is given
    t_end: float = 1000.0
    dt: float = 0.025
    seed: int = 0
    stp: bool = True              # False: static synapse, release fraction fixed at the pathway's U (tau_rec ~ 0, tau_fac 0)


def _poisson(rng, rate_bg, rate_v, win, t_end):
    out = []
    for lo, hi, r in ((0.0, win[0], rate_bg), (win[0], win[1], rate_v), (win[1], t_end, rate_bg)):
        n = rng.poisson(r * (hi - lo) / 1000.0)
        out.append(rng.uniform(lo, hi, n))
    return np.sort(np.concatenate(out))


def _stp(name, stp_on):
    p = PATHWAYS[STP_OF.get(name, name)]
    return (p.U, p.tau_rec, p.tau_fac) if stp_on else (p.U, 1e-3, 0.0)


def _syn(seg, name, stp_on, e):
    U, D, F = _stp(name, stp_on)
    s = h.TMSyn(seg)
    s.U, s.tau_rec, s.tau_fac, s.e = U, D, F, e
    if e == E_INH:
        s.tau1, s.tau2 = 0.5, 8.0
    return s


class TierB:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.rng = np.random.default_rng(cfg.seed)
        self.pyr = build_pyr()
        self.int = {k: build_interneuron(k) for k in ("pv", "bis", "olm")}
        self.keep = []                     # keep NetCons, synapses, vectors alive
        self.syn = {}                      # pathway -> list of dicts(syn, events (ms), w (uS))
        self.rec = {}
        self._build_sc()
        self._build_loops()
        self._record()

    def _add_poisson_syn(self, name, sec, n, rate, window, e, w_ns):
        for _ in range(n):
            x = float(self.rng.uniform(0.02, 0.98))
            syn = _syn(sec(x), name, self.cfg.stp, e)
            ev = _poisson(self.rng, rate[0], rate[1], window, self.cfg.t_end)
            nc = h.NetCon(None, syn)
            nc.weight[0] = w_ns * 1e-3
            self.keep += [nc, syn]
            self.syn.setdefault(name, []).append({"syn": syn, "nc": nc, "events": ev, "w": w_ns * 1e-3})

    def _build_sc(self):
        c = self.cfg
        win = c.t_volley
        self._add_poisson_syn("SC_PYR", self.pyr["prox"], c.n_sc_prox,
                              (c.rate_bg, c.rate_volley), win, E_EXC, G_HAT_NS["SC_PYR"])
        self._add_poisson_syn("SC_PYR_basal", self.pyr["basal"], c.n_sc_basal,
                              (c.rate_bg, c.rate_volley), win, E_EXC, G_HAT_NS["SC_PYR"])
        for k, name in (("pv", "SC_PV"), ("bis", "SC_BiS")):
            self._add_poisson_syn(name, self.int[k]["soma"], c.n_sc_int,
                                  (c.rate_bg, c.rate_volley), win, E_EXC, G_HAT_NS[name])
        if c.rate_t > 0:
            self._add_poisson_syn("T_PYR", self.pyr["prox"], c.n_t, (c.rate_t, c.rate_t), win,
                                  E_EXC, G_HAT_NS["T_PYR"])

    def _loop(self, name, pre_sec, post_sec, x, k, e):
        syn = _syn(post_sec(x), name, self.cfg.stp, e)
        nc = h.NetCon(pre_sec(0.5)._ref_v, syn, sec=pre_sec)
        nc.threshold, nc.delay = 0.0, 1.0
        nc.weight[0] = G_HAT_NS[name] * k * 1e-3
        self.keep += [nc, syn]
        self.syn[name] = [{"syn": syn, "nc": nc, "events": None, "w": nc.weight[0], "pre": pre_sec}]

    def _build_loops(self):
        c, P, I = self.cfg, self.pyr, self.int
        self._loop("PYR_PV", P["soma"], I["pv"]["soma"], 0.5, c.k_pyr_int, E_EXC)
        self._loop("PYR_BiS", P["soma"], I["bis"]["soma"], 0.5, c.k_pyr_int, E_EXC)
        self._loop("PYR_OLM", P["soma"], I["olm"]["soma"], 0.5, c.k_pyr_int, E_EXC)
        self._loop("PV_PYR", I["pv"]["soma"], P["soma"], 0.5, c.k_int_pyr, E_INH)
        self._loop("BiS_PYR", I["bis"]["soma"], P["prox"], 0.5, c.k_int_pyr, E_INH)
        self._loop("OLM_PYR", I["olm"]["soma"], P["dist"], 0.5, c.k_int_pyr, E_INH)

    def _record(self):
        self.rec["t"] = h.Vector(); self.rec["t"].record(h._ref_t, 0.1)
        for name, sec in (("pyr_soma", self.pyr["soma"]), ("pyr_basal", self.pyr["basal"]),
                          ("pyr_prox", self.pyr["prox"]), ("pyr_dist", self.pyr["dist"]),
                          ("pv", self.int["pv"]["soma"]), ("bis", self.int["bis"]["soma"]),
                          ("olm", self.int["olm"]["soma"])):
            v = h.Vector(); v.record(sec(0.5)._ref_v, 0.1); self.rec[name] = v
        self.spk = {}
        for name, sec in (("pyr", self.pyr["soma"]), ("pv", self.int["pv"]["soma"]),
                          ("bis", self.int["bis"]["soma"]), ("olm", self.int["olm"]["soma"])):
            tv = h.Vector(); nc = h.NetCon(sec(0.5)._ref_v, None, sec=sec); nc.threshold = 0.0
            nc.record(tv); self.spk[name] = tv; self.keep.append(nc)
        for name in ("PV_PYR", "BiS_PYR", "OLM_PYR"):
            g = h.Vector(); g.record(self.syn[name][0]["syn"]._ref_g, 0.1); self.rec["g_" + name] = g
        # one NEURON-side amp readout per pathway: the first synapse, sampled every step
        self.amp_rec = {}
        for name in ("SC_PYR", "SC_PYR_basal", "T_PYR"):
            if name in self.syn:
                a = h.Vector(); a.record(self.syn[name][0]["syn"]._ref_amp, self.cfg.dt)
                self.amp_rec[name] = a
        self.amp_t = h.Vector(); self.amp_t.record(h._ref_t, self.cfg.dt)

    def run(self):
        c = self.cfg

        def schedule():
            for lst in self.syn.values():
                for d in lst:
                    if d["events"] is not None:
                        for ts in d["events"]:
                            d["nc"].event(float(ts))
        self._fih = h.FInitializeHandler(1, schedule)
        h.cvode_active(0)
        h.dt = c.dt
        h.finitialize(-65.0)
        while h.t < c.t_end:
            h.fadvance()
        return self

    def weight_events(self):
        """Per pathway: list of (event times, release fraction u*x, effective weight w*u*x in pS) per synapse.

        Poisson-driven pathways use the recorded event list; loop pathways use the presynaptic spike times + delay.
        Release fractions come from the closed form verified against NEURON in S1; `amp_check` compares one synapse
        per pathway with the mechanism's own `amp`.
        """
        out = {}
        spk_of = {"PYR_PV": "pyr", "PYR_BiS": "pyr", "PYR_OLM": "pyr", "PV_PYR": "pv", "BiS_PYR": "bis", "OLM_PYR": "olm"}
        for name, lst in self.syn.items():
            U, D, F = _stp(name, self.cfg.stp)
            res = []
            for d in lst:
                ev = d["events"] if d["events"] is not None else np.array(self.spk[spk_of[name]]) + 1.0
                if len(ev) == 0:
                    res.append((ev, np.array([]), np.array([]))); continue
                a = an.tm_amplitudes(np.asarray(ev), U, D, F)
                res.append((np.asarray(ev), a, a * d["w"] * 1e6))     # uS -> pS
            out[name] = res
        return out

    def amp_check(self):
        """Max |NEURON amp - closed form| over the events of the first synapse of each Poisson pathway."""
        t = np.array(self.amp_t); dev = {}
        for name, vec in self.amp_rec.items():
            U, D, F = _stp(name, self.cfg.stp)
            ev = self.syn[name][0]["events"]
            if len(ev) == 0:
                continue
            a_ref = an.tm_amplitudes(ev, U, D, F)
            a_vec = np.array(vec)
            got = [a_vec[min(np.searchsorted(t, e + 2 * self.cfg.dt), len(a_vec) - 1)] for e in ev]
            dev[name] = float(np.max(np.abs(np.array(got) - a_ref)))
        return dev
