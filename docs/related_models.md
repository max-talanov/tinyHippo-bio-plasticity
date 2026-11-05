# Related plasticity models

Biologically grounded plasticity models that can be compared with
[`hippocampal_plasticity_model.md`](../hippocampal_plasticity_model.md) ("model §n") and
[`hippocampal_downscaling_mechanisms.md`](../hippocampal_downscaling_mechanisms.md) ("#n"),
ranked by relevance.

**Ranking criteria**, in order of weight:

1. How many of our mechanisms the model shares: STP, Ca²⁺ induction, the E-LTP → tag/capture → L-LTP
   path, and the downscaling pathways #1–#13.
2. Whether it covers the hippocampus or CA1.
3. Whether it is biophysical, uses real time units and can be ported to NEURON.

**Citation status.** Every entry below was checked against PubMed on 2026-11-04 (authors, year,
title, journal, volume and pages; PMID and DOI given). This confirms the bibliographic details only.
Per `CLAUDE.md`, any parameter taken from these papers must still be checked against the paper and
recorded in `params.py` with its recording conditions.

## Tier 1: direct comparisons (tag/capture and Ca²⁺ induction, real time units)

| # | Reference | What it models | Maps to |
|---|---|---|---|
| 1 | Clopath C, Ziegler L, Vasilaki E, Büsing L, Gerstner W (2008). Tag-trigger-consolidation: a model of early and late long-term-potentiation and depression. *PLoS Comput Biol* 4:e1000248. PMID 19112486, [doi:10.1371/journal.pcbi.1000248](https://doi.org/10.1371/journal.pcbi.1000248) | Three-state tags that decay, captured by a PRP-gated trigger, for both LTP and LTD | model §2 (Fig. 2), #8, #9 |
| 2 | Barrett AB, Billings GO, Morris RGM, van Rossum MCW (2009). State based model of long-term potentiation and synaptic tagging and capture. *PLoS Comput Biol* 5:e1000259. PMID 19148264, [doi:10.1371/journal.pcbi.1000259](https://doi.org/10.1371/journal.pcbi.1000259) | State-based STC that reproduces Frey–Morris slice protocols | model §2, #5, #8, #9 |
| 3 | Luboeinski J, Tetzlaff C (2021). Memory consolidation and improvement by synaptic tagging and capture in recurrent neural networks. *Commun Biol* 4:275. PMID 33658641, [doi:10.1038/s42003-021-01778-y](https://doi.org/10.1038/s42003-021-01778-y) | Graupner–Brunel Ca²⁺ early phase plus STC late phase in a spiking recurrent network over hours | model §1 rows 3–6, §2 |
| 4 | Rodrigues YE, Tigaret CM, Marie H, O'Donnell C, Veltz R (2023). A stochastic model of hippocampal synaptic plasticity with geometrical readout of enzyme dynamics. *eLife* 12:e80152. PMID 37589251, [doi:10.7554/eLife.80152](https://doi.org/10.7554/eLife.80152) | Stochastic CA3→CA1 synapse: vesicle release, NMDAR, CaMKII/calcineurin; temperature- and [Ca²⁺]ₒ-dependent | S0–S3, model §2.1, #1, #4a |
| 5 | Kastellakis G, Silva AJ, Poirazi P (2016). Linking memories across time via neuronal and dendritic overlaps in model neurons with active dendrites. *Cell Rep* 17:1491–1504. PMID 27806290, [doi:10.1016/j.celrep.2016.10.015](https://doi.org/10.1016/j.celrep.2016.10.015) | Branch-local STC with dendritic PRP synthesis | `V_seg` per segment (model §2.1), #9 |
| 6 | Ziegler L, Zenke F, Kastner DB, Gerstner W (2015). Synaptic consolidation: from synapses to behavioral modeling. *J Neurosci* 35:1319–1334. PMID 25609644, [doi:10.1523/JNEUROSCI.3989-14.2015](https://doi.org/10.1523/JNEUROSCI.3989-14.2015) | Triplet STDP plus tag/capture, from slice STC to behaviour | model §2, §1 rows 4–6 |
| 7 | Smolen P, Baxter DA, Byrne JH (2012). Molecular constraints on synaptic tagging and maintenance of long-term potentiation: a predictive model. *PLoS Comput Biol* 8:e1002620. PMID 22876169, [doi:10.1371/journal.pcbi.1002620](https://doi.org/10.1371/journal.pcbi.1002620) | Biochemical STC (kinases, PRP) with timing predictions | model §2, #9 |
| 8 | O'Donnell C, Sejnowski TJ (2014). Selective memory generalization by spatial patterning of protein synthesis. *Neuron* 82:398–412. PMID 24742462, [doi:10.1016/j.neuron.2014.02.028](https://doi.org/10.1016/j.neuron.2014.02.028) | Spatially patterned protein synthesis; PRP competition | #9, model §2 |
| 9 | Deperrois N, Graupner M (2020). Short-term depression and long-term plasticity together tune sensitive range of synaptic plasticity. *PLoS Comput Biol* 16:e1008265. PMID 32976516, [doi:10.1371/journal.pcbi.1008265](https://doi.org/10.1371/journal.pcbi.1008265) | STD combined with a Ca²⁺-based long-term rule | Bridge from S0–S3 to S4; #1 + #4a |
| 10 | Inglebert Y, Aljadeff J, Brunel N, Debanne D (2020). Synaptic plasticity rules with physiological calcium levels. *PNAS* 117:33639–33648. PMID 33328274, [doi:10.1073/pnas.2013663117](https://doi.org/10.1073/pnas.2013663117) | Graupner–Brunel rule refit at 1.3–1.8 mM [Ca²⁺]ₒ, CA1 | `g_Ca` thresholds, #4a, `params.py` conditions |

## Tier 2: Ca²⁺ and voltage induction rules (the `V_seg` / `g_Ca` level)

| # | Reference | What it models | Maps to |
|---|---|---|---|
| 11 | Graupner M, Brunel N (2012). Calcium-based plasticity model explains sensitivity of synaptic changes to spike pattern, rate, and dendritic location. *PNAS* 109:3991–3996. PMID 22357758, [doi:10.1073/pnas.1109359109](https://doi.org/10.1073/pnas.1109359109) | Ca²⁺ threshold rule (θ_d, θ_p) with bistable efficacy | #4a, model §2.1 |
| 12 | Shouval HZ, Bear MF, Cooper LN (2002). A unified model of NMDA receptor-dependent bidirectional synaptic plasticity. *PNAS* 99:10831–10836. PMID 12136127, [doi:10.1073/pnas.152343099](https://doi.org/10.1073/pnas.152343099) | Calcium-control Ω function | model §2.1 (already cited) |
| 13 | Chindemi G, Abdellah M, Amsalem O, Benavides-Piccione R, Delattre V, Doron M, et al. (2022). A calcium-based plasticity model for predicting long-term potentiation and depression in the neocortex. *Nat Commun* 13:3038. PMID 35650191, [doi:10.1038/s41467-022-30214-w](https://doi.org/10.1038/s41467-022-30214-w) | Ca²⁺ rule in detailed NEURON cells with stochastic TM release (neocortex) | Methodological template for the NEURON implementation |
| 14 | Ebner C, Clopath C, Jedlicka P, Cuntz H (2019). Unifying long-term plasticity rules for excitatory synapses by modeling dendrites of cortical pyramidal neurons. *Cell Rep* 29:4295–4307.e6. PMID 31875541, [doi:10.1016/j.celrep.2019.11.068](https://doi.org/10.1016/j.celrep.2019.11.068) | Voltage-based rule in morphologically detailed dendrites | `V_seg`, dendritic cooperativity |
| 15 | Clopath C, Büsing L, Vasilaki E, Gerstner W (2010). Connectivity reflects coding: a model of voltage-based STDP with homeostasis. *Nat Neurosci* 13:344–352. PMID 20098420, [doi:10.1038/nn.2479](https://doi.org/10.1038/nn.2479) | Voltage-based STDP | model §2.1 (already cited) |
| 16 | Saudargienė A, Graham BP (2015). Inhibitory control of site-specific synaptic plasticity in a model CA1 pyramidal neuron. *Biosystems* 130:37–50. PMID 25769669, [doi:10.1016/j.biosystems.2015.03.001](https://doi.org/10.1016/j.biosystems.2015.03.001) | CA1 pyramidal cell in which interneuron inhibition gates site-specific Ca²⁺ plasticity | CA1 + interneurons, `V_seg` |
| 17 | Cutsuridis V, Cobb S, Graham BP (2010). Encoding and retrieval in a model of the hippocampal CA1 microcircuit. *Hippocampus* 20:423–446. PMID 19489002, [doi:10.1002/hipo.20661](https://doi.org/10.1002/hipo.20661) | CA1 microcircuit (PYR, BC, AAC, BSC, OLM) with plasticity during theta | Circuit analogue of [`plan.md`](plan.md) |
| 18 | Milstein AD, Li Y, Bittner KC, Grienberger C, Soltesz I, Magee JC, et al. (2021). Bidirectional synaptic plasticity rapidly modifies hippocampal representations. *eLife* 10:e73046. PMID 34882093, [doi:10.7554/eLife.73046](https://doi.org/10.7554/eLife.73046) | CA1 behavioral-timescale plasticity: plateau-gated, seconds-long eligibility traces | Alternative to graded tag amplitude, #4a |
| 19a | Graupner M, Brunel N (2007). STDP in a bistable synapse model based on CaMKII and associated signaling pathways. *PLoS Comput Biol* 3:e221. PMID 18052535, [doi:10.1371/journal.pcbi.0030221](https://doi.org/10.1371/journal.pcbi.0030221) | CaMKII–PP1 bistability driving STDP | Captured state (model §1 row 6), #5 |
| 19b | Zhabotinsky AM (2000). Bistability in the Ca²⁺/calmodulin-dependent protein kinase-phosphatase system. *Biophys J* 79:2211–2221. PMID 11053103, [doi:10.1016/S0006-3495(00)76469-1](https://doi.org/10.1016/S0006-3495(00)76469-1) | CaMKII–PP1 switch | model §1 row 6, #5 |
| 19c | Miller P, Zhabotinsky AM, Lisman JE, Wang XJ (2005). The stability of a stochastic CaMKII switch: dependence on the number of enzyme molecules and protein turnover. *PLoS Biol* 3:e107. PMID 15819604, [doi:10.1371/journal.pbio.0030107](https://doi.org/10.1371/journal.pbio.0030107) | How long the switch persists given molecule numbers and turnover | Persistence vs stabilization (model §1 row 6) |

## Tier 3: downscaling and homeostasis

| # | Reference | What it models | Maps to |
|---|---|---|---|
| 20 | Yeung LC, Shouval HZ, Blais BS, Cooper LN (2004). Synaptic homeostasis and input selectivity follow from a calcium-dependent plasticity model. *PNAS* 101:14943–14948. PMID 15466713, [doi:10.1073/pnas.0405555101](https://doi.org/10.1073/pnas.0405555101) | Sliding threshold through NMDAR-dependent metaplasticity | #10 |
| 21 | Chen JY, Lonjers P, Lee C, Chistiakova M, Volgushev M, Bazhenov M (2013). Heterosynaptic plasticity prevents runaway synaptic dynamics. *J Neurosci* 33:15915–15929. PMID 24089497, [doi:10.1523/JNEUROSCI.5088-12.2013](https://doi.org/10.1523/JNEUROSCI.5088-12.2013) | Heterosynaptic plasticity bounding Hebbian growth | #6 |
| 22 | Zenke F, Agnes EJ, Gerstner W (2015). Diverse synaptic plasticity mechanisms orchestrated to form and retrieve memories in spiking neural networks. *Nat Commun* 6:6922. PMID 25897632, [doi:10.1038/ncomms7922](https://doi.org/10.1038/ncomms7922) | Fast compensatory processes (heterosynaptic, inhibitory) alongside Hebbian learning | #6, #10, #12 (already cited) |
| 23 | Higgins D, Graupner M, Brunel N (2014). Memory maintenance in synapses with calcium-based plasticity in the presence of background activity. *PLoS Comput Biol* 10:e1003834. PMID 25275319, [doi:10.1371/journal.pcbi.1003834](https://doi.org/10.1371/journal.pcbi.1003834) | Memory decay under background firing with Ca²⁺ rules | #8, passive forgetting |
| 24 | Costa RP, Froemke RC, Sjöström PJ, van Rossum MCW (2015). Unified pre- and postsynaptic long-term plasticity enables reliable and flexible learning. *eLife* 4:e09457. PMID 26308579, [doi:10.7554/eLife.09457](https://doi.org/10.7554/eLife.09457); correction *eLife* 4:e11988 | Joint presynaptic (P_r / TM) and postsynaptic long-term plasticity | #4b, #2, scaling of TM `U` |
| 25 | Vogels TP, Sprekeler H, Zenke F, Clopath C, Gerstner W (2011). Inhibitory plasticity balances excitation and inhibition in sensory pathways and memory networks. *Science* 334:1569–1573. PMID 22075724, [doi:10.1126/science.1211095](https://doi.org/10.1126/science.1211095) | Inhibitory STDP for E/I balance | Interneuron synapses in the circuit |
| 26 | van Rossum MCW, Bi GQ, Turrigiano GG (2000). Stable Hebbian learning from spike timing-dependent plasticity. *J Neurosci* 20:8812–8821. PMID 11102489, [doi:10.1523/JNEUROSCI.20-23-08812.2000](https://doi.org/10.1523/JNEUROSCI.20-23-08812.2000) | STDP with multiplicative synaptic scaling | #12 (already cited) |
| 27 | Olcese U, Esser SK, Tononi G (2010). Sleep and synaptic renormalization: a computational study. *J Neurophysiol* 104:3476–3493. PMID 20926617, [doi:10.1152/jn.00593.2010](https://doi.org/10.1152/jn.00593.2010) | Sleep-dependent synaptic renormalization (SHY) | #11 |
| 28 | Wei Y, Krishnan GP, Bazhenov M (2016). Synaptic mechanisms of memory consolidation during sleep slow oscillations. *J Neurosci* 36:4231–4247. PMID 27076422, [doi:10.1523/JNEUROSCI.3648-15.2016](https://doi.org/10.1523/JNEUROSCI.3648-15.2016) | Slow-oscillation replay, potentiation and depression | #3, #11 |

## Tier 4: short-term plasticity (reference for S0–S3)

| # | Reference | Maps to |
|---|---|---|
| 29a | Tsodyks MV, Markram H (1997). The neural code between neocortical pyramidal neurons depends on neurotransmitter release probability. *PNAS* 94:719–723. PMID 9012851, [doi:10.1073/pnas.94.2.719](https://doi.org/10.1073/pnas.94.2.719) | TM depression, #1 |
| 29b | Markram H, Wang Y, Tsodyks M (1998). Differential signaling via the same axon of neocortical pyramidal neurons. *PNAS* 95:5323–5328. PMID 9560274, [doi:10.1073/pnas.95.9.5323](https://doi.org/10.1073/pnas.95.9.5323) | TM with facilitation |
| 30 | Dittman JS, Kreitzer AC, Regehr WG (2000). Interplay between facilitation, depression, and residual calcium at three presynaptic terminals. *J Neurosci* 20:1374–1385. PMID 10662828, [doi:10.1523/JNEUROSCI.20-04-01374.2000](https://doi.org/10.1523/JNEUROSCI.20-04-01374.2000) | STP with Ca²⁺-dependent recovery; includes Schaffer collateral |
| 31 | Hennig MH (2013). Theoretical models of synaptic short term plasticity. *Front Comput Neurosci* 7:45. PMID 23626536, [doi:10.3389/fncom.2013.00045](https://doi.org/10.3389/fncom.2013.00045) | Review comparing STP models. PubMed also lists a second record with the same title (7:154, PMID 24198783) |

## Tier 5: late-LTP maintenance and system consolidation (mostly outside the NEURON scope)

| # | Reference | Maps to |
|---|---|---|
| 32a | Helfer P, Shultz TR (2018). Coupled feedback loops maintain synaptic long-term potentiation: a computational model of PKMzeta synthesis and AMPA receptor trafficking. *PLoS Comput Biol* 14:e1006147. PMID 29813048, [doi:10.1371/journal.pcbi.1006147](https://doi.org/10.1371/journal.pcbi.1006147) | L-LTP maintenance (model §1 row 6) |
| 32b | Jalil SJ, Sacktor TC, Shouval HZ (2015). Atypical PKCs in memory maintenance: the roles of feedback and redundancy. *Learn Mem* 22:344–353. PMID 26077687, [doi:10.1101/lm.038844.115](https://doi.org/10.1101/lm.038844.115) | L-LTP maintenance |
| 33a | Fusi S, Drew PJ, Abbott LF (2005). Cascade models of synaptically stored memories. *Neuron* 45:599–611. PMID 15721245, [doi:10.1016/j.neuron.2005.02.001](https://doi.org/10.1016/j.neuron.2005.02.001) | Multi-timescale synapse (already cited) |
| 33b | Benna MK, Fusi S (2016). Computational principles of synaptic memory consolidation. *Nat Neurosci* 19:1697–1706. PMID 27694992, [doi:10.1038/nn.4401](https://doi.org/10.1038/nn.4401) | Multi-timescale synapse (already cited) |
| 34a | Roxin A, Fusi S (2013). Efficient partitioning of memory systems and its importance for memory consolidation. *PLoS Comput Biol* 9:e1003146. PMID 23935470, [doi:10.1371/journal.pcbi.1003146](https://doi.org/10.1371/journal.pcbi.1003146) | System consolidation (model §3) |
| 34b | McClelland JL, McNaughton BL, O'Reilly RC (1995). Why there are complementary learning systems in the hippocampus and neocortex. *Psychol Rev* 102:419–457. PMID 7624455, [doi:10.1037/0033-295X.102.3.419](https://doi.org/10.1037/0033-295X.102.3.419) | System consolidation (model §3) |

## Use in the plan

- **S4–S6 benchmarks:** #1 and #2. They are the standard STC models and simulate the same slice
  protocols that the Fig. 2 falsification test needs.
- **Biophysical templates for the NEURON/CA1 setup:** #4, #10 and #13. These are the entries with
  explicit [Ca²⁺]ₒ and temperature dependence.
- **Closest to `V_seg`:** #5, which already implements branch-level tag/capture.
