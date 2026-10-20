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

## §2. S2 (partial): STP readout and fitting machinery; literature targets not yet available

**Status: the S2 pass criterion is not yet met.** It requires the pathway classes and parameters from the
literature *before* fitting. The full texts could not be fetched (the session's network policy blocks
pmc.ncbi.nlm.nih.gov, biorxiv.org and europepmc.org), and no parameter value has been entered from memory.
What is in place:

**1. Literature status (`params.py`).** Only abstract-level classes are known, from Losonczy, Zhang, Shigemoto,
Somogyi & Nusser (2002, *J Physiol* 542:193–210, mouse hippocampal interneurons): about 75% of O-LM cells
facilitating (3 of 12 also depressing); 8 of 12 basket cells depression-only; O-Bi cells 2/9 facilitating,
2/9 depressing, 5/9 combined. The stimulated afferents, recording conditions and fitted numbers are not yet
read. `SC → PYR` has no source at all. Every pathway in `params.py` carries status `abstract` or `unverified`,
and all `U, τ_rec, τ_fac` are `None`. Markram et al. 1998 is neocortical, so it is not a CA1 source.

**2. Readout** (`protocols.run_clamped`, `protocols.epsc_amplitudes`). A somatic voltage clamp at −70 mV
(series resistance 0.01 MΩ) records the EPSC of one `TMSyn`; amplitude = peak minus the current just before
the pulse, as in an experiment. Against the release fraction from S1 it agrees to < 0.5% for all three fixture
sets over paired pulses at 20–500 ms and 5–50 Hz trains (`tests/test_s2_fit.py`).

**3. Fit** (`analysis.fit_tm`). Least squares of (A, U, τ_rec, τ_fac) to normalised EPSC amplitudes with
relative residuals, multi-start, 95% CI from the Jacobian. Protocol: paired pulses at ISI 20, 50, 100, 200, 500 ms
and 10-pulse trains at 5, 10, 20, 50 Hz (9 independent trials, 50 amplitudes).
- Noise-free data from the NEURON clamp: facilitating and mixed fixture sets are recovered to < 2% in all four parameters.
- Synthetic data with 10% amplitude noise (100 replicates, analytic amplitudes): empirical coverage of the nominal 95% CI

| Set | A | U | τ_rec | τ_fac |
|---|---|---|---|---|
| facilitating | 94% | 95% | 95% | 96% |
| mixed | 90% | 93% | 91% | 91% |

  With 100 replicates the standard error of a coverage estimate is about 2–3 points, so coverage is close to
  nominal. Median CI half-widths relative to the true value: facilitating U 0.23, τ_rec 0.39, τ_fac 0.22; mixed U 0.10, τ_rec 0.16, τ_fac 0.25.
  Parameters are not tightly constrained by 50 amplitudes at 10% noise, which matters for how much weight a
  fit to real recordings can carry. For a purely depressing synapse τ_fac is not identifiable (not tested here).

**4. PPR signature** (`python run_s2.py`, NEURON clamp, fixture sets, not literature values):

| Set | ISI 20 ms | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| depressing | 0.512 | 0.530 | 0.559 | 0.611 | 0.732 |
| facilitating | 1.736 | 1.729 | 1.706 | 1.640 | 1.428 |
| mixed | 1.401 | 1.348 | 1.272 | 1.161 | 1.025 |

The sign of PPR − 1 classifies the depressing and facilitating sets correctly. The "mixed" set (U 0.2, τ_rec 300 ms,
τ_fac 200 ms) is facilitating by PPR at every ISI: a combined facilitating-depressing synapse cannot be told
apart from a facilitating one by PPR alone and needs the train data.

**Next (needs input).** Read the full texts (Losonczy 2002 and a CA1 Schaffer-collateral source), enter their
numbers in `params.py` with conditions, then run the PPR check per pathway and fit. This needs either the
hosts above added to the environment's allowed domains, or the papers (or their parameter tables) supplied directly.
