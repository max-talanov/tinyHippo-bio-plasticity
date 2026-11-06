# Hippocampal plasticity in the NEURON model: upscaling and downscaling

Nov 6, 2026 · Max Talanov

## The main idea

In this model a synapse changes at three nested levels, and upscaling and downscaling act at each one. A change survives only if it passes from a fast level to a slower one.

- **Release (ms to s).** Each spike releases a fraction of the available resources. Facilitation raises that fraction; vesicle depletion and presynaptic inhibition lower it. The stored weight does not change.
- **Tag (minutes to hours).** Coincident activity sets a local tag, graded by NMDA-receptor calcium signalling in the dendritic segment. The tag decays unless it is captured.
- **Stored weight (hours and longer).** Capture needs both a tag and plasticity-related proteins (PRPs). Captured weight stops decaying, and slower processes can later scale it down or remove it.

The hypothesis is that weakening also selects: what is captured and replayed is kept, and the rest fades or is depressed. Tag and capture are the candidate synaptic correlate of cellular consolidation, not an established identity.

The model is one CA1 pyramidal cell with one PV basket, one bistratified and one O-LM interneuron, in NEURON, in real units with no time compression. Only the release level is implemented and verified so far. The tag and capture levels are specified but not built, and most slow downscaling pathways are a literature map for later stages.

## Acronyms and abbreviations

Cell and pathway names match the [status report of November 2026](report_2026-11-06.md). Symbols are defined in the equations where they appear.

| Term | Meaning |
| --- | --- |
| A1R | Adenosine A1 receptor |
| AMPA, AMPAR | α-amino-3-hydroxy-5-methyl-4-isoxazolepropionic acid; its receptor |
| Arc | Activity-regulated cytoskeleton-associated protein |
| BCM | Bienenstock–Cooper–Munro rule with a sliding threshold |
| BiS | Bistratified interneuron |
| C1q, C3, CR3 | Complement components 1q and 3; complement receptor 3 |
| CA1, CA3 | Cornu Ammonis areas 1 and 3 |
| CaMKII, CaMKIV | Ca²⁺/calmodulin-dependent protein kinases II and IV |
| CB1 | Cannabinoid receptor type 1 |
| eCB | Endocannabinoid |
| E-LTP, L-LTP | Early and late long-term potentiation |
| E/I | Excitation/inhibition |
| GABA_A, GABA_B | γ-aminobutyric acid receptors, types A and B |
| GluA1, GluA2 | AMPA receptor subunits |
| GluN2A, GluN2B | NMDA receptor subunits |
| GPCR | G-protein-coupled receptor |
| IP3R | Inositol trisphosphate receptor |
| LFS | Low-frequency stimulation |
| LTD, t-LTD | Long-term depression; spike-timing-dependent LTD |
| LTP | Long-term potentiation |
| mGluR | Metabotropic glutamate receptor |
| NMDA, NMDAR | N-methyl-D-aspartate; its receptor |
| NREM, REM | Non-rapid and rapid eye movement sleep |
| O-LM | Oriens-lacunosum moleculare interneuron |
| P_r | Release probability |
| PKA | Protein kinase A |
| PP1 | Protein phosphatase 1 |
| PRP | Plasticity-related protein |
| PV | Parvalbumin-positive basket interneuron |
| PYR | CA1 pyramidal cell |
| S0–S7 | Project stages in the plan |
| SC | Schaffer collaterals |
| SHY | Synaptic homeostasis hypothesis |
| SLM, SO, SR | Strata lacunosum-moleculare, oriens and radiatum |
| STDP | Spike-timing-dependent plasticity |
| STEP | Striatal-enriched protein tyrosine phosphatase |
| STP | Short-term plasticity |
| SWR | Sharp-wave ripple |
| T | Tag variable; also the tagged input pathway when written "T pathway" |
| TM | Tsodyks–Markram synapse model |
| TNFα | Tumour necrosis factor alpha |
| VGCC | Voltage-gated calcium channel |

## Timescales

The processes run from milliseconds to years, and they overlap instead of handing off in sequence. Upscaling and downscaling coexist from about 10 ms to months, so no level of the synapse has only one direction.

![All upscaling and downscaling processes on one logarithmic time axis, 8 upscaling and 14 downscaling](figures/plasticity_timescales_all.png)

