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
DC rheobase (500 ms, bisection): PV 16 pA, bistratified 23 pA, O-LM 28 pA, PYR ≈ 94 pA.
**Correction (2026-10-28):** this section first stated PYR 28 pA. That value was measured on a soma-only cell: `cells.rheobase(build_pyr()["soma"])` kept only the soma in Python, so NEURON deleted the unreferenced dendrite sections, and the value coincided with O-LM's. The circuit runs themselves kept the dendrites (`TierB.pyr`) and are not affected. With dendrites the PYR rheobase is 92.8 pA (400 ms step, `calibrate.py`) or ≈ 94 pA (500 ms).

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

## §6. S3b: calibration of the four cells to the Bezaire intrinsic-property targets

`python run_s3b.py fit <PYR|PV|BiS|OLM>` (`calibrate.py`, `run_s3b.py`; results in `results/s3b_<cell>.json`). Targets:
`params.CELL_TARGETS` (Bezaire et al. 2016 Appendix 1 table 1, mouse, Soltesz lab whole-cell; T and [Ca²⁺]ₒ not read;
secondary status). Features as defined there: input resistance from a small hyperpolarising step (here −10 pA, not the
least hyperpolarised level of a 50 pA grid), membrane τ from a single-exponential fit of the step response, rheobase =
least depolarising current giving a spike during a 400 ms step (bisection, 1 pA tolerance; the experimental rheobase is
quantised by a 50 pA grid), resting potential. Fixed step dt = 0.025 ms, deterministic.

**Scoring** (`calibrate.residuals`): residual = ln(measured/target mean) / max(relative SD, 10%) for Rin, τ and rheobase;
(RMP − target) / max(SD, 2 mV) for the resting potential; fixed penalty 10 if the cell does not spike up to 1 nA. A
residual of 1 is about one experimental SD (floored at 10% of the mean, which matters for O-LM rheobase 20 ± 0 pA and
bistratified τ 12.2 ± 0.6 ms). Least squares (`scipy.optimize.least_squares`, bounds, `diff_step` 0.05), 4 free parameters
per interneuron (lumped soma size, leak, Na/K scale, hh leak reversal) and 6 for the PYR (dendritic leak, dendritic
diameter scale, soma Na/K scale, soma leak, dendritic and soma leak reversals); two starts for interneurons (the
placeholder values, and values derived from the targets), best kept.

| Cell | RMP mV (target) | Rin MΩ (target) | τ_m ms (target) | Rheobase pA (target) | residuals [Rin, τ, rheo, RMP] | sum sq |
|---|---|---|---|---|---|---|
| PYR | −70.7 (−70.7) | 140.6 (139.5) | 21.1 (21.5) | 183.6 (182.4) | 0.03, −0.04, 0.02, −0.01 | 0.00 |
| Bistratified | −65.3 (−63.6) | 110.7 (109.1) | 12.2 (12.2) | 334.5 (333.3) | 0.05, −0.03, 0.02, −0.37 | 0.14 |
| PV basket | −64.9 (−61.4) | 72.4 (65.2) | 8.2 (13.3) | 361.3 (307.1) | 0.42, −1.18, 0.46, −1.74 | 4.81 |
| O-LM | −67.2 (−64.8) | 868 (592) | 20.8 (41.4) | 22.5 (20.0) | 2.34, −2.44, 1.16, −1.21 | 14.23 |

Before: the placeholder cells had rheobase 93 / 16 / 23 / 28 pA (PYR / PV / BiS / O-LM) and τ_m 0.5–1.3 ms
(`run_s3b.py` baseline). The PYR and bistratified cells now match all four features within 0.4 tolerance units. **PV and
O-LM do not**: both starts converged to the same residuals, so a one-compartment `hh` cell cannot match τ_m, Rin and
rheobase together for them (O-LM Rin 868 vs 592 MΩ and τ_m 21 vs 41 ms with rheobase 22.5 pA). For comparison, Bezaire's own
O-LM model has Rin 344 MΩ, τ 22.4 ms and rheobase 50 pA (their Table 3), i.e. it also does not reproduce the data.

**What this is not.** The fitted values are effective lumped parameters, not measured channel densities: the interneuron
somata come out at 67–73 µm (they lump the dendrites), leak reversals at −47 to −58 mV (bistratified hits the −40 mV bound),
PYR dendritic leak 2e-6 S/cm². Four features do not constrain the firing pattern: the f–I curve, spike shape, adaptation
and the response to synaptic input are not checked. The mouse data are compared with parameters later used with rat
synaptic data. The calibrated cells are **not yet used** by `circuit.py` (the S3 pilot of §4 still has the placeholder
cells), so §4 is unchanged.

