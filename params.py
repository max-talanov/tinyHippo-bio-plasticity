"""Per-pathway synaptic parameters, with the source and status of every value.

status:
  "unverified"  value or class has no checked source yet (value is None until it has one)
  "abstract"    class taken from a paper's abstract only; numbers not yet read
  "secondary"   numbers read from a secondary compilation (Ecker 2019 Table 1, Hippocampus Hub), not yet
                checked against the primary paper
  "fitted"      fitted in this repository (give the RESULTS.md section)
Do not enter a number here that was not read from the cited source.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Pathway:
    name: str
    expected_class: str                  # "facilitating" | "depressing" | "mixed" | "unspecified"
    U: Optional[float] = None
    tau_rec: Optional[float] = None      # ms
    tau_fac: Optional[float] = None      # ms
    source: str = ""
    conditions: str = ""                 # species, age, temperature, [Ca2+]o, stimulated afferent
    status: str = "unverified"


# Sources (all read 2026-10-20):
#  ECKER: Ecker et al. 2019 bioRxiv 10.1101/716480 v1 (published Hippocampus 2020, 30:1129, PMC7687201), Table 1.
#         Rat CA1, juvenile, STP profiles valid at [Ca2+]o = 2 mM; model run at 34 C. TM parameters are fitted
#         (USE, D, F) or, where marked * in the table, taken from rat somatosensory cortex (Markram 2015).
#         v1 text only; check the published version for changes.
#  HUB:   Hippocampus Hub experimental-data page for Schaffer collaterals, quoting Wierenga & Wadman 2003
#         (Wistar rat, 14-28 d, CA1). Temperature and [Ca2+]o of that study are NOT stated on the page.
#  LOSONCZY: Losonczy et al. 2002 J Physiol 542:193 (abstract only; full text blocked by reCAPTCHA / HTTP 403).
_ECKER = "Ecker et al. 2019 bioRxiv 716480 Table 1"
_HUB = "Hippocampus Hub SC data, quoting Wierenga & Wadman 2003"
_COND_ECKER = "rat CA1, juvenile, [Ca2+]o 2 mM (model 34 C); fitted to published raw traces"
_COND_ECKER_CTX = "TM values marked * in Ecker Table 1: rat somatosensory cortex (Markram 2015), NOT CA1"
_LOSONCZY = "Losonczy et al. 2002 J Physiol 542:193 (abstract only)"

# U is USE (release fraction), tau_rec = D, tau_fac = F; times in ms.
PATHWAYS = {
    "SC_PYR": Pathway("SC_PYR", "facilitating", U=0.14, tau_rec=186.0, tau_fac=129.0,
                      source=_HUB, status="secondary",
                      conditions="Wistar rat 14-28 d, CA1, n=8 cells; U SD 0.08, D SD 71, F SD 68; "
                                 "T and [Ca2+]o not read. Not Ecker (Ecker has no SC pathway)"),
    "SC_PV": Pathway("SC_PV", "facilitating", U=0.11, tau_rec=307.0, tau_fac=195.0,
                     source=_HUB, status="secondary",
                     conditions="SC -> CA1 interneurons pooled (not PV-specific), Wistar rat 14-28 d, n=20; "
                                "U SD 0.04, D SD 233, F SD 134; T and [Ca2+]o not read"),
    "SC_BiS": Pathway("SC_BiS", "facilitating", U=0.11, tau_rec=307.0, tau_fac=195.0,
                      source=_HUB, status="secondary",
                      conditions="same pooled SC -> interneuron fit as SC_PV; not bistratified-specific"),
    "PYR_PV": Pathway("PYR_PV", "depressing", U=0.23, tau_rec=410.0, tau_fac=10.0,
                      source=_ECKER + " (class PC -> SOM-, E2, row PVBC)", status="secondary",
                      conditions=_COND_ECKER + "; U SD 0.09, D SD 190, F SD 11"),
    "PYR_BiS": Pathway("PYR_BiS", "depressing", U=0.23, tau_rec=410.0, tau_fac=10.0,
                       source=_ECKER + " (class PC -> SOM-, E2, row BS)", status="secondary",
                       conditions=_COND_ECKER + "; same class parameters as PYR_PV"),
    "PYR_OLM": Pathway("PYR_OLM", "facilitating", U=0.09, tau_rec=138.0, tau_fac=670.0,
                       source=_ECKER + " (class PC -> SOM+, E1)", status="secondary",
                       conditions=_COND_ECKER_CTX + "; U SD 0.12, D SD 211, F SD 830 (very broad)"),
    # Inhibitory outputs (S3), same table:
    "PV_PYR": Pathway("PV_PYR", "depressing", U=0.16, tau_rec=965.0, tau_fac=8.6,
                      source=_ECKER + " (PVBC -> PC, I2)", status="secondary",
                      conditions=_COND_ECKER + "; N_RRP 6; U SD 0.02, D SD 185, F SD 4.3"),
    "BiS_PYR": Pathway("BiS_PYR", "depressing", U=0.13, tau_rec=1122.0, tau_fac=9.3,
                       source=_ECKER + " (BS -> PC, I2)", status="secondary",
                       conditions=_COND_ECKER + "; U SD 0.03, D SD 156, F SD 0.7"),
    "OLM_PYR": Pathway("OLM_PYR", "depressing", U=0.3, tau_rec=1250.0, tau_fac=2.0,
                       source=_ECKER + " (SOM+ -> PC, I2)", status="secondary",
                       conditions=_COND_ECKER_CTX + "; U SD 0.08, D SD 520, F SD 4"),
}

# Kept for the record: Losonczy et al. 2002 (abstract only, mouse): ~75% of O-LM cells facilitating (3/12 also
# depressing); 8/12 basket cells depression-only; O-Bi cells 2/9 facilitating, 2/9 depressing, 5/9 combined.


@dataclass(frozen=True)
class SlowTimescale:
    name: str
    value: Optional[float] = None        # h
    low: Optional[float] = None          # h, range if given
    high: Optional[float] = None         # h
    source: str = ""
    conditions: str = ""                 # species, preparation / behavioural paradigm
    status: str = "unverified"


# Slow (cellular-consolidation) timescales. Not used by any run yet (S4).
SLOW_TIMESCALES = {
    # Edu (hippocampal neuroscientist), comment of 2026-10, relayed by the project owner. Not checked against
    # primary literature. Behavioural window, not a slice late-LTP window; the two need not coincide.
    "cellular_consolidation_window": SlowTimescale(
        "cellular_consolidation_window", value=6.0,
        source="personal communication (Edu, 2026-10)",
        conditions="behavioural, e.g. fear conditioning; window after learning in which protein-synthesis "
                   "blockade removes the memory; species, drug, dose and route not given",
        status="unverified"),
    # Late-LTP stabilization time, from the spec table (no source given there). Kept separate from persistence.
    "late_ltp_stabilization": SlowTimescale(
        "late_ltp_stabilization", low=4.0, high=8.0,
        source="spec table (hippocampal_plasticity_model.md §1), no primary source cited",
        conditions="not stated", status="unverified"),
}


@dataclass(frozen=True)
class CellTarget:
    """Intrinsic properties of one cell class, read from a source (mean, SD where given)."""
    name: str
    n: int
    r_in_mohm: tuple          # (mean, sd)
    tau_m_ms: tuple
    rheobase_pa: tuple
    source: str
    conditions: str
    status: str = "secondary"
    rmp_mv: tuple = None      # (mean, sd) resting potential, mV (negative)
    # Firing (same table). ISI: "the average time interval between spike threshold time points for the least
    # depolarized current injection level" at which the cell spiked regularly; threshold, spike amplitude and AHP from
    # the first three spikes of that sweep. grid_pa: (first level, step) of the experimental current sweeps (Appendix 1
    # table 2). Step duration not stated in the paper. Whether +- is SD is not stated.
    isi_ms: tuple = None
    grid_pa: tuple = None
    threshold_mv: tuple = None
    spike_amp_mv: tuple = None
    ahp_mv: tuple = None
    sag_mv: tuple = None


# Bezaire et al. 2016 eLife 5:e18566, Appendix 1, table 1 ("Intrinsic electrophysiological properties of experimental
# cells"), read from the PDF 2026-10-23. These are the data the CA1 model of that paper was fitted to (Soltesz lab
# whole-cell recordings, mouse; raw files on OSF). Temperature and [Ca2+]o are NOT stated in the text read: unverified.
# Firing columns read 2026-10-29 from the eLife HTML (Appendix 1 table 1 and table 2). Threshold method: pyramidal cells
# "CellData method #1", all others method #2 (dV/dt cutoff 28 mV/ms). Firing rates exist only as figures.
# The model values of that paper (Table 3: rheobase Pyr 250, PV+B 300, Bis 350, O-LM 50 pA) are model outputs, not data.
_BEZAIRE_COND = "mouse, whole-cell current clamp (Soltesz lab, unpublished or Lee et al. 2014); T and [Ca2+]o not read"
_BEZAIRE = "Bezaire et al. 2016 eLife 5:e18566, Appendix 1 table 1"
CELL_TARGETS = {
    "PYR": CellTarget("PYR", 17, (139.5, 38.8), (21.5, 8.6), (182.4, 55.7), _BEZAIRE, _BEZAIRE_COND, rmp_mv=(-70.7, 1.2),
                      isi_ms=(134.0, 44.0), grid_pa=(-400.0, 50.0), threshold_mv=(-36.7, 2.6),
                      spike_amp_mv=(78.2, 7.2), ahp_mv=(8.6, 2.1), sag_mv=(7.0, 2.2)),
    "PV": CellTarget("PV basket", 7, (65.2, 16.2), (13.3, 5.4), (307.1, 109.7), _BEZAIRE, _BEZAIRE_COND, rmp_mv=(-61.4, 2.0),
                     isi_ms=(74.2, 36.4), grid_pa=(-300.0, 50.0), threshold_mv=(-35.3, 3.7),
                     spike_amp_mv=(51.1, 9.0), ahp_mv=(18.0, 2.7), sag_mv=(1.8, 0.5)),
    "BiS": CellTarget("Bistratified", 3, (109.1, 30.5), (12.2, 0.6), (333.3, 57.7), _BEZAIRE, _BEZAIRE_COND, rmp_mv=(-63.6, 4.7),
                      isi_ms=(24.5, 21.8), grid_pa=(-300.0, 50.0), threshold_mv=(-31.9, 4.2),
                      spike_amp_mv=(47.3, 6.8), ahp_mv=(22.6, 0.7), sag_mv=(1.7, 0.6)),
    "OLM": CellTarget("O-LM", 3, (592.3, 97.0), (41.4, 11.7), (20.0, 0.0), _BEZAIRE, _BEZAIRE_COND, rmp_mv=(-64.8, 1.3),
                      isi_ms=(101.9, 30.1), grid_pa=(-100.0, 30.0), threshold_mv=(-44.2, 2.3),
                      spike_amp_mv=(76.3, 6.1), ahp_mv=(22.1, 4.7), sag_mv=(10.4, 3.8)),
}


@dataclass(frozen=True)
class ChannelParam:
    """One channel property read from a source."""
    value: float
    sd: float
    unit: str
    source: str
    conditions: str
    status: str = "unverified"


# O-LM Ih reversal. The Bezaire 2016 O-LM template never sets eh, so the published model runs its HCN at the ion default
# (0 mV); ch_HCNolm.mod declares -32.9 mV and quotes the paper below. Read from that file's comment, not from the paper.
CHANNEL_PARAMS = {
    "OLM_eh": ChannelParam(-32.9, 1.1, "mV",
                           "Maccaferri & McBain 1996 J Physiol 497:119-130, as quoted in ch_HCNolm.mod (Bezaire 2016 code)",
                           "rat CA1 stratum oriens-alveus interneurons; T and [Ca2+]o not read", status="secondary"),
}
