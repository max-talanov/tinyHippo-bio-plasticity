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

## §3. S2: PPR sign test and fit identifiability on the literature parameter set

`python run_s2_lit.py` (NEURON 9.0.2 pip, Python 3.13, macOS arm64; one run, deterministic except the seeded noise, seed 0).
Parameters are from `params.py`: Ecker et al. 2019 Table 1 and the Hippocampus Hub SC page quoting Wierenga & Wadman
2003. All are **secondary-source** values (status `secondary`); SC→PYR and SC→interneuron have no stated temperature or
[Ca²⁺]ₒ; PYR→O-LM and O-LM→PYR are rat somatosensory cortex values. No real recordings were fitted.

**PPR sign test** (voltage clamp at −70 mV, EPSC2/EPSC1, ISI 20–500 ms; expected class from `params.py`):

| Pathway | Expected | PPR at 20 / 50 / 100 / 200 / 500 ms | Result |
|---|---|---|---|
| SC→PYR | facilitating | 1.517 / 1.414 / 1.282 / 1.126 / 1.008 | pass |
| SC→PV, SC→BiS (pooled interneuron fit) | facilitating | 1.617 / 1.531 / 1.411 / 1.243 / 1.045 | pass |
| PYR→PV, PYR→BiS | depressing | 0.862 / 0.801 / 0.820 / 0.859 / 0.932 | pass |
| PYR→O-LM | facilitating | 1.736 / 1.729 / 1.706 / 1.640 / 1.428 | pass |
| PV→PYR | depressing | 0.912 / 0.850 / 0.856 / 0.870 / 0.905 | pass |
| BiS→PYR | depressing | 0.960 / 0.879 / 0.881 / 0.891 / 0.917 | pass |
| O-LM→PYR | depressing | 0.704 / 0.712 / 0.723 / 0.744 / 0.799 | pass |

NEURON agrees with the closed form to 1.0e-3 relative at most. The expected classes for SC→PYR and SC→interneuron were
set to "facilitating" after computing the closed-form PPR from these parameters (see `docs/ca1_architecture_literature.md`
§3), so those three passes confirm the NEURON readout, not an independent prediction. The plan's original wording
(SC→PV depressing) is **not** supported by these numbers.

**Fit round trip** (noisy amplitudes generated from each pathway's parameters, S2 protocol of §2, 10% noise, 100
replicates, `fit_tm`). Median 95% CI half-width relative to the true value, and empirical coverage:

| Pathway | U | τ_rec | τ_fac | coverage range |
|---|---|---|---|---|
| SC→PYR | 0.15 | 0.28 | 0.23 | 91–96% |
| SC→interneuron (PV/BiS) | 0.13–0.14 | 0.27 | 0.21–0.22 | 91–97% |
| PYR→PV/BiS | 0.11 | 0.23 | 0.76–0.78 (τ_fac = 10 ms) | 94–100% |
| PYR→O-LM | 0.24 | 0.37 | 0.20 | 90–94% |
| PV→PYR | 0.10 | 0.28 | 0.72 (τ_fac = 8.6 ms) | 91–96% |
| BiS→PYR | 0.12 | 0.40 | 0.63 (τ_fac = 9.3 ms) | 91–97% |
| O-LM→PYR | 0.07 | 0.16 | **5.91** (τ_fac = 2 ms) | 80–95% |

Coverage is near nominal (SE about 2–3 points at 100 replicates), except τ_fac of O-LM→PYR (80%): when τ_fac is a few ms,
facilitation is invisible at the protocol's shortest ISI (20 ms) and τ_fac is not identifiable (median estimate 4.8 ms
against a true 2 ms, CI wider than the value). For the other depressing pathways τ_fac is also poorly bounded (CI 0.6–0.8
of the value) but is also nearly irrelevant for the output. U and τ_rec are constrained to 7–24% and 16–40%.

**Not shown.** This does not test whether the literature values describe real synapses, and no fit to experimental
amplitudes was made. S2 acceptance (targets from the literature *before* fitting, then fit with CIs) is met for the
sign test; the fit half remains open until recordings or the primary papers' amplitudes are available.

## §4. S3 pilot: Tier-B circuit activity and PYR synaptic weight profiles (PILOT, placeholder biophysics)

