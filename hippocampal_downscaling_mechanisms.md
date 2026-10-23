# Hippocampal Downscaling Mechanisms

Companion to [`hippocampal_plasticity_model.md`](hippocampal_plasticity_model.md) ("model §n"; hardware
sections in [`hippocampal_memristive_implementation.md`](hippocampal_memristive_implementation.md),
"implementation §n"). The model document lays out the *upscaling* path: STP → Ca²⁺/kinase → E-LTP →
tag & capture → L-LTP (the synaptic correlate of cellular consolidation) → SWR replay → system
consolidation. This one lists the mechanisms that *weaken* synapses or keep their total bounded. Each
entry gives its timescale, its hook in the circuit model (model §2 tag/capture, implementation §7.2
synaptic-area "activity-dependent weight decay", model §2.1 `V_seg`, model §3 replay), and its primary
literature.

![Thirteen synaptic downscaling mechanisms on the same logarithmic time axis as Fig. 1 of the model document, from 1 ms to 10 years, ordered by onset so the bars form a descending staircase. A grey reference row 0, neurotransmission at 0.4–6 ms, sits above them. Short-term depression, presynaptic inhibition and SWR-associated depression start in the millisecond range; Hebbian, heterosynaptic and tag-related depression start at seconds to minutes; BCM metaplasticity, sleep renormalization and synaptic scaling start at tens of minutes to hours; pruning and active forgetting start at days and extend to a year.](figures/downscaling_timescale_axis.png)

*Fig. D1. Downscaling mechanisms on the log time axis of model Fig. 1, ordered
by onset (ties broken by end), as in Fig. 1. Row 0 (grey) is neurotransmission,
drawn with the span of model Fig. 1 row 1 (~0.4–6 ms) as the common fastest
reference. It is not a downscaling mechanism. A bar's position marks onset and its
length marks characteristic duration. Dotted tails
are recurring or extended effects. Spans are order-of-magnitude summaries of the
references below, not fitted values. Regenerate with
`python3 figures/make_downscaling_timescale_axis.py`.*

**Citation status.** The entries below were compiled for orientation. The
bibliographic details of Norimoto 2018, González-Rueda 2018, Oh 2015, Kim & Tsien
2008, Fonseca 2004, Royer & Paré 2003, Branco 2008, Migues 2016, Wang 2020,
Li 2017, Sajikumar & Frey 2004 and Miyawaki & Diba 2016 have been checked against
PubMed/PMC or publisher records (DOIs given). Every reference added for the
plausibility review (section "Biological plausibility", with PMIDs) has also been
checked against PubMed, together with the species, age and preparation of each
paper that the review relies on (abstract or methods text). The rest are
standard citations whose bibliographic details have not been checked. Per `CLAUDE.md`, a parameter taken from any of these must
be checked against the source and recorded in `params.py` with its recording
conditions before use.

## Summary

| # | Mechanism | Timescale | Spec hook | Class |
|---|---|---|---|---|
| 0 | *Neurotransmission (reference, not downscaling)* | ~0.4–6 ms | model §1 row 1 | signalling |
| 1 | Short-term depression | 10 ms–10 s | STP (S0–S3) | transient, presynaptic |
| 2 | Presynaptic inhibition (adenosine A1, GABA_B, mGluR) | 50 ms–min (tonic: hours) | neuromodulatory input, implementation §7.2 | transient, presynaptic |
| 3 | SWR-associated depression | ripple 100 ms, effect hours, recurs over days | model §3 replay | sleep / replay |
| 4 | NMDAR-dependent LTD / STDP depression | induction s–min, expression hours | `g_Ca(V_seg)` low-Ca branch, model §2.1 | Hebbian |
| 5 | Depotentiation / tag reset | window 1 min–1 hr | active reset of the model §2 tag | Hebbian, reversal |
| 6 | Heterosynaptic depression | min–hours | per-segment conservation (`V_seg` unit) | competitive |
| 7 | mGluR-LTD | min–1 day | PRP pool, model §2 | Hebbian, protein-synthesis dependent |
| 8 | Passive E-LTP / tag decay | τ ≈ 1–4 hr | τ_tag decay in Fig. 2 | intrinsic decay |
| 9 | PRP competition | 30 min–8 hr | capture threshold, model §2 | competitive |
| 10 | BCM sliding threshold / metaplasticity | 30 min–days | LTD/LTP crossover of `g_Ca` | homeostatic |
| 11 | Sleep renormalization (SHY) | hours, each sleep cycle | global downscaling between replay epochs | sleep / homeostatic |
| 12 | Synaptic scaling | 12 hr–days | implementation §7.2 weight decay | homeostatic |
| 13 | Pruning and active forgetting | days–months | removal of uncaptured traces | structural |

