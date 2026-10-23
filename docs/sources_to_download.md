# Sources to download

Date: 2026-10-23. Purpose: papers that unblock the open items of `docs/plan.md` (S2 finish, S3b, S3d).
I cannot fetch most of them: PubMed Central shows a reCAPTCHA, Wiley returns 403, and the Europe PMC API returned
HTTP 500. Please download the PDFs into one folder in this project (for example `docs/papers/`, not committed unless you
want them in git) and tell me; I read them with the PDF tools and enter values in `params.py` with source and conditions.

**How reliable each entry is.** "Search" means the title, venue and identifier were returned by a web search on
2026-10-23. "Ecker list" means the exact reference is copied from the reference list of Ecker et al. 2019 (bioRxiv 716480).
"Memory" means I give it from memory and it must be checked. I have not read any paper below except Ecker et al. 2019
(preprint v1) and the Hippocampus Hub page.

## A. Finish S2: primary STP data for the 9 pathways in `params.py`

| Priority | Paper | Why | Where | Basis |
|---|---|---|---|---|
| 1 | Wierenga CJ, Wadman WJ (2003). Excitatory inputs to CA1 interneurons show selective synaptic dynamics. *J Neurophysiol* 90:811–821. DOI 10.1152/jn.00865.2002, PMID 12904494 | Source of the SC→PYR and SC→interneuron U, D, F now in `params.py` (secondhand, via the Hippocampus Hub: Wistar rat, 14–28 d). Need temperature, [Ca²⁺]ₒ, interneuron types, and whether the numbers are per cell or pooled | [UvA repository record](https://dare.uva.nl/id/508febca-9d11-4539-990f-ad02ff3a3308) | Search |
| 2 | Sun HY, Lyons SA, Dobrunz LE (2005). Mechanisms of target-cell specific short-term plasticity at Schaffer collateral synapses onto interneurones versus pyramidal cells in juvenile rats. *J Physiol*. DOI 10.1113/jphysiol.2005.093948 | The most recent paper found that compares SC→pyramidal and SC→stratum-radiatum interneuron STP and explains it by release probability and pool size. Independent check of the claim that SC→interneuron facilitates, which contradicts the plan's old "SC→PV depressing" | [Wiley](https://physoc.onlinelibrary.wiley.com/doi/abs/10.1113/jphysiol.2005.093948) | Search |
| 3 | Losonczy A, Zhang L, Shigemoto R, Somogyi P, Nusser Z (2002). Cell type dependence and variability in the short-term plasticity of EPSCs in identified mouse hippocampal interneurones. *J Physiol* 542:193–210 | Classes now in `params.py` come from its abstract only (O-LM mostly facilitating, basket depressing, O-Bi mixed). Need afferent, conditions, numbers | [PMC2290398](https://pmc.ncbi.nlm.nih.gov/articles/PMC2290398/) | Ecker list, Search |
| 4 | Ecker A, et al. (2020; first-author initials and co-authors not checked). Data-driven integration of hippocampal CA1 synaptic physiology in silico. *Hippocampus* 30(11):1129–1145. DOI 10.1002/hipo.23220 | I read the preprint v1 (Table 1). The published version may have changed Table 1; it is the source of 6 of the 9 pathways (the other 3 are the SC pathways, from the Hub) | [PMC7687201](https://pmc.ncbi.nlm.nih.gov/articles/PMC7687201) | Search |
| 5 | Éltes T, Kirizs T, Nusser Z, Holderith N (2017). Target cell type-dependent differences in Ca²⁺ channel function underlie distinct release probabilities at hippocampal glutamatergic terminals. *J Neurosci* 37(7):1910–1924 | Cited by Ecker for the PC→stratum-oriens-interneuron class (facilitating). Possible CA1 source for the PYR→O-LM numbers, which are currently cortical | Search by title | Ecker list |
| 6 | Kohus Z, Káli S, Schlingloff D, et al. (2016). Properties and dynamics of inhibitory synaptic communication within the CA3 microcircuits of pyramidal cells and interneurons expressing parvalbumin or cholecystokinin. *J Physiol* 594(13):3745–3774 | Ecker fitted the PV/CCK→PYR STP to its traces and assumed mouse CA3 is representative of rat CA1 (Ecker Table 2, assumption 1). So the PV→PYR and BiS→PYR rows in `params.py` rest on CA3 data | Search by title | Ecker list |

**More recent leads (not identified precisely; search these phrases):**
- a 2012 *Science* paper on Elfn1, which sets low release probability and strong facilitation at pyramidal→O-LM synapses
  (authors and DOI not shown in the search result; from memory Sylwestrak & Ghosh, *Science* 338:536. Check);
- a 2022 *Neuron* paper reporting a ~10-fold higher release probability at CA1 pyramidal→fast-spiking interneuron synapses than
  at O-LM synapses, linked to vesicle priming (authors and title not shown in the search result).
  Both bear on the PYR→O-LM and PYR→PV parameters.

## B. S3d: gain knobs (presynaptic inhibition and [Ca²⁺]ₒ)

| Priority | Paper | Why | Where | Basis |
|---|---|---|---|---|
| 1 | Dürst CD, Wiegert JS, Schulze C, et al. (2022). Vesicular release probability sets the strength of individual Schaffer collateral synapses. *Nat Commun*. DOI 10.1038/s41467-022-33565-6 | Open access. Release probability at single SC boutons at several [Ca²⁺]ₒ (binomial N, p_ves, q). The nearest source for a CA1 [Ca²⁺]ₒ–`U` curve to replace the cortical Hill function in Ecker | [PMC9576736](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9576736/), [PDF](https://openaccess.sgul.ac.uk/114932/1/s41467-022-33565-6.pdf), [preprint](https://www.biorxiv.org/content/10.1101/2020.08.02.232850v3.full.pdf) | Search (author list partly from memory) |
| 2 | Caruana DA, Dudek SM (2020). Adenosine A1 receptor-mediated synaptic depression in the developing hippocampal area CA2. *Front Synaptic Neurosci* 12:21. DOI 10.3389/fnsyn.2020.00021 | Open access. The A1 agonist CCPA depresses CA1 responses at P14 but, in this paper, not in adult (~P70) CA1. So a large A1 `U` gain on adult SC→CA1 may be unjustified; relevant to how big the S3d gain range should be | [PMC7307308](https://pmc.ncbi.nlm.nih.gov/articles/PMC7307308), [PDF](https://publications.aston.ac.uk/id/eprint/41677/1/fnsyn_12_00021.pdf) | Search |
| 3 | An adult rat CA1 study of adenosine and paired-pulse ratio (SAGE journal, DOI 10.1177/23982128221106315) | Reports drug effects on paired-pulse ratio and frequency facilitation in adult CA1, with the caveat that part of the PPR change follows from baseline depression. Title and authors were not returned by the search; check the DOI | [DOI](https://doi.org/10.1177/23982128221106315) | Search (identity unconfirmed) |
| 4 | Dunwiddie TV, Masino SA (2001) *Annu Rev Neurosci* 24:31–55; Davies CH, Starkey SJ, Pozza MF, Collingridge GL (1991) *Nature* 349:609–611 | Cited in the downscaling document for adenosine and GABA_B. Older; likely paywalled | | Downscaling document |

Caution from the search results: paired-pulse ratio is not a clean readout of release probability (a modelling study
shows `Pr` can raise, lower or leave PPR unchanged depending on what else changes), so an effect size on `U` should come from a paper that
reports release probability or fits a TM model, not PPR alone.

## C. S3b: cell calibration

| Priority | Paper | Why | Where | Basis |
|---|---|---|---|---|
| 1 | Migliore R, Lupascu CA, Bologna LL, et al. (2018). The physiological variability of channel density in hippocampal CA1 pyramidal cells and interneurons explored using a unified data-driven modeling workflow. *PLoS Comput Biol*. DOI 10.1371/journal.pcbi.1006423 | The CA1 cell models used by Ecker 2019 (pyramidal cells and interneurons, ion-channel densities, f–I behaviour). Source for rheobase and f–I targets in S3b | [DOI](https://doi.org/10.1371/journal.pcbi.1006423) | Ecker list (title), Search (DOI) |
| 2 | Bezaire MJ, Raikov I, Burk K, Vyas D, Soltesz I (2016). Interneuronal mechanisms of hippocampal theta oscillations in a full-scale model of the rodent CA1 circuit. *eLife* 5:e18566 | Open access. Full CA1 model with channel and cell parameters; code in ModelDB 187604 and on the Open Science Framework. Also verifies a citation of `docs/plan.md` that was from memory | [PMC5313080](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5313080/), [PDF](https://elifesciences.org/articles/18566.pdf) | Search |
| 3 | Bezaire MJ, Soltesz I (2013). Quantitative assessment of CA1 local circuits: knowledge base for interneuron–pyramidal cell connectivity. *Hippocampus* 23(9):751–785 | Source of the synapse counts quoted by the Hippocampus Hub (about 20.9k SC synapses on excitatory and 12.7k on inhibitory CA1 cells in total); informs the contact counts of the pilot circuit | | Ecker list |
| 4 | HippoUnit paper (PLoS Comput Biol, 2021) | Test suite that compares the Migliore 2018 CA1 models with experimental features; a ready way to validate the S3b cells | [PMC7875359](https://pmc.ncbi.nlm.nih.gov/articles/PMC7875359) | Search (title not shown) |

## D. Still unsourced (no paper identified)

- The ~6 h protein-synthesis-sensitive window (behavioural; personal communication from Edu): a primary reference.
- `k_cap`, `n`, `τ_P` of gradual capture (S4): no source expected; they are swept.
- Temperature and [Ca²⁺]ₒ of the SC data in `params.py`: in Wierenga & Wadman 2003 (A1).
- Citations of `docs/plan.md` still from memory after this list: Cutsuridis, Cobb & Graham 2010; Clopath et al. 2008;
  Barrett et al. 2009.
