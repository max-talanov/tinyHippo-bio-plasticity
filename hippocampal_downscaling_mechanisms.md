# Hippocampal Downscaling Mechanisms

Companion to [`hippocampal_plasticity_model.md`](hippocampal_plasticity_model.md) ("model §n"; hardware
sections in [`hippocampal_memristive_implementation.md`](hippocampal_memristive_implementation.md),
"implementation §n"). The model document lays out the *upscaling* path: STP → Ca²⁺/kinase → E-LTP →
tag & capture → L-LTP (the synaptic correlate of cellular consolidation) → SWR replay → system
consolidation. This one lists the mechanisms that *weaken* synapses or keep their total bounded. Each
entry gives its timescale, its hook in the circuit model (model §2 tag/capture, implementation §7.2
synaptic-area "activity-dependent weight decay", model §2.1 `V_seg`, model §3 replay), and its primary
literature.

**Levels of description.** Each entry is a *molecular pathway*. Plasticity rules (Hebbian,
anti-Hebbian, STDP, BCM, homeostatic) are a separate, higher level. They say *which activity
pattern* changes a weight, not *how*. One rule can be carried out by several pathways: STDP
depression runs through 4a in some preparations and 4b in others. One pathway can also serve
several rules: postsynaptic NMDAR → phosphatase signalling (4a) underlies both rate-dependent LTD
and depotentiation (5). Every entry is therefore described on three levels:

| Level | Question | Examples |
|---|---|---|
| Sensor (induction) | What detects the triggering activity or state? | Postsynaptic NMDAR Ca²⁺, group I mGluR → IP3/Ca²⁺ stores, presynaptic CB1 + NMDAR, somatic Ca²⁺ → CaMKIV |
| Effector (expression) | What physically weakens the synapse? | Calcineurin/PP1 dephosphorylation of GluA1, clathrin-dependent AMPAR endocytosis, local translation of Arc/STEP, lower release probability, spine removal |
| Rule it implements | Which activity pattern produces it? | Rate-dependent LTD, t-LTD (STDP), heterosynaptic normalization, BCM threshold, firing-rate homeostasis |

Only the sensor and effector levels should be modelled as mechanisms (a dataclass plus a `build_*`
function, per `CLAUDE.md`). The rule is what a mechanism should *reproduce* when driven with the
corresponding protocol. It is an acceptance test, not a component.

![Fifteen molecular downscaling pathways on the same logarithmic time axis as Fig. 1 of the model document, from 1 ms to 10 years, ordered by onset so the bars form a descending staircase. Vesicle depletion, presynaptic GPCR inhibition and SWR-triggered NMDAR depression start in the millisecond range; NMDAR/phosphatase LTD, endocannabinoid t-LTD, depotentiation, heterosynaptic and tag-related depression start at seconds to minutes; BCM metaplasticity, sleep renormalization and synaptic scaling start at tens of minutes to hours; protein turnover runs from hours (activity-driven degradation) to weeks (basal turnover); pruning and active forgetting start at days and extend to a year.](figures/downscaling_timescale_axis.png)

*Fig. D1. Downscaling mechanisms on the log time axis of model Fig. 1, ordered
by onset (ties broken by end), as in Fig. 1. A bar's position marks onset and its
length marks characteristic duration. Dotted tails
are recurring or extended effects. Spans are order-of-magnitude summaries of the
references below, not fitted values. Regenerate with
`python3 figures/make_downscaling_timescale_axis.py`.*

**Citation status.** The entries below were compiled for orientation. The
bibliographic details of Norimoto 2018, González-Rueda 2018, Oh 2015, Kim & Tsien
2008, Fonseca 2004, Royer & Paré 2003, Branco 2008, Migues 2016, Wang 2020,
Li 2017, Sajikumar & Frey 2004 and Miyawaki & Diba 2016 have been checked against
PubMed/PMC or publisher records (DOIs given), as have Sjöström 2003, Andrade-Talavera 2016,
Huang 1999, Lee 2000 and Ibata 2008, and for #14 Crick 1984, Ehlers 2003, Colledge 2003,
Hou 2006, Dörrbaum 2018 and Heo 2018. The rest are standard citations that
have not been checked. Per `CLAUDE.md`, a parameter taken from any of these must
be checked against the source and recorded in `params.py` with its recording
conditions before use.

## Summary