---

## 1. Short-term depression

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

## 2. Presynaptic inhibition (adenosine A1, GABA_B, group II/III mGluR)

**Mechanism.** G-protein-coupled presynaptic receptors lower release probability.
Extracellular adenosine builds up with prolonged wake and metabolic load, which
ties this mechanism to sleep pressure. That makes it a tonic, hours-scale
downscaling of Schaffer-collateral release.

**Spec hook.** The separate neuromodulatory input to the synaptic area (implementation §7.2).
Expressed as a scaling of the TM parameter U.

**References.**
- Dunwiddie TV, Masino SA (2001). The role and regulation of adenosine in the central nervous system. *Annu Rev Neurosci* 24:31–55.
- Porkka-Heiskanen T et al. (1997). Adenosine: a mediator of the sleep-inducing effects of prolonged wakefulness. *Science* 276:1265–1268. (Microdialysis in cat basal forebrain, not hippocampus.)
- Isaacson JS, Solís JM, Nicoll RA (1993). Local and diffuse synaptic actions of GABA in the hippocampus. *Neuron* 10:165–175. doi:10.1016/0896-6273(93)90308-e (rat CA1 slices. Presynaptic GABA_B heteroreceptors depress Schaffer-collateral release after brief repetitive stimulation.)
- Davies CH, Starkey SJ, Pozza MF, Collingridge GL (1991). GABA autoreceptors regulate the induction of LTP. *Nature* 349:609–611. (Corrected attribution. This paper shows GABA_B *autoreceptors* on GABAergic terminals reducing GABA release, which disinhibits CA1 and favours LTP. It is not evidence for presynaptic inhibition of glutamate release.)

## 3. SWR-associated depression

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
- González-Rueda A, Pedrosa V, Feord RC, Clopath C, Paulsen O (2018). Activity-dependent downscaling of subthreshold synaptic inputs during slow-wave-sleep-like activity in vivo. *Neuron* 97:1244–1252. doi:10.1016/j.neuron.2018.01.047 (L2/3 barrel cortex of urethane-anaesthetized P15–P21 mice: juvenile, and SWS-*like* activity under anaesthesia, not natural sleep.)

Removed: Lewis PA, Durrant SJ (2011), *Trends Cogn Sci* 15:343–351. It is a
hypothesis paper on schema formation by overlapping replay and contains no
evidence for SWR-associated synaptic depression.

## 4. NMDAR-dependent LTD and STDP depression

**Mechanism.** Modest, prolonged postsynaptic Ca²⁺ influx through NMDARs (for
example 1 Hz for 15 min) preferentially activates phosphatases (calcineurin, PP1)
over CaMKII. AMPARs are then dephosphorylated and endocytosed. Under STDP, the same
low-Ca regime is reached when the postsynaptic spike precedes the presynaptic one.

**Spec hook.** model §2.1 `g_Ca(V_seg)`. Read with the calcium-control hypothesis, a single
sigmoid becomes two thresholds: θ_d < Ca < θ_p gives depression and Ca > θ_p gives
a tag. The ±20 ms STDP window in implementation §7.5 gains a negative lobe.

