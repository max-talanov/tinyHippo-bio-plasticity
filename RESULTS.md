# Results

Numbered log of experiments. Add a new section per result; do not rewrite older ones.
Record the commit of this repository (and of tinyHippo, for NEST comparisons) in each section.

## §1. S1: TMSyn verified against the closed-form Tsodyks–Markram solution

**Setup.** `mod/TMSyn.mod` (Tsodyks–Markram release state updated analytically at each event;
dual-exponential conductance, τ₁ = 0.5 ms, τ₂ = 3 ms, normalised to peak w per unit release).
Reference: `analysis.py` (numpy recursion; `scipy.integrate.solve_ivp` integration of the ODEs as an
independent check of the recursion; closed-form steady state for τ_fac = 0). Driver: `protocols.run_tm`.
NEURON 9.0.2; CVODE with atol = 1e-10, rtol = 1e-9; fixed step dt = 25 µs.
Spike times lie on the 25 µs grid. The conductance trace is recorded from the states A and B, because
the assigned variable `g` lags the states by one step in fixed-step mode.

**Conditions.** Three test parameter sets (**not literature values**): depressing (U 0.5, τ_rec 800 ms,
τ_fac 0), facilitating (U 0.09, τ_rec 138 ms, τ_fac 670 ms), mixed (U 0.2, τ_rec 300 ms, τ_fac 200 ms);
periodic trains of 2 and 20 pulses at 5, 20 and 50 Hz; one irregular 30-spike train (seeded exponential ISIs).
Command: `python run_s1.py`; tests: `pytest tests/test_s1_tmsyn.py` (56 tests across S0 and S1 pass).

**Worst case over all 3 × 7 conditions** (error relative to the reference; trace error relative to the peak):

| Quantity | CVODE | Fixed step | Criterion |
|---|---|---|---|
| Event amplitude `u⁺x⁻`, relative error | 8.0e-14 | 2.4e-15 | < 1% |
| Conductance trace, relative to peak | 1.9e-6 | 5.4e-9 | < 1% |
| CVODE vs fixed step, relative to peak | 1.9e-6 | | < 2% |

Reference recursion vs ODE integration: 1.6e-12 (worst case of the three sets).
Steady-state amplitude of a 40-pulse depressing train at 5, 20 and 50 Hz agrees with the closed form to < 0.1%.

**Result.** S1 passes with a large margin. The tiny amplitude errors are expected, because the release
state is updated analytically at events and does not depend on the integrator. The check therefore
verifies the implementation of the model, not its biological validity. S2 is where parameters
meet data.

**Notes for later stages.**
- Keep CVODE atol at 1e-8 or below (NEURON's default 1e-3 gives errors of several percent on small states).
- In fixed-step mode, record the states, not assigned variables computed in BREAKPOINT.
- With CVODE, `h.continuerun(t)` can return before `t`; `protocols._advance_to` steps with `fadvance` instead.
- Loading the compiled mechanisms twice in one process raises, so `nrn_setup.load_mechanisms` is idempotent.
