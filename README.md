# tinyHippo-bio-plasticity

NEURON implementation of the bio-plausible plasticity specified in
[**hippocampal_timescales_as_circuit_spec.md**](hippocampal_timescales_as_circuit_spec.md) (the main approach file),
tested in a minimal CA1 circuit (1 pyramidal cell, up to 3 interneurons) with
biological timescales. It is the biophysical companion of the NEST model in
[tinyHippo](https://github.com/max-talanov/tinyHippo).

**Milestone 1:** short-term plasticity (Tsodyks–Markram) per synapse class.
**Next:** synaptic tagging and capture, falsification tests, export of fitted
parameters to the NEST model.

![Tier A / Tier B circuit](docs/figures/neuron_stp_tier_b.png)

*Orange = excitatory, blue = inhibitory. Tier A (dashed box) = 1 pyramidal cell driven by
spike generators. Tier B = Tier A plus PV basket, bistratified and O-LM cells.*

## Contents

- [docs/plan.md](docs/plan.md): the plan, stages S0–S7 and acceptance criteria.
- [hippocampal_timescales_as_circuit_spec.md](hippocampal_timescales_as_circuit_spec.md): the main approach file, in the repository root (timescales, tag/capture, `V_seg`).
- [docs/neuron_model_optimization.md](docs/neuron_model_optimization.md): hardware-feasibility companion to the spec.
- `mod/`, `tests/`: NMODL mechanisms and tests (empty until S0–S1).
- [RESULTS.md](RESULTS.md): numbered experiment log.

## Status

Planning. No code yet. Stage S0 (install NEURON, compile a test mechanism) is next.
