# Synaptic tagging and capture (STC): a short literature review

**Sources read:** the full texts (PDFs) of the three papers below. Page numbers refer to the journal
pagination. All three are reviews, so the numbers quoted here are second-hand: each is attributed
to the primary study the review cites, and must be checked against that primary paper (with its
recording conditions: species, age, [Ca²⁺]ₒ, temperature) before it goes into `params.py`.

1. Martin KC, Kosik KS (2002). Synaptic tagging — who's it? *Nat Rev Neurosci* 3:813–820.
   doi:10.1038/nrn942. PMID 12360325.
2. Rogerson T, Cai DJ, Frank A, Sano Y, Shobe J, Lopez-Aranda MF, Silva AJ (2014). Synaptic tagging
   during memory allocation. *Nat Rev Neurosci* 15:157–169. doi:10.1038/nrn3667. PMID 24496410.
   PMCID PMC3992944.
3. Kim J, Park M (2025). Systems memory consolidation during sleep: oscillations, neuromodulators,
   and synaptic remodeling. *BMB Rep* 58(10):425–436. doi:10.5483/BMBRep.2025-0033. PMID 40962324.
   PMCID PMC12576410.

## The STC hypothesis in one paragraph

Synapses activated by a weak stimulus get a local, transient, protein-synthesis-independent
**tag**. Strong stimulation anywhere on the same neuron triggers transcription and translation of
**plasticity-related products (PRPs)**, which are delivered throughout the cell but strengthen
only tagged synapses. So a weak input that alone gives early LTP (E-LTP) gets late LTP (L-LTP) if
a strong input on the same neuron overlaps it in time. The synapse, not the nucleus, becomes the
unit of lasting plasticity (Martin & Kosik, pp. 813–815, 819; Rogerson et al., p. 161 and Fig. 3).

## 1. Martin & Kosik (2002): what is the tag?

### Evidence for tagging (pp. 813–815)

- ***Aplysia*, one bifurcated sensory neuron contacting two motor neurons** (Martin et al. 1997):
  - 5 puffs of serotonin (5-HT) on one branch give branch-specific long-term facilitation (LTF) lasting
    >24 h. It is blocked by actinomycin D (transcription) and by anti-CREB antibody.
  - 1 puff alone gives only transient facilitation. Given to the other branch, it is converted to
    LTF if delivered within a time window. The text gives that window as 1–2 h before or 1–4 h after
    the 5 puffs. Fig. 1c shows capture at 0 h and at 1 h after, and none at 4 h after.
- **Rat hippocampal slice, CA1, two independent inputs S1/S2** (Frey & Morris 1997, 1998):
  - 1 tetanic train gives LTP that decays after ~1.5 h.
  - 3 trains give LTP that lasts ≥8 h and depends on transcription.
  - A weak input expresses L-LTP if it is delivered 1–2 h before, or less than 2.5–3 h after, the
    strong stimulation.
  - Anisomycin during the S1 tetanus does not block persistent LTP in S2. The tag itself is
    protein-synthesis independent (Fig. 2c).
- **Two temporal features of the tag** (p. 815):
  - After strong stimulation, the cell can turn transient changes into persistent ones for 1–4 h.
  - The tag set by a weak stimulus persists for 1–2 h.

### Criteria for a tag (p. 815)

A tag must:

1. be spatially restricted (local);
2. be time-limited and reversible;
3. interact with the cell-wide events that follow strong stimulation (usually gene expression) to
   give lasting, synapse-specific strengthening.

### Candidate tags (pp. 815–819)

