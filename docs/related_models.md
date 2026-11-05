# Related plasticity models

Plasticity models that can be compared with
[`hippocampal_plasticity_model.md`](../hippocampal_plasticity_model.md) ("model §n") and
[`hippocampal_downscaling_mechanisms.md`](../hippocampal_downscaling_mechanisms.md) ("#n").

## How the list is ordered

Our model is mechanistic: weight changes come from biochemical and biophysical dynamics on several
timescales, not from one learning rule. The downscaling document separates three levels of
description: sensor, effector and the *rule* they implement. It treats rules (STDP, BCM, homeostasis)
as acceptance tests, not as components. Models are therefore ranked on two keys:

1. **Level of description**, from most to least comparable:
   - **A. Biochemical.** Molecular kinetics: kinases, phosphatases, receptor trafficking, protein
     synthesis. These are true peers of our model.
   - **B. Multi-timescale phenomenological.** No biochemistry, but separate state variables for
     E-LTP, tag, capture and L-LTP with their own time constants, the same structure as model §2.
   - **C. Ca²⁺ / voltage threshold rules.** One induction variable mapped to a weight change. They
     match only the `g_Ca(V_seg)` stage (model §2.1).
   - **D. Rule level.** STDP, BTSP and homeostatic rules expressed as spike-timing or rate updates.
     They are not comparison models. They list what our model must reproduce when driven with the
     matching protocol.
2. **Timescales covered**, given as rows of model §1 Table 1: 1 transmission, 2 STP, 3 Ca²⁺/kinase,
   4 E-LTP, 5 tag/capture, 6 L-LTP, 7 SWR replay, 8 system consolidation. More rows covered, and
   especially rows 3–6, ranks higher.

A title containing "STDP" does not place a model at level D. Graupner & Brunel (2007), for example,
is a CaMKII/PP1 kinetic model that *produces* STDP as an output. It sits at level A.

STP models (S0–S3) form their own reference section, since STP is a separate mechanism, not an
alternative to the long-term path. System-consolidation models are listed last as out of scope.

**Citation status.** Every entry was checked against PubMed or Europe PMC on 2026-11-04/05 (authors,
year, title, journal, volume and pages; PMID and DOI given). This confirms the bibliographic details
only. Per `CLAUDE.md`, any parameter taken from these papers must still be checked against the paper
and recorded in `params.py` with its recording conditions.

## A. Biochemical models (true peers)