**References.**
- Dudek SM, Bear MF (1992). Homosynaptic long-term depression in area CA1 of hippocampus and effects of NMDA receptor blockade. *PNAS* 89:4363–4367.
- Mulkey RM, Malenka RC (1992). Mechanisms underlying induction of homosynaptic long-term depression in area CA1 of the hippocampus. *Neuron* 9:967–975.
- Lisman J (1989). A mechanism for the Hebb and the anti-Hebb processes underlying learning and memory. *PNAS* 86:9574–9578.
- Mulkey RM, Endo S, Shenolikar S, Malenka RC (1994). Involvement of a calcineurin/inhibitor-1 phosphatase cascade in hippocampal long-term depression. *Nature* 369:486–488.
- Markram H, Lübke J, Frotscher M, Sakmann B (1997). Regulation of synaptic efficacy by coincidence of postsynaptic APs and EPSPs. *Science* 275:213–215.
- Bi GQ, Poo MM (1998). Synaptic modifications in cultured hippocampal neurons: dependence on spike timing, synaptic strength, and postsynaptic cell type. *J Neurosci* 18:10464–10472.
- Shouval HZ, Bear MF, Cooper LN (2002). A unified model of NMDA receptor-dependent bidirectional synaptic plasticity. *PNAS* 99:10831–10836. (model)
- Graupner M, Brunel N (2012). Calcium-based plasticity model explains sensitivity of synaptic changes to spike pattern, rate, and dendritic location. *PNAS* 109:3991–3996. (model)
- Dudek SM, Bear MF (1993). Bidirectional long-term modification of synaptic effectiveness in the adult and immature hippocampus. *J Neurosci* 13:2910–2918. doi:10.1523/JNEUROSCI.13-07-02910.1993 (age dependence of LFS-LTD)
- Manahan-Vaughan D (1997). Group 1 and 2 metabotropic glutamate receptors play differential roles in hippocampal long-term depression and long-term potentiation in freely moving rats. *J Neurosci* 17:3303–3311. doi:10.1523/JNEUROSCI.17-09-03303.1997 (adult, in vivo)
- Manahan-Vaughan D, Braunewell KH (1999). Novelty acquisition is associated with induction of hippocampal long-term depression. *PNAS* 96:8739–8744. doi:10.1073/pnas.96.15.8739 (adult, in vivo, behavioural gating)
- Wittenberg GM, Wang SS-H (2006). Malleability of spike-timing-dependent plasticity at the CA3-CA1 synapse. *J Neurosci* 26:6610–6617. doi:10.1523/JNEUROSCI.5388-05.2006

## 5. Depotentiation and tag reset

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
- Sajikumar S, Frey JU (2004). Resetting of "synaptic tags" is time- and activity-dependent in rat hippocampal CA1 in vitro. *Neuroscience* 129:503–507. doi:10.1016/j.neuroscience.2004.08.014
- Sajikumar S, Frey JU (2004). Late-associativity, synaptic tagging, and the role of dopamine during LTP and LTD. *Neurobiol Learn Mem* 82:12–25.
- Xu L, Anwyl R, Rowan MJ (1998). Spatial exploration induces a persistent reversal of long-term potentiation in rat hippocampus. *Nature* 394:891–894. doi:10.1038/29783 (in vivo, behavioural depotentiation)

## 6. Heterosynaptic depression

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
- Oh WC, Parajuli LK, Zito K (2015). Heterosynaptic structural plasticity on local dendritic segments of hippocampal CA1 neurons. *Cell Rep* 10:162–169. doi:10.1016/j.celrep.2014.12.016 (organotypic slice cultures from P6–P7 rats, two-photon glutamate uncaging)
- Royer S, Paré D (2003). Conservation of total synaptic weight through balanced synaptic depression and potentiation. *Nature* 422:518–522. doi:10.1038/nature01530 (amygdala intercalated neurons, outside hippocampus and cortex)
- Chistiakova M, Bannon NM, Bazhenov M, Volgushev M (2014). Heterosynaptic plasticity: multiple mechanisms and multiple roles. *Neuroscientist* 20:483–498.
- El-Boustani S, Ip JPK, Breton-Provencher V, et al. (2018). Locally coordinated synaptic plasticity of visual cortex neurons in vivo. *Science* 360:1349–1354. doi:10.1126/science.aao0862 (mouse V1 in vivo. Depression of spines adjacent to potentiated ones, on a slower timescale.)

## 7. mGluR-dependent LTD

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
- Nosyreva ED, Huber KM (2005). Developmental switch in synaptic mechanisms of hippocampal metabotropic glutamate receptor-dependent long-term depression. *J Neurosci* 25:2992–3001. doi:10.1523/JNEUROSCI.3652-04.2005
- Manahan-Vaughan D, Reymann KG (1997). Group 1 metabotropic glutamate receptors contribute to slow-onset potentiation in the rat CA1 region in vivo. *Neuropharmacology* 36:1533–1538. doi:10.1016/s0028-3908(97)00156-1

