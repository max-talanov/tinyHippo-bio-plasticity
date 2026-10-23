# Handoff: state of the project and decisions so far

Read this first in a new session. It records what was decided in conversation, which is not
visible from the code. Update it whenever a decision or the status changes.

## Decisions (all confirmed by the project owner)

1. Goal: a bio-plausible NEURON implementation of the plasticity in
   `hippocampal_plasticity_model.md` (root), in a minimal CA1 circuit. Real biological
   timescales, no time compression. (Until 2026-10-22 the spec was one file,
   `hippocampal_timescales_as_circuit_spec.md`; it is now split, see decision 6.)
2. Circuit: **Tier A** = 1 pyramidal cell (PYR) driven by spike generators; **Tier B** = Tier A + PV basket,
   bistratified and O-LM interneurons (diagram: `docs/figures/neuron_stp_tier_b.svg`;
   orange = excitatory, blue = inhibitory). Tier B is the target. 1 PYR is enough for synapse-local
   weight dynamics; it cannot show emergent ripples or replay ordering.
3. Order of work: **milestone 1 = short-term plasticity (S0–S3)**, then tag/capture (S4–S6). Stages and
   acceptance criteria are in `docs/plan.md`.
4. The plan and all docs are NEURON-only: no NEST references (the NEST model lives in a separate
   repository and is out of scope here).
5. Literature parameters are entered only when read from the source, with conditions, in `params.py`.
   No values from memory.
6. 2026-10-22: the spec is split into a high-level model (`hippocampal_plasticity_model.md`) and a
   hardware document (`hippocampal_memristive_implementation.md`). The old file is a pointer stub with
   a section map.
7. 2026-10-22, after a comment from Edu (hippocampal neuroscientist): "consolidation" is never used
   unqualified. **Cellular consolidation** = protein-synthesis-dependent stabilization, ~6 h after
   learning, local to each region (hippocampus, neocortex, amygdala, ...). **System consolidation** =
   memory becomes independent of the hippocampus over days-weeks or longer; this shows loss of
   dependence, not that the trace left the hippocampus. Tag/capture and late-LTP are treated as the
   hypothesised synaptic correlate of cellular consolidation. Milestone 2 (S4-S6) models only that;
   system consolidation is out of scope. Late-LTP stabilization time (~4-8 h) is kept separate from
   persistence (days+; the old "~2 days" was a persistence figure, unsourced). The ~6 h window is in
   `params.py` `SLOW_TIMESCALES` as unverified (personal communication, behavioural).

## Status

| Stage | State | Where |
|---|---|---|
| S0 environment (NEURON 9.0.2, nrnivmodl) | passes | `tests/test_s0_environment.py` |
| S1 `TMSyn` vs closed-form Tsodyks–Markram | passes (amp error 8e-14, trace 2e-6 of peak) | `RESULTS.md` §1 |
| S2 STP signatures per pathway | **sign test passes** on secondary-source literature parameters (9 pathways); fit only round-tripped, no real recordings; **open until the primary papers are read** | `RESULTS.md` §2, §3 |
| S3 (replanned 2026-10-23 as S3a–S3e) | **pilot only**: the circuit builds and runs with placeholder biophysics (`RESULTS.md` §4). S3a (balance map), S3b (cell calibration), S3c (circuit E/I balance), S3d (gain knobs), S3e (interface to S4) not started | `docs/plan.md` §3, `docs/replan_stp_balance.md`, `cells.py`, `circuit.py`, `run_s3_pilot.py` |
| S4–S7 | not started | |

## Sources (state on 2026-10-23)

Fetching: PubMed Central shows a reCAPTCHA, Wiley returns 403, Europe PMC's API returned 500; bioRxiv PDFs and the
Hippocampus Hub pages can be fetched. (Earlier sessions saw `getaddrinfo ENOTFOUND` for these hosts; that
was a network policy of the cloud environment and is not the current cause.) Not circumventing a reCAPTCHA is deliberate.
What was read: Ecker et al. 2019 (bioRxiv preprint v1, full text and Table 1) and the Hippocampus Hub SC page, which quotes
Wierenga & Wadman 2003. So `params.py` has U, D, F for 9 pathways, all `secondary`; SC→PYR and SC→interneuron facilitate
(PPR > 1), which contradicts the plan's old "SC→PV depressing"; PV/BiS/O-LM→PYR rest on CA3 and cortical data (see
`docs/ca1_architecture_literature.md` §2–§3).
**Papers to download, with priority and why: `docs/sources_to_download.md`.** Needed for S2 (Wierenga & Wadman 2003,
Sun et al. 2005, Losonczy 2002, Ecker 2020 published version, Éltes 2017, Kohus 2016), S3d (Dürst 2022, Caruana & Dudek 2020)
and S3b (Migliore 2018, Bezaire 2016). Citations in the plan still from memory: Cutsuridis 2010, Clopath 2008, Barrett 2009.

