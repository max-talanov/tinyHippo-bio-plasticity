# CA1 circuit architecture: literature check of the Tier-B design

Date: 2026-10-20. Scope: does the Tier-B circuit in `docs/plan.md` (PYR + PV basket + bistratified + O-LM) match the
published CA1 architecture, and which short-term-plasticity (STP) numbers can be entered in `params.py`.
Status of every number: read from the source named, **secondary** unless stated (see `params.py`).

## Sources actually read

| Source | What was read | Limits |
|---|---|---|
| Ecker et al. 2019 bioRxiv 10.1101/716480 v1 (Hippocampus 2020, 30:1129) | full text and Table 1 (PDF) | v1 only; internal CA1 connections only, no Schaffer collateral (SC) pathway; juvenile rat, [Ca²⁺]ₒ 2 mM, simulated at 34 °C |
| Hippocampus Hub, SC experimental data (quotes Wierenga & Wadman 2003, Le Roux 2013, Andrasfalvy & Magee 2001, Sayer 1990, Glickfeld & Scanziani 2006, Pouille & Scanziani 2001) | page text | secondary; temperature and [Ca²⁺]ₒ of the underlying studies not on the page |
| Losonczy et al. 2002 | abstract only | PMC (reCAPTCHA) and Wiley (403) block the full text, Europe PMC API returns 500 |

Not read: Cutsuridis 2010, Bezaire 2016, Wierenga & Wadman 2003, Kohus 2016, Markram 2015 (still unverified citations).

## 1. Connectivity of the Tier-B circuit against the literature

| Plan element | Literature support | Verdict |
|---|---|---|
| SC → PYR, SC → PV, SC → BiS (feedforward) | Hub: SC makes ~20.9k synapses on excitatory and ~12.7k on inhibitory CA1 cells (Bezaire & Soltesz 2013); SC→PV+ has 1.19 synapses per connection. EPSP→IPSP latency 1.9 ± 0.6 ms (Pouille & Scanziani 2001, rat, 30 d) | supported; the 1.9 ms latency is the target for the feedforward-inhibition delay in S3 |
| PYR → PV, BiS, O-LM | Ecker: PC → all interneuron classes parameterised; PC → O-LM is its facilitating class E1 | supported |
| PV → PYR soma, BiS → PYR, O-LM → PYR | Ecker: PV+ and SOM+ → PC all depressing (I2) | supported; but see 3 for the O-LM output |
| PYR → PYR recurrent | Ecker: PC → PC is a parameterised pathway (E2, 0.6 nS, N_RRP 2) | **not in the plan** (Tier A/B have 1 PYR); Tier C would add it |
| Interneuron classes omitted | Ecker lists CCK+ basket, axo-axonic, Schaffer-collateral-associated, Ivy, trilaminar cells as separate classes | acceptable simplification; state it. PV basket stands in for all PV+ perisomatic input |

Nothing in the literature read contradicts the Tier-B wiring. It does not support any claim that a single PYR with three interneurons reproduces population E/I balance (Ecker predicts first-PSP amplitudes per pathway for the full network; those are the check for contact-count scaling).

## 2. STP parameters now in `params.py`

U is the release fraction, D = τ_rec, F = τ_fac (ms). SD in brackets where stated.

| Pathway | U | D (ms) | F (ms) | Source | Caveat |
|---|---|---|---|---|---|
| SC → PYR | 0.14 (0.08) | 186 (71) | 129 (68) | Wierenga & Wadman 2003 via Hub, rat 14–28 d, n = 8 | T, [Ca²⁺]ₒ unknown |
| SC → interneurons | 0.11 (0.04) | 307 (233) | 195 (134) | same, n = 20 | pooled over interneuron types; used for both PV and BiS |
| PYR → PV basket, BiS | 0.23 (0.09) | 410 (190) | 10 (11) | Ecker class PC→SOM⁻ | class average; same value for both rows |
| PYR → O-LM | 0.09 (0.12) | 138 (211) | 670 (830) | Ecker class PC→SOM⁺ | marked * in the table: **rat somatosensory cortex**, not CA1; SDs as large as the means |
| PV basket → PYR | 0.16 (0.02) | 965 (185) | 8.6 (4.3) | Ecker | N_RRP 6 |
| BiS → PYR | 0.13 (0.03) | 1122 (156) | 9.3 (0.7) | Ecker | |
| O-LM → PYR | 0.30 (0.08) | 1250 (520) | 2 (4) | Ecker | marked *: cortical (SOM⁺ → PC) |