## 8. Passive E-LTP and tag decay

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
- Racine RJ, Milgram NW, Hafner S (1983). Long-term potentiation phenomena in the rat limbic forebrain. *Brain Res* 260:217–231. doi:10.1016/0006-8993(83)90676-5 (decremental LTP components in vivo)
- Abraham WC, Logan B, Greenwood JM, Dragunow M (2002). Induction and experience-dependent consolidation of stable long-term potentiation lasting months in the hippocampus. *J Neurosci* 22:9626–9634. doi:10.1523/JNEUROSCI.22-21-09626.2002
- Pastalkova E, Serrano P, Pinkhasova D, et al. (2006). Storage of spatial information by the maintenance mechanism of LTP. *Science* 313:1141–1144. (PKMζ maintenance. Contested by Volk LJ et al. 2013, *Nature* 493:420–423, and Lee AM et al. 2013, *Nature* 493:416–419.)

## 9. Competition for plasticity-related proteins

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

## 10. BCM sliding threshold and metaplasticity

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
- Kirkwood A, Rioult MC, Bear MF (1996). Experience-dependent modification of synaptic plasticity in visual cortex. *Nature* 381:526–528. doi:10.1038/381526a0
- He HY, Hodos W, Quinlan EM (2006). Visual deprivation reactivates rapid ocular dominance plasticity in adult visual cortex. *J Neurosci* 26:2951–2955. doi:10.1523/JNEUROSCI.5554-05.2006

## 11. Sleep-dependent renormalization (synaptic homeostasis hypothesis)

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
- Yang G, Lai CSW, Cichon J, Ma L, Li W, Gan WB (2014). Sleep promotes branch-specific formation of dendritic spines after learning. *Science* 344:1173–1178. doi:10.1126/science.1249098 (evidence for sleep-dependent *growth*)
- Frank MG (2012). Erasing synapses in sleep: is it time to be SHY? *Neural Plast* 2012:264378. doi:10.1155/2012/264378 (critique)
- Puentes-Mestril C, Aton SJ (2017). Linking network activity to synaptic plasticity during sleep: hypotheses and recent data. *Front Neural Circuits* 11:61. doi:10.3389/fncir.2017.00061

## 12. Homeostatic synaptic scaling

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
- Kim J, Tsien RW (2008). Synapse-specific adaptations to inactivity in hippocampal circuits achieve homeostatic gain control while dampening network reverberation. *Neuron* 58:925–937. doi:10.1016/j.neuron.2008.05.009
- Stellwagen D, Malenka RC (2006). Synaptic scaling mediated by glial TNF-α. *Nature* 440:1054–1059.
- Shepherd JD, Rumbaugh G, Wu J, et al. (2006). Arc/Arg3.1 mediates homeostatic synaptic scaling of AMPA receptors. *Neuron* 52:475–484.
- Branco T, Staras K, Darcy KJ, Goda Y (2008). Local dendritic activity sets release probability at hippocampal synapses. *Neuron* 59:475–485.
- Murthy VN, Schikorski T, Stevens CF, Zhu Y (2001). Inactivity produces increases in neurotransmitter release and synapse size. *Neuron* 32:673–682.
- Desai NS, Cudmore RH, Nelson SB, Turrigiano GG (2002). Critical periods for experience-dependent synaptic scaling in visual cortex. *Nat Neurosci* 5:783–789. doi:10.1038/nn878 (in vivo manipulation, juvenile rat V1)
- Keck T, Keller GB, Jacobsen RI, Eysel UT, Bonhoeffer T, Hübener M (2013). Synaptic scaling and homeostatic plasticity in the mouse visual cortex in vivo. *Neuron* 80:327–334. doi:10.1016/j.neuron.2013.08.018 (scaling *up* after retinal lesion)

Related non-synaptic homeostatic routes, listed for completeness: intrinsic
excitability scaling (Desai NS, Rutherford LC, Turrigiano GG 1999, *Nat Neurosci*
2:515–520) and inhibitory plasticity (Vogels TP, Sprekeler H, Zenke F, Clopath C,
Gerstner W 2011, *Science* 334:1569–1573). Both lower output without depressing
excitatory weights.

