# STDP-like plasticity rules ranked by bio-plausibility

Nov 10, 2026 · analysis for the project owner

This document compares long-term plasticity rules of the STDP family (timing-, rate- and
frequency-dependent rules, including Markram's frequency-dependent results) and ranks them by
bio-plausibility. It complements [`related_models.md`](related_models.md), which ranks models by
*level of description*. Here the question is narrower: **which update rule is the most credible
account of how a CA1 excitatory synapse changes, and in particular how it gets weaker?**

**Citation status (2026-11-10).** Every reference in Section 6 was checked against PubMed
(authors, year, title, journal, volume, pages, PMID, DOI). Claims attributed to a paper were
checked against its **abstract only**. Claims that the abstract does not cover are marked
*[not in abstract]* and remain from memory. Per `CLAUDE.md`, no number from this document goes into
`params.py` until it is read from the full paper with its recording conditions.

## 1. Why classical Hebbian depression fails

Hebb's postulate only describes strengthening. Every classical rule adds weakening by hand, and
each way of adding it lacks a biological counterpart:

| Classical device | Example | Problem |
|---|---|---|
| Passive decay `−γw` | Hebb + decay | Weakening does not depend on activity. Real LTD needs specific induction: low-frequency drive, moderate Ca²⁺, mGluR or eCB signalling |
| Subtractive or divisive normalization | Σw = const | Each synapse would need the sum of all other weights on the cell. No such signal exists at the synapse on a seconds timescale. Synaptic scaling exists but takes hours to days and is multiplicative |
| Oja term `−y²w` | Oja 1982 | Local in form, but it is a mathematical device that makes the neuron converge to the principal component, with no mechanism behind it |
| Covariance below the mean | Sejnowski 1977 | Depression when activity is below its mean. It predicts LTD from silence and has no frequency threshold |
| Heterosynaptic depression of inactive inputs | Stent 1973 | Stent proposed that a postsynaptic spike removes receptors at every synapse that did not help fire it. Heterosynaptic LTD exists in CA1, but only under specific conditions (e.g. reduced NMDAR Ca²⁺ with IP3R signalling; Nishiyama 2000), not after every postsynaptic spike |

The objection is to *how* depression is produced, not to its existence. Low-frequency LTD in CA1 is
well documented: 900 pulses at 1–3 Hz depress Schaffer collateral input for more than 1 h, 10 Hz
gives no lasting change and 50 Hz usually potentiates, and NMDAR antagonists block the depression
(Dudek & Bear 1992). A plausible rule has to obtain depression from an induction signal that is
present at the synapse and that has been measured. The ranking below rewards that.

## 2. Criteria

Each rule is scored 0–2 on seven criteria (maximum 14).

| Code | Criterion | 2 = | 0 = |
|---|---|---|---|
| **L** | Locality | Uses only quantities present at the synapse or dendritic segment: transmitter release, local V or Ca²⁺, bAP, neuromodulator concentration | Needs sums or averages over other synapses |
| **D** | Grounded depression | LTD comes from a measured induction pathway (moderate NMDAR Ca²⁺ → calcineurin/PP1; mGluR/eCB/CB1; presynaptic NMDAR) | LTD is decay, normalization or a term chosen for stability |
| **F** | Frequency and pattern dependence | Reproduces the rate dependence of pairing (Sjöström 2001) and LFS-LTD vs HFS-LTP (Dudek & Bear 1992) | Insensitive to rate; timing only |
| **C** | Conditions | Sensitive to [Ca²⁺]ₒ and dendritic location (Inglebert 2020; Froemke 2005; Golding 2002) | Neither |
| **S** | Local stability | Bounded through soft bounds, bistability or a cell-local sliding threshold | Needs hard clipping or global normalization |
| **H** | Hippocampal evidence | Fitted to or tested against CA3→CA1 data | Cortex or theory only |
| **M** | Mechanistic transparency | State variables are measurable molecules or quantities (Ca²⁺, P_r, CaMKII) | Abstract traces |

## 3. Ranking

| Rank | Rule | Tier | L | D | F | C | S | H | M | Σ |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Stochastic CA3→CA1 biochemical synapse (Rodrigues 2023) | I | 2 | 2 | 2 | 2 | 2 | 2 | 2 | **14** |
| 2 | Ca²⁺ two-threshold rule at physiological [Ca²⁺]ₒ (Graupner & Brunel 2012 thresholds; CA1 data and model from Inglebert 2020) | II | 2 | 2 | 2 | 2 | 2 | 2 | 1 | **13** |
| 3 | CaMKII/PP1 bistable kinetics, STDP as an output (Graupner & Brunel 2007) | I | 2 | 2 | 2 | 1 | 2 | 1 | 2 | **12** |
| 4 | Ca²⁺ two-threshold rule, original parameters (Graupner & Brunel 2012) | II | 2 | 2 | 2 | 1 | 2 | 1 | 1 | **11** |
| 5 | Two coincidence detectors: NMDAR-Ca²⁺ for LTP, mGluR/eCB/CB1 and presynaptic NMDAR for t-LTD (Karmarkar & Buonomano 2002; Sjöström 2003; Nevian & Sakmann 2006; CA1: Andrade-Talavera 2016) | II | 2 | 2 | 1 | 1 | 1 | 1 | 2 | **10** |
| 6 | Unified postsynaptic biochemistry, cortex (Mäki-Marttunen 2020) | I | 2 | 2 | 2 | 1 | 1 | 0 | 2 | **10** |
| 7 | Markram–Tsodyks redistribution of efficacy plus pre/post STDP (Markram & Tsodyks 1996; Costa 2015) | III | 2 | 1 | 2 | 0 | 1 | 1 | 1 | **8** |
| 8 | Voltage-based STDP (Clopath 2010) | III | 1 | 1 | 2 | 1 | 1 | 1 | 1 | **8** |
| 9 | NMDAR-Ca²⁺ Ω function (Shouval 2002) | II | 2 | 1 | 2 | 1 | 0 | 1 | 1 | **8** |
| 10 | BCM sliding threshold (Bienenstock 1982; data Dudek & Bear 1992, Kirkwood 1996) | III | 1 | 1 | 2 | 0 | 2 | 2 | 0 | **8** |
| 11 | BTSP, plateau-gated, seconds-scale (Bittner 2017; Milstein 2021) | III | 1 | 1 | 1 | 0 | 2 | 2 | 0 | **7** |
| 12 | Triplet STDP (Pfister & Gerstner 2006) | IV | 2 | 1 | 2 | 0 | 0 | 1 | 0 | **6** |
| 13 | Three-factor (neuromodulated) STDP with eligibility trace (Izhikevich 2007; CA1 data Brzosko 2015, 2017) | III | 2 | 1 | 0 | 0 | 0 | 2 | 1 | **6** |
| 14 | Weight-dependent pair STDP, soft bounds (van Rossum 2000; Gütig 2003) | IV | 2 | 1 | 0 | 0 | 2 | 1 | 0 | **6** |
| 15 | Suppression model (Froemke & Dan 2002) | IV | 2 | 1 | 1 | 0 | 0 | 0 | 0 | **4** |
| 16 | Nearest-neighbour pair STDP (Izhikevich & Desai 2003) | IV | 2 | 1 | 1 | 0 | 0 | 0 | 0 | **4** |
| 17 | Additive all-to-all pair STDP (Song, Miller & Abbott 2000) | IV | 2 | 0 | 0 | 0 | 0 | 1 | 0 | **3** |
| 18 | Classical Hebb with decay or normalization; Oja; covariance | V | 1 | 0 | 0 | 0 | 0 | 0 | 0 | **1** |

Tiers: **I** molecular kinetics, with plasticity rules as outputs; **II** one or two biophysical
induction signals (Ca²⁺, mGluR/eCB) mapped to the weight; **III** a measured quantity (V, P_r, a
plateau, a neuromodulator) combined with phenomenological dynamics; **IV** abstract spike-time
traces; **V** rate products.

The scores are a judgement, made to keep the reasoning explicit. A 1-point difference is not
meaningful, but the tiers are: tier boundaries track the D and M columns.

## 4. Notes per rule

### Tier V: classical Hebbian rules (rank 18)
`Δw ∝ x·y` with decay, normalization or the Oja term. These rules have no timing, no frequency
threshold and no activity-dependent LTD (Section 1). Their only use here is as a null model.

### Tier IV: pair and triplet STDP (ranks 12, 14–17)

- **Additive pair STDP** (Song 2000). `Δw = A₊e^{−Δt/τ₊}` for pre-before-post and
  `−A₋e^{Δt/τ₋}` for post-before-pre, summed over all pairs, with hard bounds. The abstract states
  that the rule balances synaptic strengths and makes inputs compete. The way it does so is
  *[not in abstract]*: the depression window's area is set larger than the potentiation window's,
  which makes depression a stability term, and the weights become bimodal. Pair rules cannot
  account for the dependence on pairing frequency (stated in Pfister & Gerstner 2006), so
  high-rate pairing cannot give LTP, unlike Sjöström 2001.
- **Weight-dependent STDP** (van Rossum 2000; Gütig 2003). Potentiation shrinks as `w` grows. This
  matches Bi & Poo 1998 in hippocampal culture: significant LTP only at synapses of low initial
  strength, LTD independent of initial strength. Gütig 2003 shows that tuning the weight dependence
  trades stability against sensitivity to input correlations. The rule is still blind to frequency.
- **Nearest-neighbour pairing** (Izhikevich & Desai 2003). With nearest-neighbour interactions and
  uncorrelated Poisson trains, STDP reduces to BCM. The rate dependence comes from bookkeeping, not
  mechanism.
- **Suppression model** (Froemke & Dan 2002, visual cortex slices). Each spike's efficacy is
  suppressed by the preceding spike of the same neuron within several tens of ms, and the first spike
  of a burst dominates. This predicts plasticity from in vivo spike trains well, but it does not
  produce the Sjöström 2001 result that LTP wins at high rate *[comparison not in abstract]*.
- **Triplet STDP** (Pfister & Gerstner 2006). Adds a term over spike triplets, so LTP grows with
  postsynaptic rate. It fits visual-cortex slice data (Sjöström 2001) and hippocampal-culture triplet
  data (Wang 2005), and it maps onto BCM for stochastic spike trains. **This is the best
  phenomenological model of Markram/Sjöström-type frequency dependence**, but its depression is
  still a pair term, and its traces have no assigned molecule.

**Weakness of tier IV at the CA3→CA1 synapse.** The evidence is mixed, and it depends on conditions:
- Wittenberg & Wang 2006: potentiation needs postsynaptic bursts at 5 Hz or more and appears after
  tens of pairings; depression needs hundreds of pairings and has broad timing dependence. Depending
  on these parameters the curve is LTP-only, bidirectional or LTD-only, so no single STDP window
  describes the synapse.
- Inglebert 2020: pairs of single pre- and postsynaptic spikes induce **no change at 1.3 and 1.5 mM
  [Ca²⁺]ₒ and depression at 1.8 mM**. Plasticity returns only with postsynaptic bursts or high enough
  firing frequency.
- Against this, Andrade-Talavera 2016 induced both t-LTP and t-LTD with single postsynaptic spikes at
  0.2 Hz in young mice (P12–P18). [Ca²⁺]ₒ is *[not in abstract]*. A likely reading is that the
  canonical pair window holds in young animals at high [Ca²⁺]ₒ, but this is a hypothesis to check
  against the methods sections.

### Markram's frequency-dependent plasticity (rank 7, and the target of rank 12)

The phrase covers three results that are worth separating:

1. **Timing** (Markram, Lübke, Frotscher & Sakmann 1997, paired neocortical pyramidal cells). EPSPs
   were up- or down-regulated depending on the precise timing of postsynaptic APs relative to EPSPs.
   The abstract describes timing only. Any frequency dependence in that paper is *[not in abstract]*.
2. **Rate × timing × cooperativity** (Sjöström, Turrigiano & Nelson 2001, L5). The abstract reports
   "a complex dependence of LTP and LTD on rate and timing" and a model in which LTP-favouring timing
   "wins" over LTD. The usual summary (pre-before-post pairing gives LTP only above about 10 Hz, and
   both orders give LTP at about 40–50 Hz) is *[not in abstract]*. These are data. At rule level
   triplet STDP (rank 12) captures them; at mechanism level Ca²⁺ rules (ranks 2, 4) do, because more
   spikes summate Ca²⁺ above the LTP threshold.
3. **Redistribution of synaptic efficacy** (Markram & Tsodyks 1996, L5 pairs). After pairing, the
   synaptic response increased only when input arrived at low frequencies. The authors attribute this
   to a redistribution of the available efficacy, not to an increase in efficacy: plasticity changes
   the *content* of the signal, not its gain. In Tsodyks–Markram terms this is an increase in the
   release fraction `U` *[not in abstract]*. Costa 2015 combines pre- and postsynaptic expression of
   STDP, based on rat sensory-cortex data. Their model develops receptive fields with lower
   variability and leaves a hidden postsynaptic trace that speeds relearning.

Redistribution is the most bio-plausible of the purely phenomenological rules, because its state
variable is measurable (P_r through paired-pulse ratio, CV analysis or failure rate). Its weak point
is that the induction stage is borrowed from STDP. **It fits this project directly**: the verified
`TMSyn`/`TMSynPI` mechanisms already carry `U`. A slow, activity-dependent change of `U` would be
the presynaptic long-term arm, and it would sit next to the postsynaptic `T`/`w_cap` arm without a
new synapse model. Whether CA1 LTP has a presynaptic component is contested, so it should enter as
an arm to test, not as a default. Note that CA3→CA1 t-LTD is expressed presynaptically
(Andrade-Talavera 2016: fluctuation analysis, paired-pulse ratio, MK-801 rate), so a presynaptic
*depression* arm has direct CA1 support.

### Tier III: measured quantity, phenomenological dynamics (ranks 8, 10, 11, 13)

- **Voltage-based STDP** (Clopath 2010). The change depends on presynaptic spike arrival and on
  postsynaptic membrane potential filtered with two time constants. It reproduces several nonlinear
  STDP effects and the voltage dependence of plasticity. Details *[not in abstract]*: LTD when a
  presynaptic spike arrives while filtered voltage is above θ₋; LTP when instantaneous voltage is
  above θ₊ while filtered voltage is above θ₋; a homeostatic factor `ū²/u_ref²`, which is a slow
  cell-level average; hard bounds. Its voltage stands in for Ca²⁺.
- **BCM** (Bienenstock, Cooper & Munro 1982). `Δw ∝ x·y(y − θ)` with `θ` sliding with recent
  activity. The CA1 frequency curve supports it: LTD at 1–3 Hz, nothing at 10 Hz, LTP at 50 Hz (Dudek
  & Bear 1992). In visual cortex of light-deprived rats LTP is enhanced and LTD reduced over a range of
  frequencies, and two days of light reverse it (Kirkwood 1996), which is direct evidence that `θ`
  slides. The depression is activity-dependent and matches protocols, unlike the classical rules. But
  BCM is rate-based, has no timing, and its threshold has no single identified mechanism.
- **BTSP** (Bittner 2017; Milstein 2021). In vivo a single plateau potentiates inputs that arrived
  seconds before and after it; in slices five pairings of subthreshold input with plateaus give
  large, asymmetric, seconds-long potentiation (Bittner 2017). The rule is bidirectional and depends
  on the current weight: weak inputs potentiate and strong inputs depress (Milstein 2021). It is
  CA1-specific, has strong in vivo support and stabilizes itself. Its signals (eligibility trace,
  instructive signal) have no identified molecules yet, and it does not address Hz-scale frequency
  dependence. It is the right acceptance test for behavioural-timescale induction.
- **Three-factor STDP** (Izhikevich 2007; review Frémaux & Gerstner 2015). STDP sets a slow
  eligibility trace, and extracellular dopamine within a few seconds converts it into a weight change.
  In mouse hippocampal slices dopamine *retroactively* converts timing-dependent depression into
  potentiation, through NMDARs and in part cAMP/PKA (Brzosko 2015). Acetylcholine biases STDP toward
  depression, and dopamine applied afterwards converts that depression into potentiation (Brzosko
  2017). The third factor is physiological, but the rule inherits the pair-STDP window and its
  frequency blindness.

### Tier II: Ca²⁺ and other induction signals (ranks 2, 4, 5, 9)

- **Two Ca²⁺ thresholds** (Graupner & Brunel 2012). Potentiation and depression are activated above
  separate Ca²⁺ thresholds. The rule gives a wide range of STDP curves and accounts quantitatively
  for protocols with variable timing and rate in hippocampus and neocortex. Bistability of the
  efficacy and the dendritic-location effect are *[not in abstract]* (the title names location).
  Depression is tied to the best-supported LTD mechanism in CA1: prolonged, moderate NMDAR Ca²⁺
  (Dudek & Bear 1992; Kirkwood 1996). Two results support the Ca²⁺-level idea directly. Partial NMDAR
  block converts LTP into LTD in CA1 (Nishiyama 2000). In L2/3 cortex, presynaptic stimulation with
  partial NMDAR block induces LTD that occludes t-LTD (Froemke 2005). In models driven by irregular,
  in vivo-like firing, timing matters much less than rate (Graupner, Wallisch & Ostojic 2016).
  **Inglebert 2020 measured CA3→CA1 plasticity at 1.3–1.8 mM [Ca²⁺]ₒ and modelled it.** Whether their
  model uses exactly the Graupner–Brunel thresholds is *[not in abstract]*; the full text could not
  be fetched (PNAS 403, Europe PMC 500). With that caveat, this is the strongest induction rule for
  this project.
- **Two coincidence detectors.** A single NMDAR-Ca²⁺ detector predicts LTD at long *positive*
  intervals as well, because Ca²⁺ falls monotonically with the interval into the LTD range; a second
  coincidence detector removes this (Karmarkar & Buonomano 2002). Experiments support a separate LTD
  pathway:
  - L2/3 somatosensory cortex: spine Ca²⁺ transients were similar for protocols that gave LTP or LTD;
    LTD required mGluR → PLC → eCB as a retrograde messenger; LTP required a large NMDAR Ca²⁺
    transient (Nevian & Sakmann 2006). This contradicts a rule that reads the direction from Ca²⁺
    amplitude alone.
  - L5 cortex: t-LTD is expressed presynaptically and needs coincident presynaptic NMDAR and CB1
    activation (Sjöström 2003).
  - **CA3→CA1, young mouse:** t-LTD needs postsynaptic Ca²⁺ but not postsynaptic ionotropic NMDARs.
    It needs GluN2C/D-type NMDARs, mGluR, PLC, IP3R Ca²⁺ release, eCB synthesis, CB1, astrocytic
    signalling (possibly D-serine) and presynaptic calcineurin, and it is expressed presynaptically
    (Andrade-Talavera 2016).
  - Hippocampal culture: CaMKII-mediated potentiation and calcineurin-mediated depression run
    concurrently and integrate depending on their timing (Wang 2005).
  - Corticostriatal synapses: eCB itself is bidirectional; prolonged, moderate eCB gives t-LTD (needs
    calcineurin) and short, large eCB transients give t-LTP (needs presynaptic PKA) (Cui 2016).
    Different region, but a worked model of eCB-level coding.

  These models get depression from a distinct, identified mechanism, which answers the objection to
  Hebbian depression most directly. The cost is more parameters and less hippocampal data than the
  single-Ca²⁺ rule.
- **Ω function** (Shouval, Bear & Cooper 2002). Weight change as a function of NMDAR Ca²⁺, with an
  LTD dip at intermediate levels. It explains protocols that vary voltage, rate and timing with one
  parameter set. As a single-detector model it has the problem Karmarkar & Buonomano describe: LTD
  at long positive intervals. It also passes through LTD on the way to LTP and has no bounds or
  bistability *[not in abstract]*.

### Tier I: molecular kinetics (ranks 1, 3, 6)

The rule is not written down: STDP, frequency dependence and LTD come out of CaMKII, calcineurin,
PP1, PKA and AMPAR trafficking. Rodrigues 2023 is a stochastic CA3→CA1 synapse with vesicle release,
NMDAR and enzyme readout that depends on temperature and [Ca²⁺]ₒ. It is the closest peer to this
project. Graupner & Brunel 2007 is the classical CaMKII/PP1 bistable version. Mäki-Marttunen 2020 is
the most complete postsynaptic biochemistry but is fitted to cortex. The price of tier I is many
parameters with weak constraints, and run time. (Abstracts of these three were checked for
`related_models.md`; the descriptions here follow that document.)

## 5. Conclusions for this project

1. **The model is already aimed at tiers I–II.** The planned chain `V_seg → g_Ca → tag T → capture`
   (model §2.1, plan S4) is a Ca²⁺-induction rule that feeds a tag/capture stage. A two-threshold Ca²⁺
   rule constrained by Inglebert 2020's physiological-Ca²⁺ data is the obvious concrete form of the
   `g_Ca` → tag step, including the LTD side.
2. **Depression should come from a mechanism, never from a normalization term.** In tier II it comes
   from moderate NMDAR Ca²⁺ (LFS-LTD). The CA3→CA1 t-LTD data (Andrade-Talavera 2016) show a second,
   presynaptically expressed route through mGluR/eCB/CB1 and non-postsynaptic NMDARs. Nevian & Sakmann
   2006 show that Ca²⁺ amplitude alone need not predict the direction. **A single-Ca²⁺ rule is
   therefore probably not enough for t-LTD**: plan a separate eCB/presynaptic t-LTD detector (rank 5)
   from the start, or at least an explicit test that the single-Ca²⁺ version fails. This is
   consistent with the downscaling list (D4a/D4b) in `plasticity_up_down_model_2026-11-06.md`.
3. **A presynaptic long-term arm on `U` is cheap to add and should be tested.** In the existing,
   verified `TMSyn` it would cover Markram–Tsodyks redistribution (potentiation) and the
   presynaptically expressed CA1 t-LTD (depression). It would change the synapse's frequency filter,
   which links milestone 1 (STP) to milestone 2.
4. **Tier III–IV rules are acceptance tests, not components**, as `related_models.md` already
   proposes for level D. When driven with the matching protocol the model should reproduce:
   - Dudek & Bear 1992: 900 pulses at 1–3 Hz → LTD, 10 Hz → no change, 50 Hz → LTP; NMDAR-dependent;
   - Inglebert 2020: single-spike pairs → no change at 1.3 and 1.5 mM [Ca²⁺]ₒ, depression at 1.8 mM;
     plasticity restored by postsynaptic bursts or high frequency;
   - Wittenberg & Wang 2006: LTP needs postsynaptic bursts at ≥ 5 Hz and tens of pairings; LTD needs
     hundreds of pairings and has a broad timing window;
   - Sjöström 2001 rate × timing curve, via the triplet-rule fit (visual cortex; values to be read from
     the paper);
   - BTSP (Bittner 2017; Milstein 2021) for seconds-scale induction, including weight-dependent
     depression;
   - Brzosko 2015/2017: dopamine after pairing converts t-LTD into t-LTP; acetylcholine biases toward
     depression (only if neuromodulation is modelled).
5. **Age and conditions must be recorded with every LTD parameter.** LFS-LTD in CA1 is −45 ± 4% in
   rats under 2 weeks old and −20 ± 4% at 5 weeks (900 pulses at 1 Hz; Dudek & Bear 1993), and LTD
   develops before LTP. The CA1 t-LTD mechanism above is from P12–P18 mice. Adult in vivo values are
   not covered by these abstracts. Most STDP data come from juvenile slices, often at high [Ca²⁺]ₒ.

## 6. References

All entries checked against PubMed on 2026-11-10. † = also listed in `related_models.md`
(checked 2026-11-04/05).

| Reference | PMID | DOI |
|---|---|---|
| Andrade-Talavera Y, Duque-Feria P, Paulsen O, Rodríguez-Moreno A (2016). Presynaptic spike timing-dependent long-term depression in the mouse hippocampus. *Cereb Cortex* 26:3637–3654 | 27282393 | [10.1093/cercor/bhw172](https://doi.org/10.1093/cercor/bhw172) |
| Bi GQ, Poo MM (1998). Synaptic modifications in cultured hippocampal neurons: dependence on spike timing, synaptic strength, and postsynaptic cell type. *J Neurosci* 18:10464–10472 | 9852584 | [10.1523/JNEUROSCI.18-24-10464.1998](https://doi.org/10.1523/JNEUROSCI.18-24-10464.1998) |
| Bienenstock EL, Cooper LN, Munro PW (1982). Theory for the development of neuron selectivity: orientation specificity and binocular interaction in visual cortex. *J Neurosci* 2:32–48 | 7054394 | [10.1523/JNEUROSCI.02-01-00032.1982](https://doi.org/10.1523/JNEUROSCI.02-01-00032.1982) |
| Bittner KC, Milstein AD, Grienberger C, Romani S, Magee JC (2017). Behavioral time scale synaptic plasticity underlies CA1 place fields. *Science* 357:1033–1036 | 28883072 | [10.1126/science.aan3846](https://doi.org/10.1126/science.aan3846) |
| Brzosko Z, Schultz W, Paulsen O (2015). Retroactive modulation of spike timing-dependent plasticity by dopamine. *eLife* 4:e09685 | 26516682 | [10.7554/eLife.09685](https://doi.org/10.7554/eLife.09685) |
| Brzosko Z, Zannone S, Schultz W, Clopath C, Paulsen O (2017). Sequential neuromodulation of Hebbian plasticity offers mechanism for effective reward-based navigation. *eLife* 6:e27756 | 28691903 | [10.7554/eLife.27756](https://doi.org/10.7554/eLife.27756) |
| Clopath C, Büsing L, Vasilaki E, Gerstner W (2010). Connectivity reflects coding: a model of voltage-based STDP with homeostasis. *Nat Neurosci* 13:344–352 † | 20098420 | [10.1038/nn.2479](https://doi.org/10.1038/nn.2479) |
| Costa RP, Froemke RC, Sjöström PJ, van Rossum MCW (2015). Unified pre- and postsynaptic long-term plasticity enables reliable and flexible learning. *eLife* 4:e09457 † | 26308579 | [10.7554/eLife.09457](https://doi.org/10.7554/eLife.09457) |
| Cui Y, Prokin I, Xu H, Delord B, Genet S, Venance L, Berry H (2016). Endocannabinoid dynamics gate spike-timing dependent depression and potentiation. *eLife* 5:e13185 | 26920222 | [10.7554/eLife.13185](https://doi.org/10.7554/eLife.13185) |
| Dudek SM, Bear MF (1992). Homosynaptic long-term depression in area CA1 of hippocampus and effects of N-methyl-D-aspartate receptor blockade. *PNAS* 89:4363–4367 | 1350090 | [10.1073/pnas.89.10.4363](https://doi.org/10.1073/pnas.89.10.4363) |
| Dudek SM, Bear MF (1993). Bidirectional long-term modification of synaptic effectiveness in the adult and immature hippocampus. *J Neurosci* 13:2910–2918 | 8331379 | [10.1523/JNEUROSCI.13-07-02910.1993](https://doi.org/10.1523/JNEUROSCI.13-07-02910.1993) |
| Frémaux N, Gerstner W (2015). Neuromodulated spike-timing-dependent plasticity, and theory of three-factor learning rules. *Front Neural Circuits* 9:85 | 26834568 | [10.3389/fncir.2015.00085](https://doi.org/10.3389/fncir.2015.00085) |
| Froemke RC, Dan Y (2002). Spike-timing-dependent synaptic modification induced by natural spike trains. *Nature* 416:433–438 | 11919633 | [10.1038/416433a](https://doi.org/10.1038/416433a) |
| Froemke RC, Poo MM, Dan Y (2005). Spike-timing-dependent synaptic plasticity depends on dendritic location. *Nature* 434:221–225 | 15759002 | [10.1038/nature03366](https://doi.org/10.1038/nature03366) |
| Golding NL, Staff NP, Spruston N (2002). Dendritic spikes as a mechanism for cooperative long-term potentiation. *Nature* 418:326–331 | 12124625 | [10.1038/nature00854](https://doi.org/10.1038/nature00854) |
| Graupner M, Brunel N (2007). STDP in a bistable synapse model based on CaMKII and associated signaling pathways. *PLoS Comput Biol* 3:e221 † | 18052535 | [10.1371/journal.pcbi.0030221](https://doi.org/10.1371/journal.pcbi.0030221) |
| Graupner M, Brunel N (2012). Calcium-based plasticity model explains sensitivity of synaptic changes to spike pattern, rate, and dendritic location. *PNAS* 109:3991–3996 † | 22357758 | [10.1073/pnas.1109359109](https://doi.org/10.1073/pnas.1109359109) |
| Graupner M, Wallisch P, Ostojic S (2016). Natural firing patterns imply low sensitivity of synaptic plasticity to spike timing compared with firing rate. *J Neurosci* 36:11238–11258 | 27807166 | [10.1523/JNEUROSCI.0104-16.2016](https://doi.org/10.1523/JNEUROSCI.0104-16.2016) |
| Gütig R, Aharonov R, Rotter S, Sompolinsky H (2003). Learning input correlations through nonlinear temporally asymmetric Hebbian plasticity. *J Neurosci* 23:3697–3714 | 12736341 | [10.1523/JNEUROSCI.23-09-03697.2003](https://doi.org/10.1523/JNEUROSCI.23-09-03697.2003) |
| Inglebert Y, Aljadeff J, Brunel N, Debanne D (2020). Synaptic plasticity rules with physiological calcium levels. *PNAS* 117:33639–33648 † | 33328274 | [10.1073/pnas.2013663117](https://doi.org/10.1073/pnas.2013663117) |
| Izhikevich EM (2007). Solving the distal reward problem through linkage of STDP and dopamine signaling. *Cereb Cortex* 17:2443–2452 | 17220510 | [10.1093/cercor/bhl152](https://doi.org/10.1093/cercor/bhl152) |
| Izhikevich EM, Desai NS (2003). Relating STDP to BCM. *Neural Comput* 15:1511–1523 | 12816564 | [10.1162/089976603321891783](https://doi.org/10.1162/089976603321891783) |
| Karmarkar UR, Buonomano DV (2002). A model of spike-timing dependent plasticity: one or two coincidence detectors? *J Neurophysiol* 88:507–513 | 12091572 | [10.1152/jn.2002.88.1.507](https://doi.org/10.1152/jn.2002.88.1.507) |
| Kirkwood A, Rioult MC, Bear MF (1996). Experience-dependent modification of synaptic plasticity in visual cortex. *Nature* 381:526–528 | 8632826 | [10.1038/381526a0](https://doi.org/10.1038/381526a0) |
| Mäki-Marttunen T, et al. (2020). A unified computational model for cortical post-synaptic plasticity. *eLife* 9:e55714 † | 32729828 | [10.7554/eLife.55714](https://doi.org/10.7554/eLife.55714) |
| Markram H, Lübke J, Frotscher M, Sakmann B (1997). Regulation of synaptic efficacy by coincidence of postsynaptic APs and EPSPs. *Science* 275:213–215 | 8985014 | [10.1126/science.275.5297.213](https://doi.org/10.1126/science.275.5297.213) |
| Markram H, Tsodyks M (1996). Redistribution of synaptic efficacy between neocortical pyramidal neurons. *Nature* 382:807–810 | 8752273 | [10.1038/382807a0](https://doi.org/10.1038/382807a0) |
| Milstein AD, Li Y, Bittner KC, Grienberger C, Soltesz I, Magee JC, Romani S (2021). Bidirectional synaptic plasticity rapidly modifies hippocampal representations. *eLife* 10:e73046 † | 34882093 | [10.7554/eLife.73046](https://doi.org/10.7554/eLife.73046) |
| Nevian T, Sakmann B (2006). Spine Ca²⁺ signaling in spike-timing-dependent plasticity. *J Neurosci* 26:11001–11013 | 17065442 | [10.1523/JNEUROSCI.1749-06.2006](https://doi.org/10.1523/JNEUROSCI.1749-06.2006) |
| Nishiyama M, Hong K, Mikoshiba K, Poo MM, Kato K (2000). Calcium stores regulate the polarity and input specificity of synaptic modification. *Nature* 408:584–588 | 11117745 | [10.1038/35046067](https://doi.org/10.1038/35046067) |
| Oja E (1982). A simplified neuron model as a principal component analyzer. *J Math Biol* 15:267–273 | 7153672 | [10.1007/BF00275687](https://doi.org/10.1007/BF00275687) |
| Pfister JP, Gerstner W (2006). Triplets of spikes in a model of spike timing-dependent plasticity. *J Neurosci* 26:9673–9682 | 16988038 | [10.1523/JNEUROSCI.1425-06.2006](https://doi.org/10.1523/JNEUROSCI.1425-06.2006) |
| Rodrigues YE, Tigaret CM, Marie H, O'Donnell C, Veltz R (2023). A stochastic model of hippocampal synaptic plasticity with geometrical readout of enzyme dynamics. *eLife* 12:e80152 † | 37589251 | [10.7554/eLife.80152](https://doi.org/10.7554/eLife.80152) |
| Sejnowski TJ (1977). Storing covariance with nonlinearly interacting neurons. *J Math Biol* 4:303–321 | 925522 | [10.1007/BF00275079](https://doi.org/10.1007/BF00275079) |
| Shouval HZ, Bear MF, Cooper LN (2002). A unified model of NMDA receptor-dependent bidirectional synaptic plasticity. *PNAS* 99:10831–10836 † | 12136127 | [10.1073/pnas.152343099](https://doi.org/10.1073/pnas.152343099) |
| Sjöström PJ, Turrigiano GG, Nelson SB (2001). Rate, timing, and cooperativity jointly determine cortical synaptic plasticity. *Neuron* 32:1149–1164 | 11754844 | [10.1016/s0896-6273(01)00542-6](https://doi.org/10.1016/s0896-6273(01)00542-6) |
| Sjöström PJ, Turrigiano GG, Nelson SB (2003). Neocortical LTD via coincident activation of presynaptic NMDA and cannabinoid receptors. *Neuron* 39:641–654 | 12925278 | [10.1016/s0896-6273(03)00476-8](https://doi.org/10.1016/s0896-6273(03)00476-8) |
| Song S, Miller KD, Abbott LF (2000). Competitive Hebbian learning through spike-timing-dependent synaptic plasticity. *Nat Neurosci* 3:919–926 | 10966623 | [10.1038/78829](https://doi.org/10.1038/78829) |
| Stent GS (1973). A physiological mechanism for Hebb's postulate of learning. *PNAS* 70:997–1001 | 4352227 | [10.1073/pnas.70.4.997](https://doi.org/10.1073/pnas.70.4.997) |
| van Rossum MCW, Bi GQ, Turrigiano GG (2000). Stable Hebbian learning from spike timing-dependent plasticity. *J Neurosci* 20:8812–8821 † | 11102489 | [10.1523/JNEUROSCI.20-23-08812.2000](https://doi.org/10.1523/JNEUROSCI.20-23-08812.2000) |
| Wang HX, Gerkin RC, Nauen DW, Bi GQ (2005). Coactivation and timing-dependent integration of synaptic potentiation and depression. *Nat Neurosci* 8:187–193 | 15657596 | [10.1038/nn1387](https://doi.org/10.1038/nn1387) |
| Wittenberg GM, Wang SSH (2006). Malleability of spike-timing-dependent plasticity at the CA3-CA1 synapse. *J Neurosci* 26:6610–6617 | 16775149 | [10.1523/JNEUROSCI.5388-05.2006](https://doi.org/10.1523/JNEUROSCI.5388-05.2006) |

### Corrections made by the 2026-11-10 check

| Earlier text (from memory) | Corrected after reading the abstract |
|---|---|
| Frémaux & Gerstner 2016 | 2015 (*Front Neural Circuits* 9:85) |
| Stent 1973: depression of an active input onto a silent cell | Stent proposed depression of *inactive* synapses when the postsynaptic cell fires |
| Inglebert 2020: no plasticity at 1.3–1.8 mM | No change at 1.3 and 1.5 mM, **depression** at 1.8 mM |
| Wittenberg & Wang 2006: LTD for both orders | Abstract: LTP needs bursts at ≥ 5 Hz; LTD needs hundreds of pairings and has broad timing dependence ("both orders" not stated) |
| Pair window is a high-Ca²⁺ artefact | Andrade-Talavera 2016 obtained t-LTP and t-LTD with single spikes at 0.2 Hz in young CA1; now presented as conflicting evidence |
| Markram 1997 cited for frequency dependence | Its abstract covers timing only; frequency dependence is attributed to Sjöström 2001 |
| Brzosko 2015: cholinergic tone favours depression | That is Brzosko 2017; 2015 covers dopamine only |
| Cui 2016 listed as a two-detector t-LTD model | Corticostriatal eCB level model; eCB is bidirectional (moderate prolonged → LTD, brief large → LTP) |
| Nishiyama 2000 cited for a second LTD window at positive delays | Its abstract shows LTP → LTD under partial NMDAR block, plus heterosynaptic LTD via IP3R; the positive-delay LTD problem is attributed to Karmarkar & Buonomano 2002 |
| Dudek & Bear 1993: LTD much weaker in adults and in vivo | −45 ± 4% (< 2 weeks) vs −20 ± 4% (5 weeks), slices; no in vivo data in the abstract |
| Kirkwood 1996: dark rearing | Light-deprived rats, reversed by 2 days of light |
