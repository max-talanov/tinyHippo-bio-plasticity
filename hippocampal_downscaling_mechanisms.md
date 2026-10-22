# Hippocampal Downscaling Mechanisms

Companion to `hippocampal_timescales_as_circuit_spec.md`. That document lays out the
*upscaling* path: STP → Ca²⁺/kinase → E-LTP → tag & capture → L-LTP → SWR replay →
systems consolidation. This one lists the mechanisms that *weaken* synapses or keep
their total bounded. Each entry gives its timescale, its hook in the spec's circuit
model (§2 tag/capture, §3.2 synaptic-area "activity-dependent weight decay", §4.2
`V_seg`, §4.5 replay), and its primary literature.

![Thirteen synaptic downscaling mechanisms plotted on the same logarithmic time axis as Fig. 1 of the circuit spec, from 1 ms to 10 years. Short-term depression and presynaptic inhibition occupy milliseconds to minutes; Hebbian, heterosynaptic and tag-related depression occupy minutes to hours; BCM metaplasticity, SWR-associated depression, sleep renormalization and synaptic scaling span hours to days; pruning and active forgetting extend from days to a year.](figures/downscaling_timescale_axis.png)

*Fig. D1. Downscaling mechanisms on the log time axis of the spec's Fig. 1. A bar's
position marks onset and its length marks characteristic duration. Dotted tails
are recurring or extended effects. Spans are order-of-magnitude summaries of the
references below, not fitted values. Regenerate with
`python3 figures/make_downscaling_timescale_axis.py`.*

**Citation status.** The entries below were compiled for orientation. The
bibliographic details of Norimoto 2018, González-Rueda 2018, Oh 2015, Kim & Tsien
2008, Fonseca 2004, Royer & Paré 2003, Branco 2008, Migues 2016, Wang 2020,
Li 2017, Sajikumar & Frey 2004 and Miyawaki & Diba 2016 have been checked against
PubMed/PMC or publisher records (DOIs given). The rest are standard citations that
have not been checked. Per `CLAUDE.md`, a parameter taken from any of these must
be checked against the source and recorded in `params.py` with its recording
conditions before use.

## Summary

| # | Mechanism | Timescale | Spec hook | Class |
|---|---|---|---|---|
| 1 | Short-term depression | 10 ms–10 s | STP (S0–S3) | transient, presynaptic |
| 2 | Presynaptic inhibition (adenosine A1, GABA_B, mGluR) | 50 ms–min (tonic: hours) | neuromodulatory input, §3.2 | transient, presynaptic |
| 3 | NMDAR-dependent LTD / STDP depression | induction s–min, expression hours | `g_Ca(V_seg)` low-Ca branch, §4.2 | Hebbian |
| 4 | mGluR-LTD | min–1 day | PRP pool, §2 | Hebbian, protein-synthesis dependent |
| 5 | Depotentiation / tag reset | window 1 min–1 hr | active reset of the §2 tag | Hebbian, reversal |
| 6 | Passive E-LTP / tag decay | τ ≈ 1–4 hr | τ_tag decay in Fig. 2 | intrinsic decay |
| 7 | Heterosynaptic depression | min–hours | per-segment conservation (`V_seg` unit) | competitive |
| 8 | PRP competition | 30 min–8 hr | capture threshold, §2 | competitive |
| 9 | BCM sliding threshold / metaplasticity | 30 min–days | LTD/LTP crossover of `g_Ca` | homeostatic |
| 10 | SWR-associated depression | ripple 100 ms, effect hours, recurs over days | §4.5 replay | sleep / replay |
| 11 | Sleep renormalization (SHY) | hours, each sleep cycle | global downscaling between replay epochs | sleep / homeostatic |
| 12 | Synaptic scaling | 12 hr–days | §3.2 weight decay | homeostatic |
| 13 | Pruning and active forgetting | days–months | removal of uncaptured traces | structural |

