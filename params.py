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
