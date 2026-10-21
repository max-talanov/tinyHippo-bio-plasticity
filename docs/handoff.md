# Handoff: state of the project and decisions so far

Read this first in a new session. It records what was decided in conversation, which is not
visible from the code. Update it whenever a decision or the status changes.

## Decisions (all confirmed by the project owner)

1. Goal: a bio-plausible NEURON implementation of the plasticity in
   `hippocampal_timescales_as_circuit_spec.md` (root), in a minimal CA1 circuit. Real biological
   timescales, no time compression.
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

## Status

| Stage | State | Where |
|---|---|---|
| S0 environment (NEURON 9.0.2, nrnivmodl) | passes | `tests/test_s0_environment.py` |
| S1 `TMSyn` vs closed-form Tsodyks–Markram | passes (amp error 8e-14, trace 2e-6 of peak) | `RESULTS.md` §1 |
| S2 STP signatures per pathway | **sign test passes** on secondary-source literature parameters (9 pathways); fit only round-tripped, no real recordings | `RESULTS.md` §2, §3 |
| S3 STP × inhibition (Tier B) | **pilot only**: circuit builds and runs with placeholder biophysics; the 6 STP on/off conditions, [Ca²⁺]ₒ sweep, E/I ratio and ablations are not done | `RESULTS.md` §4, `cells.py`, `circuit.py`, `run_s3_pilot.py` |
| S4–S7 | not started | |

## Blocker on S2

The full texts could not be fetched: the cloud environment's network policy blocks
`pmc.ncbi.nlm.nih.gov`, `biorxiv.org` and `europepmc.org` (`getaddrinfo ENOTFOUND`). Allowing them is an
environment setting (Network access, Allowed domains) and may only take effect in a new session.
Until then `params.py` holds abstract-level classes only (Losonczy et al. 2002: O-LM mostly facilitating,
basket cells mostly depressing, O-Bi mixed) and no numbers. `SC → PYR` has no source.
Papers to read: Losonczy et al. 2002 (J Physiol 542:193, PMC2290398) and a CA1 Schaffer-collateral source,
e.g. the 2019 bioRxiv "Data-driven integration of hippocampal CA1 synapse physiology in silico"
(10.1101/716480). Markram et al. 1998 is neocortical, so it is not a CA1 source.
Two citations in the plan (Cutsuridis 2010, Bezaire 2016) are from memory and unverified.

## Update 2026-10-20

The blocker moved: the env fetched Ecker 2019 (bioRxiv PDF via curl) and the Hippocampus Hub SC page, but PMC, Wiley
and Europe PMC are blocked by reCAPTCHA / 403 / 500. `params.py` now has sourced (secondary) U, D, F for 9 pathways.
Analysis and caveats: `docs/ca1_architecture_literature.md`. Main finding: the SC-> interneuron/PYR numbers give PPR > 1,
which contradicts the plan's "SC -> PV depressing" criterion. Still needed: primary text of Wierenga & Wadman 2003 and Losonczy 2002.

## Next steps

1. Fill `params.py` from the papers (value, source, species, age, temperature, [Ca²⁺]ₒ, afferent).
2. Run the S2 pass criterion: sign of PPR − 1 per pathway, then `fit_tm` with CIs (`run_s2.py`).
3. S3: build the Tier-B circuit (`cells.py`, `circuit.py`) and the volley protocols.

## Pitfalls found (also in `RESULTS.md` §1)

- CVODE absolute tolerance must be ≤ 1e-8 (default 1e-3 gives percent-level errors on small states).
- In fixed-step mode record the states, not assigned variables computed in BREAKPOINT (one-step lag).
- With CVODE, `h.continuerun(t)` can return early; `protocols._advance_to` uses `fadvance`.
- Loading the compiled mechanisms twice in one process raises; `nrn_setup.load_mechanisms` is idempotent.
- The three `PARAMS` fixtures in the tests are test values, not literature values.

- Run NEURON from a Python 3.9-3.13 venv with `PYTHONPATH` unset: the app-bundle NEURON in `PYTHONPATH` shadows pip's and fails to load. On macOS the mechanisms build to `libnrnmech.dylib`.
