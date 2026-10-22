# Hippocampal Plasticity Model: Memristive Circuit Implementation

This document specifies hardware realizations — memristive and digital — of the model described in
[hippocampal_plasticity_model.md](hippocampal_plasticity_model.md) (cited below as "model §n"). Section
references without a prefix are to this document. Further hardware-feasibility detail is in
[docs/neuron_model_optimization.md](docs/neuron_model_optimization.md) (the "companion hardware document").

*Terminology follows model §1: "consolidation" is always qualified as **cellular** (protein-synthesis-
dependent stabilization within ~6 h, local to each region, cortex included) or **system** (the memory
becoming independent of the hippocampus over days or longer). The text was moved from the original
combined specification (`hippocampal_timescales_as_circuit_spec.md`) and revised on this point.*

## 1. Timescale constraints on circuits

What matters for hardware is not the molecular detail of each process in model §1 but three facts:
which processes are fast enough to force analog/continuous-time circuitry, which are slow enough that a
clocked digital design is free, and where the biological threshold behavior maps directly onto a
specific circuit primitive.

| Stage | Time constant | What it forces on a circuit |
|---|---|---|
| Neurotransmission (AMPA/NMDA gating) | ~0.5–5 ms | Sets the fastest timescale in the whole system — the floor for any front-end comparator bandwidth. |
| Short-term plasticity | ~10 ms–1 s | NMDAR's slower deactivation is *why* a ±20 ms coincidence window exists at all — a real biophysical constant, not a modeling convenience. |
| Ca²⁺/kinase cascades | ~1 s–5 min | The "weight update decision" happens on this timescale; anything reading it out only needs to sample in the low-second range. |
| AMPAR trafficking / early-LTP | ~1–30 min, decays over 1–3 hr | A real, decaying analog state — this *is* the tag described below. |
| Synaptic tagging & capture | tag set in 1–2 min, decays τ≈1–4 hr | The pivot point: a local, transient, decaying signal that is either captured or lost — directly analogous to a volatile-memristor relaxation state (§2). |
| Transcription / late-LTP | onset ~30–60 min, stable by ~4–8 hr | Once captured, this state should stop decaying — a discrete regime change, not a continuous process. |
| Sharp-wave-ripple replay | ripple 100–300 ms, recurs over hours–days | Compressed replay packs sequence elements only a few milliseconds apart — this is the number that actually sizes circuit timing budgets in §4 of the companion hardware document (`docs/neuron_model_optimization.md`). |
| System consolidation | days–weeks (rodent) to months–years (human) | Fully clocked-digital territory; no continuous-time requirement whatsoever. |

### 1.1 Tier assignment

The eight processes on one time axis are model Fig. 1 (`figures/timescale_axis.png`). The table assigns each to the memristor tier that implements it (§6): quick/organic (hippocampal-local), the replay bridge that touches both tiers, or slow/inorganic (cortical).

![The eight plasticity and memory processes on one logarithmic time axis (model Fig. 1).](figures/timescale_axis.png)