| # | Molecular pathway | Timescale | Sensor | Effector | Site | Rule it implements | Model hook |
|---|---|---|---|---|---|---|---|
| 1 | Vesicle-pool depletion | 10 ms–10 s | presynaptic spike → VGCC Ca²⁺ | depletion of the readily releasable pool | pre | use-dependent (frequency) depression | STP (S0–S3), TM depression term |
| 2 | Presynaptic GPCR inhibition | 50 ms–min (tonic: hours) | A1R, GABA_B, group II/III mGluR (G_i/o) | Gβγ inhibition of VGCCs and release machinery → lower P_r | pre | neuromodulatory / tonic gain control | scaling of TM `U`, implementation §7.2 |
| 3 | SWR-triggered NMDAR-dependent depression | ripple 100 ms, effect hours, recurs over days | postsynaptic NMDAR during SWR bursts | AMPAR weakening (downstream not resolved) | post | state-gated depression of non-replayed inputs | model §3 replay |
| 4a | NMDAR → calcineurin/PP1 LTD | induction s–min, expression hours | moderate postsynaptic NMDAR Ca²⁺ | calcineurin → PP1; GluA1-S845 dephosphorylation; AMPAR endocytosis | post | rate-dependent LTD (low-frequency) | low-Ca branch of `g_Ca(V_seg)`, model §2.1 |
| 4b | Endocannabinoid → CB1 t-LTD | induction s–min, expression hours | postsynaptic mGluR + VGCC Ca²⁺ → eCB; presynaptic CB1 + NMDAR coincidence | lower P_r (presynaptic calcineurin in CA1) | pre (induced post) | STDP depression (post-before-pre) | negative STDP lobe, implementation §7.5; scaling of `U` |
| 5 | PP1-mediated depotentiation | window 1 min–1 hr | NMDAR Ca²⁺ + extracellular adenosine (A1R) after LFS | PP1 reverses CaMKII/PKA phosphorylation; AMPAR removal | post | time-limited reversal of recent LTP | active reset of the model §2 tag |
| 6 | IP3R/calcineurin heterosynaptic depression | min–hours | neighbour potentiation → group I mGluR, IP3R Ca²⁺ release | calcineurin → shrinkage of inactive spines, AMPAR loss | post (unstimulated synapses) | heterosynaptic normalization | per-segment conservation (`V_seg` unit) |
| 7 | mGluR5 → local-translation LTD | min–1 day | group I mGluR (G_q) | local translation of Arc, STEP, MAP1B → AMPAR endocytosis | post | homosynaptic, protein-synthesis-dependent LTD | PRP pool, model §2 |
| 8 | Constitutive GluA2 endocytosis (E-LTP decay) | τ ≈ 1–4 hr | none: absence of capture | removal of inserted GluA2-AMPARs | post | decay of unconsolidated LTP | τ_tag decay in Fig. 2 |
| 9 | PRP competition | 30 min–8 hr | none: finite resource | limited PRPs (synthesis vs proteasomal degradation) | post (cell-wide pool) | competition for consolidation | capture threshold, model §2 |
| 10 | NMDAR subunit (GluN2A/2B) threshold shift | 30 min–days | integrated postsynaptic activity history | GluN2A/GluN2B ratio change | post | BCM sliding threshold | moves θ_p of `g_Ca` |
| 11 | Homer1a–mGluR5 sleep scaling-down | hours, each sleep cycle | sleep state: falling noradrenaline, rising adenosine → Homer1a | ligand-independent mGluR5 signalling → GluA1 dephosphorylation, AMPAR removal | post | SHY (wake potentiation, sleep renormalization) | global downscaling between replay epochs |
| 12 | CaMKIV/TNFα synaptic scaling | 12 hr–days | somatic Ca²⁺ → CaMKIV → transcription; glial TNFα | multiplicative change in synaptic AMPARs (Arc-dependent endocytosis) | post (and pre: P_r) | firing-rate homeostasis | implementation §7.2 weight decay |
| 13 | Complement/microglial pruning; Rac1/cofilin forgetting | days–months | C1q/C3 deposition at weak synapses | microglial CR3 phagocytosis; actin disassembly | whole synapse | structural forgetting | removal of uncaptured traces |
| 14 | Ubiquitin–proteasome degradation and protein turnover | hours (activity-driven) to days–weeks (basal) | NMDAR Ca²⁺ or sustained activity → E3 ligases (e.g. Mdm2); basal turnover has no sensor | proteasomal degradation of PSD proteins (PSD-95, scaffolds); replacement of the proteins holding a stored weight | post (and the PRP pool) | homeostatic PSD remodelling; contribution to LTD; loss of unmaintained weight | turnover and maintenance of `w_cap`; degraded constraint on capture |

---

## 1. Vesicle-pool depletion (short-term depression)

**Pathway.** Presynaptic spike → VGCC Ca²⁺ → release that depletes the readily releasable pool
(presynaptic). **Rule:** use-dependent, frequency-dependent depression.

**Mechanism.** Each spike depletes the readily releasable vesicle pool, so later
EPSCs in a train shrink until the pool recovers (τ_rec ~ 100 ms–1 s). Release-site
refractoriness and receptor desensitization add to the effect. The stored weight
does not change, only the efficacy read out from it. This is the TM-model
depression term already used in S0–S3.

**Spec hook.** STP in model §1 and model §2.1. It downscales transmission during high-rate
bursts, including the compressed sequences of SWR replay.

**References.**
- Tsodyks MV, Markram H (1997). The neural code between neocortical pyramidal neurons depends on neurotransmitter release probability. *PNAS* 94:719–723.
- Zucker RS, Regehr WG (2002). Short-term synaptic plasticity. *Annu Rev Physiol* 64:355–405.
- Dobrunz LE, Stevens CF (1997). Heterogeneity of release probability, facilitation, and depletion at central synapses. *Neuron* 18:995–1008.

## 2. Presynaptic GPCR inhibition (adenosine A1, GABA_B, group II/III mGluR)

**Pathway.** G_i/o-coupled receptors → Gβγ inhibition of N/P/Q-type VGCCs and of the release
machinery → lower release probability (presynaptic). **Rule:** neuromodulatory or tonic gain
control. This is state-dependent, not activity-pattern-dependent.