## §7. S3b: interneurons with the Bezaire 2016 dendritic morphology

`python run_s3b.py fit <PV|BiS|OLM>` (now the default for interneurons; `fit <cell> point` reproduces §6); results in
`results/s3b_<cell>_dend.json`. Morphology `cells.IN_MORPH`, taken from the Bezaire et al. 2016 model code
(github.com/mbezaire/ca1, commit a8655fa, `cells/class_pvbasketcell.hoc`, `class_bistratifiedcell.hoc`,
`class_olmcell.hoc`; status: model value, simplified, not a reconstruction):
- PV basket and bistratified (one morphology in that code): soma 20 × 10 µm, two apical trees of five sections (600 µm,
  diameter 4 → 1 µm) and two basal trees of three sections (300 µm, 2 → 1 µm); cm 1.4 µF/cm², Ra 100 Ω cm.
- O-LM: soma 20 × 10 µm, two dendrites of 250 µm × 3 µm, axon stub 150 µm × 1.5 µm; cm 1.3 µF/cm², Ra 150 Ω cm.

Channels are **not** Bezaire's: `hh` in the soma, passive dendrites and axon (Bezaire has Na and K in the dendrites of all
three cells and HCN in the O-LM soma). Seven free parameters: dendritic leak, dendrite diameter scale (bounded 0.5–2, so the
morphology stays near the source), soma Na and K scales (separate), soma leak, dendritic and soma leak reversals. Rheobase
searched up to 3 nA. Two starts: dendritic leak from g = 1/(Rin × membrane area) with Na/K scale 1 and 0.1. Scoring as §6.

The membrane area alone almost gives the passive targets: with cm from the source, C = 167 pF (PV/BiS morphology) and
79 pF (O-LM), against τ/Rin = 204 pF (PV), 112 pF (BiS) and 70 pF (O-LM) in the data. A first run with one shared Na/K
scale fitted the bistratified cell but not PV (rheobase 913 pA) or O-LM (no spike up to 1 nA, flat penalty); separating
the Na and K scales and widening the rheobase search fixed PV.

| Cell | RMP mV (target) | Rin MΩ (target) | τ_m ms (target) | Rheobase pA (target) | residuals [Rin, τ, rheo, RMP] | sum sq | §6 one-compartment |
|---|---|---|---|---|---|---|---|
| PV basket | −61.4 (−61.4) | 65.2 (65.2) | 13.3 (13.3) | 306.9 (307.1) | 0.00, 0.00, 0.00, 0.00 | 0.00 | 4.81 |
| Bistratified | −64.5 (−63.6) | 107.7 (109.1) | 12.2 (12.2) | 332.9 (333.3) | −0.05, 0.01, −0.01, −0.19 | 0.04 | 0.14 |
| O-LM | −64.9 (−64.8) | 850 (592) | 63.3 (41.4) | 22.0 (20.0) | 2.20, 1.50, 0.94, −0.06 | 7.99 | 14.23 |

Fitted values: PV dendrite diameter scale 1.22, Na 1.67 × and K 0.30 × the `hh` default, soma leak 4.4e-4 S/cm² with
reversal −82 mV (a K-like resting conductance); bistratified scale 0.84, Na 1.0 ×, K 0.62 ×; O-LM scale 1.01, Na 0.97 ×,
K 0.27 ×. PV and bistratified now match all four features **with a sourced morphology and no lumped soma**. O-LM still
misses Rin and τ (1.5–2.2 tolerance units): with a 20 pA rheobase the cell must be 12 mV from threshold at Rin 592 MΩ, and
the fit trades Rin up to reach threshold. The missing mechanism is probably Ih, which lowers Rin and τ near rest; Bezaire's O-LM has
HCN (`gH` 5e-4 S/cm²) and the experimental O-LM Rin is taken at a step where Ih is active. Not tested.

**Temperature.** No script sets `h.celsius`, so every simulation so far runs at NEURON's default 6.3 °C, where `hh`
(squid axon kinetics) is calibrated. Bezaire's model runs at 34 °C. Rin, τ and RMP do not depend on it much; rheobase and
everything spike-timing related do. This affects the PYR of §6, these cells and the S3 pilot of §4.

Not checked: f–I curve, spike shape, adaptation, synaptic responses. `circuit.py` still uses the point placeholder
interneurons (default `INParams.morph = "point"`), so §4 is unchanged.