| Stage | Time constant | Tier | Jump to |
|---|---|---|---|
| Neurotransmission (AMPA/NMDA gating) | ~0.5–5 ms | Quick (organic) | model §3.1 |
| Short-term plasticity | ~10 ms–1 s | Quick (organic) | model §3.4 |
| Ca²⁺/kinase cascades | ~1 s–5 min | Quick (organic) | model §3.4 |
| [AMPAR trafficking / early-LTP](#2-synaptic-tagging-and-capture-as-a-volatile-memristor-circuit) | ~1–30 min, decays over 1–3 hr | Quick (organic) | [§2](#2-synaptic-tagging-and-capture-as-a-volatile-memristor-circuit) |
| [Synaptic tagging & capture](#2-synaptic-tagging-and-capture-as-a-volatile-memristor-circuit) | tag set 1–2 min, decays τ≈1–4 hr | Quick (organic) | [§2](#2-synaptic-tagging-and-capture-as-a-volatile-memristor-circuit) |
| [Transcription / late-LTP](#6-system-consolidation-replay-as-a-volatile-to-non-volatile-handoff) | onset ~30–60 min, stabilized ~4–8 hr; persists days or longer | Quick (organic); cortical counterpart on the slow tier (§6) | [§6](#6-system-consolidation-replay-as-a-volatile-to-non-volatile-handoff) |
| [Sharp-wave-ripple replay](#6-system-consolidation-replay-as-a-volatile-to-non-volatile-handoff) | ripple 100–300 ms, recurs over hours–days | Bridge (organic → inorganic) | [§6](#6-system-consolidation-replay-as-a-volatile-to-non-volatile-handoff) |
| [System consolidation](#6-system-consolidation-replay-as-a-volatile-to-non-volatile-handoff) | days–weeks (rodent) to months–years (human) | Slow (inorganic) | [§6](#6-system-consolidation-replay-as-a-volatile-to-non-volatile-handoff) |

## 2. Synaptic tagging and capture as a volatile-memristor circuit

The tag/capture dynamic of model §2 — a tag set by coincident activity, decaying with a fixed time constant, and captured only if the PRP signal crosses threshold before it decays — is close to the operating description of a **volatile threshold-switching memristor**: a device that transitions to a low-resistance state on a triggering pulse and spontaneously relaxes back over an intrinsic retention time — unless something latches it into a non-volatile state first.

The falsification test of model §2 (model Fig. 2: the weight distribution stays flat when capture is blocked, while replay quality, measured independently, stays unchanged) defines the test for a candidate memristive tagging device: drive it with the same input statistics and check whether blocking "capture" produces the same flat, non-accumulating signature.

## 3. Stage-by-stage feasibility

The three-stage pipeline of model §3 — postsynaptic threshold, OR-gated refractory junction, somatic summation — is treated in the companion hardware document as an information-reduction pipeline, and each stage is a candidate site for replacing an expensive analog circuit with a cheap thresholding one. The model §3.3 topology maps onto circuit primitives as follows: each first-tier junction is a plain wired-OR (§4.2 of the companion document), and the repeated `th/rp` primitive is the reusable leaf cell specified there.

| Stage | Circuit primitive | Feasibility | Main open risk |
|---|---|---|---|
| Postsynaptic threshold (dSpike) | Memristor + local comparator | High — prototype-ready | Conductance drift shifting the threshold near the decision boundary |
| Junction (OR + refractory) | Wired-OR + edge-catcher + counter FSM, or a volatile memristor | High | Volatile-memristor relaxation-time variability, if used in place of a digital counter |
| Synaptic clustering | Non-uniform crossbar floorplan / reconfigurable interconnect | Moderate — the binding constraint | Needs 3D memristive/CMOS integration to be biologically faithful; not yet a mature foundry process |
| Somatic E/I summation | Differential integrate-and-fire | High — already standard (Loihi, BrainScaleS, TrueNorth-class cores) | None specific to this proposal |

Three of the four stages are near off-the-shelf. The junction/tag stage is the exception: it is the hardest stage, and the one where biology and device physics align most directly. §2 and §5 specify it in detail.

## 4. `V_seg` as a circuit block

`V_seg` (model §3.4) is one added analog block per `thr` unit (a leaky-integrator capacitor plus a differential-pair sigmoid stage, both standard sub-threshold-CMOS primitives) driving a graded-amplitude SET pulse into the same volatile memristor proposed as the tag element in §2, instead of a fixed-height pulse. The open risk is whether that memristor's SET response is graded over a useful amplitude range — parallel to the `τ_rf` variability already flagged for the junction stage, but along the amplitude axis.

## 5. Tag-element implementations: digital and non-digital

Model §2 and model §3.4 specify the tag element at the level of dynamics, independent of device technology. The junction stage (§3) admits two implementation options for its own `τ_rf` timer — a wired-OR/counter FSM or a volatile memristor — and the tag element admits the same choice. §5.1 specifies the digital option; §5.2 specifies a non-digital (memristive) candidate under active development.

### 5.1 Digital implementation

A fully digital tag/capture circuit uses: a multi-bit register per tag site, holding the tag amplitude; a down-counter clocked by a slow divider, decrementing the register at a rate set to reach zero after `τ_tag` (an 8–12 bit register decremented roughly once per 1–15 minutes covers the `τ_tag ≈ 1–4 hr` range); and a digital comparator that checks the register against zero before each decrement. Capture is a single conditional write: if the PRP-threshold signal (already sampled at low-second resolution per §1's table, well within reach of a digital sampler) crosses its set point while the register is still nonzero, the register's current value is copied into a separate, non-decrementing capture register and the down-counter is disabled for that site; if the PRP-threshold signal has not crossed by the time the register reaches zero, the tag register clears and no capture occurs. `V_seg`'s graded tag amplitude (model §3.4) sets the register's initial loaded value rather than a fixed constant, and the falsification test in model §2 (flat weight distribution when capture is blocked, replay quality unaffected) applies unchanged by disabling the conditional-write path. This circuit uses only standard cells — register, down-counter, comparator, clock divider — with no memristor, retention variability, or device characterization; each site's `τ_tag` is set by a clock-divider ratio, deterministic and identical across sites. The cost is area: one register, counter, and comparator per tag site, versus one two-terminal memristor in the non-digital route of §5.2.

### 5.2 Non-digital implementation: copper-aspirinate memristors

Caus, Sławek, Mazur, Zawal, Baś, Szaciłowski, Talanov & Abdi (2026, "The memristive implementation of the hippocampus: a hypothesis") report a concrete candidate for the volatile threshold-switching memristor specified as the tag element in §2, built and electrically tested. The material is polycrystalline copper(II) bis-aspirinate, [Cu₂(asp)₄], spin-coated as a thin layer on ITO and capped with a sputtered copper electrode; three axially-ligated derivatives — [Cu₂(asp)₄(py)₂] (pyridine), [Cu₂(asp)₄(bimi)₂] (benzimidazole), and [Cu₂(asp)₄(DABCO)₂] — were prepared from the same parent complex by adding an axial N-donor ligand. All but the DABCO derivative show pinched I–V hysteresis loops under cyclic voltammetry, the standard electrical signature of memristive switching. The axial ligand tunes two properties: conductivity (the pyridine and benzimidazole derivatives conduct roughly two orders of magnitude more than the unligated parent) and retention. In chronoamperometric retention testing, the unligated parent's low-resistance state decayed to the high-resistance state within about 50 minutes (volatile); the benzimidazole derivative's high- and low-resistance states remained stable, essentially noise-free, after 6 hours (non-volatile on the timescale tested).

This volatile-versus-latched split, produced by changing only the axial ligand on one underlying complex, brackets the `τ_tag ≈ 1–4 hr` range in §1's table and provides the two states the tag/capture analogy in §2 requires: a device that relaxes on its own (parent complex, minutes-scale retention) and a device that holds once switched (benzimidazole derivative, hours-plus retention) — a materials-level realization of "tag decays unless captured." The paper's I–V and retention data characterize switching and retention, not conductance-step-versus-pulse-amplitude behavior; the graded-SET behavior specified in §4's `V_seg` block is not demonstrated by this data and remains an open device-characterization question. The same paper's methylammonium-lead-iodide perovskite devices, modified with graphene oxide, fullerenol (C₆₀(OH)), or multiwalled carbon nanotubes, show measurable STDP-like potentiation directly in the memristive response, a second materials route toward stage-1's threshold-plus-plasticity behavior. The same paper also proposes a random-junction stochastic-network framing (percolating Ag–Ag₂S and SWNT/Por-POM meshes) as a physical analogue for the probabilistic, disordered connectivity in the clustering stage.

## 6. System consolidation: replay as a volatile-to-non-volatile handoff

§1's system-consolidation row and §5.2's device data point at the same architecture from two directions: a hippocampal trace forms fast, locally, and is volatile until captured; a cortical trace is slow to form but, once formed, stable. Replay (§1, SWR row) is the proposed mechanism by which the memory comes to be supported by the cortical trace, and the two memristor technologies proposed as tag elements above map onto the two sides of that process by more than analogy.

What system consolidation is defined by matters for the hardware reading (model §1, §4): after it, the memory no longer *depends* on the hippocampus. That observation does not establish that the hippocampal trace is gone. Three accounts are compatible with it (citations from memory, unverified): the standard model, in which the hippocampal trace is no longer needed once the cortical one is established (e.g. Squire & Alvarez, 1995); multiple-trace theory, in which the hippocampus remains necessary for detailed episodic recall (Nadel & Moscovitch, 1997); and trace-transformation theory, in which the cortical trace is a schematic version of the hippocampal one (Winocur & Moscovitch, 2011). The architecture below commits to none of them: the state of the fast tier after system consolidation is a free parameter.

**Fast tier: organic volatile memristors.** The tag/capture element in §2 and §5.2 is deliberately a device that relaxes on its own unless captured — matching Victor Erokhin's organic (polymeric) memristors, which switch and decay on short, biologically-relevant timescales and, being solution-processed, can be additively 3D-printed rather than requiring foundry fabrication. That fabrication route trades device count for reconfigurability: organic memristors are cheap to print in small numbers at synapse-like density, which is exactly the local, per-tag-site role §2 and §5 assign them, not a route to the device counts a cortex-scale store needs.

**Slow tier: inorganic non-volatile memristors, at scale.** System consolidation makes the memory supported by a much larger, distributed population of cortical synapses — a fan-out, not a copy. Themis Prodromakis's inorganic (metal-oxide) memristor crossbars are the complementary device for that side: individually slower to switch and non-volatile once set, but fabricated at silicon densities reaching on the order of 10⁶ devices per chip. What this tier contributes is not per-device sophistication but sheer number — the same property that lets a sparse hippocampal representation drive a large population of stable cortical sites.

Cortical synapses undergo cellular consolidation of their own (model §4): a cortical change is labile until a local, protein-synthesis-dependent step stabilizes it. The slow tier therefore cannot be a write-once store in which every SET pulse is permanent. Each cortical site needs a labile state that decays unless enough replay passes arrive to latch it — the cortical counterpart of tag/capture. Whether a single inorganic device shows this volatile-until-latched behavior, or a volatile and a non-volatile device must be paired per site, is an open device requirement.

**Replay as the handoff mechanism.** Each SWR event (§1: 100–300 ms, recurring over hours–days) replays a compressed version of a stored sequence, re-driving the same volatile organic tag sites that stored it originally. Repeated replay is the network-level equivalent of the PRP-threshold capture signal in §2: each pass is one more SET pulse toward a target inorganic memristor, and once enough passes have accumulated, that cortical-side device latches into its own non-volatile state — the same discrete regime change §1 assigns to transcription/late-LTP, now occurring at cortical sites: the slow tier's own cellular consolidation. Before enough replay has occurred, recall depends on the fast organic tier, and the memory is lost if the organic trace decays uncaptured; after, recall no longer depends on the organic device's state. That loss of dependence — not erasure of the organic trace — is the hardware reading of system consolidation.

**Process-to-device mapping.** The split follows the anatomy, not the process list: every stage that runs *at the hippocampal synapse* — from neurotransmission through late-LTP, including the full tag-decay/capture dynamic of model Fig. 2 — stays on the quick, organic-volatile side. Only replay and system consolidation involve the slow, inorganic side, because they are the only processes in this model that engage cortical synapses. Cellular consolidation is not confined to one tier: it is tag/capture on the organic side and the latching step on the inorganic side.

| Process (§1) | Time constant | Hippocampal / quick tier — organic volatile memristor (Erokhin) | Cortical / slow tier — inorganic non-volatile memristor (Prodromakis) |
|---|---|---|---|
| Neurotransmission (AMPA/NMDA gating) | ~0.5–5 ms | Upstream of any memristive state — sets comparator bandwidth only | — |
| Short-term plasticity | ~10 ms–1 s | Organic memristor's own fast conductance dynamics, alongside `V_seg`/dSpike (model §3.4) | — |
| Ca²⁺/kinase cascades | ~1 s–5 min | Sets tag-induction amplitude (`tag_amplitude`, model §3.4) — the SET pulse into the organic device | — |
| AMPAR trafficking / early-LTP | ~1–30 min, decays 1–3 hr | The organic device's own relaxing low-resistance state (§2, §5.2 parent complex) | — |
| Synaptic tagging & capture | tag set 1–2 min, decay τ≈1–4 hr | Model Fig. 2's decay/capture dynamic, entirely within the organic device — PRP-threshold crossing is the capture event | — |
| Transcription / late-LTP | onset 30–60 min, stabilized ~4–8 hr; persists days or longer | Captured, stabilized organic-device state, held locally at the hippocampal synapse (hippocampal cellular consolidation) | Same regime change at cortical sites when replay latches them (cortical cellular consolidation) |
| Sharp-wave-ripple replay | 100–300 ms, recurs over hours–days | Re-drives the stabilized organic synapse on every pass | Each pass delivers one accumulating SET pulse toward the cortical device — the fan-out source |
| System consolidation | days–weeks (rodent) to months–years (human) | Recall stops depending on the organic device once the trace has been sufficiently replayed; the device's state afterwards (cleared, kept or transformed) is a free parameter | Inorganic crossbar — the distributed cortical store (10⁶ devices/chip), stable once latched |

Everything through late-LTP is a hippocampal-synapse-local, organic-volatile story — nothing inorganic is involved yet. Replay is the only process that touches both tiers at once: it reads the stabilized organic state and writes it, pulse by pulse, into the cortical inorganic array, which is why system consolidation (days to years) is orders of magnitude slower than tagging and capture (minutes to hours) — it is rate-limited by how often replay revisits a given trace, not by either device's intrinsic switching speed.

**Open risk.** This is an architectural hypothesis, not a demonstrated circuit: it requires a working interface between an organic volatile array and a much larger inorganic non-volatile array, with the replay-driven SET-accumulation rate on the inorganic side calibrated against the days-or-longer system-consolidation timescale in §1's table — a two-technology integration problem on top of the single-device characterization risks already flagged in §4 and §5.2, plus the volatile-until-latched requirement on the cortical device above.

---

*Full technical detail: [Consolidation Cascade](https://claude.ai/code/artifact/f879468e-00e8-4ca1-9acc-348b12cc7e33) (molecular timescales) and [`docs/neuron_model_optimization.md`](docs/neuron_model_optimization.md) (hardware feasibility).*