**Mechanism.** G-protein-coupled presynaptic receptors lower release probability.
Extracellular adenosine builds up with prolonged wake and metabolic load, which
ties this mechanism to sleep pressure. That makes it a tonic, hours-scale
downscaling of Schaffer-collateral release.

**Spec hook.** The separate neuromodulatory input to the synaptic area (implementation §7.2).
Expressed as a scaling of the TM parameter U.

**References.**
- Dunwiddie TV, Masino SA (2001). The role and regulation of adenosine in the central nervous system. *Annu Rev Neurosci* 24:31–55.
- Porkka-Heiskanen T et al. (1997). Adenosine: a mediator of the sleep-inducing effects of prolonged wakefulness. *Science* 276:1265–1268.
- Davies CH, Starkey SJ, Pozza MF, Collingridge GL (1991). GABA_B autoreceptors regulate the induction of LTP. *Nature* 349:609–611.

## 3. SWR-triggered NMDAR-dependent depression

**Pathway.** Synchronous CA3 bursts during a ripple → postsynaptic NMDAR activation in CA1 →
long-lasting, pathway-specific AMPAR weakening (postsynaptic). Norimoto et al. establish the
NMDAR dependence but not the downstream effector. **Rule:** state-gated depression during
offline (slow-wave) states. A SWR is a network *event* that engages this pathway. It is not
itself a molecular mechanism.

**Mechanism.** In mouse hippocampus, sharp-wave ripples during slow-wave states
trigger long-lasting, NMDAR-dependent and pathway-specific synaptic depression.
Suppressing ripples prevents the spontaneous downregulation of net synaptic
weight and impairs learning of new memories. Across sleep, CA1 firing rates fall,
and the size of that drop is predicted by NREM spindle/SWR incidence followed by
REM. In cortex, Up states bias plasticity toward depression of inputs that do not
drive the postsynaptic cell, while inputs that do drive it are spared.

**Spec hook.** Model §3. The same SWR event that replays and captures the stored
sequence also depresses the rest of the synapses. Replay therefore acts as
selection (capture what is replayed, depress what is not), not only as
potentiation.

**References.**
- Norimoto H, Makino K, Gao M, et al. (2018). Hippocampal ripples down-regulate synapses. *Science* 359:1524–1527. doi:10.1126/science.aao0702
- Miyawaki H, Diba K (2016). Regulation of hippocampal firing by network oscillations during sleep. *Curr Biol* 26:893–902.
- Grosmark AD, Mizuseki K, Pastalkova E, Diba K, Buzsáki G (2012). REM sleep reorganizes hippocampal excitability. *Neuron* 75:1001–1007.
- González-Rueda A, Pedrosa V, Feord RC, Clopath C, Paulsen O (2018). Activity-dependent downscaling of subthreshold synaptic inputs during slow-wave-sleep-like activity in vivo. *Neuron* 97:1244–1252. doi:10.1016/j.neuron.2018.01.047 (cortex)
- Lewis PA, Durrant SJ (2011). Overlapping memory replay during sleep builds cognitive schemata. *Trends Cogn Sci* 15:343–351.

## 4a. Postsynaptic NMDAR → calcineurin/PP1 LTD

**Pathway.** Moderate, prolonged postsynaptic Ca²⁺ influx through NMDARs → calcineurin →
inhibitor-1 → PP1 → dephosphorylation of GluA1 (S845) → clathrin-dependent AMPAR endocytosis
(postsynaptic). **Rule:** rate-dependent LTD (low-frequency stimulation). It is also the
low-activity branch of BCM.

**Mechanism.** Modest, prolonged Ca²⁺ influx (for example 1 Hz for 15 min) preferentially
activates phosphatases over CaMKII. LTD lowers GluA1 phosphorylation at the PKA site S845,
while LTP raises phosphorylation at the CaMKII/PKC site S831 (Lee et al. 2000). Which site
changes depends on the synapse's history. The calcium-control hypothesis (Lisman 1989)
reduces this to two Ca²⁺ thresholds.

**Spec hook.** model §2.1 `g_Ca(V_seg)`. A single sigmoid becomes two thresholds:
θ_d < Ca < θ_p gives depression and Ca > θ_p gives a tag. This entry supplies the *rate*
dependence of depression only. The timing-dependent lobe is 4b.

**References.**
- Dudek SM, Bear MF (1992). Homosynaptic long-term depression in area CA1 of hippocampus and effects of NMDA receptor blockade. *PNAS* 89:4363–4367.
- Mulkey RM, Malenka RC (1992). Mechanisms underlying induction of homosynaptic long-term depression in area CA1 of the hippocampus. *Neuron* 9:967–975.
- Lisman J (1989). A mechanism for the Hebb and the anti-Hebb processes underlying learning and memory. *PNAS* 86:9574–9578.
- Mulkey RM, Endo S, Shenolikar S, Malenka RC (1994). Involvement of a calcineurin/inhibitor-1 phosphatase cascade in hippocampal long-term depression. *Nature* 369:486–488.
- Lee HK, Barbarosie M, Kameyama K, Bear MF, Huganir RL (2000). Regulation of distinct AMPA receptor phosphorylation sites during bidirectional synaptic plasticity. *Nature* 405:955–959. doi:10.1038/35016089
- Shouval HZ, Bear MF, Cooper LN (2002). A unified model of NMDA receptor-dependent bidirectional synaptic plasticity. *PNAS* 99:10831–10836. (model)
- Graupner M, Brunel N (2012). Calcium-based plasticity model explains sensitivity of synaptic changes to spike pattern, rate, and dendritic location. *PNAS* 109:3991–3996. (model)

