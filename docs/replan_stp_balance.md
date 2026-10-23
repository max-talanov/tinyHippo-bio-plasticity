# Replan: upscaling and downscaling inside the STP boundary

Date: 2026-10-23. Status: **applied to `docs/plan.md` on 2026-10-23** (§6 lists the edits made; the decisions in §7 are answered by that approval, except the sources in §7.3, which are still needed).
Inputs: [hippocampal_plasticity_model.md](../hippocampal_plasticity_model.md) (upscaling path),
[hippocampal_downscaling_mechanisms.md](../hippocampal_downscaling_mechanisms.md) (13 weakening mechanisms),
the code and results of S0–S3 pilot (`RESULTS.md` §1–§4).

## 1. State of the programmed CA1

| Component | State | Evidence | Gap against the updated documents |
|---|---|---|---|
| `mod/TMSyn.mod` | the only synaptic mechanism; verified against the closed form (S1), amplitudes agree to < 1e-3 in the S2/S3 readouts | `RESULTS.md` §1, §3, §4 | one pool per instance, deterministic release, no stochastic release, no NMDA (Mg²⁺ block), no GABA-specific mechanism, **no `U` modulation hook**; `SegTag` (tag, `V_seg`, PRP pool, gradual capture) does not exist |
| `params.py` | 9 pathways with U, D, F and sources, all status `secondary`; `SLOW_TIMESCALES` unverified | Ecker 2019 Table 1 (v1 preprint), Hippocampus Hub quoting Wierenga & Wadman 2003 | no parameter for any downscaling mechanism; PYR→O-LM and O-LM→PYR are cortical values; SC→interneuron is a pooled fit; temperature and [Ca²⁺]ₒ of the SC data unknown |
| `cells.py`, `circuit.py` | Tier B builds and runs (≈1 s per 1 s of biology); PYR 4 sections, 3 one-compartment interneurons | `RESULTS.md` §4 | **all cell biophysics are placeholders** (NEURON `hh`, passive dendrites; interneurons differ only in size); SC/T conductances, contact counts, delays assumed; PYR fires ~2 spikes per volley and fewer when the drive is doubled (cause not examined) |
| Tests | 61 pass | `pytest tests` | none cover `cells.py`, `circuit.py` or `run_s3_pilot.py` |
| Stages | S0, S1 done; S2 sign test passes, fit only round-tripped; S3 pilot only; S4–S7 not started | `docs/handoff.md` | S3's own acceptance items (6 conditions, [Ca²⁺]ₒ sweep, E/I ratio, ablations) are open |

**Downscaling coverage.** Of the 13 mechanisms in the downscaling document, one is in the code: #1 short-term depression
(the `x` resource in `TMSyn`). #2 presynaptic inhibition needs only a `U` gain and is not wired. #3–#13 are absent, as
the downscaling document itself schedules them after S4–S6.

**What the pilot already says about balance** (`RESULTS.md` §4, seed 0): excitatory effective weights stay within about
±20% of `w·U` over a 20 Hz volley, while the inhibitory weights fall to 13% (PV→PYR) and 29% (bistratified→PYR) of their
first-event value. STP therefore moves the E/I balance toward excitation during a volley. On PYR output the effect is
not detectable (2.4 ± 0.5 vs 2.2 ± 0.4 spikes, 5 seeds), but that is measured in a placeholder cell.

**Housekeeping found.** `docs/plan.md` S2 still says "SC→PV depressing" (the sourced numbers give facilitation; §3);
the plan cites Cutsuridis 2010 and Bezaire 2016 from memory; `docs/handoff.md` keeps a stale "Blocker on S2" section
and stale "Next steps"; the plan's figure is `neuron_stp_tier_b.svg`, while `ca1_tier_b_architecture.svg` is the figure
of the built circuit.

## 2. Where "inside STP" ends

STP boundary used here: processes with time constants up to about 1 s (model §1, row 2), plus **static or phasic gain
knobs on `U`** that are set per run. Everything slower is a state variable that persists and belongs to later stages.