## §8. S3b: Bezaire 2016 channels at 34 °C, verified port, refit, and O-LM HCN

**Port.** The 13 channel files of the Bezaire et al. 2016 model (github.com/mbezaire/ca1, commit a8655fa, CC0) are in
`mod/` unchanged (`mod/BEZAIRE_CHANNELS.md`); `cells.build_bezaire_interneuron` rebuilds the PV basket, bistratified and
O-LM templates in Python (`cells.BEZ_CHANNELS`, `IN_MORPH`), 34 °C. **Verified** against the original hoc templates
(`reference/bezaire2016/`, `tests/test_s3b_bezaire_cells.py`, −50 pA and +500 pA steps): O-LM agrees to 2e-10 mV, PV and
bistratified to 3e-8 mV subthreshold and 2e-3 / 7e-4 mV during spiking, with equal spike counts; with the template's own
section lengths copied in the residual drops to 6e-11 mV, so it is geometry rounding of the 3-D points.
Facts of the published templates that the port reproduces (found by running them):
- PV and bistratified do not insert `iconc_Ca` (Ca²⁺ is not accumulated; cai = 5e-5 mM, eca fixed at 171 mV);
- O-LM sets neither `ena`/`ek` (NEURON defaults 50 / −77 mV) nor `eh`: its HCN runs at **eh = 0 mV**, although
  `ch_HCNolm.mod` declares −32.9 mV from Maccaferri & McBain 1996 (now `params.CHANNEL_PARAMS["OLM_eh"]`, secondary);