## 13. Structural pruning and active forgetting

**Mechanism.** On timescales of days to months, synapses are physically removed.
In adult hippocampus, microglia eliminate synapses through complement tagging, and
depleting microglia or blocking complement prevents forgetting of contextual fear
memory. Rac1/cofilin signalling drives active forgetting (first shown in
*Drosophila*; in mouse hippocampus, Rac1 inhibition prolongs and Rac1 activation
shortens object-recognition memory). Adult neurogenesis in the dentate gyrus causes forgetting of
hippocampus-dependent memories.

**Spec hook.** The fate of an uncaptured or unreplayed trace on the slow side of
model §3. Neurogenesis acts in DG, outside the minimal CA1 circuit.

**References.**
- Wang C, Yue H, Hu Z, et al. (2020). Microglia mediate forgetting via complement-dependent synaptic elimination. *Science* 367:688–694. doi:10.1126/science.aaz2288
- Schafer DP, Lehrman EK, Kautzman AG, et al. (2012). Microglia sculpt postnatal neural circuits in an activity and complement-dependent manner. *Neuron* 74:691–705. (developing retinogeniculate system. Mechanistic precedent only, not adult evidence.)
- Shuai Y, Lu B, Hu Y, Wang L, Sun K, Zhong Y (2010). Forgetting is regulated through Rac activity in *Drosophila*. *Cell* 140:579–589. (invertebrate)
- Liu Y, Du S, Lv L, et al. (2016). Hippocampal activation of Rac1 regulates the forgetting of object recognition memory. *Curr Biol* 26:2351–2357. doi:10.1016/j.cub.2016.06.056 (mouse hippocampus)
- Davis RL, Zhong Y (2017). The biology of forgetting: a perspective. *Neuron* 95:490–503.
- Akers KG, Martinez-Canabal A, Restivo L, et al. (2014). Hippocampal neurogenesis regulates forgetting during adulthood and infancy. *Science* 344:598–602.

---

## Biological plausibility in the healthy adult mammalian hippocampus and cortex

The question for each entry is whether the mechanism has been shown to operate in
healthy, adult mammalian hippocampus or neocortex, or whether the evidence comes
from developing, cultured, anaesthetized, pharmacologically altered, non-mammalian
or out-of-region preparations. Grades:

- **Established.** Shown in adult hippocampus or cortex *in vivo* under
  physiological conditions (behaviour or natural sleep), not only after
  pharmacological manipulation.
- **Probable.** Shown in adult or near-adult tissue, but only *in vitro* or with
  artificial induction. Occurrence in the intact healthy animal is inferred,
  not directly shown, by the cited evidence.
- **Conditional.** The cited evidence comes mainly from developing, cultured,
  anaesthetized or pharmacologically altered preparations, or from outside
  hippocampus and cortex. Occurrence in healthy adult hippocampus is open.

None of the 13 mechanisms is disease-specific: each has been reported in
tissue from animals without a disease model. Grades refer to the evidence cited
in this document, not to an exhaustive literature search.