`python run_s3_pilot.py` (`cells.py`, `circuit.py`; NEURON 9.0.2, fixed step dt = 0.025 ms, 1 s, ≈1 s wall clock per run).
Figures: `docs/figures/s3_pilot_activity.png`, `docs/figures/s3_pilot_weights.png` (seed 0).
**What is not literature-based:** all cell biophysics (NEURON textbook `hh` soma, passive dendrites, one-compartment
interneurons that differ only in size), the SC and T conductances (0.6 nS = the PC→PC value, no CA1 SC source), SC→interneuron
conductances (taken from PC→interneuron), contact counts, NetCon delay (1 ms), AMPA-only, and the GABA_A kinetics
(0.5/8 ms). STP (U, D, F) and the PC↔interneuron peak conductances come from `params.py` / Ecker 2019 (secondary sources).
DC rheobase (500 ms, bisection): PV 16 pA, bistratified 23 pA, O-LM 28 pA, PYR 28 pA.

**Protocol.** 600 SC synapses on apical prox (SR), 300 on basal (SO), 300 T synapses (SR) at 5 Hz, 40 SC synapses on each
of PV and bistratified; every synapse has its own Tsodyks–Markram pool and an independent Poisson train: 1 Hz background,
20 Hz per fibre during a 300 ms volley (200–500 ms). PYR→interneuron projections use one pool with weight 10 × ĝ,
interneuron→PYR one pool with 5 × ĝ. No time compression.

**Spike counts in the 300 ms volley** (mean ± SD, 5 seeds; Poisson trains differ per seed, nothing else):

| Condition | PYR | PV | Bistratified | O-LM |
|---|---|---|---|---|
| STP on | 2.4 ± 0.5 | 19.0 ± 1.2 | 13.2 ± 1.1 | 2.2 ± 0.8 |
| STP off (static, release fraction = U) | 2.2 ± 0.4 | 17.4 ± 0.5 | 8.8 ± 1.3 | 1.6 ± 0.5 |

STP changes the PYR count by 0.2 spikes (within one SD), so no PYR effect can be claimed. Bistratified fires about 50% more
with STP on, consistent with the facilitating SC→interneuron fit, but the SC→interneuron parameters are the pooled fit
and 5 seeds with SD ≈ 1 is a small sample. Doubling the SC contact count lowered PYR spikes from 2 to 1 (3 seeds, not tabulated);
the cause was not examined (depolarization block of the placeholder soma or stronger feedforward inhibition are candidates),
so the drive level was not tuned upward.

**Effective weight w·u·x (pS) per release event, seed 0** (w·U, the static-control level, is 84 pS for the three excitatory pathways):

| Pathway | w (pS) | n synapses | events | pre-volley | first 50 ms of volley | last 50 ms | last / first |
|---|---|---|---|---|---|---|---|
| SC → PYR apical prox | 600 | 600 | 3922 | 87.1 | 102.7 | 95.5 | 0.93 |
| SC → PYR basal | 600 | 300 | 2048 | 89.9 | 104.6 | 94.2 | 0.90 |
| T → PYR apical prox (5 Hz) | 600 | 300 | 1512 | 97.2 | 100.1 | 105.5 | 1.05 |
| PV → PYR soma | 8750 | 1 | 28 | none | 1269 | 166 | 0.13 |
| BiS → PYR apical prox | 12000 | 1 | 12 | none | 1478 | 434 | 0.29 |
| O-LM → PYR apical dist | 6500 | 1 | 1 | none | 1950 | n/a | n/a |

Excitatory SC and T weights stay within about ±20% of w·U (population mean; SD in the figure): facilitation at low per-synapse
rates (1–20 Hz Poisson) and mild depression at the end of the volley. Inhibitory weights depress strongly, to 13% (PV)
and 29% (bistratified) of their first-event value within the volley, so the inhibition that the PYR receives decays as
the volley proceeds. The release fraction in NEURON (`TMSyn.amp`) equals the closed form used for these profiles to
< 3e-17 for the first synapse of each excitatory pathway. Single synapse pools make the inhibitory profiles per-event
values of one pool, not an average over contacts. The PV firing after the volley (550–880 ms) is Poisson-driven
background with strong placeholder conductances (3 nS × 40 synapses); it was not examined further. PYR dendrites have no
voltage-gated channels, so their "spikes" are the passive spread of the somatic action potential.