## Open items from Edu's consolidation comment (2026-10-22)

Applied: terminology in the model document, late-LTP stabilization vs persistence, this record.
Applied 2026-10-22: the memristive document uses the same terminology; system consolidation is
"recall no longer depends on the organic tier" (the organic state afterwards is a free parameter;
standard, multiple-trace and trace-transformation accounts named); the cortical tier has its own
cellular-consolidation (volatile-until-latched) step, an open device requirement. Fig. 1 regenerated
(`figures/src/make_timescale_axis.py`); Fig. 3B (now implementation Fig. I1, panel B) relabelled "cellular consolidation" (raster patch, no
source file). 2026-10-22: the tier-map SVG was removed as a duplicate of Fig. 1; the memristive document
uses Fig. 1 plus its tier table. Fig. 1 now shades the ~6 h protein-synthesis-sensitive window.
8. 2026-10-22: capture in `SegTag` is **gradual** (rate ∝ h(P)·T, soft PRP threshold), not instantaneous;
   instantaneous capture is kept as a limiting case. S4 gets a time-resolved PRP-synthesis block, arm (d).
   See `docs/plan.md` §2 and §3.
9. 2026-10-22: S4(d)'s half-retention time `t_50` is compared with the **behavioural** ~6 h
   protein-synthesis-sensitive window (not a slice late-LTP window). It is compared, not fitted: the
   capture parameters are swept, not tuned to give 6 h. Caveat: the target is a whole-animal behavioural
   measure and the model is one CA1 synapse, so agreement supports consistency, not mechanism.
10. 2026-10-23: the model document is the plasticity model only (terminology, timescales, tag/capture,
    graded tag amplitude `V_seg` as model §2.1, system consolidation as model §3). The dendritic-
    convolution architecture (old model §3) moved to implementation §7. The old spec file is a contents
    page listing the model, implementation and downscaling documents.
11. 2026-10-23: the balance between upscaling (facilitation) and downscaling (depression) is studied **inside the
    STP boundary**: time constants up to ~1 s plus per-run `U` gains (presynaptic inhibition, [Ca²⁺]ₒ). Downscaling
    mechanisms #4–#13 are deferred to after S4–S6. Inside that boundary short-term depression is the only fast
    compensatory process. See `docs/replan_stp_balance.md`.
12. 2026-10-23: S3 is replaced by S3a–S3e (balance map, cell calibration, circuit E/I balance, gain knobs,
    interface to S4) and the S2 criterion uses the sourced classes. Applied in `docs/plan.md`; STP-off in the
    circuit means a static synapse at the pathway's `U`, not `U` → 0.
Not yet applied (need a decision by the project owner):
- (resolved 2026-10-22, decisions 8 and 9) gradual capture and S4(d) are in `docs/plan.md`; S4(d) is
  compared with the behavioural ~6 h window. Still open: sources for k_cap, n, τ_P, and a primary source
  for the ~6 h window itself.

## Next steps

1. **S3a** (needs no new sources): balance index `B(f)`, `f*` and `U`-gain dependence per pathway from the NEURON clamp
   against the closed form (`docs/plan.md` §3). Closed-form expectation: SC→PYR `f*` ≈ 27.5 Hz; inhibitory pathways `B < 1`.
2. Project owner downloads the papers of `docs/sources_to_download.md` (priority A1, A2, B1, B2, C1, C2); read them, enter values
   in `params.py` with conditions, finish S2.
3. **S3b** cell calibration from the CA1 model papers, then **S3c** circuit E/I balance (≥ 5 seeds, E-STP × I-STP on/off, ablations).
4. S3d once a presynaptic-inhibition effect size and a CA1 [Ca²⁺]ₒ–`U` curve are read; S3e before starting S4.
5. Fix before relying on circuit results: the pilot PYR fires fewer spikes when the SC drive is doubled (cause not examined).

## Pitfalls found (also in `RESULTS.md` §1)

- CVODE absolute tolerance must be ≤ 1e-8 (default 1e-3 gives percent-level errors on small states).
- In fixed-step mode record the states, not assigned variables computed in BREAKPOINT (one-step lag).
- With CVODE, `h.continuerun(t)` can return early; `protocols._advance_to` uses `fadvance`.
- Loading the compiled mechanisms twice in one process raises; `nrn_setup.load_mechanisms` is idempotent.
- The three `PARAMS` fixtures in the tests are test values, not literature values.

- `circuit.py` and `cells.py` are placeholders (textbook `hh`); every pre-S3b circuit result is a pilot (`RESULTS.md` §4).
- Run NEURON from a Python 3.9-3.13 venv with `PYTHONPATH` unset: the app-bundle NEURON in `PYTHONPATH` shadows pip's and fails to load. On macOS the mechanisms build to `libnrnmech.dylib`.