| Class | Candidates and evidence |
|---|---|
| Fast synaptic changes | AMPA receptor clustering; lateral mobility of NMDA receptors; Homer-driven insertion of mGluR5; palmitate cycling on PSD-95 |
| Kinases | CaMKII, made autonomous by autophosphorylation. PKMζ, whose persistent activity needs protein synthesis, is necessary and sufficient for L-LTP maintenance. PKA in *Aplysia*: ubiquitin–proteasome degradation of its regulatory subunit gives persistent activity, via an induced ubiquitin C-terminal hydrolase |
| Adhesion molecules | Fasciclin II (*Drosophila* NMJ), apCAM (*Aplysia*), NCAM, cadherins, β-catenin, δ-catenin |
| Actin network | Remodelling after repeated tetanus lasts ≥18 h (Colicos et al. 2001) |
| Ion channels | Presynaptic I_h channels at the crayfish NMJ. The tag lasts ~1 h, needs local protein synthesis, does **not** need transcription, and depends on intact actin |
| Local translation and degradation | mRNA released from RNA granules into polysomes on depolarisation. More spines contain polyribosomes after LTP. Dendritic targeting of *BDNF*/*TrkB* mRNA. *Arc* mRNA accumulates at stimulated sites. Local ubiquitin-mediated protein degradation |

### Key qualifications

- **Local translation is not a general tag** (pp. 818–819). It is required for synapse-specific LTF
  in *Aplysia* but not for synaptic tagging at rodent hippocampal synapses (Frey & Morris 1997, 1998).
  In *Aplysia* it is not needed for facilitation at 24 h, but it is needed at 72 h, where stable new
  synaptic growth accompanies it.
- **Captured products** (p. 819):
  - Largely unknown. MicroRNAs are a speculative candidate.
  - Mice expressing constitutively active CREB (VP16-CREB) in CA1 have a lower threshold for L-LTP,
    and their L-LTP becomes independent of transcription (Barco et al. 2002). This suggests the PRPs
    are CREB targets.
- **Conclusion** (p. 819):
  - There are probably several molecular tags. Different stimuli recruit different ones, and they act
    over different time domains, from hours to days.
  - A single tag molecule would be "extremely surprising". The common feature of all candidates is
    that they are spatially restricted and persistent.

**For the model:** a single abstract tag variable per synapse, decaying over ~1–2 h and
protein-synthesis independent, matches the rodent CA1 data this review summarises. The review
argues against identifying it with any one molecule.

## 2. Rogerson et al. (2014): tagging as part of memory allocation

### Neuronal allocation (pp. 157–160)

- **CREB raises excitability, and that biases which neurons store a memory.**
  - Lateral amygdala: neurons with virally raised CREB are ~3× more likely to be recruited into an
    auditory fear memory trace (Han et al. 2007).
  - Only ~⅓ of recorded lateral amygdala neurons show synaptic changes after fear conditioning
    (Rumpel et al. 2005).
  - CA1: virus transduced ~25% of neurons. Raising CREB before training, but not after, enhances
    the memory.
  - CA1 with constitutively active CREB: smaller afterhyperpolarisation, higher excitability, lower
    LTP threshold (Lopez de Armentia et al. 2007).
  - CA1 neurons recruited as place cells have lower spike thresholds (Epsztein et al. 2011).
    Preplay is consistent with excitability deciding allocation in advance.
- **Linking memories in time** (p. 160, Fig. 2):
  - A first memory raises excitability in the neurons that store it.
  - So, shortly afterwards, a second memory is stored largely in the same neurons. Recalling one then
    recalls the other.
  - As excitability decays, later memories no longer overlap.
  - Supported by Garner et al. 2012 (*Fos*-driven DREADDs).

### Synaptic allocation and STC (pp. 161–163, Figs 3–4)

- **Classic slice data** (Frey & Morris 1997, 1998), as reported by the review:
  - A weak S2 tetanus preceded 1 h earlier by L-LTP induction in S1 gives L-LTP in S2.
  - Weak tetanization of S2 that gives only E-LTP can come up to 1 h before the strong S1 tetanus
    and still be converted. The tag lasts up to ~1 h.
- **Tag and products work for LTD too** (Sajikumar & Frey 2004): short-lived LTD at one set of
  synapses becomes late LTD when L-LTP is induced at another set on the same neurons.
- **Molecules:**
  - Setting the tag needs CaMKII and actin remodelling.
  - Making the PRPs needs the CaMKII–CaMKIV–CREB pathway.
  - Candidate PRPs: ARC, GluR1, HOMER1A, PKMζ.
  - L-LTP can also be induced by low-frequency stimulation combined with dopamine D1/D5 agonists,
    BDNF or carbachol.
- **Crosstalk between spines (Fig. 4):**
  - LTP at one spine lowers the LTP threshold at neighbouring spines. The effect falls with both
    distance and time (Harvey et al. 2008).
  - Active RAS persists ~5 min and spreads ~10 µm. Active RHOA persists ~5 min and spreads ~5 µm
    (Harvey et al. 2008; Murakoshi et al. 2011).
  - In the Fig. 4 scheme, a weakly firing input must arrive within ~10 min.
- **Single-spine STC** (Govindarajan et al. 2011):
  - E-LTP at one spine is converted to L-LTP when L-LTP was induced at a nearby spine. The
    conversion needs protein synthesis and is temporally asymmetric.
  - There is little STC if the spines are >70 µm apart, and less across dendritic branches.
  - Simultaneous L-LTP at two nearby spines reduces spine growth. This suggests competition for a
    limited pool of PRPs.

### Metaplasticity and behavioural tagging (pp. 164–165)

- **Metaplasticity** links bouts of plasticity separated by minutes to days. Excitability changes
  driven by CREB are one proposed mechanism for heterosynaptic metaplasticity.
- **Behavioural tagging, inhibitory avoidance** (Moncada & Viola 2007):
  - A weak memory, lasting hours, becomes long-term, lasting days, when the rat explores a novel
    environment 1 h before training.
  - This depends on dopamine and on protein synthesis.
- **Behavioural tagging, food location** (Wang et al. 2010):
  - Novelty 30 min after a weak encoding episode makes the memory last.
  - Needs hippocampal D1/D5 receptors and protein synthesis.
  - The slice equivalent: strong tetanization converts E-LTP to L-LTP on a convergent pathway.
- **Counter-example** (Izquierdo et al. 1999):
  - A novel open field 1 h *after* inhibitory avoidance training impairs the memory.
  - There is no effect at 5 min or at 6 h, or when the field is familiar.
  - The exact parameters (strength, interval, novelty) matter.

### Clustering, synergy, open questions (pp. 165–167)

- **Spine clustering:**
  - Spines added during motor learning cluster on dendrites, and clustered spines are more stable
    (Fu et al. 2012).
  - Molecules involved: RHOA, CDC42, CaMKII, TIAM1, β-PIX.
- **Synaptic and neuronal allocation work together** (Fig. 3):
  - For ≥1 h after strong training, neuronal ensemble 1 has PRPs that can turn a weak memory into a
    strong one, so STC also decides which *neurons* store a memory.
  - Conversely, local excitability can bias which dendrites take part.
- **The authors' own caveat:** there is still no direct evidence that the behavioural interactions
  actually use STC. They might instead reflect protein-synthesis-dependent rises in neuromodulators
  such as dopamine.

**For the model:**

- STC decides where changes are stored, not only whether they last.
- The paper suggests these model features:
  - tags and PRP pools that are local to a branch or spine neighbourhood, with distance limits of
    ~10 µm (fast crosstalk) and ~70 µm (STC);
  - a limited PRP pool that synapses compete for;
  - dopamine (D1/D5) as a trigger for PRP synthesis;
  - neuron-level excitability as an allocation variable separate from the tag.

## 3. Kim & Park (2025): sleep, neuromodulators and synaptic remodelling

**Not an STC paper.** It never discusses synapse-level tagging. "Emotional tagging" (pp. 425, 427)
means REM sleep prioritising emotional memories. What it adds is the setting in which tagged
changes would be consolidated or downscaled.

- **Oscillations** (p. 426):
  - slow oscillations, 0.1–4 Hz;
  - spindles, 10–15 Hz, lasting 0.5–2 s;
  - sharp-wave ripples, 150–250 Hz, from CA3 to CA1;
  - REM theta, 5–8 Hz.
- **NREM:** coupling of slow oscillations, spindles and ripples drives replay and transfer from
  hippocampus to cortex (p. 427).
- **Slow oscillations vs delta waves:** they play opposing roles. Slow oscillations promote
  consolidation and delta waves promote forgetting (Kim et al. 2019).
- **Neuromodulators** (pp. 427–429):
  - In NREM, noradrenaline oscillates at ~0.02 Hz. Bursts of the locus coeruleus (LC) end individual
    spindles, while sustained low noradrenaline lets spindles cluster (Fig. 2B caption).
  - Noradrenaline is lowest in REM.
  - Suppressing noradrenaline too early, or raising it during NREM, impairs consolidation.
  - Dopamine surges in the nucleus accumbens and basolateral amygdala at the NREM→REM transition.
  - Dopamine from the VTA during NREM aligns with memory-related activity and may decide which
    memories are prioritised.
- **Synaptic regulation** (pp. 429–430):
  - Synaptic Homeostasis Hypothesis (Tononi & Cirelli): synapses potentiate overall during waking and
    are downscaled during sleep. Axon–spine contact area and synaptic AMPA receptors fall.
  - Homer1a drives this downscaling (Diering et al. 2017). This is the same molecule as the candidate
    PRP HOMER1A in Rogerson et al.
  - Sleep also *forms* and *preserves* synapses. Sleep promotes branch-specific spine formation after
    learning (Yang et al. 2014). REM sleep selectively prunes and maintains new spines (Li et al.
    2017).
  - Fig. 2C caption: NREM selectively downscales highly active neurons, REM weakens the network more
    broadly, and assemblies reactivated in NREM keep their strength.
  - The main text instead says NREM mainly potentiates and REM mainly prunes (p. 430). The review is
    not fully consistent on how NREM and REM divide the work.

**For the model:** relevant to the downscaling pathways (D1–D13) and to a later consolidation stage,
not to S4–S6 directly. It gives a reason to gate PRP synthesis or capture by neuromodulators
(dopamine, noradrenaline), and a reason to protect tagged or captured synapses from global
downscaling.

## The tagging mechanism, step by step

Assembled from the three reviews. "M&K" is Martin & Kosik 2002, "R" is Rogerson et al. 2014, "K&P" is
Kim & Park 2025.

1. **Tag setting (weak input).**
   - Activity that is too weak for lasting plasticity still produces E-LTP (or early LTD) and sets
     a tag at the activated synapses.
   - Setting the tag needs no new protein (anisomycin does not block it; M&K Fig. 2c).
   - It involves CaMKII and actin remodelling (R p. 163). Other candidates are PKMζ, PKA, adhesion
     molecules, ion channels, and activated local translation (M&K pp. 815–818).
   - The tag is local, transient and reversible (M&K p. 815). It is probably a synaptic state made of
     several components rather than one molecule (M&K p. 819).
2. **Tag decay.**
   - Without capture the tag decays within ~1–2 h (M&K p. 815) or ~1 h (R p. 162).
   - The E-LTP it supports also decays: 1 tetanic train gives LTP that is gone after ~1.5 h
     (M&K Fig. 2b).
3. **PRP synthesis (strong input or neuromodulator).**
   - Strong stimulation of any input on the neuron (e.g. 3 tetanic trains, or 5 puffs of serotonin in
     *Aplysia*) activates the CaMKII–CaMKIV–CREB pathway and transcription (R p. 163; M&K p. 813).
   - The same can be triggered by weak stimulation combined with dopamine D1/D5 agonists, BDNF or
     carbachol (R p. 163).
   - Products (candidates: ARC, GluR1, HOMER1A, PKMζ; R p. 163) are delivered throughout the cell
     and remain available for hours (M&K p. 814).
4. **Capture.**
   - A synapse that still carries its tag when PRPs are present converts E-LTP into
     protein-synthesis-dependent L-LTP, lasting ≥8 h in slices (M&K Fig. 2).
   - The order can go either way, weak before strong or strong before weak, within the windows in
     the synthesis table below.
   - Untagged synapses ignore the PRPs. That keeps the change input-specific even though the PRPs
     spread across the whole cell (R p. 161).
5. **Spatial and resource limits.**
   - Fast crosstalk: RAS and RHOA spread ~5–10 µm for ~5 min after LTP at one spine (R p. 163).
   - STC itself: weak beyond ~70 µm, and weaker across dendritic branches.
   - When two nearby spines are potentiated together they compete for a limited PRP pool
     (Govindarajan et al. 2011; R p. 164).
6. **Bidirectionality.** Early LTD is captured into late LTD in the same way, including by PRPs from
   L-LTP at other synapses (cross-capture; R p. 162).

```
weak input ──► E-LTP + TAG (local, no new protein, decays ~1–2 h)
                    │
                    ├── no PRPs before the tag decays ──► weight returns to baseline
                    │
strong input / ──► CaMKII–CaMKIV–CREB ──► transcription ──► PRPs (cell-wide, limited)
DA (D1/D5),                                                    │
BDNF, ACh                                                      ▼
                    └── tag still present when PRPs arrive ──► CAPTURE ──► L-LTP (stable)
```

## Influence on memory consolidation

The two meanings of "consolidation" follow
[hippocampal_plasticity_model.md](../hippocampal_plasticity_model.md) (Terminology section).

### Cellular consolidation

- **STC is the proposed synaptic correlate.** It turns a transient, protein-synthesis-independent
  change into a lasting, protein-synthesis-dependent one, the same transition that defines cellular
  consolidation. That is a hypothesis, not an identity.
- **Behavioural tagging:** the evidence that the same rules work at the level of behaviour (R pp. 164–165).
  - A weak inhibitory-avoidance memory, lasting hours, became long-term, lasting days, when the rat
    explored a *novel* environment 1 h before training. A familiar environment did not do this. The
    effect needed dopamine and protein synthesis (Moncada & Viola 2007).
  - The same held for spatial object recognition, contextual fear conditioning and conditioned taste
    aversion (Ballarini et al. 2009).
  - A weakly encoded food location became long-lasting when novelty followed 30 min later. This
    needed hippocampal D1/D5 receptors and protein synthesis. In slices, the matching strong tetanus
    converted E-LTP to L-LTP on a convergent pathway (Wang et al. 2010).
- **What the model takes from this:**
  - A strong or novel event within the window supplies the PRPs that rescue a weak memory.
  - Dopamine is the gate that links novelty to PRP synthesis.
- **Limits:**
  - Novelty 1 h *after* inhibitory-avoidance training *impaired* the memory. There was no effect at
    5 min or at 6 h (Izquierdo et al. 1999; R p. 165).
  - The authors say there is no direct evidence that behavioural tagging actually runs through STC,
    rather than through protein-synthesis-dependent changes in neuromodulators (R p. 167).

### Memory allocation and linking

- **STC decides where a memory is stored** (R pp. 161–166, Fig. 3):
  - For ≥1 h after a strong memory, the neurons that stored it hold PRPs.
  - A weak memory arriving then gets L-LTP in those neurons but not in others.
  - So STC selects the storing *neurons*, not just the synapses.
- **Excitability works alongside it.** CREB-driven excitability makes recently active neurons more
  likely to store the next memory. Memories formed close together in time therefore overlap and are
  linked, so recalling one recalls the other (R Fig. 2).
- **Clustering:** crosstalk over short distances and the ~70 µm STC limit favour clusters of
  potentiated spines on one branch. Clustered new spines are more stable (Fu et al. 2012; R p. 165).
- **Metaplasticity:** one memory changes the plasticity thresholds that apply to the next, over
  minutes to days (R p. 164).

### System consolidation and sleep

None of the three reviews links STC directly to sleep. Kim & Park describe the setting in which
captured changes are then consolidated or pruned:

- **Replay:**
  - In NREM sleep, sharp-wave ripples, coupled to spindles and slow oscillations, replay recent
    experience and drive transfer from hippocampus to cortex (K&P p. 427).
  - The cortical side then needs its own cellular consolidation.
- **Neuromodulator gating:**
  - VTA dopamine during NREM lines up with memory-related activity and may decide which memories are
    prioritised (K&P pp. 428–430).
  - Noradrenaline from the locus coeruleus oscillates at ~0.02 Hz and controls when spindles occur.
  - Dopamine is the same signal that gates PRP synthesis in behavioural tagging. So it is a plausible
    common gate for capture during waking and for prioritisation during sleep. This is our inference,
    not a claim of the reviews.
- **Downscaling vs preservation:**
  - Sleep weakens synapses overall (Synaptic Homeostasis Hypothesis; Homer1a-driven scaling,
    Diering et al. 2017).
  - Assemblies reactivated in NREM keep their strength (K&P Fig. 2C).
  - Sleep promotes branch-specific spine formation after learning (Yang et al. 2014), and REM
    selectively prunes or keeps new spines (Li et al. 2017).
  - **For the model:** captured, replayed synapses should be protected from global downscaling;
    uncaptured ones should not be.
- **Timescale:**
  - Capture needs PRPs and tags within hours of each other. Only replay in the first hours after
    learning can drive capture.
  - Replay over days is the proposed driver of system consolidation, not of STC.

## Synthesis for S4–S6 (tag/capture)

| Element | What the three reviews report | Source |
|---|---|---|
| Tag | Local, transient, needs no new protein; CaMKII and actin; probably several tags, not one molecule | M&K pp. 815, 819; R p. 163 |
| Tag lifetime (CA1) | ~1–2 h (M&K); "up to 1 h" (R) | M&K p. 815; R p. 162 |
| Weak → strong window (CA1) | Weak 1–2 h before strong (M&K); up to 1 h before (R) | M&K p. 814; R p. 162 |
| Strong → weak window (CA1) | Weak <2.5–3 h after strong (M&K); ≥1 h after (R, Fig. 3) | M&K p. 814; R p. 162 |
| E-LTP / L-LTP decay | 1 train decays after ~1.5 h; 3 trains persist ≥8 h | M&K Fig. 2 |
| PRPs | Need transcription and translation (CaMKII–CaMKIV–CREB); candidates ARC, GluR1, HOMER1A, PKMζ; limited pool, competition | R pp. 163–164 |
| Spatial range | Fast crosstalk ~5–10 µm for ~5 min (RAS/RHOA); STC weak beyond ~70 µm and across branches | R pp. 163–164 |
| LTD | Tags and products also convert early LTD into late LTD (cross-capture) | R p. 162 |
| Neuromodulation | Dopamine D1/D5 needed for behavioural tagging; dopamine and noradrenaline in sleep gate which memories are prioritised | R pp. 163–165; K&P pp. 428–430 |
| Allocation | CREB-driven excitability chooses neurons; STC chooses synapses (and neurons) | R pp. 158–166 |
| Sleep | Homeostatic downscaling (Homer1a) and targeted preservation and pruning of synapses | K&P pp. 429–430 |

### Caveats

- **The two reviews give different time windows.** Martin & Kosik give a 1–2 h tag and accept a
  weak input up to 3 h after the strong one. Rogerson et al. cite 1 h in both directions. Both cite
  Frey & Morris 1997/1998, so take the window from those primary papers, together with their
  recording conditions.
- **No recording conditions are given** (temperature, [Ca²⁺]ₒ, age) for any quoted number. All
  values are second-hand from reviews.
- **Behavioural tagging may not use STC.** Rogerson et al. say directly that it has not been shown
  to.