---

## 1. Short-term depression

**Mechanism.** Each spike depletes the readily releasable vesicle pool, so later
EPSCs in a train shrink until the pool recovers (τ_rec ~ 100 ms–1 s). Release-site
refractoriness and receptor desensitization add to the effect. The stored weight
does not change, only the efficacy read out from it. This is the TM-model
depression term already used in S0–S3.

**Spec hook.** STP in §1 and §4.2. It downscales transmission during high-rate
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

**Spec hook.** The separate neuromodulatory input to the synaptic area (§3.2).
Expressed as a scaling of the TM parameter U.

**References.**
- Dunwiddie TV, Masino SA (2001). The role and regulation of adenosine in the central nervous system. *Annu Rev Neurosci* 24:31–55.
- Porkka-Heiskanen T et al. (1997). Adenosine: a mediator of the sleep-inducing effects of prolonged wakefulness. *Science* 276:1265–1268.
- Davies CH, Starkey SJ, Pozza MF, Collingridge GL (1991). GABA_B autoreceptors regulate the induction of LTP. *Nature* 349:609–611.

## 3. NMDAR-dependent LTD and STDP depression

**Mechanism.** Modest, prolonged postsynaptic Ca²⁺ influx through NMDARs (for
example 1 Hz for 15 min) preferentially activates phosphatases (calcineurin, PP1)
over CaMKII. AMPARs are then dephosphorylated and endocytosed. Under STDP, the same
low-Ca regime is reached when the postsynaptic spike precedes the presynaptic one.

**Spec hook.** §4.2 `g_Ca(V_seg)`. Read with the calcium-control hypothesis, a single
sigmoid becomes two thresholds: θ_d < Ca < θ_p gives depression and Ca > θ_p gives
a tag. The ±20 ms STDP window in §4.3 gains a negative lobe.

**References.**
- Dudek SM, Bear MF (1992). Homosynaptic long-term depression in area CA1 of hippocampus and effects of NMDA receptor blockade. *PNAS* 89:4363–4367.
- Mulkey RM, Malenka RC (1992). Mechanisms underlying induction of homosynaptic long-term depression in area CA1 of the hippocampus. *Neuron* 9:967–975.
- Lisman J (1989). A mechanism for the Hebb and the anti-Hebb processes underlying learning and memory. *PNAS* 86:9574–9578.
- Mulkey RM, Endo S, Shenolikar S, Malenka RC (1994). Involvement of a calcineurin/inhibitor-1 phosphatase cascade in hippocampal long-term depression. *Nature* 369:486–488.
- Markram H, Lübke J, Frotscher M, Sakmann B (1997). Regulation of synaptic efficacy by coincidence of postsynaptic APs and EPSPs. *Science* 275:213–215.
- Bi GQ, Poo MM (1998). Synaptic modifications in cultured hippocampal neurons: dependence on spike timing, synaptic strength, and postsynaptic cell type. *J Neurosci* 18:10464–10472.
- Shouval HZ, Bear MF, Cooper LN (2002). A unified model of NMDA receptor-dependent bidirectional synaptic plasticity. *PNAS* 99:10831–10836. (model)
- Graupner M, Brunel N (2012). Calcium-based plasticity model explains sensitivity of synaptic changes to spike pattern, rate, and dendritic location. *PNAS* 109:3991–3996. (model)

## 4. mGluR-dependent LTD

**Mechanism.** Group I mGluR activation (DHPG or paired-pulse LFS) triggers local
dendritic translation of Arc, STEP and MAP1B, which drives AMPAR endocytosis. Like
L-LTP, it depends on protein synthesis, so it draws on the same translational
machinery as capture.

**Spec hook.** The §2 PRP pool. A depressive process that competes with
potentiation for capture.