| # | Mechanism | Grade | Strongest healthy-adult evidence cited | Main limitation |
|---|---|---|---|---|
| 1 | Short-term depression | Probable | Vesicle depletion at hippocampal synapses (Dobrunz & Stevens 1997) | Magnitude depends on [Ca²⁺]ₒ and release probability; slice ACSF usually has higher [Ca²⁺]ₒ than brain interstitial fluid |
| 2 | Presynaptic inhibition | Probable | GABA_B heteroreceptor depression of CA1 transmission after repetitive stimulation, rat slices (Isaacson et al. 1993) | Wake-dependent adenosine rise is shown in cat basal forebrain, not hippocampus |
| 3 | SWR-associated depression | Probable | Ripple silencing during natural slow-wave states blocks downregulation of net synaptic weight, mouse hippocampus (Norimoto et al. 2018) | One direct hippocampal study in this list; cortical support is from P15–P21 mice under urethane |
| 4 | NMDAR-LTD / STDP depression | Established (LFS-LTD) | 1 Hz × 900 pulses gives NMDAR-dependent LTD in adult freely moving rats (Manahan-Vaughan 1997); enabled by novelty exploration (Manahan-Vaughan & Braunewell 1999) | Magnitude falls with age; STDP windows come from young slices and cultures |
| 5 | Depotentiation / tag reset | Established (depotentiation) | Exploration of a novel environment reverses E-LTP in CA1 in vivo within a time window (Xu et al. 1998) | Tag reset itself is shown only in vitro (Sajikumar & Frey 2004) |
| 6 | Heterosynaptic depression | Probable | Depression of spines adjacent to potentiated ones, mouse V1 in vivo (El-Boustani et al. 2018) | CA1 evidence is from slices and P6–P7 organotypic cultures; weight *conservation* is shown only in amygdala |
| 7 | mGluR-LTD (protein-synthesis dependent) | Conditional | Protein-synthesis-dependent, postsynaptic mGluR-LTD in P21–P35 rat CA1 slices (Nosyreva & Huber 2005; mechanism in Huber et al. 2000) | In adult freely moving rats, group I agonists *potentiate* CA1 transmission (Manahan-Vaughan & Reymann 1997) |
| 8 | Passive E-LTP / tag decay | Established | Decremental LTP in vivo (Racine et al. 1983); blocking GluA2 endocytosis prevents natural forgetting in adult rats (Migues et al. 2016) | The τ ≈ 1–3 h value is an in vitro figure; in vivo decay is partly experience-driven (Abraham et al. 2002) |
| 9 | PRP competition | Conditional | "Competitive maintenance" in hippocampal slices (Fonseca et al. 2004) | Shown only under partial pharmacological inhibition of protein synthesis |
| 10 | BCM sliding threshold | Probable (phenomenon); Conditional (BCM functional form) | Experience shifts the LTD/LTP crossover in rat V1 (Kirkwood et al. 1996); adult V1 regains plasticity after dark exposure (He et al. 2006) | Direct θ_m measurements are developmental and in visual cortex; θ_m as a function of mean activity is not measured in adult hippocampus |
| 11 | Sleep renormalization (SHY) | Probable in cortex; contested in hippocampus | Wake/sleep changes in GluA1 and evoked responses, rat cortex (Vyazovskiy et al. 2008); ~18% ASI shrinkage after sleep, mouse cortex (de Vivo et al. 2017) | Sleep also promotes spine formation (Yang et al. 2014); in CA1, firing rates rise within NREM and fall within REM (Grosmark et al. 2012) |
| 12 | Synaptic scaling (down) | Conditional in adult hippocampus | Sleep-associated scaling-down in mice in vivo (Diering et al. 2017; this overlaps #11) | Core evidence is from dissociated or TTX-treated organotypic cultures; in vivo cortical evidence is mostly scaling *up* |
| 13 | Pruning / active forgetting | Established | Microglial, complement-dependent synapse elimination drives forgetting in healthy adult mice (Wang et al. 2020); neurogenesis-induced forgetting in adult mice (Akers et al. 2014); Rac1 in mouse hippocampus (Liu et al. 2016) | Schafer et al. 2012 is developmental; Shuai et al. 2010 is *Drosophila* |

### Notes by mechanism

**#1.** Vesicle depletion is a general property of release, so the mechanism
itself is not in doubt. Its *size* is condition-dependent. Lower [Ca²⁺]ₒ lowers
release probability, which reduces depletion and favours facilitation at
Schaffer-collateral synapses. Per `CLAUDE.md`, TM parameters must be recorded
with the [Ca²⁺]ₒ at which they were measured.

**#2.** The original Davies et al. (1991) citation was misattributed. That paper
concerns GABA_B *autoreceptors* on interneuron terminals, which disinhibit CA1
and *promote* LTP. Isaacson et al. (1993) is the correct evidence for GABA_B
heteroreceptors depressing glutamate release. Linking hippocampal A1 tone to
sleep pressure extrapolates from basal-forebrain microdialysis (Porkka-Heiskanen
et al. 1997). That link is not shown for hippocampus by the cited evidence.

**#3.** Norimoto et al. (2018) is the only direct hippocampal synaptic evidence
cited. Grosmark et al. (2012) and Miyawaki & Diba (2016) measure firing rates,
not synaptic weights. González-Rueda et al. (2018) used juvenile (P15–P21) mice
with slow-wave-sleep-*like* activity under urethane anaesthesia. Lewis & Durrant
(2011) was removed because it contains no evidence on this mechanism.

**#4.** The mechanism is present in adults but weaker and state-gated. LFS-LTD
was −45 ± 4% in rats under 2 weeks old versus −20 ± 4% at 5 weeks (Dudek & Bear
1993). In vivo it differed by strain (Wistar vs Hooded Lister) and was enabled
or enhanced by novelty (Manahan-Vaughan & Braunewell 1999). Parameters fitted to
juvenile slices therefore overestimate adult LTD. For STDP, the canonical windows
come from young neocortical slices (Markram et al. 1997) and dissociated culture
(Bi & Poo 1998). At CA3→CA1, depression needs hundreds of pairings and has a
broad timing dependence, while potentiation needs postsynaptic bursts at ≥5 Hz
(Wittenberg & Wang 2006). A fixed, symmetric negative lobe of ±20 ms is
therefore not an accurate description of the CA1 rule.

**#5.** This mechanism has the strongest physiological evidence of the Hebbian
group. A natural behaviour (exploring a novel, non-stressful environment)
reverses early-LTP but not long-established LTP, which matches the time window
in the spec hook (Xu et al. 1998).

**#6.** The hippocampal evidence comes from slices and from neonatal-derived
organotypic cultures (Oh et al. 2015, P6–P7). Exact conservation of total weight
was shown in amygdala intercalated neurons (Royer & Paré 2003), not in
hippocampus or cortex. A strict per-segment conservation rule is therefore a
modelling assumption that is stronger than the evidence. Depression of
neighbouring synapses is the supported part.

**#7.** The protein-synthesis-dependent, postsynaptic form that the spec hook
relies on is documented in adolescent (P21–P35) slices. In neonates (P8–P15),
mGluR-LTD is presynaptic and independent of protein synthesis (Nosyreva & Huber
2005). In adult freely moving rats, intracerebroventricular DHPG produced
slow-onset *potentiation* in CA1 and a group II agonist produced depression
(Manahan-Vaughan & Reymann 1997). Synaptically induced LTD in vivo requires group
II mGluRs and is only partly reduced by group I antagonism (Manahan-Vaughan
1997). The slice DHPG-LTD phenomenon therefore does not transfer directly to the
adult animal. Do not take parameters from Fmr1-knockout studies, where
mGluR-LTD is enhanced in a disease model (Huber KM, Gallagher SM, Warren ST,
Bear MF 2002, *PNAS* 99:7746–7750, doi:10.1073/pnas.122205699).

**#8.** In vivo, potentiation contains decremental components (Racine et al.
1983). Even LTP that lasts months in dentate gyrus was reversed by repeated
enriched-environment exposure that began 14 days after induction, but not when
exposure began at 90 days (Abraham et al. 2002). Part of the in vivo "decay" is
therefore active and experience-driven, overlapping #5 and #13. "Passive" decay
is a modelling simplification.