## 4b. Endocannabinoid → CB1 presynaptic t-LTD

**Pathway.** A postsynaptic spike before the presynaptic one → postsynaptic VGCC Ca²⁺ and group
I mGluR → endocannabinoid synthesis → retrograde activation of presynaptic CB1, coincident with
presynaptic NMDAR activation → lower release probability. In mouse CA3→CA1 this form needs
presynaptic calcineurin (presynaptic expression, postsynaptic induction). **Rule:** the
depression lobe of STDP (post-before-pre).

**Mechanism.** STDP is a *protocol and rule*, not a pathway. The depression it produces is
carried at least partly by a different pathway from 4a. In neocortical L5 it is presynaptic
and needs coincident presynaptic NMDAR and CB1 activation (Sjöström et al. 2003). In mouse
hippocampus, t-LTD at CA3→CA1 is presynaptic and needs presynaptic calcineurin. That
presynaptic form fades by about the fourth postnatal week (Andrade-Talavera et al. 2016). So
whether a strong STDP depression lobe exists at **adult** CA3→CA1 synapses is not
established. A tinyHippo model of an adult healthy rodent should not assume it without a
source.

**Spec hook.** The negative lobe of the ±20 ms STDP window (implementation §7.5) belongs here,
not to 4a. Because expression is presynaptic, it should be modelled as a reduction of TM `U`,
not of the postsynaptic weight. It then interacts with STP (#1).

**References.**
- Markram H, Lübke J, Frotscher M, Sakmann B (1997). Regulation of synaptic efficacy by coincidence of postsynaptic APs and EPSPs. *Science* 275:213–215. (neocortex)
- Bi GQ, Poo MM (1998). Synaptic modifications in cultured hippocampal neurons: dependence on spike timing, synaptic strength, and postsynaptic cell type. *J Neurosci* 18:10464–10472. (culture)
- Sjöström PJ, Turrigiano GG, Nelson SB (2003). Neocortical LTD via coincident activation of presynaptic NMDA and cannabinoid receptors. *Neuron* 39:641–654. (neocortex L5)
- Andrade-Talavera Y, Duque-Feria P, Paulsen O, Rodríguez-Moreno A (2016). Presynaptic spike timing-dependent long-term depression in the mouse hippocampus. *Cereb Cortex* 26:3637–3654. doi:10.1093/cercor/bhw172

## 5. PP1-mediated depotentiation (tag reset)

**Pathway.** LFS shortly after LTP → NMDAR Ca²⁺ plus extracellular adenosine acting on A1R →
protein phosphatases (PP1) → reversal of CaMKII/PKA phosphorylation and removal of the newly
inserted AMPARs (postsynaptic). **Rule:** time-limited reversal of recent potentiation. It
shares its sensor and effector with 4a. What differs is the target: a synapse that was
potentiated recently and is still labile.

**Mechanism.** Low-frequency stimulation delivered shortly after LTP induction
(within roughly 10–60 min) erases E-LTP. Once the potentiation has stabilized (late-LTP), the
same stimulation no longer reverses it. Sajikumar & Frey showed that this
time-dependent reset acts on the synaptic tag itself: a reset tag can no longer
capture PRPs. Cross-tagging (LTP and LTD inputs sharing PRPs) comes from the same
group.

**Spec hook.** An **active** reset of the model §2 tag, separate from passive τ_tag decay.
It gives the S4–S6 falsification test a second arm: LFS within the window should
abolish capture.

**References.**
- Staubli U, Lynch G (1990). Stable depression of potentiated synaptic responses in the hippocampus with 1–5 Hz stimulation. *Brain Res* 513:113–118.
- Fujii S, Saito K, Miyakawa H, Ito K, Kato H (1991). Reversal of long-term potentiation (depotentiation) induced by tetanus stimulation of the input to CA1 neurons of guinea pig hippocampal slices. *Brain Res* 555:112–122.
- O'Dell TJ, Kandel ER (1994). Low-frequency stimulation erases LTP through an NMDA receptor-mediated activation of protein phosphatases. *Learn Mem* 1:129–139.
- Huang CC, Liang YC, Hsu KS (1999). A role for extracellular adenosine in time-dependent reversal of long-term potentiation by low-frequency stimulation at hippocampal CA1 synapses. *J Neurosci* 19:9728–9738.
- Sajikumar S, Frey JU (2004). Resetting of "synaptic tags" is time- and activity-dependent in rat hippocampal CA1 in vitro. *Neuroscience* 129:503–507. doi:10.1016/j.neuroscience.2004.08.014
- Sajikumar S, Frey JU (2004). Late-associativity, synaptic tagging, and the role of dopamine during LTP and LTD. *Neurobiol Learn Mem* 82:12–25.

## 6. IP3R/calcineurin heterosynaptic depression

**Pathway.** Potentiation of a cluster of neighbouring spines → group I mGluR and IP3R-mediated
Ca²⁺ release from stores → calcineurin → shrinkage and AMPAR loss at nearby *inactive* spines
(postsynaptic, at unstimulated synapses). **Rule:** heterosynaptic normalization, conserving
weight within a segment.

**Mechanism.** Potentiation of a cluster of synapses depresses or shrinks nearby
*unstimulated* synapses on the same dendritic segment. In CA1 this needs
calcineurin, IP3R and group I mGluR, and only appears after several neighbours
are potentiated. In amygdala intercalated cells, opposite-signed heterosynaptic
changes conserve the total synaptic weight.

**Spec hook.** Per-segment weight conservation at the same granularity as `V_seg`
(one state per `thr` unit). It gives the cluster topology of implementation §7.3 a
normalization rule.

**References.**
- Lynch GS, Dunwiddie T, Gribkoff V (1977). Heterosynaptic depression: a postsynaptic correlate of long-term potentiation. *Nature* 266:737–739.
- Oh WC, Parajuli LK, Zito K (2015). Heterosynaptic structural plasticity on local dendritic segments of hippocampal CA1 neurons. *Cell Rep* 10:162–169. doi:10.1016/j.celrep.2014.12.016
- Royer S, Paré D (2003). Conservation of total synaptic weight through balanced synaptic depression and potentiation. *Nature* 422:518–522. doi:10.1038/nature01530
- Chistiakova M, Bannon NM, Bazhenov M, Volgushev M (2014). Heterosynaptic plasticity: multiple mechanisms and multiple roles. *Neuroscientist* 20:483–498.
- El-Boustani S, Ip JPK, Breton-Provencher V, et al. (2018). Locally coordinated synaptic plasticity of visual cortex neurons in vivo. *Science* 360:1349–1354. (cortex)

## 7. mGluR5 → local-translation LTD

**Pathway.** Group I mGluR (mGluR5, G_q) → rapid dendritic translation of Arc, STEP and MAP1B
→ a sustained increase in AMPAR endocytosis rate (postsynaptic). **Rule:** homosynaptic,
protein-synthesis-dependent LTD. It is not Hebbian in the strict sense. Presynaptic activity
alone (paired-pulse LFS) or a group I agonist (DHPG) is enough, and no pre–post conjunction is
needed.

**Mechanism.** Group I mGluR activation (DHPG or paired-pulse LFS) triggers local
dendritic translation of Arc, STEP and MAP1B, which drives AMPAR endocytosis. Like
L-LTP, it depends on protein synthesis, so it draws on the same translational
machinery as capture.

**Spec hook.** The model §2 PRP pool. A depressive process that competes with
potentiation for capture.

**References.**
- Oliet SHR, Malenka RC, Nicoll RA (1997). Two distinct forms of long-term depression coexist in CA1 hippocampal pyramidal cells. *Neuron* 18:969–982.
- Huber KM, Kayser MS, Bear MF (2000). Role for rapid dendritic protein synthesis in hippocampal mGluR-dependent long-term depression. *Science* 288:1254–1257.
- Waung MW, Pfeiffer BE, Nosyreva ED, Ronesi JA, Huber KM (2008). Rapid translation of Arc/Arg3.1 selectively mediates mGluR-dependent LTD through persistent increases in AMPAR endocytosis rate. *Neuron* 59:84–97.

## 8. Constitutive GluA2 endocytosis (passive E-LTP and tag decay)

**Pathway.** No sensor is needed. Without capture, constitutive endocytosis of GluA2-containing
AMPARs removes the extra receptors (postsynaptic). It is blocked by the GluA2-3Y interference
peptide. **Rule:** decay of unconsolidated potentiation, the default fate of a trace.

**Mechanism.** Without capture, E-LTP decays over 1–3 hr as inserted AMPARs are
removed by constitutive, GluA2-dependent endocytosis. Even consolidated memories
show an ongoing, decay-like forgetting process that blocking GluA2 removal
prevents.

**Spec hook.** τ_tag decay in model Fig. 2, and the volatile-memristor
relaxation of implementation §5.2. This is the baseline against which capture is measured.

**References.**
- Frey U, Morris RGM (1997). Synaptic tagging and long-term potentiation. *Nature* 385:533–536.
- Redondo RL, Morris RGM (2011). Making memories last: the synaptic tagging and capture hypothesis. *Nat Rev Neurosci* 12:17–30.
- Migues PV, Liu L, Archbold GEB, et al. (2016). Blocking synaptic removal of GluA2-containing AMPA receptors prevents the natural forgetting of long-term memories. *J Neurosci* 36:3481–3494. doi:10.1523/JNEUROSCI.3333-15.2016
- Hardt O, Nader K, Nadel L (2013). Decay happens: the role of active forgetting in memory. *Trends Cogn Sci* 17:111–120.
- Pastalkova E, Serrano P, Pinkhasova D, et al. (2006). Storage of spatial information by the maintenance mechanism of LTP. *Science* 313:1141–1144. (PKMζ maintenance. Contested by Volk LJ et al. 2013, *Nature* 493:420–423, and Lee AM et al. 2013, *Nature* 493:416–419.)

## 9. Competition for plasticity-related proteins

**Pathway.** No sensor is needed: this is a finite resource. Protein synthesis and proteasomal
degradation set the size of a cell-wide PRP pool, and tagged synapses draw on it. **Rule:**
competition between inputs for consolidation.

**Mechanism.** When protein synthesis is limited, potentiating one input at the
expense of another makes the other pathway's established LTP decay. Synapses
compete for a finite PRP pool, so capture at one site can leave another
uncaptured. A balance between synthesis and proteasomal degradation sets how
long LTP is maintained.

**Spec hook.** Makes the model §2 capture threshold a shared, depletable resource rather
than an independent per-synapse gate.

**References.**
- Fonseca R, Nägerl UV, Morris RGM, Bonhoeffer T (2004). Competing for memory: hippocampal LTP under regimes of reduced protein synthesis. *Neuron* 44:1011–1020. doi:10.1016/j.neuron.2004.10.033
- Fonseca R, Vabulas RM, Hartl FU, Bonhoeffer T, Nägerl UV (2006). A balance of protein synthesis and proteasome-dependent degradation determines the maintenance of LTP. *Neuron* 52:239–245.

## 10. NMDAR subunit (GluN2A/2B) threshold shift

**Pathway.** Integrated postsynaptic activity over hours → change in the GluN2A/GluN2B ratio of
synaptic NMDARs → altered Ca²⁺ kinetics for a given input → a shifted LTD/LTP crossover
(postsynaptic). **Rule:** the BCM sliding threshold, i.e. metaplasticity. BCM is the *rule*,
and the subunit switch is one molecular substrate of it.

**Mechanism.** The LTD/LTP crossover point shifts with the recent history of
postsynaptic activity. High prior activity raises the threshold, which favours
depression. Low prior activity lowers it. NMDAR subunit composition (GluN2A/2B)
is one substrate of the shift.

**Spec hook.** A slow variable that moves θ_p of `g_Ca` in model §2.1. It costs one extra
state per neuron or segment.

**References.**
- Bienenstock EL, Cooper LN, Munro PW (1982). Theory for the development of neuron selectivity. *J Neurosci* 2:32–48.
- Abraham WC, Bear MF (1996). Metaplasticity: the plasticity of synaptic plasticity. *Trends Neurosci* 19:126–130.
- Abraham WC (2008). Metaplasticity: tuning synapses and networks for plasticity. *Nat Rev Neurosci* 9:387–399.
- Philpot BD, Sekhar AK, Shouval HZ, Bear MF (2001). Visual experience and deprivation bidirectionally modify the composition and function of NMDA receptors in visual cortex. *Neuron* 29:157–169.

## 11. Homer1a–mGluR5 sleep scaling-down

**Pathway.** Sleep state (falling noradrenaline, rising adenosine) → Homer1a accumulates at
synapses → ligand-independent mGluR5 signalling → GluA1 dephosphorylation and AMPAR removal
(postsynaptic) (Diering et al. 2017). **Rule:** the synaptic homeostasis hypothesis (SHY): net
potentiation during wake, renormalization during sleep. SHY is a systems-level *hypothesis*,
and Homer1a–mGluR5 is the best-described pathway behind it.

**Mechanism.** Wake brings net synaptic potentiation, and sleep, mainly NREM slow
oscillations, brings net downscaling. This restores energy and space budgets and
raises signal-to-noise. The evidence includes wake/sleep changes in GluA1
phosphorylation and levels, a ~18% shrinkage of the axon–spine interface after
sleep, and Homer1a-driven mGluR5 signalling that scales down synapses during
sleep. REM sleep both prunes and keeps selected new spines.

**Spec hook.** A global, recurring downscaling step between replay epochs in the
consolidation loop. Each sleep cycle is a dotted repeat in Fig. D1.

**References.**
- Tononi G, Cirelli C (2003). Sleep and synaptic homeostasis: a hypothesis. *Brain Res Bull* 62:143–150.
- Tononi G, Cirelli C (2014). Sleep and the price of plasticity: from synaptic and cellular homeostasis to memory consolidation and integration. *Neuron* 81:12–34.
- Vyazovskiy VV, Cirelli C, Pfister-Genskow M, Faraguna U, Tononi G (2008). Molecular and electrophysiological evidence for net synaptic potentiation in wake and depression in sleep. *Nat Neurosci* 11:200–208.
- de Vivo L, Bellesi M, Marshall W, et al. (2017). Ultrastructural evidence for synaptic scaling across the wake/sleep cycle. *Science* 355:507–510.
- Diering GH, Nirujogi RS, Roth RH, et al. (2017). Homer1a drives homeostatic scaling-down of excitatory synapses during sleep. *Science* 355:511–515.
- Li W, Ma L, Yang G, Gan WB (2017). REM sleep selectively prunes and maintains new synapses in development and learning. *Nat Neurosci* 20:427–437. doi:10.1038/nn.4479 (motor cortex)

## 12. CaMKIV/TNFα homeostatic synaptic scaling

**Pathway.** Sustained change in firing → somatic Ca²⁺ → CaMKIV → transcription (Ibata et al.
2008), together with glial TNFα → a multiplicative change in synaptic AMPAR number. Scaling
down uses Arc-dependent endocytosis (postsynaptic). In parallel, release probability is set by
local dendritic activity (presynaptic). **Rule:** firing-rate homeostasis.

**Mechanism.** Chronic changes in firing rate scale all of a neuron's excitatory
synapses multiplicatively, which preserves their relative weights. Prolonged
activity scales them down and silencing scales them up, over about 24–48 hr.
Effectors include TNFα from glia, Arc/Arg3.1 and Homer1a. The response in the
hippocampus is synapse-type specific: silencing strengthens the throughput
DG→CA3 and CA3→CA1 synapses but weakens recurrent CA3→CA3 synapses. Release
probability is also regulated homeostatically by local dendritic activity.

**Spec hook.** The "activity-dependent weight decay" of the synaptic area (implementation §7.2).
Presynaptically, it acts as a branch-level scaling of U. This mechanism is slow,
so short runs must either state a compression factor or leave it out (see
`CLAUDE.md`).

**References.**
- Turrigiano GG, Leslie KR, Desai NS, Rutherford LC, Nelson SB (1998). Activity-dependent scaling of quantal amplitude in neocortical neurons. *Nature* 391:892–896.
- Turrigiano GG (2008). The self-tuning neuron: synaptic scaling of excitatory synapses. *Cell* 135:422–435.
- Ibata K, Sun Q, Turrigiano GG (2008). Rapid synaptic scaling induced by changes in postsynaptic firing. *Neuron* 57:819–826.
- Kim J, Tsien RW (2008). Synapse-specific adaptations to inactivity in hippocampal circuits achieve homeostatic gain control while dampening network reverberation. *Neuron* 58:925–937. doi:10.1016/j.neuron.2008.05.009
- Stellwagen D, Malenka RC (2006). Synaptic scaling mediated by glial TNF-α. *Nature* 440:1054–1059.
- Shepherd JD, Rumbaugh G, Wu J, et al. (2006). Arc/Arg3.1 mediates homeostatic synaptic scaling of AMPA receptors. *Neuron* 52:475–484.
- Branco T, Staras K, Darcy KJ, Goda Y (2008). Local dendritic activity sets release probability at hippocampal synapses. *Neuron* 59:475–485.
- Murthy VN, Schikorski T, Stevens CF, Zhu Y (2001). Inactivity produces increases in neurotransmitter release and synapse size. *Neuron* 32:673–682.

Related non-synaptic homeostatic routes, listed for completeness: intrinsic
excitability scaling (Desai NS, Rutherford LC, Turrigiano GG 1999, *Nat Neurosci*
2:515–520) and inhibitory plasticity (Vogels TP, Sprekeler H, Zenke F, Clopath C,
Gerstner W 2011, *Science* 334:1569–1573). Both lower output without depressing
excitatory weights.

## 13. Complement/microglial pruning and Rac1/cofilin forgetting

**Pathway.** C1q/C3 complement deposited on weak or inactive synapses → phagocytosis by
microglia through CR3. In parallel, Rac1 → cofilin-driven actin disassembly removes spine
structure. Both remove the whole synapse. **Rule:** structural forgetting, the elimination of
traces that were not maintained.

**Mechanism.** On timescales of days to months, synapses are physically removed.
In adult hippocampus, microglia eliminate synapses through complement tagging, and
depleting microglia or blocking complement prevents forgetting of contextual fear
memory. Rac1/cofilin signalling drives active forgetting (first shown in
*Drosophila*). Adult neurogenesis in the dentate gyrus causes forgetting of
hippocampus-dependent memories.

**Spec hook.** The fate of an uncaptured or unreplayed trace on the slow side of
model §3. Neurogenesis acts in DG, outside the minimal CA1 circuit.

**References.**
- Wang C, Yue H, Hu Z, et al. (2020). Microglia mediate forgetting via complement-dependent synaptic elimination. *Science* 367:688–694. doi:10.1126/science.aaz2288
- Schafer DP, Lehrman EK, Kautzman AG, et al. (2012). Microglia sculpt postnatal neural circuits in an activity and complement-dependent manner. *Neuron* 74:691–705.
- Shuai Y, Lu B, Hu Y, Wang L, Sun K, Zhong Y (2010). Forgetting is regulated through Rac activity in *Drosophila*. *Cell* 140:579–589.
- Davis RL, Zhong Y (2017). The biology of forgetting: a perspective. *Neuron* 95:490–503.
- Akers KG, Martinez-Canabal A, Restivo L, et al. (2014). Hippocampal neurogenesis regulates forgetting during adulthood and infancy. *Science* 344:598–602.

## 14. Ubiquitin–proteasome degradation and protein turnover

**Pathway.** Two parts. *Basal turnover* has no sensor: the proteins that hold a stored weight
are degraded and replaced over days to weeks. *Activity-driven degradation*: NMDAR Ca²⁺ or
sustained activity → E3 ubiquitin ligases (e.g. Mdm2) → ubiquitination of postsynaptic density
proteins → proteasomal degradation → fewer synaptic AMPAR slots (postsynaptic). **Rule:**
homeostatic remodelling of the PSD, a contribution to LTD, and loss of any weight that is not
actively maintained.

**Mechanism.** In rat hippocampal cultures, protein half-lives range from under a day to more
than 20 days. In mouse synapses, a set of long-lived proteins persists for weeks or longer, and
synaptic proteins turn over more slowly than cytosolic ones. A memory therefore outlives its
molecules only if something rebuilds it (Crick's turnover problem). The candidate answers are a
self-maintaining kinase switch or recurring protein synthesis. Activity changes the composition
of the PSD in both directions through the ubiquitin–proteasome system. NMDAR activation leads
Mdm2 to ubiquitinate PSD-95, which is then degraded. Blocking this prevents NMDA-induced AMPAR
endocytosis and reduces LTD. Later work conflicts: proteasome inhibition was reported to leave
NMDAR-LTD unchanged and to enhance mGluR-LTD (Citri et al. 2009). Proteasomal degradation of
FMRP was reported to be needed for mGluR-LTD (Hou et al. 2006). Degradation is also needed for
late-LTP: blocking it disrupts late-LTP, and blocking synthesis as well restores it (Fonseca et
al. 2006, under #9).

**Spec hook.** Captured weight `w_cap`, which the model currently holds stable. Turnover adds a
decay term with time constant τ_turn (days), and maintenance can be added as a synthesis-gated
bistable term. On the PRP side, a synthesised constraint that the proteasome degrades would
reproduce Fonseca et al. 2006. Equations 16–17 of
[`docs/plasticity_up_down_model_2026-11-06.md`](docs/plasticity_up_down_model_2026-11-06.md)
give the proposed forms. A τ_turn of days needs a stated compression factor in any short run.

**References.**
- Crick F (1984). Memory and molecular turnover. *Nature* 312:101. (News and Views)
- Lisman JE (1985). A mechanism for memory storage insensitive to molecular turnover: a bistable autophosphorylating kinase. *PNAS* 82:3055–3057. doi:10.1073/pnas.82.9.3055
- Miller P, Zhabotinsky AM, Lisman JE, Wang XJ (2005). The stability of a stochastic CaMKII switch: dependence on the number of enzyme molecules and protein turnover. *PLoS Biol* 3:e107. doi:10.1371/journal.pbio.0030107
- Ehlers MD (2003). Activity level controls postsynaptic composition and signaling via the ubiquitin-proteasome system. *Nat Neurosci* 6:231–242. (cultured rat hippocampal neurons)
- Colledge M, Snyder EM, Crozier RA, et al. (2003). Ubiquitination regulates PSD-95 degradation and AMPA receptor surface expression. *Neuron* 40:595–607.
- Hou L, Antion MD, Hu D, et al. (2006). Dynamic translational and proteasomal regulation of fragile X mental retardation protein controls mGluR-dependent long-term depression. *Neuron* 51:441–454. (proteasome claim checked only through a secondary excerpt)
- Citri A, Soler-Llavina G, Bhattacharyya S, Malenka RC (2009). N-methyl-D-aspartate receptor- and metabotropic glutamate receptor-dependent long-term depression are differentially regulated by the ubiquitin-proteasome system. *Eur J Neurosci*. (not yet checked)
- Dörrbaum AR, Kochen L, Langer JD, Schuman EM (2018). Local and global influences on protein turnover in neurons and glia. *eLife* 7:e34202. doi:10.7554/eLife.34202 (rat hippocampal cultures)
- Heo S, Diering GH, Na CH, et al. (2018). Identification of long-lived synaptic proteins by proteomic analysis of synaptosome protein turnover. *PNAS* 115:E3827–E3836. doi:10.1073/pnas.1720956115 (mouse)

---

## Computational references

| Topic | References |
|---|---|
| Weight normalization | von der Malsburg C (1973) *Kybernetik* 14:85–100; Oja E (1982) *J Math Biol* 15:267–273; Miller KD, MacKay DJC (1994) *Neural Comput* 6:100–126 |
| STDP with synaptic scaling | van Rossum MCW, Bi GQ, Turrigiano GG (2000) *J Neurosci* 20:8812–8821 |
| Homeostasis across timescales | Zenke F, Agnes EJ, Gerstner W (2015) *Nat Commun* 6:6922; Zenke F, Gerstner W (2017) *Phil Trans R Soc B* 372:20160259 |
| Tag/capture models with decay | Clopath C, Ziegler L, Vasilaki E, Büsing L, Gerstner W (2008) *PLoS Comput Biol* 4:e1000248; Barrett AB, Billings GO, Morris RGM, van Rossum MCW (2009) *PLoS Comput Biol* 5:e1000259 |
| Multi-timescale memory | Fusi S, Drew PJ, Abbott LF (2005) *Neuron* 45:599–611; Benna MK, Fusi S (2016) *Nat Neurosci* 19:1697–1706 |

A ranked list of models to compare against, with PubMed-checked references, is in
[`docs/related_models.md`](docs/related_models.md).

Zenke & Gerstner (2017) argue that compensatory processes must be fast (comparable
to the Hebbian timescale). Biologically slow scaling (#12) alone cannot stabilize
Hebbian growth. Fast candidates are #3, #6 and #10.

## Candidates for tinyHippo (after S4–S6 tag/capture)

1. **#8 + #5.** Passive tag decay plus LFS-driven active reset. Fills model §2 directly
   and adds a second falsification arm.
2. **#4a + #10.** Two-threshold `g_Ca` with a sliding θ_p. One extra state variable per segment.
3. **#6.** Per-segment heterosynaptic conservation at `V_seg` granularity.
4. **#3.** SWR-gated depression of non-replayed synapses. Needs ripple-epoch input,
   and any timescale compression factor must be stated.
5. **#12.** Multiplicative scaling, only with a stated compression factor.
6. **#14.** Turnover of `w_cap` with an optional maintenance switch. It decides how long a
   captured weight lasts, so its compression factor must be stated.

<!-- test text: push check -->
