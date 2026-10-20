"""Simulation protocols. S1: drive one TMSyn with a given spike train."""
import numpy as np

from nrn_setup import load_mechanisms

h = load_mechanisms()
h.load_file("stdrun.hoc")

DT_FIXED = 0.025        # ms, fixed-step reference
CVODE_ATOL = 1e-10      # NEURON's default (1e-3) is too coarse for small state variables
REC_DT = 0.1            # ms, sampling interval of recorded traces


def _advance_to(t_target):
    """Step until h.t >= t_target. (continuerun can return early in variable-step mode.)"""
    while h.t < t_target:
        h.fadvance()


def run_tm(spikes, U, tau_rec, tau_fac, w=1e-3, tau1=0.5, tau2=3.0, cvode=True, tail=50.0):
    """Drive a TMSyn with `spikes` (ms). Returns (amps, t, g).

    amps: release fraction of each event, read from the mechanism right after each event.
    t, g: conductance trace (uS) sampled every REC_DT.
    """
    soma = h.Section(name="soma")
    soma.L = soma.diam = 20.0
    soma.insert("pas")
    syn = h.TMSyn(soma(0.5))
    syn.U, syn.tau_rec, syn.tau_fac, syn.tau1, syn.tau2 = U, tau_rec, tau_fac, tau1, tau2
    nc = h.NetCon(None, syn)
    nc.weight[0] = w

    def schedule():
        for ts in spikes:
            nc.event(float(ts))

    fih = h.FInitializeHandler(1, schedule)      # keep a reference alive

    # Record the states A and B, not the assigned variable g: in fixed-step mode an
    # assigned variable computed in BREAKPOINT lags the states by one step.
    tv, av, bv = h.Vector(), h.Vector(), h.Vector()
    tv.record(h._ref_t, REC_DT)
    av.record(syn._ref_A, REC_DT)
    bv.record(syn._ref_B, REC_DT)

    cv = h.CVode()
    if cvode:
        cv.active(1)
        cv.atol(CVODE_ATOL)
        cv.rtol(1e-9)
    else:
        cv.active(0)
        h.dt = DT_FIXED
    h.finitialize(-65.0)
    amps = []
    for ts in spikes:
        _advance_to(float(ts) + 2 * DT_FIXED)   # events are delivered at the start of a step
        amps.append(syn.amp)
    _advance_to(float(spikes[-1]) + tail)
    t_arr = np.array(tv)
    keep = t_arr <= float(spikes[-1]) + tail + 1e-9      # fadvance may overshoot by one step
    out = (np.array(amps), t_arr[keep], (np.array(bv) - np.array(av))[keep])
    # Release everything so that no stale section, synapse or init handler leaks into the next run.
    for vec in (tv, av, bv):
        vec.play_remove()
    fih = nc = syn = None
    h.delete_section(sec=soma)
    return out