**#9.** Fonseca et al. (2004) demonstrated competition only "under regimes of
reduced protein synthesis". The cited evidence does not show whether synapses
compete at physiological synthesis rates. A depletable, shared PRP pool is
therefore a hypothesis for the healthy state and should be tested as such: run
S4–S6 with and without depletion.

**#10.** The direct evidence that θ_m depends on experience is from light
deprivation in rat visual cortex (Kirkwood et al. 1996) and from developmental
NMDAR subunit changes (Philpot et al. 2001). He et al. (2006) show adult V1
regains rapid plasticity after dark exposure. That result is consistent with a
lowered threshold, but it is not a θ_m measurement. Metaplasticity in general is
well documented in adults (Abraham 2008). The BCM functional form, θ_m as a
function of time-averaged postsynaptic activity, is a theory that has not been
measured in adult hippocampus.

**#11.** The supporting data are mainly cortical (Vyazovskiy et al. 2008; de
Vivo et al. 2017; Diering et al. 2017). In de Vivo et al. (2017), scaling spared
the largest synapses, so it is not uniform. Sleep also promotes branch-specific
spine formation after learning (Yang et al. 2014), and REM both prunes and
strengthens new spines (Li et al. 2017). In CA1, rates rise within NREM and fall
within REM (Grosmark et al. 2012). Frank (2012) concludes that the mechanisms of
SHY are unknown. For the hippocampus, the specific downscaling evidence in this
document is #3.