| # | Reference | What it models | Rows | Maps to |
|---|---|---|---|---|
| A1 | Smolen P, Baxter DA, Byrne JH (2012). Molecular constraints on synaptic tagging and maintenance of long-term potentiation: a predictive model. *PLoS Comput Biol* 8:e1002620. PMID 22876169, [doi:10.1371/journal.pcbi.1002620](https://doi.org/10.1371/journal.pcbi.1002620) | Kinase-based STC: tag set by CaMKII/PKA, capture by PRP, with timing predictions | 3–6 | model §2, #8, #9 |
| A2 | Rodrigues YE, Tigaret CM, Marie H, O'Donnell C, Veltz R (2023). A stochastic model of hippocampal synaptic plasticity with geometrical readout of enzyme dynamics. *eLife* 12:e80152. PMID 37589251, [doi:10.7554/eLife.80152](https://doi.org/10.7554/eLife.80152) | Stochastic CA3→CA1 synapse: vesicle release, NMDAR, CaMKII/calcineurin. Depends on temperature and [Ca²⁺]ₒ | 1–4 | S0–S3, model §2.1, #1, #4a |
| A3 | Smolen P, Baxter DA, Byrne JH (2006). A model of the roles of essential kinases in the induction and expression of late long-term potentiation. *Biophys J* 90:2760–2775. PMID 16415049, [doi:10.1529/biophysj.105.072470](https://doi.org/10.1529/biophysj.105.072470) | CaMKII, PKA, MAPK and transcription in L-LTP induction and expression | 3–6 | model §1 rows 3–6 |
| A4 | Helfer P, Shultz TR (2018). Coupled feedback loops maintain synaptic long-term potentiation: a computational model of PKMzeta synthesis and AMPA receptor trafficking. *PLoS Comput Biol* 14:e1006147. PMID 29813048, [doi:10.1371/journal.pcbi.1006147](https://doi.org/10.1371/journal.pcbi.1006147) | PKMζ synthesis plus AMPAR trafficking feedback | 4–6 | L-LTP stabilization vs persistence (model §1 row 6) |
| A5 | Hayer A, Bhalla US (2005). Molecular switches at the synapse emerge from receptor and kinase traffic. *PLoS Comput Biol* 1:137–154. PMID 16110334, [doi:10.1371/journal.pcbi.0010020](https://doi.org/10.1371/journal.pcbi.0010020) | Bistability from AMPAR and CaMKII trafficking | 3, 4, 6 | Captured state, #8 |
| A6 | Graupner M, Brunel N (2007). STDP in a bistable synapse model based on CaMKII and associated signaling pathways. *PLoS Comput Biol* 3:e221. PMID 18052535, [doi:10.1371/journal.pcbi.0030221](https://doi.org/10.1371/journal.pcbi.0030221) | CaMKII/PP1/calcineurin kinetics. STDP is the output, not the rule | 1, 3, 6 | #4a, #5, model §2.1 |
| A7 | Bhalla US, Iyengar R (1999). Emergent properties of networks of biological signaling pathways. *Science* 283:381–387. PMID 9888852, [doi:10.1126/science.283.5400.381](https://doi.org/10.1126/science.283.5400.381) | Coupled MAPK/PKC/CaMKII networks, bistability and persistence | 3, 6 | model §1 rows 3, 6 |
| A8 | Bhalla US (2017). Synaptic input sequence discrimination on behavioral timescales mediated by reaction-diffusion chemistry in dendrites. *eLife* 6:e25827. PMID 28422010, [doi:10.7554/eLife.25827](https://doi.org/10.7554/eLife.25827) | Dendritic reaction–diffusion that integrates input over seconds | 3, 4 | `V_seg` segment state (model §2.1) |
| A9 | Ajay SM, Bhalla US (2007). A propagating ERKII switch forms zones of elevated dendritic activation correlated with plasticity. *HFSP J* 1:49–66. PMID 19404460, [doi:10.2976/1.2721383](https://doi.org/10.2976/1.2721383) | Propagating ERK switch that defines dendritic plasticity zones | 3, 4 | Per-segment state, #6 |
| A10 | Mäki-Marttunen T, Iannella N, Edwards AG, Einevoll GT, Blackwell KT (2020). A unified computational model for cortical post-synaptic plasticity. *eLife* 9:e55714. PMID 32729828, [doi:10.7554/eLife.55714](https://doi.org/10.7554/eLife.55714) | Postsynaptic biochemistry (CaMKII, PKA, PKC, AMPAR phosphorylation and trafficking); cortex | 3, 4 | #4a, model §2.1 |
| A11 | Jalil SJ, Sacktor TC, Shouval HZ (2015). Atypical PKCs in memory maintenance: the roles of feedback and redundancy. *Learn Mem* 22:344–353. PMID 26077687, [doi:10.1101/lm.038844.115](https://doi.org/10.1101/lm.038844.115) | PKMζ/PKCι/λ feedback in maintenance | 6 | model §1 row 6 |
| A12 | Miller P, Zhabotinsky AM, Lisman JE, Wang XJ (2005). The stability of a stochastic CaMKII switch: dependence on the number of enzyme molecules and protein turnover. *PLoS Biol* 3:e107. PMID 15819604, [doi:10.1371/journal.pbio.0030107](https://doi.org/10.1371/journal.pbio.0030107) | Lifetime of the switch given molecule numbers and turnover | 6 | Persistence (model §1 row 6) |
| A13 | Zhabotinsky AM (2000). Bistability in the Ca²⁺/calmodulin-dependent protein kinase-phosphatase system. *Biophys J* 79:2211–2221. PMID 11053103, [doi:10.1016/S0006-3495(00)76469-1](https://doi.org/10.1016/S0006-3495(00)76469-1) | CaMKII–PP1 bistable switch | 3, 6 | #5 |
| A14 | Lisman JE (1985). A mechanism for memory storage insensitive to molecular turnover: a bistable autophosphorylating kinase. *PNAS* 82:3055–3057. PMID 2986148, [doi:10.1073/pnas.82.9.3055](https://doi.org/10.1073/pnas.82.9.3055) | Original kinase-switch proposal | 6 | model §1 row 6 |
| A15 | Kim B, Hawes SL, Gillani F, Wallace LJ, Blackwell KT (2013). Signaling pathways involved in striatal synaptic plasticity are sensitive to temporal pattern and exhibit spatial specificity. *PLoS Comput Biol* 9:e1002953. PMID 23516346, [doi:10.1371/journal.pcbi.1002953](https://doi.org/10.1371/journal.pcbi.1002953) | Striatal PKA/CaMKII signalling. Useful for method only, not region | 3 | Method only |
| A16 | Jędrzejewska-Szmek J, Damodaran S, Dorman DB, Blackwell KT (2017). Calcium dynamics predict direction of synaptic plasticity in striatal spiny projection neurons. *Eur J Neurosci* 45:1044–1056. PMID 27233469, [doi:10.1111/ejn.13287](https://doi.org/10.1111/ejn.13287) | Ca²⁺ amplitude and duration as a readout for LTP/LTD in a NEURON model; striatum | 1, 3 | `g_Ca` thresholds, method |

Review: Kotaleski JH, Blackwell KT (2010). Modelling the molecular mechanisms of synaptic plasticity
using systems biology approaches. *Nat Rev Neurosci* 11:239–251. PMID 20300102,
[doi:10.1038/nrn2807](https://doi.org/10.1038/nrn2807).

## B. Multi-timescale phenomenological models (the tag/capture structure)

| # | Reference | What it models | Rows | Maps to |
|---|---|---|---|---|
| B1 | Clopath C, Ziegler L, Vasilaki E, Büsing L, Gerstner W (2008). Tag-trigger-consolidation: a model of early and late long-term-potentiation and depression. *PLoS Comput Biol* 4:e1000248. PMID 19112486, [doi:10.1371/journal.pcbi.1000248](https://doi.org/10.1371/journal.pcbi.1000248) | Three-state decaying tags with PRP-gated capture, LTP and LTD | 4–6 | model §2 (Fig. 2), #8, #9 |
| B2 | Barrett AB, Billings GO, Morris RGM, van Rossum MCW (2009). State based model of long-term potentiation and synaptic tagging and capture. *PLoS Comput Biol* 5:e1000259. PMID 19148264, [doi:10.1371/journal.pcbi.1000259](https://doi.org/10.1371/journal.pcbi.1000259) | State-based STC that reproduces Frey–Morris slice protocols | 4–6 | model §2, #5, #8, #9 |
| B3 | Luboeinski J, Tetzlaff C (2021). Memory consolidation and improvement by synaptic tagging and capture in recurrent neural networks. *Commun Biol* 4:275. PMID 33658641, [doi:10.1038/s42003-021-01778-y](https://doi.org/10.1038/s42003-021-01778-y) | Ca²⁺ early phase plus STC late phase in a spiking network over hours | 3–6 | model §1 rows 3–6, §2 |
| B4 | Kastellakis G, Silva AJ, Poirazi P (2016). Linking memories across time via neuronal and dendritic overlaps in model neurons with active dendrites. *Cell Rep* 17:1491–1504. PMID 27806290, [doi:10.1016/j.celrep.2016.10.015](https://doi.org/10.1016/j.celrep.2016.10.015) | Branch-local STC with dendritic PRP synthesis | 3–6 | `V_seg` per segment, #9 |
| B5 | O'Donnell C, Sejnowski TJ (2014). Selective memory generalization by spatial patterning of protein synthesis. *Neuron* 82:398–412. PMID 24742462, [doi:10.1016/j.neuron.2014.02.028](https://doi.org/10.1016/j.neuron.2014.02.028) | Spatially patterned PRP and competition between synapses | 5–6 | #9, model §2 |
| B6 | Ziegler L, Zenke F, Kastner DB, Gerstner W (2015). Synaptic consolidation: from synapses to behavioral modeling. *J Neurosci* 35:1319–1334. PMID 25609644, [doi:10.1523/JNEUROSCI.3989-14.2015](https://doi.org/10.1523/JNEUROSCI.3989-14.2015) | Tag/capture with STDP-based (triplet) induction | 4–6 | model §2. Its induction stage is level D |
| B7 | Benna MK, Fusi S (2016). Computational principles of synaptic memory consolidation. *Nat Neurosci* 19:1697–1706. PMID 27694992, [doi:10.1038/nn.4401](https://doi.org/10.1038/nn.4401) | Chain of coupled variables spanning many timescales | 4–8 | Multi-timescale structure overall |
| B8 | Fusi S, Drew PJ, Abbott LF (2005). Cascade models of synaptically stored memories. *Neuron* 45:599–611. PMID 15721245, [doi:10.1016/j.neuron.2005.02.001](https://doi.org/10.1016/j.neuron.2005.02.001) | Cascade of metastable states | 4–6 | Multi-timescale structure overall |

## C. Ca²⁺ / voltage threshold rules (induction stage only)

| # | Reference | What it models | Rows | Maps to |
|---|---|---|---|---|
| C1 | Inglebert Y, Aljadeff J, Brunel N, Debanne D (2020). Synaptic plasticity rules with physiological calcium levels. *PNAS* 117:33639–33648. PMID 33328274, [doi:10.1073/pnas.2013663117](https://doi.org/10.1073/pnas.2013663117) | Ca²⁺ threshold rule fit at 1.3–1.8 mM [Ca²⁺]ₒ, CA1 | 1, 3 | `g_Ca` thresholds, `params.py` conditions |
| C2 | Chindemi G, Abdellah M, Amsalem O, Benavides-Piccione R, Delattre V, Doron M, et al. (2022). A calcium-based plasticity model for predicting long-term potentiation and depression in the neocortex. *Nat Commun* 13:3038. PMID 35650191, [doi:10.1038/s41467-022-30214-w](https://doi.org/10.1038/s41467-022-30214-w) | Ca²⁺ rule in detailed NEURON cells with stochastic TM release; neocortex | 1–3 | Template for the NEURON implementation |
| C3 | Deperrois N, Graupner M (2020). Short-term depression and long-term plasticity together tune sensitive range of synaptic plasticity. *PLoS Comput Biol* 16:e1008265. PMID 32976516, [doi:10.1371/journal.pcbi.1008265](https://doi.org/10.1371/journal.pcbi.1008265) | STD feeding a Ca²⁺ rule | 2, 3 | Bridge from S0–S3 to S4; #1 + #4a |
| C4 | Graupner M, Brunel N (2012). Calcium-based plasticity model explains sensitivity of synaptic changes to spike pattern, rate, and dendritic location. *PNAS* 109:3991–3996. PMID 22357758, [doi:10.1073/pnas.1109359109](https://doi.org/10.1073/pnas.1109359109) | Two Ca²⁺ thresholds (θ_d, θ_p) and bistable efficacy | 3 | #4a, model §2.1 |
| C5 | Shouval HZ, Bear MF, Cooper LN (2002). A unified model of NMDA receptor-dependent bidirectional synaptic plasticity. *PNAS* 99:10831–10836. PMID 12136127, [doi:10.1073/pnas.152343099](https://doi.org/10.1073/pnas.152343099) | NMDAR Ca²⁺ mapped to weight change through the Ω function | 1, 3 | model §2.1 (already cited) |
| C6 | Yeung LC, Shouval HZ, Blais BS, Cooper LN (2004). Synaptic homeostasis and input selectivity follow from a calcium-dependent plasticity model. *PNAS* 101:14943–14948. PMID 15466713, [doi:10.1073/pnas.0405555101](https://doi.org/10.1073/pnas.0405555101) | Sliding threshold through NMDAR-dependent metaplasticity | 3 (+ slow θ) | #10 |
| C7 | Higgins D, Graupner M, Brunel N (2014). Memory maintenance in synapses with calcium-based plasticity in the presence of background activity. *PLoS Comput Biol* 10:e1003834. PMID 25275319, [doi:10.1371/journal.pcbi.1003834](https://doi.org/10.1371/journal.pcbi.1003834) | How background activity erodes memories under Ca²⁺ rules | 3, 4 | #8 |
| C8 | Saudargienė A, Graham BP (2015). Inhibitory control of site-specific synaptic plasticity in a model CA1 pyramidal neuron. *Biosystems* 130:37–50. PMID 25769669, [doi:10.1016/j.biosystems.2015.03.001](https://doi.org/10.1016/j.biosystems.2015.03.001) | Ca²⁺-detector plasticity in a CA1 cell, gated by interneuron inhibition | 1, 3 | CA1 + interneurons, `V_seg` |
| C9 | Ebner C, Clopath C, Jedlicka P, Cuntz H (2019). Unifying long-term plasticity rules for excitatory synapses by modeling dendrites of cortical pyramidal neurons. *Cell Rep* 29:4295–4307.e6. PMID 31875541, [doi:10.1016/j.celrep.2019.11.068](https://doi.org/10.1016/j.celrep.2019.11.068) | Voltage-based rule in detailed dendrites | 1, 3 | `V_seg`, dendritic cooperativity |

## D. Rule-level models (acceptance-test references, not comparisons)

What each rule should be reproduced by, when our model is driven with the matching protocol.

| # | Reference | Rule | Acceptance test for |
|---|---|---|---|
| D1 | Clopath C, Büsing L, Vasilaki E, Gerstner W (2010). Connectivity reflects coding: a model of voltage-based STDP with homeostasis. *Nat Neurosci* 13:344–352. PMID 20098420, [doi:10.1038/nn.2479](https://doi.org/10.1038/nn.2479) | Voltage-based STDP | Pairing and frequency protocols via model §2.1 |
| D2 | Milstein AD, Li Y, Bittner KC, Grienberger C, Soltesz I, Magee JC, et al. (2021). Bidirectional synaptic plasticity rapidly modifies hippocampal representations. *eLife* 10:e73046. PMID 34882093, [doi:10.7554/eLife.73046](https://doi.org/10.7554/eLife.73046) | BTSP (CA1, plateau-gated, seconds) | Seconds-long induction in CA1; #4a |
| D3 | Costa RP, Froemke RC, Sjöström PJ, van Rossum MCW (2015). Unified pre- and postsynaptic long-term plasticity enables reliable and flexible learning. *eLife* 4:e09457. PMID 26308579, [doi:10.7554/eLife.09457](https://doi.org/10.7554/eLife.09457); correction *eLife* 4:e11988 | Joint pre (P_r) and post STDP | #4b, #2 |
| D4 | Chen JY, Lonjers P, Lee C, Chistiakova M, Volgushev M, Bazhenov M (2013). Heterosynaptic plasticity prevents runaway synaptic dynamics. *J Neurosci* 33:15915–15929. PMID 24089497, [doi:10.1523/JNEUROSCI.5088-12.2013](https://doi.org/10.1523/JNEUROSCI.5088-12.2013) | Heterosynaptic normalization | #6 |
| D5 | Zenke F, Agnes EJ, Gerstner W (2015). Diverse synaptic plasticity mechanisms orchestrated to form and retrieve memories in spiking neural networks. *Nat Commun* 6:6922. PMID 25897632, [doi:10.1038/ncomms7922](https://doi.org/10.1038/ncomms7922) | Fast compensatory rules | #6, #10, #12 (already cited) |
| D6 | van Rossum MCW, Bi GQ, Turrigiano GG (2000). Stable Hebbian learning from spike timing-dependent plasticity. *J Neurosci* 20:8812–8821. PMID 11102489, [doi:10.1523/JNEUROSCI.20-23-08812.2000](https://doi.org/10.1523/JNEUROSCI.20-23-08812.2000) | STDP plus multiplicative scaling | #12 (already cited) |
| D7 | Vogels TP, Sprekeler H, Zenke F, Clopath C, Gerstner W (2011). Inhibitory plasticity balances excitation and inhibition in sensory pathways and memory networks. *Science* 334:1569–1573. PMID 22075724, [doi:10.1126/science.1211095](https://doi.org/10.1126/science.1211095) | Inhibitory STDP | E/I balance at interneuron synapses |
| D8 | Olcese U, Esser SK, Tononi G (2010). Sleep and synaptic renormalization: a computational study. *J Neurophysiol* 104:3476–3493. PMID 20926617, [doi:10.1152/jn.00593.2010](https://doi.org/10.1152/jn.00593.2010) | Sleep downscaling (SHY) | #11 |
| D9 | Wei Y, Krishnan GP, Bazhenov M (2016). Synaptic mechanisms of memory consolidation during sleep slow oscillations. *J Neurosci* 36:4231–4247. PMID 27076422, [doi:10.1523/JNEUROSCI.3648-15.2016](https://doi.org/10.1523/JNEUROSCI.3648-15.2016) | STDP during slow-oscillation replay | #3, #11 |
| D10 | Cutsuridis V, Cobb S, Graham BP (2010). Encoding and retrieval in a model of the hippocampal CA1 microcircuit. *Hippocampus* 20:423–446. PMID 19489002, [doi:10.1002/hipo.20661](https://doi.org/10.1002/hipo.20661) | STDP-like learning in a CA1 microcircuit | Circuit reference for [`plan.md`](plan.md), not for plasticity |

## Short-term plasticity (reference for S0–S3)

| # | Reference | Maps to |
|---|---|---|
| S1 | Tsodyks MV, Markram H (1997). The neural code between neocortical pyramidal neurons depends on neurotransmitter release probability. *PNAS* 94:719–723. PMID 9012851, [doi:10.1073/pnas.94.2.719](https://doi.org/10.1073/pnas.94.2.719) | TM depression, #1 |
| S2 | Markram H, Wang Y, Tsodyks M (1998). Differential signaling via the same axon of neocortical pyramidal neurons. *PNAS* 95:5323–5328. PMID 9560274, [doi:10.1073/pnas.95.9.5323](https://doi.org/10.1073/pnas.95.9.5323) | TM with facilitation |
| S3 | Dittman JS, Kreitzer AC, Regehr WG (2000). Interplay between facilitation, depression, and residual calcium at three presynaptic terminals. *J Neurosci* 20:1374–1385. PMID 10662828, [doi:10.1523/JNEUROSCI.20-04-01374.2000](https://doi.org/10.1523/JNEUROSCI.20-04-01374.2000) | STP with Ca²⁺-dependent recovery; includes Schaffer collateral |
| S4 | Hennig MH (2013). Theoretical models of synaptic short term plasticity. *Front Comput Neurosci* 7:45. PMID 23626536, [doi:10.3389/fncom.2013.00045](https://doi.org/10.3389/fncom.2013.00045) | Review comparing STP models. PubMed also lists a second record with the same title (7:154, PMID 24198783) |

A2 (Rodrigues 2023) and C3 (Deperrois 2020) also model STP, coupled to the long-term path.

## Out of scope: system consolidation (model §3)

| # | Reference |
|---|---|
| X1 | Roxin A, Fusi S (2013). Efficient partitioning of memory systems and its importance for memory consolidation. *PLoS Comput Biol* 9:e1003146. PMID 23935470, [doi:10.1371/journal.pcbi.1003146](https://doi.org/10.1371/journal.pcbi.1003146) |
| X2 | McClelland JL, McNaughton BL, O'Reilly RC (1995). Why there are complementary learning systems in the hippocampus and neocortex. *Psychol Rev* 102:419–457. PMID 7624455, [doi:10.1037/0033-295X.102.3.419](https://doi.org/10.1037/0033-295X.102.3.419) |

## Use in the plan

- **Peers for S4–S6:** A1 (biochemical STC) and A2 (hippocampal synapse in real conditions). These
  are the models whose mechanisms, not only behaviour, our model should be compared with.
- **Time-domain benchmarks for the Fig. 2 test:** B1 and B2. They simulate the same slice protocols.
- **`V_seg` and dendritic locality:** A8, A9 and B4.
- **Parameter conditions ([Ca²⁺]ₒ, temperature):** A2 and C1.
- **Rule-level checks:** each mechanism added from the downscaling list should reproduce the matching
  D entry when driven with the matching protocol.