**References.**
- Oliet SHR, Malenka RC, Nicoll RA (1997). Two distinct forms of long-term depression coexist in CA1 hippocampal pyramidal cells. *Neuron* 18:969–982.
- Huber KM, Kayser MS, Bear MF (2000). Role for rapid dendritic protein synthesis in hippocampal mGluR-dependent long-term depression. *Science* 288:1254–1257.
- Waung MW, Pfeiffer BE, Nosyreva ED, Ronesi JA, Huber KM (2008). Rapid translation of Arc/Arg3.1 selectively mediates mGluR-dependent LTD through persistent increases in AMPAR endocytosis rate. *Neuron* 59:84–97.

## 5. Depotentiation and tag reset

**Mechanism.** Low-frequency stimulation delivered shortly after LTP induction
(within roughly 10–60 min) erases E-LTP. Once the potentiation has consolidated, the
same stimulation no longer reverses it. Sajikumar & Frey showed that this
time-dependent reset acts on the synaptic tag itself: a reset tag can no longer
capture PRPs. Cross-tagging (LTP and LTD inputs sharing PRPs) comes from the same
group.

**Spec hook.** An **active** reset of the §2 tag, separate from passive τ_tag decay.
It gives the S4–S6 falsification test a second arm: LFS within the window should
abolish capture.

**References.**
- Staubli U, Lynch G (1990). Stable depression of potentiated synaptic responses in the hippocampus with 1–5 Hz stimulation. *Brain Res* 513:113–118.
- Fujii S, Saito K, Miyakawa H, Ito K, Kato H (1991). Reversal of long-term potentiation (depotentiation) induced by tetanus stimulation of the input to CA1 neurons of guinea pig hippocampal slices. *Brain Res* 555:112–122.
- O'Dell TJ, Kandel ER (1994). Low-frequency stimulation erases LTP through an NMDA receptor-mediated activation of protein phosphatases. *Learn Mem* 1:129–139.
- Sajikumar S, Frey JU (2004). Resetting of "synaptic tags" is time- and activity-dependent in rat hippocampal CA1 in vitro. *Neuroscience* 129:503–507. doi:10.1016/j.neuroscience.2004.08.014
- Sajikumar S, Frey JU (2004). Late-associativity, synaptic tagging, and the role of dopamine during LTP and LTD. *Neurobiol Learn Mem* 82:12–25.

## 6. Passive E-LTP and tag decay

**Mechanism.** Without capture, E-LTP decays over 1–3 hr as inserted AMPARs are
removed by constitutive, GluA2-dependent endocytosis. Even consolidated memories
show an ongoing, decay-like forgetting process that blocking GluA2 removal
prevents.

**Spec hook.** τ_tag decay in Fig. 2 of the spec, and the volatile-memristor
relaxation of §4.4.2. This is the baseline against which capture is measured.

**References.**
- Frey U, Morris RGM (1997). Synaptic tagging and long-term potentiation. *Nature* 385:533–536.
- Redondo RL, Morris RGM (2011). Making memories last: the synaptic tagging and capture hypothesis. *Nat Rev Neurosci* 12:17–30.
- Migues PV, Liu L, Archbold GEB, et al. (2016). Blocking synaptic removal of GluA2-containing AMPA receptors prevents the natural forgetting of long-term memories. *J Neurosci* 36:3481–3494. doi:10.1523/JNEUROSCI.3333-15.2016
- Hardt O, Nader K, Nadel L (2013). Decay happens: the role of active forgetting in memory. *Trends Cogn Sci* 17:111–120.
- Pastalkova E, Serrano P, Pinkhasova D, et al. (2006). Storage of spatial information by the maintenance mechanism of LTP. *Science* 313:1141–1144. (PKMζ maintenance. Contested by Volk LJ et al. 2013, *Nature* 493:420–423, and Lee AM et al. 2013, *Nature* 493:416–419.)

## 7. Heterosynaptic depression

