COMMENT
S0 environment check: event-driven jump plus exponential decay.
x jumps by the event weight and decays with time constant tau,
x(t) = w * exp(-(t - t_event) / tau). Exercises NET_RECEIVE, a STATE
variable with a DERIVATIVE, and state_discontinuity (CVODE-safe).
ENDCOMMENT

NEURON {
    POINT_PROCESS S0Check
    RANGE tau, x
}

PARAMETER {
    tau = 20 (ms)
}

STATE { x }

INITIAL { x = 0 }

BREAKPOINT {
    SOLVE state METHOD cnexp
}

DERIVATIVE state {
    x' = -x / tau
}

NET_RECEIVE(w) {
    state_discontinuity(x, x + w)
}