## §5. S3a: single-synapse balance map (up- vs downscaling inside STP)

`python run_s3a.py` (NEURON 9.0.2 `TMSyn`, CVODE, release read from `TMSyn.amp`; deterministic, no seeds).
Data: `results/s3a_balance.csv` (693 trains); figure: `docs/figures/s3a_balance_map.png`.
Parameters: the 9 pathways of `params.py`, all **secondary-source** values (§3); so every number below is provisional.
No time compression. Protocol: periodic trains at 25 rates from 1 to 300 Hz (13 rates for the other `U` gains), spike
times snapped to the 0.025 ms grid, length 8 × max(τ_rec, τ_fac) + 20 pulses so that the steady state is reached.
Balance index `B(f) = R_ss(f)/U`, with `R_ss` the release fraction of the last pulse; `B > 1` net upscaling, `B < 1` net
downscaling; `f*` where `B` crosses 1 downwards (log-linear interpolation).

**Check against the reference.** NEURON vs the closed form on the identical spike times: max relative difference 3.0e-11
over all 693 trains (criterion < 1e-2). Voltage-clamp EPSC amplitude (peak minus pre-pulse current) vs
`w · 70 mV · release` at 5 and 20 Hz, all 9 pathways: max deviation 1.3e-4. Above ~20 Hz the EPSCs overlap, so release is read
from the mechanism, not from the clamp current.

| Pathway | B at 1 / 5 / 20 / 80 / 200 / 300 Hz | max B (at) | f* (Hz) | Class |
|---|---|---|---|---|
| SC → PYR | 1.00 / 1.13 / 1.11 / 0.49 / 0.20 / 0.13 | 1.25 (10.8 Hz) | 27.5 | up, then down |
| SC → interneuron (pooled; PV and BiS) | 1.00 / 1.26 / 1.02 / 0.39 / 0.16 / 0.10 | 1.34 (8.5 Hz) | 22.6 | up, then down |
| PYR → PV, BiS | 0.98 / 0.72 / 0.34 / 0.13 / 0.06 / 0.03 | 0.98 (1 Hz) | none | down only |
| PYR → O-LM | 1.26 / 2.90 / 2.63 / 1.04 / 0.42 / 0.27 | 3.32 (10.8 Hz) | 75.7 | up, then down |
| PV → PYR | 0.92 / 0.58 / 0.23 / 0.08 / 0.03 / 0.02 | 0.92 (1 Hz) | none | down only |
| BiS → PYR | 0.92 / 0.59 / 0.24 / 0.09 / 0.04 / 0.02 | 0.92 (1 Hz) | none | down only |
| O-LM → PYR | 0.80 / 0.35 / 0.11 / 0.04 / 0.01 / 0.01 | 0.80 (1 Hz) | none | down only |

`f*` from the NEURON points agrees with the dense closed-form `f*` (27.5, 22.6, 75.4 Hz). The hypotheses of
`docs/replan_stp_balance.md` §5 that this stage tests:
- **H1 confirmed** (for these parameters): SC → PYR is net upscaling at about 3–27 Hz and net downscaling above `f* = 27.5 Hz`.
- **H2 confirmed**: PYR → PV/BiS and all interneuron → PYR pathways have `B < 1` at every rate (even at 1 Hz for those with τ_rec ≥ 410 ms).
- **H4 confirmed at the single-synapse level**: a `U` gain (0.5–1.5) moves `f*` for SC → PYR from 66 to 14 Hz, and at 5–20 Hz
  it changes the absolute release (`R_ss(5 Hz)` 0.079–0.219), but at 80 Hz `R_ss` varies only 0.066–0.070 and at 200 Hz it is
  0.028 for every gain: ripple-rate release is set by τ_rec, not `U`. A presynaptic-inhibition or [Ca²⁺]ₒ change would therefore
  act on transmission at theta and gamma rates and almost not at ripple rates. (The `R_ss(5/20 Hz)` columns for gains ≠ 1 are
  taken at the nearest of 13 grid rates, not exactly at 5 and 20 Hz.)

**Not shown.** This is the per-synapse steady state of a deterministic release model; stochastic release, a mixed rate
history and the circuit (rates set by the cells, E/I balance) are S3c. The sign and size of every `B(f)` depend on the
secondary-source parameters; the main uncertainty is the pooled SC → interneuron fit and the cortical O-LM values.