Qualitative agreement with Losonczy 2002 (abstract): PYR → O-LM facilitating, basket depressing, O-Bi mixed. Consistent.

## 3. Findings that change the plan

1. **The S2 pass criterion "SC → PV depressing" is not what the data say.** Closed-form paired-pulse ratio from the Wierenga numbers (U 0.14, D 186, F 129): PPR = 1.52 / 1.41 / 1.28 / 1.13 / 1.01 at ISI 20 / 50 / 100 / 200 / 500 ms for SC → PYR; 1.62 / 1.53 / 1.41 / 1.24 / 1.05 for SC → interneurons. Both facilitate at paired pulses (low U, F comparable to D). `params.py` classes for SC_PYR, SC_PV, SC_BiS are now "facilitating" accordingly. The plan text ("SC → PYR mild, SC → PV depressing") should be revised after the primary paper is read. Caution: Ecker's tables place PC → interneuron and interneuron → PC as depressing, so only the SC → interneuron entry is in tension with the plan, and that entry pools all interneuron types.
2. Computed PPR for the other pathways (same formula): PYR → PV/BiS 0.86 / 0.80 / 0.82 / 0.86 / 0.93 (depressing); PYR → O-LM 1.74 / 1.73 / 1.71 / 1.64 / 1.43 (facilitating); PV → PYR 0.91–0.85 (depressing); O-LM → PYR 0.70–0.80 (depressing). These pass the sign test, using closed-form TM, not a NEURON run.
3. **PYR → O-LM has the weakest evidence**: cortical values with SDs of the order of the means. Its facilitating class is supported by several CA1 papers cited in Ecker (Ali & Thomson 1998, Biro 2005, Losonczy 2002, Pouille & Scanziani 2004), so the sign is solid and the numbers are not. Fit it in S2 against CA1 traces rather than adopting them.
4. **Receptors on SC → interneuron synapses**: NMDA/AMPA ratio 0.16 ± 0.07 (mouse 17–23 d, Le Roux 2013) against 1.23 ± 0.03 for SC → excitatory. The plan gives AMPA only for interneuron inputs, which fits. Ecker, in contrast, assumes the excitatory-to-excitatory ratio for E→I (their assumption 3), so the two sources disagree here.
5. NMDA kinetics for S5: τ_rise 2.93 ms, τ_decay 148.5 ms (rat 6–12 weeks, CA1, Andrasfalvy & Magee 2001) for SC → PYR. Different age from the STP data (14–28 d); record that when mixing.
6. Release probability scales with [Ca²⁺]ₒ (Ecker uses a Hill function fitted on cortical data). At 1.1–1.3 mM, PC → PC loses its depressing profile. The S3 volleys are meant as in-vivo-like, so the 2 mM parameters are an upper bound on U. Sweep it.

## 4. What is still missing for S2

- Primary full texts: Wierenga & Wadman 2003 (SC STP, conditions), Losonczy 2002 (afferent, conditions, numbers). Network policy was not the blocker this time; the publishers' anti-bot checks are. A PDF supplied by the user, or an institutional proxy, would resolve it.
- SC → bistratified and SC → PV individually (only a pooled interneuron fit exists in what was read).
- A CA1 source for PYR → O-LM numbers.
- Temperature and [Ca²⁺]ₒ for the Wierenga data.
