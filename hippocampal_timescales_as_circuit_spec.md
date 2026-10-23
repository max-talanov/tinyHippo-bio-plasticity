# Hippocampal Timescales as a Circuit Specification (contents)

This specification is divided into three documents:

- [hippocampal_plasticity_model.md](hippocampal_plasticity_model.md): the plasticity model
  (timescales, cellular vs. system consolidation, tag/capture, graded tag amplitude `V_seg`).
- [hippocampal_memristive_implementation.md](hippocampal_memristive_implementation.md): the neuron
  architecture (dendritic-convolution pipeline) and its memristive and digital hardware implementation
  (circuit constraints, device tiers, replay handoff).
- [hippocampal_downscaling_mechanisms.md](hippocampal_downscaling_mechanisms.md): mechanisms that weaken
  synapses or keep their total bounded (short-term depression, LTD, depotentiation, PRP competition,
  synaptic scaling, sleep renormalization, forgetting), each with its timescale and its hook in the model.

Section map from the original combined file to the new documents: §1 → model §1 (biology) and
implementation §1 (circuit constraints); §1.1 → implementation §1.1; §2 → model §2 and implementation §2;
§3–§3.2 → implementation §7–§7.2; §3.3 → implementation §3; §4.1 → implementation §7.3; §4.2 → model §2.1
and implementation §4, §7.4; §4.3 → implementation §7.5; §4.4 → implementation §5; §4.5 → model §3 and
implementation §6. The full original text is in git history.