Bars are order-of-magnitude summaries of the two source documents, not fitted values. Where a source gives only "hours" or "days", the bar's end is our rounding.

**Two meanings of "consolidation".** This document always says which one it means.

- **Cellular consolidation:** for about 6 h after learning, a memory can be removed by blocking protein synthesis; after that it cannot. It happens locally in each region that stores the memory. The 6 h figure is behavioural, from a personal communication (Edu, a hippocampal neuroscientist), and is not yet checked against primary literature.
- **System consolidation:** over days to weeks in rodents and longer in humans, a memory stops depending on the hippocampus. This shows loss of dependence, not that the trace has left the hippocampus.

Late-LTP has two separate times: about 4–8 h until it stabilises, then days or longer of persistence. The slice late-LTP window and the 6 h behavioural window need not coincide, so every comparison must state which one it uses.

## Upscaling: from one spike to a lasting weight

Upscaling is a chain of eight processes. Of these, only facilitation is implemented as plasticity so far. The NEURON model will reach as far as late-LTP, and replay enters only as an imposed input.

| # | Process | Timescale | What it does | Term in the model | Status |
| --- | --- | --- | --- | --- | --- |
| U1 | Neurotransmission | ms | Receptor gating carries each synaptic event | AMPA and GABA_A conductances | AMPA and GABA_A run; NMDA planned |
| U2 | Facilitation (STP) | 10 ms–1 s | Each spike raises the release fraction u | u in `TMSyn` | Verified |
| U3 | Ca²⁺/kinase cascades | 1 s–5 min | Decides whether a weight update happens | Lumped into g_Ca(V_seg); no explicit kinase | Planned, S4–S5 |
| U4 | AMPAR trafficking, early-LTP | 1–30 min, decays over 1–3 h | Adds receptors, independent of protein synthesis, and fades | Carried by the tag T | Planned, S4 |
| U5 | Synaptic tagging and capture | Set in 1–2 min; τ_tag about 1–4 h | A local tag is captured if PRPs arrive before it decays | T, P, h(P) in `SegTag` | Planned, S4 |
| U6 | Transcription, late-LTP | Onset 30–60 min; stable by 4–8 h | The potentiated state stops decaying | w_cap | Planned, S4 |
| U7 | SWR replay | Ripple 100–300 ms; recurs over hours to days | Repeated events drive capture | Imposed sharp-wave-like input, not emergent | Planned, S4 |
| U8 | System consolidation | Days to years | Memory stops depending on the hippocampus | None | Out of scope |

**Release level (U2).** At spike n, with u the utilisation and x the available resources:

```math
u_n^+ = u_n^- + U(1 - u_n^-), \quad A_n = u_n^+ x_n^-, \quad x_n^+ = x_n^-(1 - u_n^+)
```

Between spikes u decays to 0 with τ_fac and x recovers to 1 with τ_rec. The conductance step is w · A_n.

**Tag amplitude (U3).** One continuous state per dendritic segment leakily integrates its synaptic input. A sigmoid patterned on the NMDAR unblock curve turns it into an induction amplitude, so induction strength is graded rather than all-or-nothing.

```math
\tau_v \frac{dV_{seg}}{dt} = -V_{seg} + \sum_i w_i s_i(t), \qquad g_{Ca}(V_{seg}) = \frac{1}{1 + K e^{-\lambda V_{seg}}}
```

Here τ_v is 10–30 ms. Because V_seg is shared on a segment, several subthreshold synapses can together reach the steep part of g_Ca. Here K is the sigmoid constant, not the contact count used in the circuit.

**Tag, PRP pool and capture (U4–U6).** A coincident event with a dendritic spike adds g_Ca(V_seg) to the tag. Somatic bursts add ΔP · s(t) to the PRP pool, where s is the protein-synthesis gate, 0 or 1.

```math
\frac{dP}{dt} = -\frac{P}{\tau_P}, \qquad h(P) = \frac{P^n}{P^n + \theta_{PRP}^n}
```

```math
\frac{dT}{dt} = -\frac{T}{\tau_{tag}} - k_{cap}\, h(P)\, T, \qquad \frac{dw_{cap}}{dt} = k_{cap}\, h(P)\, T
```

