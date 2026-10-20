# tinyHippo-bio-plasticity

NEURON implementation of the bio-plausible plasticity specified in
[**hippocampal_timescales_as_circuit_spec.md**](hippocampal_timescales_as_circuit_spec.md) (the main approach file),
tested in a minimal CA1 circuit (1 pyramidal cell, up to 3 interneurons) with
biological timescales.

**Milestone 1:** short-term plasticity (Tsodyks–Markram) per synapse class.
**Next:** synaptic tagging and capture, falsification tests, graded `V_seg`.

![Tier A / Tier B circuit](docs/figures/neuron_stp_tier_b.png)

*Orange = excitatory, blue = inhibitory. Tier A (dashed box) = 1 pyramidal cell driven by
spike generators. Tier B = Tier A plus PV basket, bistratified and O-LM cells.*

## Contents

- [docs/plan.md](docs/plan.md): the plan, stages S0–S7 and acceptance criteria.
- [hippocampal_timescales_as_circuit_spec.md](hippocampal_timescales_as_circuit_spec.md): the main approach file, in the repository root (timescales, tag/capture, `V_seg`).
- [docs/neuron_model_optimization.md](docs/neuron_model_optimization.md): hardware-feasibility companion to the spec.
- `mod/`, `tests/`: NMODL mechanisms and tests (empty until S0–S1).
- [RESULTS.md](RESULTS.md): numbered experiment log.

## Setup

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
pytest -q tests          # S0: compiles mod/ with nrnivmodl and checks Exp2Syn + an event-driven mechanism
```

Tested with NEURON 9.0.2, Python 3.13, numpy 2.5, scipy 1.18, matplotlib 3.11, pytest 9.1 (Linux x86_64).
`nrn_setup.load_mechanisms()` recompiles `mod/` when a `.mod` file is newer than the build.

## Status

S0 (environment) passes. S1 (verify the Tsodyks–Markram synapse against the closed form) is next.