**#12.** Most of the evidence comes from chronic pharmacological silencing (TTX)
or disinhibition in dissociated cultures (Turrigiano et al. 1998; Stellwagen &
Malenka 2006; Shepherd et al. 2006; Branco et al. 2008; Murthy et al. 2001) or in
organotypic hippocampal cultures (Kim & Tsien 2008). These activity regimes lie
outside the physiological range. In vivo studies in cortex show scaling *up*
after sensory deprivation (Desai et al. 2002, juvenile rat V1 within a critical
period; Keck et al. 2013, mouse V1). Desai et al. also report a developmental
decrease in mEPSC amplitude (P12–P23) that dark rearing prevents, which is an in
vivo scaling-down during development. In adults, in vivo scaling-down evidence
is the sleep data of #11. Scaling-down in adult hippocampus is open.

**#13.** Wang et al. (2020) explicitly used healthy adult mice. Schafer et al.
(2012) is retained only as a mechanistic precedent from the developing
retinogeniculate system. The *Drosophila* Rac result is supported in mammals by
Liu et al. (2016).

### Consequences for the model

- Use the **Established** mechanisms (#4 as LFS-LTD, #5, #8, #13) without
  qualification beyond the usual parameter sourcing.
- Treat **Probable** mechanisms (#1, #2, #3, #6, #10 as phenomenon, #11 in
  cortex) as supported, but take parameters from the closest adult preparation
  and record the preparation in `params.py`.
- Treat **Conditional** mechanisms (#7 as a protein-synthesis-dependent
  competitor for PRPs, #9, #12 as scaling-down) as hypotheses. Each needs an
  on/off comparison, and none of them should be required for a stage's
  acceptance criterion.

---

## Computational references

| Topic | References |
|---|---|
| Weight normalization | von der Malsburg C (1973) *Kybernetik* 14:85–100; Oja E (1982) *J Math Biol* 15:267–273; Miller KD, MacKay DJC (1994) *Neural Comput* 6:100–126 |
| STDP with synaptic scaling | van Rossum MCW, Bi GQ, Turrigiano GG (2000) *J Neurosci* 20:8812–8821 |
| Homeostasis across timescales | Zenke F, Agnes EJ, Gerstner W (2015) *Nat Commun* 6:6922; Zenke F, Gerstner W (2017) *Phil Trans R Soc B* 372:20160259 |
| Tag/capture models with decay | Clopath C, Ziegler L, Vasilaki E, Büsing L, Gerstner W (2008) *PLoS Comput Biol* 4:e1000248; Barrett AB, Billings GO, Morris RGM, van Rossum MCW (2009) *PLoS Comput Biol* 5:e1000259 |
| Multi-timescale memory | Fusi S, Drew PJ, Abbott LF (2005) *Neuron* 45:599–611; Benna MK, Fusi S (2016) *Nat Neurosci* 19:1697–1706 |

Zenke & Gerstner (2017) argue that compensatory processes must be fast (comparable
to the Hebbian timescale). Biologically slow scaling (#12) alone cannot stabilize
Hebbian growth. Fast candidates are #3, #6 and #10.

## Candidates for tinyHippo (after S4–S6 tag/capture)

Plausibility grades from the section above are given in brackets.

1. **#8 + #5** [Established]. Passive tag decay plus LFS-driven active reset. Fills model §2 directly
   and adds a second falsification arm.
2. **#4 + #10** [Established + Probable]. Two-threshold `g_Ca` with a sliding θ_p. One extra state
   variable per segment. Fit LTD to adult data, not juvenile slices, and do not
   assume a symmetric ±20 ms negative STDP lobe at CA3→CA1.
3. **#6** [Probable]. Heterosynaptic depression at `V_seg` granularity. Strict conservation
   is an assumption that goes beyond the evidence.
4. **#3** [Probable]. SWR-gated depression of non-replayed synapses. Needs ripple-epoch input,
   and any timescale compression factor must be stated.
5. **#12** [Conditional]. Multiplicative scaling, only with a stated compression factor,
   and as an on/off hypothesis.

<!-- test text: push check -->
