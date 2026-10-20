# Plan: minimal NEURON circuit for short-term plasticity and tag/capture dynamics

**Spec:** [hippocampal_timescales_as_circuit_spec.md](../hippocampal_timescales_as_circuit_spec.md) §1, §2, §4.1, §4.2.

![Tier A (dashed) and Tier B (whole figure) circuit](figures/neuron_stp_tier_b.svg)

*Orange = excitatory, blue = inhibitory. Tier A = 1 PYR driven by spike generators. Tier B = Tier A plus PV basket, bistratified and O-LM cells.*

## 0. Purpose and scope

Build a small, biophysical NEURON testbed of a CA1 pyramidal cell (PYR) and its
interneurons that shows how synaptic weights evolve over the spec's timescales,
simulated in real (biological) units with no time compression.

1. **Milestone 1 (S0–S3): short-term plasticity (STP)**, 10 ms–1 s, for each synapse class.
2. **Milestone 2 (S4–S6): tag/capture**, minutes–hours: the spec's Fig. 2, its two
   falsification tests, and the graded `V_seg` mechanism of §4.2.

Out of scope: emergent sharp-wave-ripple generation, replay ordering as a network
property, and anything that needs hundreds of cells.

## 1. How small can the circuit be?

STP and synaptic tagging are **synapse-local** (the plasticity-related-protein (PRP) pool is
cell-wide, but per cell). The minimum is therefore set by what is read out:

| Tier | Cells | Enough for | Not enough for |
|---|---|---|---|
| **A** | 1 PYR, 0 interneurons; presynaptic inputs are spike generators (`VecStim`) | STP of each synapse class (paired-pulse ratio, train depression/facilitation); tag/capture; Frey–Morris weak/strong design | Circuit-level effects of STP: E/I balance, dendritic gating |
| **B (target)** | 1 PYR + 3 interneurons (PV basket, bistratified, O-LM) | Everything in A, plus how STP at each pathway shapes PYR output and the E/I ratio during a volley | Population effects: ensemble competition, ripple emergence |
| **C (optional)** | 5–10 PYR + the same 3 interneurons | Reciprocal PYR→INT→PYR loops with more than one source | Ripple generation |

The three interneurons cover the three canonical CA1 inhibitory motifs:

| Interneuron | Motif | Target on PYR | Input | Role |
|---|---|---|---|---|
| **PV basket** | feedforward, perisomatic | soma | Schaffer collateral (SC) + PYR | The spec's `Cluster3` bypass (§4.1): inhibition that skips the threshold/junction pipeline |
| **Bistratified** | feedforward, dendritic | proximal apical (SR) + basal (SO) | SC + PYR | Dendritic inhibition acting on `V_seg` of the segment that carries SC synapses |
| **O-LM** | feedback, dendritic | distal apical (SLM) | PYR only | Facilitating feedback onto a segment separate from SC; a pure STP readout |

Caveat: with one PYR, the PYR→INT drive stands in for an ensemble. Scale it by the
contact count and report that factor. Do not read Tier-B E/I numbers as population values.
Precedent for this size: Cutsuridis, Cobb & Graham (2010, *J Comput Neurosci*), a CA1
microcircuit with one cell of each interneuron class; Bezaire et al. (2016, *eLife*), the full
CA1 NEURON model (ModelDB 187604), a source for channel and interneuron parameters.
(Both citations are from memory; verify before use.)

## 2. Circuit specification (Tier B)

```
CA3 (SC) stand-in ──┬─► PYR.apical_prox (SR)   AMPA+NMDA, TM-STP        ← strong pathway S
 VecStim trains     ├─► PYR.basal (SO)
                    ├─► PV.soma                AMPA, TM-STP
                    └─► BiS.soma               AMPA, TM-STP
T pathway (weak) ───────► PYR.apical_prox (SR)   AMPA+NMDA, TM-STP + tag/capture   ← tagged pathway T
PYR.soma ──► PV, BiS, OLM  (AMPA, TM-STP)
PV ──► PYR.soma (GABA_A)    BiS ──► PYR.apical_prox + basal (GABA_A)    OLM ──► PYR.apical_dist (GABA_A)
```

- **PYR:** soma + basal + apical_prox + apical_dist (4 sections). Na, Kdr, K_A and
  h conductances in the soma. Dendrites start passive; Na/K are added only to test the
  dendritic-spike `thr` of §3.1 (S5).
- **Interneurons:** one compartment each, Na/Kdr, with class-specific rheobase and
  membrane τ.
- **Synapses:** AMPA (Exp2Syn kinetics) and NMDA with the Jahr–Stevens Mg²⁺ block
  (needed for §4.2); GABA_A.

### Mechanisms to write (NMODL, `NET_RECEIVE`-based, CVODE-safe via `state_discontinuity`)

1. **`TMSyn.mod`**: Tsodyks–Markram synapse. State `u` (utilisation), `x` (available
   resources). On spike n: `u⁺ = u⁻ + U(1−u⁻)`, `Δg = w·u⁺·x⁻`, `x⁺ = x⁻ − u⁺·x⁻`.
   Between spikes: `du/dt = −u/τ_fac`, `dx/dt = (1−x)/τ_rec`. Parameters `U, τ_rec, τ_fac`
   per pathway. Optional stochastic release: N sites, Bernoulli with `p = u⁺·x⁻`
   (Random123, fixed seed).