| Mechanism | Direction | Inside the STP boundary? |
|---|---|---|
| Facilitation (`τ_fac`, residual Ca²⁺, `U`) | up | **yes** |
| Short-term depression (`τ_rec`, downscaling #1) | down | **yes** |
| Presynaptic inhibition, A1 / GABA_B / mGluR (#2) | down | **yes as a `U` gain** (50 ms–min, tonic over hours); its time course is not modelled |
| [Ca²⁺]ₒ dependence of `U` (Hill function in Ecker 2019) | up or down | **yes as a `U` gain** (`U` at 1.1–1.3 mM vs 2 mM) |
| SWR-associated depression (#3) | down | within-ripple part = STD, yes; the hours-long NMDAR-dependent part, no |
| Post-tetanic potentiation, augmentation (s–min) | up | no: not in the TM model; flagged as a missing upscaling term |
| #4 LTD, #5 tag reset, #6 heterosynaptic, #7 mGluR-LTD, #8 tag decay, #9 PRP competition, #10 BCM, #11 sleep, #12 scaling, #13 pruning | down | no: minutes to months; scheduled after S4–S6 |

Consequence worth stating: inside STP, depression (#1) is the **only fast compensatory process** in the plan. The
downscaling document cites Zenke & Gerstner (2017) that compensation must be as fast as Hebbian growth; its fast
candidates (#3 in its ripple form, #6, #10) all sit outside the STP boundary. So until S4+, nothing in the model
limits runaway potentiation except STD and the inhibitory loop.

## 3. The balance, quantified (closed-form TM, steady state, per synapse; not yet run in NEURON)

Balance index `B(f) = R_ss(f) / U`: steady-state release per spike at presynaptic rate `f` relative to the first spike.
`B > 1` is net upscaling (facilitation wins), `B < 1` net downscaling (depression wins), `f*` is where `B = 1`.
Parameters are the secondary-source values in `params.py` (400-pulse periodic trains).

| Pathway | B at 1 / 5 / 20 / 80 / 200 Hz | max B (at) | f* |
|---|---|---|---|
| SC → PYR | 1.00 / 1.12 / 1.15 / 0.45 / 0.19 | 1.26 (12 Hz) | 27.5 Hz |
| SC → interneuron (pooled) | 1.00 / 1.25 / 1.07 / 0.36 / 0.15 | 1.34 (9 Hz) | 22.6 Hz |
| PYR → PV, BiS | 0.98 / 0.73 / 0.36 / 0.12 / 0.05 | none | always < 1 |
| PYR → O-LM | 1.26 / 2.84 / 2.77 / 0.95 / 0.39 | 3.32 (10 Hz) | 75.4 Hz |
| PV → PYR | 0.92 / 0.59 / 0.25 / 0.08 / 0.03 | none | always < 1 |
| BiS → PYR | 0.92 / 0.60 / 0.26 / 0.08 / 0.03 | none | always < 1 |
| O-LM → PYR | 0.80 / 0.37 / 0.12 / 0.03 / 0.01 | none | always < 1 |

Reading it:

1. **Rate decides the sign for the excitatory input.** SC→PYR is net upscaling from about 3 to 27 Hz (theta to low
   gamma) and net downscaling above (4–5× at ripple rates). The facilitating O-LM input stays in the upscaling regime to
   about 75 Hz.
2. **Every inhibitory output onto the PYR, and PYR→PV/BiS, is downscaling-only.** The inhibitory synapses cannot
   upscale at any rate in these parameters.
3. **E/I shift from STP alone** (ratio of `B` for SC→PYR to `B` for PV→PYR at equal presynaptic rate): 1.9× at 5 Hz,
   4.6× at 20 Hz, 5.6× at 80 Hz, 6.3× at 200 Hz. Caveat: the presynaptic rates differ in the circuit (the interneuron
   rate is set by the circuit, not by the SC fibre), so this is an upper-level expectation that S3c must test, and it
   is consistent in sign with the pilot.
4. **`U` gain moves `f*` but not the saturated release.** For SC→PYR, gain 0.5 / 1.0 / 1.5 gives `f*` = 66 / 27.5 / 14 Hz.
   At 80 Hz the absolute release is 0.060 / 0.063 / 0.064 for U × 0.5 / 1 / 1.5: at high rates transmission is set by
   `τ_rec`, not by `U`. Presynaptic inhibition (#2) and [Ca²⁺]ₒ therefore change low-rate transmission and extend the
   upscaling regime, and do almost nothing at ripple rates. This is a prediction of the TM model with these parameters.

## 4. Replanned stages (replace S3; S2 stays open)

Order is chosen so that each stage can be checked against a reference before the next relies on it.

| Stage | Experiment | Pass criterion |
|---|---|---|
| **S2 (finish)** | Primary texts of Wierenga & Wadman 2003 and Losonczy 2002 (PDFs supplied by the project owner, or the sources are blocked); re-enter U, D, F and conditions; fit real amplitudes if tables are available | Every `params.py` value has `status` ≠ `secondary` or is labelled secondary in the report; the SC→PV class in the plan is corrected to the sourced one |
| **S3a** Balance map, single synapse | `B(f)`, `f*` and release `R(f)` per pathway for `f` = 1–300 Hz and `U` gain ∈ {0.5, 0.75, 1, 1.25, 1.5}, from the NEURON clamp (`run_clamped`) against the closed form | NEURON vs closed form < 1% at every (pathway, f, gain); `f*` and the sign of `B − 1` reported per pathway; gain dependence of §3 item 4 confirmed or refuted. No new unverified biophysics |
| **S3b** Cell calibration | Replace the placeholder cells with sourced biophysics: DC rheobase and f–I curve of PYR and the three interneurons compared with literature values read from the sources (Bezaire 2016, Migliore 2018 are candidate sources, not yet read); fix the drive-dependent PYR block | PYR rheobase and f–I within the cited range; PYR spike count rises monotonically with SC drive over the working range; sources and conditions in `params.py` |
| **S3c** Circuit E/I balance | SC volleys at 5, 20, 80 and 200 Hz per fibre (theta-nested and ripple-like) through Tier B. Conditions: E-STP {on, off} × I-STP {on, off} (off = static synapse at the pathway's U), plus ablating PV, BiS or O-LM. ≥ 5 seeds | Reports PYR spikes and latency, E/I conductance ratio over the volley and its time course, `w·u·x` per pathway. Prediction to test: E/I conductance ratio rises during the volley, more with I-STP on; ablating a depressing inhibitory pathway changes PYR output in the sign predicted by its `B(f)` |
| **S3d** Gain knobs | Presynaptic inhibition (#2) as a `U` gain on SC→PYR; [Ca²⁺]ₒ sweep (1.1–2.5 mM) through the Hill scaling of `U` for all pathways | Shift of `f*` and of the E/I ratio reported per condition. **Needs sources**: the size of the A1 / GABA_B effect on `U` at SC→CA1, and a CA1 [Ca²⁺]ₒ–`U` curve (Ecker's Hill function is parametrised on cortical data) |
| **S3e** Interface to S4 | Define what S4's `SegTag` reads from STP: per event release `u·x` and `w·u·x` (not stored in the tag), and test that tag induction as a function of rate follows `B(f)` before PRP is added | Tag amplitude vs rate for pathway T under STP on/off reported, so S4's tag/capture starts from a known rate dependence |

**Not planned inside STP, deferred as in the downscaling document:** #8 + #5 (tag decay and LFS reset; second falsification
arm for S4), then #4 + #10 (two-threshold `g_Ca`, sliding threshold), #6 (per-segment conservation), #3 (SWR-gated
depression), #12 (scaling, only with a stated compression factor).

## 5. Hypotheses that S3a–S3d can falsify

- H1. SC→PYR is net upscaling for `f` below about 28 Hz and net downscaling above it (S3a). Falsified if the NEURON
  readout or the sourced parameters give a different `f*`.
- H2. Inhibitory pathways onto the PYR never upscale (S3a, S3c).
- H3. STP raises the E/I conductance ratio during a volley, and more so at higher rates (S3c). Falsified if the ratio
  falls, or does not depend on I-STP.
- H4. A `U` gain changes transmission at ≤ 20 Hz but not at ripple rates (S3d).

## 6. Edits made to `docs/plan.md`

1. §3 S2: replace "SC→PV depressing" by the sourced classes; keep "target values before fitting".
2. §3 S3: replace by S3a–S3e above.
3. §0 and §3: state the STP boundary of §2 and the "no fast compensation inside STP except #1" consequence.
4. §1: label Cutsuridis 2010 and Bezaire 2016 as unverified until read (already noted) and add the calibration source list for S3b.
5. §5 risks: add "cell biophysics are placeholders until S3b" and "S3d sources missing".

## 7. Decisions needed

1. Is the STP boundary of §2 (≤ ~1 s plus per-run `U` gain) the intended one, or should post-tetanic potentiation and
   the minutes-scale presynaptic inhibition time course be modelled as dynamic states?
2. Replace S3 by S3a–S3e, and apply the §6 edits to `docs/plan.md`?
3. Sources: the PDFs of Wierenga & Wadman 2003 and Losonczy 2002, and any reference for the A1 / GABA_B effect on `U`
   at SC→CA1 (Dunwiddie & Masino 2001 and Davies 1991 are cited in the downscaling document, not read).
