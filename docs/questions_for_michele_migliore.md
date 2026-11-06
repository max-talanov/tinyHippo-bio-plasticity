# Questions for Michele Migliore

Nov 6, 2026 · Max Talanov

These are the decisions where an expert view would change what we do next, roughly in order of impact within each group. Background is in the [status report](report_2026-11-06.md) and the [plasticity overview](plasticity_up_down_model_2026-11-06.md).

## Cells and circuit

1. **Pyramidal cell model.** Our Bezaire `poolosyncell` refit reaches the target Rin only by cutting HCN to 10%. Would you recommend one of the data-driven CA1 pyramidal models of Migliore et al. 2018 (*PLoS Comput Biol* 14:e1006423) instead, given that dendritic Ih and A-type K shape EPSP summation and the tag depends on segment voltage? If we keep this cell, is a 10% Ih acceptable?
2. **Synapse placement.** How should 900 SC synapses be distributed over SR and SO: uniformly by membrane area, by path distance, or following a measured density? For inhibition, we use PV on the soma, BiS on SR and O-LM on SLM. Should BiS also cover SO, as our plan first specified? Is a single site per projection acceptable for a first pass?
3. **SC synaptic strength and AMPA/NMDA.** Which CA1 values would you use for SC unitary conductance, AMPA and NMDA kinetics at 34 °C, and the AMPA:NMDA ratio along the dendrite? Our 0.6 nS is borrowed from PC → PC.
4. **SC → interneuron STP.** We use a pooled fit quoted from Wierenga & Wadman 2003. That abstract reports similar SC dynamics in basket and bistratified cells, which supports pooling. It also reports plateaus near 150% of the first response, while the quoted parameters give ×1.02 at 20 Hz. Do you know better type-specific SC → PV and SC → bistratified data (U, τ_rec, τ_fac), ideally at known temperature and \[Ca²⁺\]ₒ?
5. **PYR → interneuron STP.** Our PYR → PV and BiS parameters are strongly depressing (net ×0.36 at 20 Hz). Losonczy et al. 2002 report depressing or mixed EPSCs in basket cells and mixed classes in oriens-bistratified cells. Wierenga & Wadman 2003 report alveus-input plateaus close to the first response up to 40 Hz. Which data would you trust for these pathways?
6. **O-LM cell.** Our O-LM port misses Rin by 6.6 SD and rheobase by 8 SD. Is there a better-constrained O-LM model? Our STP values for PYR → O-LM and O-LM → PYR are cortical. The facilitating class of PYR → O-LM has CA1 support (Losonczy 2002; Wierenga & Wadman 2003), but do you know usable CA1 parameters?
7. **Circuit size.** Is one PYR with contact-scaled projections defensible for an E/I readout during a volley, or should we move to 5–10 PYR before drawing any circuit conclusion?
8. **Experimental conditions.** The synapses are rat data at 2–2.5 mM Ca (or unstated); the cells are fitted to mouse targets at 34 °C. How would you reconcile them: a \[Ca²⁺\]ₒ scaling of U, and temperature factors on τ_rec?
9. **Validation target.** Which experimental readout would you trust most to validate the circuit with STP: for example, PYR spike probability and latency during theta-burst SC stimulation with and without GABA_A block?

## Plasticity model

10. **Segment signal.** V_seg is an abstract leaky integral of synaptic input. In a biophysical cell, should the tag read local membrane voltage and NMDAR calcium directly instead?
11. **Tag and early-LTP.** Our plan carries early-LTP in the tag T. Redondo & Morris 2011 report that the tagged state and LTP expression are dissociable. Should they be separate state variables?
12. **PRP trigger.** Our plan increments the PRP pool on somatic bursts, which has no source. Evidence points to strong synaptic input and D1/D5 signalling (Huang & Kandel 1995; Moncada & Viola 2007). With no dopaminergic input in the circuit, what is the most defensible trigger?
13. **Extent of the PRP pool.** The original hypothesis is cell-wide, but later work confines tagging and capture to dendritic compartments or branches (Sajikumar 2007, 2011; Govindarajan 2011). At what spatial scale would you model the pool, and should capture consume it so that inputs compete?
14. **Upper bound.** Nothing in our equations saturates the captured weight. Which bound is biologically defensible: a hard limit, a soft limit, or a limit set by PRP or synaptic resources?
15. **Sign of the change.** Would you model depression with two calcium thresholds in one variable, or with a separate LTD tag? Late-LTD is also tagged, with different tag molecules in apical CA1 (Sajikumar & Frey 2004; Sajikumar 2007). Which CA1 threshold values, if any, can be trusted?
16. **Adult STDP.** Presynaptic t-LTD at mouse CA3 → CA1 is lost in the fourth postnatal week (Pérez-Rodríguez 2019), yet adult rat CA1 population data show depression when post precedes pre by 20 ms (Pang 2019). Should an adult model include a ±20 ms depression lobe, and through which mechanism?
17. **Timing target for capture.** We planned to compare the half-retention time with a 6 h behavioural window. Published studies show discrete sensitive periods, around training and about 3–6 h later (Igaz 2002; Bourtchouladze 1998), plus a phase at 12 h (Bekinschtein 2007). Is a slice late-LTP time course a better target for a single-synapse model?
