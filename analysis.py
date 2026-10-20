"""Reference implementations for checking the NMODL mechanisms (numpy / scipy only)."""
import numpy as np
from scipy.integrate import solve_ivp


def tm_amplitudes(spikes, U, tau_rec, tau_fac):
    """Release fraction amp_n = u+_n * x-_n of the Tsodyks-Markram model, by recursion.

    u(0) = 0, x(0) = 1. Between spikes du/dt = -u/tau_fac and dx/dt = (1-x)/tau_rec.
    At a spike u+ = u- + U(1-u-), amp = u+ x-, x+ = x- (1 - u+).
    tau_fac = 0 means no facilitation (u- = 0 at every spike).
    """
    amps = np.empty(len(spikes))
    u, x, t_prev = 0.0, 1.0, None
    for n, t in enumerate(spikes):
        if t_prev is None:
            um, xm = 0.0, 1.0
        else:
            dt = t - t_prev
            um = u * np.exp(-dt / tau_fac) if tau_fac > 0 else 0.0
            xm = 1.0 - (1.0 - x) * np.exp(-dt / tau_rec)
        up = um + U * (1.0 - um)
        amps[n] = up * xm
        x, u, t_prev = xm * (1.0 - up), up, t
    return amps


def tm_amplitudes_ode(spikes, U, tau_rec, tau_fac):
    """Independent check of tm_amplitudes: integrate the ODEs numerically, jump at spikes."""
    def rhs(_, y):
        return [-y[0] / tau_fac if tau_fac > 0 else 0.0, (1.0 - y[1]) / tau_rec]

    amps = np.empty(len(spikes))
    u, x, t_prev = 0.0, 1.0, spikes[0]
    for n, t in enumerate(spikes):
        if t > t_prev:
            sol = solve_ivp(rhs, (t_prev, t), [u, x], rtol=1e-11, atol=1e-13)
            u, x = sol.y[0, -1], sol.y[1, -1]
        if tau_fac <= 0:
            u = 0.0
        up = u + U * (1.0 - u)
        amps[n] = up * x
        x, u, t_prev = x * (1.0 - up), up, t
    return amps


def tm_steady_state_amplitude(U, tau_rec, interval):
    """Closed-form steady-state amp of a periodic train without facilitation (tau_fac = 0)."""
    e = np.exp(-interval / tau_rec)
    x_minus = (1.0 - e) / (1.0 - (1.0 - U) * e)
    return U * x_minus


def dual_exp_factor(tau1, tau2):
    """Normalisation so that a unit event of g = B - A peaks at 1 (as Exp2Syn)."""
    tp = tau1 * tau2 / (tau2 - tau1) * np.log(tau2 / tau1)
    return 1.0 / (-np.exp(-tp / tau1) + np.exp(-tp / tau2))


def tm_conductance(t, spikes, amps, w, tau1, tau2):
    """Conductance trace: superposition of dual-exponential kernels scaled by w * amp_n."""
    f = dual_exp_factor(tau1, tau2)
    g = np.zeros_like(t, dtype=float)
    for ts, a in zip(spikes, amps):
        m = t >= ts
        dt = t[m] - ts
        g[m] += w * a * f * (np.exp(-dt / tau2) - np.exp(-dt / tau1))
    return g
