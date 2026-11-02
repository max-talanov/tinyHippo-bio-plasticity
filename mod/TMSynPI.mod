COMMENT
TMSyn (Tsodyks-Markram release, dual-exponential conductance) with presynaptic GPCR inhibition of U
(downscaling mechanism #2 of hippocampal_downscaling_mechanisms.md). Release events and GABA events arrive on
NetCons to the same instance; NetCon weight[1] selects the kind (0 = release, 1 = GABA onto the terminal).

Inhibition, updated analytically at events (exact, independent of the integrator):
    D(t)   = sum over GABA events k of c * nrm * (exp(-(t-t_k)/tau_d) - exp(-(t-t_k)/tau_r))
             (nrm makes one event peak at c)
    I(t)   = i_max * (1 - exp(-D(t)))                      phasic (GABA_B-like), saturating at i_max
    U_eff  = U * (1 - i_tonic) * (1 - I(t))                i_tonic: tonic (A1R-like), constant
Release at spike n as TMSyn, with U_eff in place of U:
    u+ = u- + U_eff (1 - u-),  amp = u+ x-,  x+ = x- (1 - u+)
Every release reports u_last (= u+), xminus (= x-), ueff and iph (= I at that spike), so
    log(amp / U) = log(u+/U_eff) + log(x-) + log(1 - iph) + log(1 - i_tonic)
splits the per-spike weight into facilitation (up) and depletion, phasic and tonic inhibition (down).
Requires tau_rec > 0 and tau_d > tau_r > 0.
ENDCOMMENT

NEURON {
    POINT_PROCESS TMSynPI
    RANGE tau1, tau2, e, U, tau_rec, tau_fac
    RANGE i_tonic, i_max, c, tau_r, tau_d
    RANGE i, g, amp, u_last, x_last, xminus, ueff, iph
    NONSPECIFIC_CURRENT i
}

UNITS {
    (nA) = (nanoamp)
    (mV) = (millivolt)
    (uS) = (microsiemens)
}

PARAMETER {
    tau1    = 0.5   (ms)
    tau2    = 3     (ms)
    e       = 0     (mV)
    U       = 0.5
    tau_rec = 100   (ms)
    tau_fac = 0     (ms)
    i_tonic = 0
    i_max   = 0
    c       = 0
    tau_r   = 50    (ms)
    tau_d   = 300   (ms)
}

ASSIGNED {
    v (mV)
    i (nA)
    g (uS)
    factor
    nrm
    amp
    u_last
    x_last
    xminus
    ueff
    iph
    t_last (ms)
    dr
    dd
    t_g (ms)
}

STATE { A (uS)  B (uS) }

INITIAL {
    LOCAL tp
    tp = (tau1*tau2)/(tau2 - tau1) * log(tau2/tau1)
    factor = 1 / (-exp(-tp/tau1) + exp(-tp/tau2))
    tp = (tau_r*tau_d)/(tau_d - tau_r) * log(tau_d/tau_r)
    nrm = 1 / (exp(-tp/tau_d) - exp(-tp/tau_r))
    A = 0
    B = 0
    u_last = 0
    x_last = 1
    xminus = 1
    t_last = -1e9
    amp = 0
    ueff = U * (1 - i_tonic)
    iph = 0
    dr = 0
    dd = 0
    t_g = 0
}

BREAKPOINT {
    SOLVE state METHOD cnexp
    g = B - A
    i = g * (v - e)
}

DERIVATIVE state {
    A' = -A / tau1
    B' = -B / tau2
}

NET_RECEIVE(w (uS), kind) {
    LOCAL dt, um, xm, up
    INITIAL {
        : keep kind: without a NET_RECEIVE INITIAL block, finitialize sets weight[1] to 0
        kind = kind
    }
    : bring the inhibition drive to time t
    dd = dd * exp(-(t - t_g) / tau_d)
    dr = dr * exp(-(t - t_g) / tau_r)
    t_g = t
    if (kind == 1) {
        dd = dd + c * nrm
        dr = dr + c * nrm
    } else {
        iph = i_max * (1 - exp(-(dd - dr)))
        ueff = U * (1 - i_tonic) * (1 - iph)
        dt = t - t_last
        if (tau_fac > 0) {
            um = u_last * exp(-dt / tau_fac)
        } else {
            um = 0
        }
        xm = 1 - (1 - x_last) * exp(-dt / tau_rec)
        up = um + ueff * (1 - um)
        amp = up * xm
        xminus = xm
        x_last = xm * (1 - up)
        u_last = up
        t_last = t
        state_discontinuity(A, A + w * amp * factor)
        state_discontinuity(B, B + w * amp * factor)
    }
}