- `nseg` is computed before Ra and cm are set (with NEURON's defaults).

**Settling.** The O-LM HCN time constant at rest is about 2.6 s (from the mod file's rate; 2.8 ± 0.8 s at −70 mV
quoted from Maccaferri & McBain). Measured 50 ms after initialisation (the §6–§7 protocol), the published O-LM gives Rin
334 MΩ; settled, 227 MΩ. `calibrate.measure(settle_ms=...)` now runs the cell for that long at zero current with a 10 ms
step (as Bezaire's presimulation; the features agree with a 0.025 ms settle to within 0.02%), saves the state and
starts every recording from it. All §8 numbers use 20 s.

**Published cells, measured** (no fitting; O-LM with eh = −32.9 mV, the §8 choice; with eh = 0 as published: RMP
−67.2, Rin 227, τ 27.8, rheobase 30.8):

| Cell | RMP mV (target) | Rin MΩ (target) | τ_m ms (target) | Rheobase pA (target) | residuals [Rin, τ, rheo, RMP] |
|---|---|---|---|---|---|
| PV basket | −65.0 (−61.4) | 52.2 (65.2) | 7.0 (13.3) | 289 (307) | −0.90, −1.58, −0.17, −1.81 |
| Bistratified | −67.0 (−63.6) | 98.9 (109.1) | 14.7 (12.2) | 313 (333) | −0.35, 1.85, −0.35, −0.73 |
| O-LM | −70.1 (−64.8) | 200 (592) | 19.4 (41.4) | 44.7 (20.0) | −6.62, −2.68, 8.04, −2.65 |

**Refit** (`python run_s3b.py fit <cell> bez`; `results/s3b_<cell>_bez.json`): scales on the published leak, Na and fast
K (`ch_Kdrfast`) densities, dendrite diameter scale (0.5–2), leak reversal; O-LM also the HCN scale. Start = the
published cell. Other channels (A-type K, Ca, KCa) unchanged.

| Cell | RMP | Rin | τ_m | Rheobase | residuals | fitted scales (leak, diam, Na, K[, HCN]), e_leak |
|---|---|---|---|---|---|---|
| PV basket | −62.5 | 54.6 | 10.3 | 202 | −0.72, −0.64, −1.17, −0.56 | 0.72, 1.30, 1.03, **0.155**; −62.5 mV |
| Bistratified | −65.3 | 95.5 | 12.2 | 315 | −0.48, 0.02, −0.33, −0.37 | 1.18, 0.89, 1.00, 1.01; −65.3 mV |
| O-LM with HCN | −65.3 | 340 | 27.3 | 16.8 | −3.39, −1.47, −1.72, −0.23 | 0.40, **0.60**, 1.53, **0.10**, 1.79; −56.3 mV |
| O-LM, HCN removed | −66.3 | 348 | 31.3 | 16.8 | −3.24, −0.99, −1.72, −0.75 | 2.86, **0.59**, 3.63, 1.00; −43.6 mV |

**Firing (f–I, Hz in a 400 ms step at 0.3 / 0.5 / 1 / 2 nA), not a fit target:**

| Cell | published | fitted |
|---|---|---|
| PV basket | 8 / 48 / 98 / 162 | 35 / 65 / 108 / 118 |
| Bistratified | 0 / 42 / 90 / 158 | 0 / 50 / 100 / 172 |
| O-LM (eh −32.9) | 80 / 122 / 195 / 2 | 132 / 180 / **8** / 2 |

What this shows:
- **Bistratified**: the refit moves every scale by < 20% and keeps the f–I curve; all four features within 0.5
  tolerance units. Usable.
- **PV**: the four-feature fit improves (sum sq 6.6 → 2.6) only by cutting the fast delayed rectifier to 15%, and the
  f–I curve then saturates (118 vs 162 Hz at 2 nA). PV basket cells are fast-spiking through high Kv3-type K
  conductance (textbook, not read here), so this fit is less bio-plausible than the published cell, which is within
  1.8 tolerance units on every feature.
- **O-LM**: neither the published cell nor any fit within the bounds reaches Rin 592 MΩ (best 340–348), and the fits
  press the dendrite diameter onto its lower bound and enter depolarisation block at 1 nA. **HCN does not help the four
  features**: with and without it the fits are about equally good (sum sq 16.7 vs 15.0); the §7 guess that missing Ih
  explained the O-LM misfit is not supported. HCN at −32.9 mV is still the bio-plausible choice for sag, rebound and
  slow pacemaking, which these four features do not test. The O-LM target is weak: n = 3, rheobase 20 ± 0 pA on a 50 pA grid.
- Four static features do not constrain a cell with this many channels: two of the three fits trade firing behaviour for feature
  agreement. A firing target (f–I curve, or the spike-train features of Migliore 2018 / HippoUnit) is needed before
  fitting further.

Temperature: the interneurons are now at 34 °C; `build_bezaire_interneuron` sets `h.celsius` globally. The PYR of §6
(`hh`) was fitted at 6.3 °C and becomes a different cell at 34 °C, so it must be revisited before the circuit uses both.
`circuit.py` is unchanged (point placeholders).

## §9. S3b: firing target, chosen interneurons, and the pyramidal cell at 34 °C

Project owner's decision (2026-10-29): the circuit uses the published PV basket cell, the published O-LM cell with
eh −32.9 mV (`params.CHANNEL_PARAMS["OLM_eh"]`), and the bistratified refit of §8 (`cells.TIER_B_IN`).

**Firing target.** From Bezaire 2016 Appendix 1 table 1 (mouse): ISI, threshold, spike amplitude, AHP and sag
(`params.CELL_TARGETS`, fields `isi_ms` … `sag_mv`), with each cell type's current-step grid from table 2. Measured by
`calibrate.firing`. Assumptions, because the paper does not state them:
- ISI: mean ISI at the lowest grid level that gives ≥ 2 spikes in the step; threshold, amplitude and AHP are from the first 3 spikes.
- Threshold: dV/dt = 28 mV/ms for all cells. The paper uses this "method #2" for interneurons but method #1 for
  pyramidal cells.
- Step 400 ms. **The step duration is not stated, and the ISI depends strongly on it:** at 1000 ms PV gives 150 instead
  of 110 ms, and O-LM gives 144 ms at 50 pA instead of 48 ms at 80 pA. Bistratified barely changes (34 vs 33 ms). The ISI target is
  therefore only as good as the guessed protocol; ± is not stated to be SD.
- Sag: at the most hyperpolarised grid level.
ISI is a fit residual (5th, after Rin, τ, rheobase, RMP); threshold, amplitude, AHP and sag are checks only.

**Chosen interneurons, settled 20 s, 34 °C (target in parentheses):**

| Cell | ISI ms | threshold mV | amplitude mV | AHP mV | sag mV | residuals Rin, τ, rheo, RMP, ISI |
|---|---|---|---|---|---|---|
| PV basket (published) | 110 (74 ± 36) | −31.7 (−35.3) | 85.0 (51.1) | 45.5 (18.0) | 0 (1.8) | −0.90, −1.58, −0.17, −1.81, 0.81 |
| Bistratified (refit) | 33 (25 ± 22) | −19.0 (−31.9) | 42.0 (47.3) | 57.3 (22.6) | — | −0.48, 0.02, −0.33, −0.37, 0.34 |
| O-LM (published, eh −32.9) | 48 @ 80 pA (102 ± 30) | −29.4 (−44.2) | 33.3 (76.3) | 42.3 (22.1) | 14.1 (10.4) | −6.62, −2.68, 8.04, −2.65, −2.56 |

The spike shapes miss widely (AHP ≈ 2× in all three; BiS and O-LM thresholds 13–15 mV too depolarised). None of these was fitted.

**Pyramidal cell at 34 °C.** The `hh` PYR of §6 (6.3 °C) is replaced by Bezaire's `poolosyncell` (Poolos 2002-based,
202 sections, 1104 segments), loaded from `reference/bezaire2016/class_poolosyncell.hoc` by `cells.build_bezaire_pyr`,
with channels `ch_Navp/ch_Navaxonp/ch_Kdrp/ch_KvAproxp/ch_KvAdistp/ch_HCNp` (`mod/`). The fit has 6 parameters: scales on leak, Na, Kdr, HCN, KA
and e_pas. Bounds 0.1–10 and −90…−50 mV; 154 evaluations; `run_s3b.py fit PYR bez` → `results/s3b_PYR_bez.json`.

| PYR | RMP | Rin MΩ | τ ms | rheo pA | ISI ms | thr mV | amp mV | AHP mV | sag mV | sum sq |
|---|---|---|---|---|---|---|---|---|---|---|
| target | −70.7 ± 1.2 | 139.5 ± 38.8 | 21.5 ± 8.6 | 182 ± 56 | 134 ± 44 | −36.7 ± 2.6 | 78.2 ± 7.2 | 8.6 ± 2.1 | 7.0 ± 2.2 | |
| published | −63.0 | 70.6 | 5.7 | 240 | 74 | −37.3 | 77.4 | 16.9 | 6.6 | 36.2 |
| refit | −71.5 | 129.4 | 15.1 | 248 | 129 | −35.7 | 65.6 | 16.6 | 4.8 | 2.0 |

Refit scales: leak 0.30, Na 0.69, Kdr 1.46, **HCN 0.10**, KA 1.57, e_pas −75.2 mV. The published values match
Bezaire's own Table 3 model (62.2 MΩ, 4.8 ms, −63 mV, 250 pA), which confirms the port.

f–I (spikes in 400 ms at 250 / 300 / 400 / 500 / 700 / 1000 / 1500 pA): published 5/10/15/19/26/9/3, refit
3/9/15/19/27/17/3. Both are regular up to 700 pA (≈ 67 Hz) and enter **depolarisation block at ≥ 1 nA**. This comes
from the template, not from the refit.

What this shows:
- The refit improves every passive feature and the ISI (sum sq 36 → 2.0), keeps the f–I curve, and leaves threshold
  in range. Spike amplitude drops by 1.7 SD (Na × 0.69). AHP stays ≈ 2× the target, as in the published cell.
- It reaches the high Rin by cutting HCN to 10% and leak to 30%. CA1 pyramidal cells have a strong dendritic Ih
  gradient (textbook, not read here), and Ih shapes EPSP summation, which matters for plasticity, so the HCN cut needs
  checking. Sag (4.8 mV) is still within 1 SD.
- Every cell is now at 34 °C with Bezaire channels. `circuit.py` still uses point placeholders.

## §10. S3a: presynaptic GPCR inhibition (downscaling #2) inside STP, and the up/down balance of the per-spike weight

`python run_s3a_downscaling.py` → `results/s3a_downscaling.csv`, `docs/figures/s3a_downscaling_profiles.png`,
`docs/figures/s3a_downscaling_balance.png`. Mechanism `mod/TMSynPI.mod`: `TMSyn` plus GPCR inhibition of `U`, a tonic
part (A1R-like, `U·(1−i_tonic)`) and a phasic part (GABA_B-like, `U·(1−I(t))`). `I = i_max (1 − e^−D)`, and D is driven by
GABA events onto the terminal (difference of exponentials τ_r 50 / τ_d 300 ms; one event peaks at `c`). The GABA source is a
feedforward interneuron that fires once per presynaptic spike, 3 ms later. This is a proxy: in the circuit, the
interneurons set it.

**Verification.** `tests/test_s3a_presyn_inhib.py` (7 tests) checks `TMSynPI` against the closed form
`analysis.tm_pi_terms`. Max relative difference: 1e-15 in the tests and 1.3e-14 over all trains of this run. With no
inhibition, `TMSynPI` equals `TMSyn`, and the log terms below sum to log(amp/U) to 1e-12. NMODL pitfall found: a
NET_RECEIVE without an `INITIAL` block has `weight[1]` zeroed by `finitialize`, which turned GABA events into releases.

**Up/down split.** Per spike n, `log(w_eff,n / (w·U)) = fac + dep + phasic + tonic`. `fac = log(u⁺/U_eff)` (facilitation)
is the upscaling term. The three downscaling terms are `dep = log x⁻` (depletion, #1), `phasic = log(1−I)` and
`tonic = log(1−i_tonic)` (#2). This is an identity on the actual trajectory, so interactions between the terms are visible
in it.

**Parameters.** STP from `params.PATHWAYS` (secondary sources). Inhibition from `params.PRESYN_INHIB["SC"]`
(i_tonic 0.25, i_max 0.8, c 0.3, τ 50/300 ms). **None of these was read from a paper; all are marked unverified**, so
everything is also swept. Only SC terminals are modelled (SC→PYR, SC→PV = SC→BiS), the terminals where A1R and GABA_B
inhibition of release is described.

**SC→PYR per train** (sum over spikes of each term; mean w_eff/(wU)):

| Train | condition | mean w/wU | up (fac) | dep | phasic | tonic |
|---|---|---|---|---|---|---|
| 5 Hz, 1 s | STP only | 1.10 | 0.76 | −0.29 | 0 | 0 |
| | + tonic + phasic | 0.68 | 0.91 | −0.18 | −1.23 | −1.44 |
| 20 Hz, 1 s | STP only | 1.21 | 15.7 | −12.0 | 0 | 0 |
| | + phasic | 0.76 | 20.4 | −6.9 | −19.7 | 0 |
| | + tonic + phasic | 0.63 | 20.9 | −5.5 | −19.7 | −5.8 |
| 80 Hz, 1 s | STP only | 0.51 | 116.3 | −173.7 | 0 | 0 |
| | + phasic | 0.45 | 167.4 | −119.1 | −117.0 | 0 |
| | + tonic + phasic | 0.43 | 172.2 | −105.1 | −117.0 | −23.0 |
| theta burst (10 × 4 @ 100 Hz) | STP only | 1.13 | 35.8 | −31.3 | 0 | 0 |
| | + tonic + phasic | 0.61 | 45.1 | −12.5 | −42.8 | −11.5 |

**STP absorbs part of the presynaptic inhibition, and more at higher rates.** Lowering `U` leaves more vesicles
(dep less negative) and more room for facilitation (fac larger). The fraction of the direct phasic term that comes back
through these two terms is 14% at 5 Hz, 50% at 20 Hz, 73% at 40 Hz, 56% in the theta burst and 90% at 80 Hz. For the tonic
term it is 8% at 5 Hz, 53% at 20 Hz and 96% at 80 Hz. So GPCR inhibition is a strong downscaling at theta-range rates
and almost none at gamma and ripple rates. This extends §5 H4, which found the same for a static `U` gain, to the
dynamic case.

**Steady-state balance `B(f) = R_ss / U`** (nominal `U`):

| | f* SC→PYR (Hz) | max B | f* SC→PV (Hz) | max B |
|---|---|---|---|---|
| STP only | 27.3 | 1.25 | 22.5 | 1.33 |
| phasic c = 0.03 / 0.1 / 0.3 / 1 | 23.5 / 9.7 / none / none | 1.16 / 1.00 / 0.98 / 0.95 | 20.5 / 15.0 / none / none | 1.27 / 1.13 / 0.99 / 0.95 |
| tonic 0.125 / 0.25 / 0.5 | 25.4 / 21.4 / none | 1.16 / 1.05 / 0.84 | 21.3 / 19.3 / none | 1.23 / 1.12 / 0.90 |

The upscaling window (B > 1) closes at phasic drive c ≥ 0.3 or tonic inhibition 0.5. Above ~60 Hz, every condition
converges on the same `B`: the τ_rec limit. With strong phasic drive (c = 1), `B(f)` becomes non-monotonic, with a minimum
near 10 Hz and partial recovery near 30 Hz. At higher rates depletion dominates, and the inhibition only redistributes
the downscaling between terms.

**Not shown.** Real GABA drive comes from interneurons whose firing depends on the circuit (S3c), not one GABA event per
presynaptic spike. Every absolute number here depends on the unverified `PRESYN_INHIB` values. Sources to read:
Isaacson, Solís & Nicoll 1993 (time course and size of heterosynaptic GABA_B inhibition at SC), Davies et al. 1991, and
Dunwiddie & Masino 2001 (size of the tonic A1R block). The downscaling at E-LTP or slower timescales (#3–#13) stays
outside STP, as in `docs/plan.md`.

## §11. S3a: presynaptic inhibition with sourced values (adenosine A1R, Mitchell et al. 1993)

Same run as §10 (`python run_s3a_downscaling.py`, same outputs, overwritten) with `params.PRESYN_INHIB["SC_A1R"]` in
place of the values from memory. The phasic term is now **activity-dependent adenosine**, not GABA_B: it is the only
presynaptic GPCR inhibition at SC terminals for which a time course and size could be read.

**Sources read (2026-11-02).**
- **Mitchell, Lupica & Dunwiddie 1993, J Neurosci 13:3439, full text.** Rat (SD, 180–220 g), slices at 34 ± 1 °C,
  [Ca²⁺]ₒ 2.5 mM, [Mg²⁺]ₒ 2.4 mM, SC fEPSP in CA1. Conditioning volleys on an independent SC pathway at the
  1-mV-fEPSP strength. Values used:
  - Tonic: theophylline raised baseline responses by about 15–20% (Fig. 2 legend) → `i_tonic` 0.15.
  - Time course: no effect at 50 ms, visible at 100 ms, maximal at about 250 ms, back to baseline at 750–1000 ms.
  - Size: 2 pulses gave −18.5 ± 2.9% at 250 ms (n = 6); saturation from 16 pulses; 64 pulses gave 60.2 ± 7.3% of baseline.
  - Pharmacology: 8-CPT blocked the effect (A1R). Baclofen 10 µM gave −68 ± 6% (GABA_B maximum).
- **Wu & Saggau 1994 (Neuron) and 1995 (J Physiol 485:649), abstracts only.** A1R and GABA_B both act by reducing the
  presynaptic Ca²⁺ transient, and the fEPSP scales with about its 4th power. DPCPX raises the fEPSP, confirming tonic
  A1R inhibition. They give no numbers.
- **Not readable:** Isaacson, Solís & Nicoll 1993 (abstract has no numbers) and Molyneaux & Hasselmo 2002, J Neurophysiol
  87:1196 (GABA_B time constant in vivo; full text returned 403). **GABA_B therefore has a maximum (0.68) but no
  kinetics, and is not run.** Dunwiddie & Masino 2001 is a review and was not used.

**Fitted here.**
- Lag 50 ms, delivered as the drive event's delay. A difference of exponentials cannot be zero at 50 ms and peak at
  250 ms; Mitchell et al. attribute the effect to extracellular adenosine (formed from released ATP), which adds a delay.
- τ_r 168 / τ_d 176 ms, fitted to a peak at 250 ms and 10% at 875 ms. The fit gives a peak at 222 ms, 19% at 750 ms and
  6% at 1000 ms. The near-equal taus make an alpha-like shape.
- `i_max` 0.40 from the 64-pulse saturation (a lower bound: the test interval for that point was not read).
- `c` 0.315 per volley from the 2-pulse point (0.25–0.39 for ±SEM).
- Check: the model gives −31% for 5 pulses at 200 ms; the paper's Fig. 1 example slice shows about 15–20%. Text
  numbers only; the figures were not digitised.
- **`c` is per population volley** (about the strength of a 1 mV fEPSP). Using it per spike of one synapse assumes the
  SC population fires with that synapse, as in a stimulated slice. In sparse in-vivo firing, the effective drive is
  smaller, so c = 0.315 is the upper, slice-like end; the sweep covers the rest.

**SC→PYR per train** (sum of log terms; tonic 0.15, phasic as above):

| Train | condition | mean w/wU | up | dep | phasic | tonic | share of the direct inhibition returned by STP |
|---|---|---|---|---|---|---|---|
| 5 Hz, 1 s | + tonic + phasic | 0.83 (STP only 1.10) | 0.85 | −0.22 | −0.73 | −0.81 | phasic 14%, tonic 9% |
| 20 Hz, 1 s | + tonic + phasic | 0.96 (1.21) | 18.1 | −8.9 | −7.0 | −3.3 | phasic 57%, tonic 55% |
| 40 Hz, 1 s | + tonic + phasic | 0.78 (0.88) | 54.1 | −41.7 | −16.6 | −6.5 | phasic 81% |
| 80 Hz, 1 s | + tonic + phasic | 0.49 (0.51) | 141.0 | −152.8 | −35.4 | −13.0 | phasic 94%, tonic 96% |
| theta burst | + tonic + phasic | 0.92 (1.13) | 40.4 | −21.4 | −16.3 | −6.5 | phasic 66% |

The returned share is (Δup + Δdep) / |direct term|, from each condition alone against STP only.

**Steady-state balance `B(f)`:**

| | f* SC→PYR (Hz) | max B | f* SC→PV (Hz) | max B |
|---|---|---|---|---|
| STP only | 27.3 | 1.25 | 22.5 | 1.33 |
| tonic 0.15 (sourced) | 24.9 | 1.14 | 20.9 | 1.21 |
| phasic c = 0.1 | 21.4 | 1.11 | 19.6 | 1.22 |
| phasic c = 0.315 (sourced) | none | 0.99 (1 Hz) | 15.9 | 1.07 |

What changed against §10:
- The sourced tonic inhibition (0.15) is smaller than the guess (0.25). The phasic inhibition has a lower maximum (0.40 vs
  0.80), a 50 ms lag, and a shape close to an alpha function. Downscaling by inhibition is about half as strong as in §10,
  and the ordering is unchanged.
- The §10 conclusion holds with sourced values: STP returns 9–14% of the inhibition at 5 Hz and 94–96% at 80 Hz.
  Presynaptic adenosine inhibition is therefore a theta-range downscaling that ripple-rate transmission barely feels.
- New: **at slice-like drive (c = 0.315), steady-state SC→PYR transmission has no upscaling window left (max B 0.99),
  while SC→PV keeps one up to 15.9 Hz**. SC→PV has the longer τ_rec and τ_fac and more facilitation, so it outlasts the
  inhibition. If the drive is that strong, sustained SC activity would tilt the balance toward feedforward inhibition.
  This needs the circuit (S3c), where the drive comes from actual population activity.

Status: `SC_A1R` is primary (one paper, text values; kinetics and c fitted here, the tonic value approximate).
`SC_GABAB` has the maximum only. Still to read: a GABA_B time course at SC→CA1 (Molyneaux & Hasselmo 2002) and an
A1R-selective tonic measurement (DPCPX rather than theophylline; Wu & Saggau 1994 full text).

## §12. S3a: facilitation vs depression on every STP pathway (figures)

`python run_s3a_stp_all.py` → `results/s3a_stp_all.csv` and four 1650 × 1275 px figures (11 × 8.5 in, 150 dpi), each
a 3 × 3 grid with one panel per pathway (T → PYR uses the SC → PYR parameters):
- `docs/figures/s3a_stp_all_profiles.png`: per-spike weight w_eff/(wU) in 1 s trains at 5, 20 and 80 Hz.
- `docs/figures/s3a_stp_all_split_20Hz.png` and `…_split_theta.png`: per-spike split `log(w_eff/wU) = fac + dep`,
  with facilitation (up) and depletion (down).
- `docs/figures/s3a_stp_all_steady.png`: steady-state up and down terms against rate, with the crossover f*.

Release is in closed form and checked against NEURON `TMSyn` on the same spike times: max relative difference 7.1e-13.
Parameters are those of §3 (secondary sources), with no presynaptic inhibition (see §11 for SC). SC→PV = SC→BiS and
PYR→PV = PYR→BiS share one parameter set, so those panels are identical.

| Pathway | mean w/wU in 1 s at 5 / 20 / 80 Hz | f* (Hz) | max steady net factor (at) |
|---|---|---|---|
| SC → PYR (T → PYR) | 1.10 / 1.21 / 0.51 | 27.5 | 1.25 (10.8 Hz) |
| SC → PV, SC → BiS | 1.21 / 1.22 / 0.45 | 22.5 | 1.34 (8.5 Hz) |
| PYR → PV, PYR → BiS | 0.83 / 0.46 / 0.17 | none | 0.98 (1 Hz) |
| PYR → O-LM | 1.90 / 2.49 / 1.03 | 75.4 | 3.32 (10.8 Hz) |
| PV → PYR | 0.81 / 0.43 / 0.15 | none | 0.92 (1 Hz) |
| BiS → PYR | 0.83 / 0.48 / 0.17 | none | 0.92 (1 Hz) |
| O-LM → PYR | 0.66 / 0.25 / 0.07 | none | 0.80 (1 Hz) |

The crossovers equal those of §5. What the split adds: on the facilitating pathways (SC, PYR → O-LM), up and down
terms grow together with rate, and the net is their small difference. At 20 Hz SC → PYR sums +15.7 up against −12.0
down over 1 s. On the depressing pathways, facilitation contributes almost nothing below ~50 Hz (τ_fac ≤ 10 ms), so
their weight profile is depletion alone. At 80 Hz they gain some facilitation, but the depletion term is about 10×
larger. O-LM → PYR is the most depressed synapse at every rate (3% of its first-spike weight at 80 Hz).