Capture is gradual by design. The protein-synthesis-sensitive window is therefore an output of the model, not an input. Instantaneous capture is the limit of large k_cap and n, kept for comparison. k_cap, n and τ_P have no source and will be swept, not tuned to give 6 h.

## Downscaling: fourteen pathways that weaken or bound a synapse

Downscaling is not one process. We list 14 molecular pathways, each described by what senses the trigger and what physically weakens the synapse. Two of them are implemented: depletion in the circuit, and A1R inhibition as a verified mechanism not yet wired in.

Rules such as STDP, BCM or firing-rate homeostasis are a separate level: they say which activity pattern changes a weight, not how. One rule can use several pathways, and one pathway can serve several rules. So only sensors and effectors become mechanisms; a rule is what a mechanism must reproduce, which makes it an acceptance test.

| Pathway (site) | Timescale | Sensor → effector | Rule | Term in the model | Status |
| --- | --- | --- | --- | --- | --- |
| #1 Vesicle-pool depletion (pre) | 10 ms–10 s | Spike and VGCC Ca²⁺ → readily releasable pool depleted | Frequency-dependent depression | x in `TMSyn` | Verified, in circuit |
| #2 Presynaptic GPCR inhibition (pre) | 50 ms–min; tonic over hours | A1R, GABA_B, group II/III mGluR → lower P_r | Tonic and neuromodulatory gain | U_eff in `TMSynPI` | A1R verified, not in circuit |
| #3 SWR-triggered NMDAR depression (post) | Ripple 100 ms; effect lasts hours | NMDAR during SWR → AMPAR weakening (effector unresolved) | Offline depression | Stored weight of non-replayed inputs | Candidate |
| #4a NMDAR → calcineurin/PP1 LTD (post) | Induction s–min; expression hours | Moderate NMDAR Ca²⁺ → GluA1-S845 dephosphorylation, AMPAR endocytosis | Rate-dependent LTD | Low-Ca branch of g_Ca | Candidate |
| #4b Endocannabinoid → CB1 t-LTD (pre, induced post) | Induction s–min; expression hours | Post mGluR and Ca²⁺ → eCB; pre CB1 and NMDAR → lower P_r | STDP depression | Reduction of U | Open: see limits |
| #5 PP1 depotentiation (post) | Window 1 min–1 h | LFS, NMDAR Ca²⁺ and A1R → PP1 reverses phosphorylation | Reversal of recent LTP | Active reset of T | Candidate |
| #6 IP3R/calcineurin heterosynaptic depression (post, unstimulated) | Min–hours | Neighbour potentiation, group I mGluR, IP3R Ca²⁺ → inactive spines shrink | Heterosynaptic normalisation | Conservation per segment | Candidate |
| #7 mGluR5 → local-translation LTD (post) | Min–1 day | Group I mGluR → Arc, STEP, MAP1B translation, AMPAR endocytosis | Protein-synthesis-dependent LTD | Draws on the PRP machinery | Deferred |
| #8 Constitutive GluA2 endocytosis (post) | τ about 1–4 h | No sensor: absence of capture → inserted AMPARs removed | Decay of unconsolidated LTP | τ_tag | Planned, S4 |
| #9 PRP competition (post, cell-wide) | 30 min–8 h | No sensor: finite pool, synthesis against degradation | Competition between inputs | Shared capture resource | Not in the equations yet |
| #10 GluN2A/2B threshold shift (post) | 30 min–days | Activity history → subunit ratio changes | BCM sliding threshold | Moves θ_p of g_Ca | Candidate |
| #11 Homer1a–mGluR5 sleep scaling (post) | Hours, each sleep cycle | Sleep state → Homer1a → GluA1 dephosphorylation, AMPAR removal | SHY | Global step between replay epochs | Deferred |
| #12 CaMKIV/TNFα synaptic scaling (post; also P_r) | 12 h–days | Somatic Ca²⁺, glial TNFα → multiplicative AMPAR change | Firing-rate homeostasis | Multiplicative factor on weights | Candidate, needs stated compression |
| #13 Complement pruning, Rac1/cofilin (whole synapse) | Days–months | C1q/C3 at weak synapses → microglial removal; actin disassembly | Structural forgetting | Removal of uncaptured traces | Deferred |

"Candidate" means proposed for after S4–S6, in this order: #8 and #5, #4a and #10, #6, #3, #12. Nothing in this group is built yet.

