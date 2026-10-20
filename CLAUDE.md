# tinyHippo-bio-plasticity

## Goal

Implement the plasticity of `hippocampal_timescales_as_circuit_spec.md` in NEURON
in a minimal CA1 circuit (see `docs/plan.md`), simulated in real biological units.
First milestone: short-term plasticity (S0–S3). Then tag/capture (S4–S6).

**Start here:** read `docs/handoff.md` (decisions, status, blockers, next steps) before working.

## Rules

- Follow `docs/plan.md` stage by stage. Each stage has an acceptance criterion; report against it.
- Verify every NMODL mechanism against an analytic or numpy reference before using it (S1).
- Runs are bit-identical at a fixed seed, config and thread count; rerunning an identical
  config adds nothing. Replicate across seeds (≥5 for stochastic release). Single-seed results are pilots.
- Measure rheobase with injected DC current, not synaptic drive rate.
- Literature parameters go in `params.py` with source and recording conditions
  (species, age, [Ca²⁺]ₒ, temperature). Do not enter values from memory without marking them unverified.
- Block-by-block or per-condition reporting beats whole-run means.
- Do not compress timescales without stating the factor. Add a numbered section to RESULTS.md for each result.
- Capabilities and mechanisms are self-contained: a dataclass plus a `build_*` function.
