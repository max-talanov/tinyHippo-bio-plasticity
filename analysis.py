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


# ---------------------------------------------------------------- S2: fitting TM parameters
def tm_model_amplitudes(theta, trials):
    """Concatenated model amplitudes A * u+ x- for a list of spike trains; theta = (A, U, tau_rec, tau_fac)."""
    A, U, tau_rec, tau_fac = theta
    return np.concatenate([A * tm_amplitudes(sp, U, tau_rec, tau_fac) for sp in trials])


def fit_tm(trials, observed, starts=None, rel_sigma=None):
    """Least-squares fit of (A, U, tau_rec, tau_fac) to observed EPSC amplitudes.

    trials: list of spike-time arrays (ms); observed: matching list of amplitude arrays.
    Residuals are relative ((obs - model) / obs), i.e. a constant coefficient of variation.
    Returns dict with theta, 95% CI (from the Jacobian; NaN if the Hessian is singular),
    correlation matrix, and the residual coefficient of variation.
    Several starting points are tried and the best cost wins (the surface has local minima).
    """
    from scipy.optimize import least_squares

    obs = np.concatenate([np.asarray(o, float) for o in observed])
    scale = np.median(obs)
    lo = np.array([1e-3 * scale, 0.01, 10.0, 1.0])
    hi = np.array([1e3 * scale, 0.99, 5000.0, 5000.0])
    if starts is None:
        starts = [(scale / u, u, tr, tf) for u in (0.1, 0.3, 0.6) for tr in (100.0, 500.0, 1500.0)
                  for tf in (5.0, 200.0, 1000.0)]

    def resid(th):
        return (obs - tm_model_amplitudes(th, trials)) / obs

    best = None
    for s0 in starts:
        s0 = np.clip(s0, lo * 1.001, hi * 0.999)
        r = least_squares(resid, s0, bounds=(lo, hi), x_scale=[scale, 0.3, 300.0, 300.0])
        if best is None or r.cost < best.cost:
            best = r
    n, p = len(obs), 4
    dof = max(n - p, 1)
    s2 = 2.0 * best.cost / dof
    try:
        cov = s2 * np.linalg.inv(best.jac.T @ best.jac)
        se = np.sqrt(np.diag(cov))
        from scipy.stats import t as student
        ci = student.ppf(0.975, dof) * se
        corr = cov / np.outer(se, se)
    except np.linalg.LinAlgError:
        se = ci = np.full(p, np.nan)
        corr = np.full((p, p), np.nan)
    return dict(theta=best.x, ci95=ci, corr=corr, cv=float(np.sqrt(s2)), cost=best.cost)