**Presynaptic A1R inhibition (#2).** This is the one slow-signalling pathway already written as a mechanism. It scales the release parameter:

```math
U_{eff} = U\,(1 - i_{tonic})\,(1 - I(t))
```

Each SC volley drives I(t) after a 50 ms lag, and I(t) saturates at i_max. From Mitchell, Lupica & Dunwiddie 1993 (rat, 34 °C, 2.5 mM Ca, SC fEPSP): i_tonic = 0.15, i_max = 0.40 as a lower bound, and c = 0.315 per volley. The rise and decay constants were fitted to that paper's time course.

## How the processes combine

Each process acts on one term of a single chain, so their effects can be located and combined. Release multiplies the stored weight, the tag feeds the stored weight, and the PRP pool gates the transfer.

![The chain of model states, with the upscaling and downscaling processes acting on each](figures/plasticity_combination_chain.png)

Read down the middle for the chain, and across each row for what raises or lowers that state. Only the top state runs in NEURON today.

Written as one expression, the amplitude of spike n is:

```math
\Delta g_n = \big[\,w_0 + \alpha\, T(t_n) + w_{cap}(t_n)\,\big] \cdot A_n
```

This summary is ours. The plan does not yet state it, and α, the scale from tag to early-LTP weight, is undefined there.

**1. Inside release, up and down terms add on a log scale.** We split each release exactly:

```math
\log\frac{A_n}{U} = \log\frac{u_n^+}{U_{eff}} + \log x_n^- + \log(1 - I_n) + \log(1 - i_{tonic})
```

The terms are facilitation, depletion, phasic A1R and tonic A1R. On the three facilitating pathways the net effect flips from up to down at a crossover rate f\*: 27.5 Hz for SC→PYR, 22.5 Hz for SC→PV and BiS, and 75.4 Hz for PYR→O-LM. Inhibitory synapses onto PYR are net down at every rate.

**2. The balance differs by pathway, so STP reshapes E/I.** At a steady 20 Hz, the net factors are ×1.15 for SC→PYR, ×2.77 for PYR→O-LM, ×0.25 for PV→PYR, ×0.26 for BiS→PYR and ×0.12 for O-LM→PYR. Adding A1R inhibition turns SC→PYR to ×0.86. These are single-synapse values; the implied tilt towards excitation is a prediction for the circuit, not a result.

**3. Presynaptic gain acts at theta and gamma rates, not at ripple rates.** A gain of 0.5–1.5× on U moves f\* for SC→PYR from 66 to 14 Hz. At 200 Hz, steady-state release stays at 0.028 for every gain, because τ_rec sets it there.

**4. Release feeds induction.** S3e will test what the tag reads from STP: per-event u · x and w · u · x. If tag amplitude follows B(f), the steady-state release relative to the first spike, then fast release dynamics decide which rates can set a tag.

**5. Calcium could set the sign.** With two thresholds, θ_d < Ca < θ_p gives depression (#4a) and Ca > θ_p gives a tag. Recent activity moves θ_p (#10), so history changes the sign of the next change. The current plan has one sigmoid; two thresholds are a candidate extension.

**6. A tag has three possible fates.** It is captured, it decays passively (#8), or low-frequency stimulation resets it within about 10–60 min (#5). A reset tag can no longer capture PRPs, and stabilised late-LTP no longer reverses.

**7. The PRP pool links synapses across the cell.** A strong input can supply PRPs for a weak input's tag, which is the Frey–Morris design. With limited synthesis, inputs compete (#9), and protein-synthesis-dependent LTD (#7) draws on the same machinery.

**8. Replay may select as well as store.** The same ripple could capture what is replayed and depress the rest (#3). Sleep (#11) and homeostatic scaling (#12) then lower total weight, and scaling preserves relative weights because it is multiplicative. Synapses that remain weak can be removed (#13). This sequence is a hypothesis.

**9. Stability needs fast compensation.** Zenke & Gerstner 2017 argue that compensation must be comparable in speed to Hebbian growth, so slow scaling alone cannot stabilise it. The fast candidates are #3, #6 and #10. Inside the STP stage, nothing limits potentiation except depletion and the inhibitory loop.

## What is in NEURON today

The release level runs in NEURON; everything slower is still specification. Every mechanism must match an analytic or numpy reference before use, and the two written so far do.

| Milestone | Levels covered | Mechanisms | State on 6 November 2026 |
| --- | --- | --- | --- |
| 1. STP, S0–S3 | Release, up to about 1 s, plus U gains set per run | `TMSyn`, `TMSynPI` | Single-synapse work done: `TMSyn` matches the closed form to 8e-14, and steady-state rates match to 3e-11. Cells calibrated to Bezaire et al. 2016 at 34 °C but not yet running in the circuit |
| 2. Tag and capture, S4–S6 | Segment signal, tag, PRP pool, captured weight | `SegTag`, NMDA with Mg²⁺ block, STDP step | Not started; none of these is written |
| After S4–S6 | Slower downscaling, #3 to #13 except #8 | Each a dataclass plus a `build_*` function | Candidates only |

The circuit has two spike generators, four cells and 11 projections, all with Tsodyks–Markram STP. Its only full run used placeholder cells, so it is a pilot and supports no PYR claim. The [status report of November 2026](report_2026-11-06.md) gives the projection table, cell fits and parameter sources.

## What the model predicts, and how each prediction is tested

The combined scheme makes predictions that can fail. Only the first has been tested, and only at the single-synapse level.

| Prediction | Test | Stage | State |
| --- | --- | --- | --- |
| A U gain moves f\* but not the saturated high-rate release | NEURON clamp against the closed form | S3a | Holds on secondary-source parameters |
| The E/I conductance ratio rises during a volley, more with inhibitory STP on | SC volleys at 5, 20, 80 and 200 Hz; STP on or off; at least 5 seeds | S3c | Next, after synapse placement |
| Removing a depressing inhibitory pathway changes PYR output in the sign its B(f) predicts | Ablate PV, BiS or O-LM | S3c | Not run |
| Tag amplitude against rate follows B(f) | Pathway T, STP on and off | S3e | Not started |
| Blocking capture leaves the weight at baseline, while PYR spike times during pathway S volleys stay identical | Normal capture against blocked capture | S4 | Not started |
| Retained weight does not decrease as a protein-synthesis block starts later | Block at 0–8 h; report t₅₀ with its CI | S4 | Not started |
| Partial NMDAR block shrinks the captured weight continuously, not all-or-nothing | NMDAR conductance 0–100% | S5 | Not started |
| LFS inside the reset window abolishes capture | Add active reset (#5) as a second falsification arm | After S4–S6 | Candidate |

t₅₀, the half-retention time, is compared with the 6 h behavioural window, not fitted to it. The target is a whole-animal measure and the model is one CA1 synapse, so agreement would show consistency, not mechanism.

## Limits and open points

The scheme is a hypothesis built largely from secondary and partly unchecked sources, and its equations have known gaps. These are the points where expert input would change the design.

1. **Segment signal.** V_seg is an abstract leaky integral of synaptic input. In a biophysical cell the local membrane voltage already exists. Should the tag read local voltage and NMDAR calcium directly instead?
2. **Adult t-LTD.** The plan has a ±20 ms STDP window with a depression lobe. Presynaptic t-LTD at mouse CA3→CA1 fades by about the fourth postnatal week, so an adult lobe is not established. If kept, it should reduce U, not the postsynaptic weight.
3. **No upper bound.** Nothing in the planned equations saturates w_cap, so repeated events can raise it without limit. Which bound is biologically defensible?
4. **PRP pool.** The model calls the pool cell-wide, but the plan builds one `SegTag` per tagged synapse group, and capture does not consume P. Competition (#9) therefore needs a shared pool with a consumption term.
5. **Sign of the change.** One sigmoid can only set a tag. Depression needs the two-threshold form, and its thresholds have no CA1 values yet.
6. **NMDAR timescale.** Our model table lists AMPA and NMDA gating together at 0.5–5 ms, yet credits slow NMDAR deactivation for the ±20 ms window. That range cannot describe NMDAR decay, so the table needs correcting from a primary source.
7. **Bistratified target.** The plan places BiS input on SR and SO; the circuit currently places it on SR only.

Other limits on the evidence:

- **Unsourced values:** k_cap, n, τ_P, K, λ and τ_v have no source and will be swept.
- **Mixed preparations:** cell targets are mouse and STP values are rat; two pathways use cortical values. Pathway #3 comes from mouse, #6's weight conservation from amygdala, and Rac1 forgetting (#13) from *Drosophila*.
- **Timespans:** the spans of the downscaling pathways are order-of-magnitude summaries, not fitted values.
- **Circuit size:** one PYR with contact-scaled projections cannot show population effects, ripple generation or replay ordering. Replay enters only as imposed input.
- **Slow pathways:** those running over days need a stated compression factor in any short run, or they stay out.

## Sources

This document combines `hippocampal_plasticity_model.md` and `hippocampal_downscaling_mechanisms.md`, with `docs/plan.md` and `docs/handoff.md`, from the repository [max-talanov/tinyHippo-bio-plasticity](https://github.com/max-talanov/tinyHippo-bio-plasticity). Numbers from simulations come from its `RESULTS.md`. Full references per pathway are in the downscaling document.

**Details checked against PubMed, PMC or publisher records, not necessarily read in full:**

- Norimoto et al. 2018, *Science* 359:1524. [doi:10.1126/science.aao0702](https://doi.org/10.1126/science.aao0702) (#3)
- Miyawaki & Diba 2016, *Curr Biol* 26:893 (#3)
- González-Rueda et al. 2018, *Neuron* 97:1244. [doi:10.1016/j.neuron.2018.01.047](https://doi.org/10.1016/j.neuron.2018.01.047) (#3, cortex)
- Lee et al. 2000, *Nature* 405:955. [doi:10.1038/35016089](https://doi.org/10.1038/35016089) (#4a)
- Sjöström et al. 2003, *Neuron* 39:641 (#4b, neocortex)
- Andrade-Talavera et al. 2016, *Cereb Cortex* 26:3637. [doi:10.1093/cercor/bhw172](https://doi.org/10.1093/cercor/bhw172) (#4b)
- Huang et al. 1999, *J Neurosci* 19:9728 (#5)
- Sajikumar & Frey 2004, *Neuroscience* 129:503. [doi:10.1016/j.neuroscience.2004.08.014](https://doi.org/10.1016/j.neuroscience.2004.08.014) (#5)
- Oh et al. 2015, *Cell Rep* 10:162. [doi:10.1016/j.celrep.2014.12.016](https://doi.org/10.1016/j.celrep.2014.12.016) (#6)
- Royer & Paré 2003, *Nature* 422:518. [doi:10.1038/nature01530](https://doi.org/10.1038/nature01530) (#6)
- Migues et al. 2016, *J Neurosci* 36:3481. [doi:10.1523/JNEUROSCI.3333-15.2016](https://doi.org/10.1523/JNEUROSCI.3333-15.2016) (#8)
- Fonseca et al. 2004, *Neuron* 44:1011. [doi:10.1016/j.neuron.2004.10.033](https://doi.org/10.1016/j.neuron.2004.10.033) (#9)
- Li et al. 2017, *Nat Neurosci* 20:427. [doi:10.1038/nn.4479](https://doi.org/10.1038/nn.4479) (#11, motor cortex)
- Ibata et al. 2008, *Neuron* 57:819 (#12)
- Kim & Tsien 2008, *Neuron* 58:925. [doi:10.1016/j.neuron.2008.05.009](https://doi.org/10.1016/j.neuron.2008.05.009) (#12)
- Branco et al. 2008, *Neuron* 59:475 (#12)
- Wang et al. 2020, *Science* 367:688. [doi:10.1126/science.aaz2288](https://doi.org/10.1126/science.aaz2288) (#13)

**Read for parameter values already in the code:**

- Bezaire et al. 2016, *eLife*: cell morphologies, channels and intrinsic targets.
- Ecker et al. 2019, bioRxiv [10.1101/716480](https://doi.org/10.1101/716480): STP and peak conductances.
- Wierenga & Wadman 2003, read only through the Hippocampus Hub data page: SC STP.
- Mitchell, Lupica & Dunwiddie 1993, *J Neurosci* 13:3439: A1R inhibition.

**Standard citations not yet checked by us:** Frey & Morris 1997; Redondo & Morris 2011; Jahr & Stevens 1990; Lisman 1989; Shouval, Bear & Cooper 2002; Clopath et al. 2010; Clopath et al. 2008; Barrett et al. 2009; Tsodyks & Markram 1997; Zenke & Gerstner 2017. Any parameter taken from these must first be read from the source and recorded with its conditions.