**Mechanism.** Potentiation of a cluster of synapses depresses or shrinks nearby
*unstimulated* synapses on the same dendritic segment. In CA1 this needs
calcineurin, IP3R and group I mGluR, and only appears after several neighbours
are potentiated. In amygdala intercalated cells, opposite-signed heterosynaptic
changes conserve the total synaptic weight.

**Spec hook.** Per-segment weight conservation at the same granularity as `V_seg`
(one state per `thr` unit). It gives the cluster topology of §4.1 a
normalization rule.

**References.**
- Lynch GS, Dunwiddie T, Gribkoff V (1977). Heterosynaptic depression: a postsynaptic correlate of long-term potentiation. *Nature* 266:737–739.
- Oh WC, Parajuli LK, Zito K (2015). Heterosynaptic structural plasticity on local dendritic segments of hippocampal CA1 neurons. *Cell Rep* 10:162–169. doi:10.1016/j.celrep.2014.12.016
- Royer S, Paré D (2003). Conservation of total synaptic weight through balanced synaptic depression and potentiation. *Nature* 422:518–522. doi:10.1038/nature01530
- Chistiakova M, Bannon NM, Bazhenov M, Volgushev M (2014). Heterosynaptic plasticity: multiple mechanisms and multiple roles. *Neuroscientist* 20:483–498.
- El-Boustani S, Ip JPK, Breton-Provencher V, et al. (2018). Locally coordinated synaptic plasticity of visual cortex neurons in vivo. *Science* 360:1349–1354. (cortex)

## 8. Competition for plasticity-related proteins

**Mechanism.** When protein synthesis is limited, potentiating one input at the
expense of another makes the other pathway's established LTP decay. Synapses
compete for a finite PRP pool, so capture at one site can leave another
uncaptured. A balance between synthesis and proteasomal degradation sets how
long LTP is maintained.

**Spec hook.** Makes the §2 capture threshold a shared, depletable resource rather
than an independent per-synapse gate.

**References.**
- Fonseca R, Nägerl UV, Morris RGM, Bonhoeffer T (2004). Competing for memory: hippocampal LTP under regimes of reduced protein synthesis. *Neuron* 44:1011–1020. doi:10.1016/j.neuron.2004.10.033
- Fonseca R, Vabulas RM, Hartl FU, Bonhoeffer T, Nägerl UV (2006). A balance of protein synthesis and proteasome-dependent degradation determines the maintenance of LTP. *Neuron* 52:239–245.

## 9. BCM sliding threshold and metaplasticity

**Mechanism.** The LTD/LTP crossover point shifts with the recent history of
postsynaptic activity. High prior activity raises the threshold, which favours
depression. Low prior activity lowers it. NMDAR subunit composition (GluN2A/2B)
is one substrate of the shift.

**Spec hook.** A slow variable that moves θ_p of `g_Ca` in §4.2. It costs one extra
state per neuron or segment.

**References.**
- Bienenstock EL, Cooper LN, Munro PW (1982). Theory for the development of neuron selectivity. *J Neurosci* 2:32–48.
- Abraham WC, Bear MF (1996). Metaplasticity: the plasticity of synaptic plasticity. *Trends Neurosci* 19:126–130.
- Abraham WC (2008). Metaplasticity: tuning synapses and networks for plasticity. *Nat Rev Neurosci* 9:387–399.
- Philpot BD, Sekhar AK, Shouval HZ, Bear MF (2001). Visual experience and deprivation bidirectionally modify the composition and function of NMDA receptors in visual cortex. *Neuron* 29:157–169.

## 10. SWR-associated depression

**Mechanism.** In mouse hippocampus, sharp-wave ripples during slow-wave states
trigger long-lasting, NMDAR-dependent and pathway-specific synaptic depression.
Suppressing ripples prevents the spontaneous downregulation of net synaptic
weight and impairs learning of new memories. Across sleep, CA1 firing rates fall,
and the size of that drop is predicted by NREM spindle/SWR incidence followed by
REM. In cortex, Up states bias plasticity toward depression of inputs that do not
drive the postsynaptic cell, while inputs that do drive it are spared.