2. **`SegTag.mod`** (spec §2 + §4.2), one instance per tagged synapse group:
   - `τ_v · dV_seg/dt = −V_seg + Σ wᵢ·sᵢ` (τ_v 10–30 ms)
   - `g_Ca(V_seg) = 1/(1 + K·exp(−λ·V_seg))`
   - tag set by a coincident pre/post event: `T ← T + g_Ca(V_seg)·[dSpike]`; `dT/dt = −T/τ_tag`
   - PRP pool `P`: incremented by somatic burst events, decays with `τ_P`
   - capture: if `P ≥ θ_PRP` while `T > 0`: `w_cap += κ·T`, and decay of `T` stops for that synapse
   - `θ_PRP = 999` disables capture (the blocked-capture arm of the falsification test).
3. **STDP in the tag step:** ±20 ms window (A₊, A₋).

Time scales: the slow module runs in **real units** (τ_tag 1–4 h). With CVODE and no
events between sharp-wave events the ODEs are linear decays, so hours of simulated time
should be cheap. This is a risk to check in S4; the fallback is to advance the slow
state analytically between events.

## 3. Stages and acceptance criteria

| Stage | Experiment | Pass criterion |
|---|---|---|
| **S0** | Environment: `pip install neuron`, `nrnivmodl`, run a toy `Exp2Syn` | Imports and compiles; NEURON version recorded in the README |
| **S1** | **Verify `TMSyn`** against the closed-form TM solution in numpy: 2-pulse and 20-pulse trains at 5, 20, 50 Hz | Relative error of every Δg < 1%; CVODE vs fixed dt = 25 µs differ < 2% |
| **S2** | **STP signatures per pathway** (voltage clamp at −70 mV, PYR and each interneuron): paired-pulse ratio at ISI 20–500 ms; steady-state amplitude vs frequency | Sign of PPR−1 matches the expected class: SC→PYR mild, SC→PV depressing, PYR→OLM facilitating. Target values are taken from the literature (e.g. Markram et al. 1998; Losonczy et al. 2002 for PYR→OLM) **before** fitting. `U, τ_rec, τ_fac` fit by least squares with CIs |
| **S3** | **STP × inhibition on PYR output.** Imposed 100–300 ms SC volley (theta-nested and ripple-like at ~150–200 Hz) through the full Tier-B circuit; each pathway's STP on/off (6 conditions) | Reports PYR spike count and latency, E/I conductance ratio over the volley, and the effective-weight `w·u·x` trace per pathway; ablating one pathway changes the output in the predicted direction |
| **S4** | **Tag/capture, spec Fig. 2.** Pathway T (subthreshold alone) receives K = 1…12 sharp-wave-like events at fixed spacing, with PYR driven by pathway S (Frey–Morris weak/strong design). Arms: normal capture vs `θ_PRP = 999` | (a) Tag amplitude per event and τ_tag recovered from the trace within 10%. (b) Captured arm shows a staircase after PRP crossing; blocked arm stays at baseline. (c) **Falsification:** PYR spike times during pathway-S volleys identical (to the sim dt) in both arms, since S is not plastic; only T's weight differs |
| **S5** | **Graded `V_seg`**: scale NMDAR conductance 0–100%; optionally enable dendritic Na to test the `thr` dendritic spike | Captured-weight step shrinks continuously with NMDAR dose (spec §4.2 prediction), not all-or-nothing. Dose–response with CI over seeds |
| **S6** | **Forward vs reverse order.** Three SC afferent groups A, B, C onto the PYR; fire A→B→C and C→B→A with 3–5 ms spacing (ripple-compressed) | Reports the tag-amplitude pattern per group under STDP + STP for each order. Pilot only: with one PYR this tests synapse-level order sensitivity, not replay |
| **S7** | **Parameter summary.** Table of fitted `U, τ_rec, τ_fac` per pathway, τ_tag, A±, PRP kinetics, with source, conditions and confidence intervals | Table in RESULTS.md; every value traceable to a run or a cited source |

**Statistics:** stochastic-release runs use ≥5 seeds, reported as mean ± SD. Runs are
bit-identical at fixed seed, config and thread count, so rerunning an identical config adds
nothing. Anything seen at one seed is a pilot.

## 4. Proposed layout

```
(repository root)
  mod/            TMSyn.mod  SegTag.mod  NMDA_Mg.mod  (+ interneuron channels)
  cells.py        build_pyr(), build_pv(), build_bis(), build_olm()   (dataclass + build_* pattern)
  circuit.py      build_tier_b(params) -> handles, connections, recorders
  protocols.py    paired_pulse(), train(), swr_volley(), frey_morris(), order_test()
  analysis.py     TM closed form, PPR fit, tag-trace fit, dose-response
  params.py       per-pathway U, tau_rec, tau_fac, tau_tag, ... with source citation per value
  tests/          test_tmsyn_vs_closed_form.py  test_segtag_block.py
  run_s1.py … run_s7.py
```

Each result becomes a new numbered section in [RESULTS.md](../RESULTS.md); older sections stay untouched.

## 5. Risks

| Risk | Mitigation |
|---|---|
| Literature STP parameters vary with species, age, [Ca²⁺]ₒ and temperature | Record source and conditions for each value in `params.py`; fit to the S2 targets, not to remembered numbers |
| One PYR stands for an ensemble, so PYR→INT drive is under- or over-scaled | Report the contact-count scaling factor; Tier C as a check on S3 |
| Hours of simulated time slow the S4 runs | Linear decays between events; analytic fallback; report wall-clock |
| NMDA/Mg²⁺ and `V_seg` parameters (K, λ, τ_v) are not constrained by the spec | Sweep them in S5 and report sensitivity, not a single value |
| Spec §4.4.2 device data does not show graded SET | S5 predicts the graded response from the biology; it does not validate the device |
