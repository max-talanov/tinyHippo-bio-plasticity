COMMENT
Tsodyks-Markram short-term plasticity synapse with dual-exponential conductance.

Release state is updated analytically at each event (exact, independent of the
integrator). With u = utilisation, x = available resources, spike n at t_n:

    u-   = u(t_{n-1}+) * exp(-dt/tau_fac)          (0 if tau_fac = 0 or first spike)
    x-   = 1 - (1 - x(t_{n-1}+)) * exp(-dt/tau_rec)
    u+   = u- + U (1 - u-)
    amp  = u+ * x-                                  (release fraction of this event)
    x+   = x- (1 - u+)

The conductance jumps by w * amp (w from the NetCon, in uS) and follows
g(t) = B - A with A' = -A/tau1, B' = -B/tau2, normalised so a single event with
amp = 1 peaks at w (same normalisation as Exp2Syn).

All NetCons onto one TMSyn instance share one resource pool (one synapse).
Requires tau_rec > 0.
ENDCOMMENT

NEURON {
    POINT_PROCESS TMSyn
    RANGE tau1, tau2, e, U, tau_rec, tau_fac
    RANGE i, g, amp, u_last, x_last
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
}

ASSIGNED {
    v (mV)
    i (nA)
    g (uS)
    factor
    amp
    u_last
    x_last
    t_last (ms)
}

STATE { A (uS)  B (uS) }

INITIAL {
    LOCAL tp
    tp = (tau1*tau2)/(tau2 - tau1) * log(tau2/tau1)
    factor = 1 / (-exp(-tp/tau1) + exp(-tp/tau2))
    A = 0
    B = 0
    u_last = 0
    x_last = 1
    t_last = -1e9
    amp = 0
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

NET_RECEIVE(w (uS)) {
    LOCAL dt, um, xm, up
    dt = t - t_last
    if (tau_fac > 0) {
        um = u_last * exp(-dt / tau_fac)
    } else {
        um = 0
    }
    xm = 1 - (1 - x_last) * exp(-dt / tau_rec)
    up = um + U * (1 - um)
    amp = up * xm
    x_last = xm * (1 - up)
    u_last = up
    t_last = t
    state_discontinuity(A, A + w * amp * factor)
    state_discontinuity(B, B + w * amp * factor)
}