**Spec hook.** §4.5. The same SWR event that replays and captures the stored
sequence also depresses the rest of the synapses. Replay therefore acts as
selection (capture what is replayed, depress what is not), not only as
potentiation.

**References.**
- Norimoto H, Makino K, Gao M, et al. (2018). Hippocampal ripples down-regulate synapses. *Science* 359:1524–1527. doi:10.1126/science.aao0702
- Miyawaki H, Diba K (2016). Regulation of hippocampal firing by network oscillations during sleep. *Curr Biol* 26:893–902.
- Grosmark AD, Mizuseki K, Pastalkova E, Diba K, Buzsáki G (2012). REM sleep reorganizes hippocampal excitability. *Neuron* 75:1001–1007.
- González-Rueda A, Pedrosa V, Feord RC, Clopath C, Paulsen O (2018). Activity-dependent downscaling of subthreshold synaptic inputs during slow-wave-sleep-like activity in vivo. *Neuron* 97:1244–1252. doi:10.1016/j.neuron.2018.01.047 (cortex)
- Lewis PA, Durrant SJ (2011). Overlapping memory replay during sleep builds cognitive schemata. *Trends Cogn Sci* 15:343–351.

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

## 12. Homeostatic synaptic scaling

**Mechanism.** Chronic changes in firing rate scale all of a neuron's excitatory
synapses multiplicatively, which preserves their relative weights. Prolonged
activity scales them down and silencing scales them up, over about 24–48 hr.
Effectors include TNFα from glia, Arc/Arg3.1 and Homer1a. The response in the
hippocampus is synapse-type specific: silencing strengthens the throughput
DG→CA3 and CA3→CA1 synapses but weakens recurrent CA3→CA3 synapses. Release
probability is also regulated homeostatically by local dendritic activity.

**Spec hook.** The "activity-dependent weight decay" of the synaptic area (§3.2).
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
*Drosophila*). Adult neurogenesis in the dentate gyrus causes forgetting of
hippocampus-dependent memories.

**Spec hook.** The fate of an uncaptured or unreplayed trace on the slow side of
§4.5. Neurogenesis acts in DG, outside the minimal CA1 circuit.

**References.**
- Wang C, Yue H, Hu Z, et al. (2020). Microglia mediate forgetting via complement-dependent synaptic elimination. *Science* 367:688–694. doi:10.1126/science.aaz2288
- Schafer DP, Lehrman EK, Kautzman AG, et al. (2012). Microglia sculpt postnatal neural circuits in an activity and complement-dependent manner. *Neuron* 74:691–705.
- Shuai Y, Lu B, Hu Y, Wang L, Sun K, Zhong Y (2010). Forgetting is regulated through Rac activity in *Drosophila*. *Cell* 140:579–589.
- Davis RL, Zhong Y (2017). The biology of forgetting: a perspective. *Neuron* 95:490–503.
- Akers KG, Martinez-Canabal A, Restivo L, et al. (2014). Hippocampal neurogenesis regulates forgetting during adulthood and infancy. *Science* 344:598–602.

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
Hebbian growth. Fast candidates are #7, #9 and #10.

## Candidates for tinyHippo (after S4–S6 tag/capture)

1. **#6 + #5.** Passive tag decay plus LFS-driven active reset. Fills §2 directly
   and adds a second falsification arm.
2. **#3 + #9.** Two-threshold `g_Ca` with a sliding θ_p. One extra state variable per segment.
3. **#7.** Per-segment heterosynaptic conservation at `V_seg` granularity.
4. **#10.** SWR-gated depression of non-replayed synapses. Needs ripple-epoch input,
   and any timescale compression factor must be stated.
5. **#12.** Multiplicative scaling, only with a stated compression factor.
