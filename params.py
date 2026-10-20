"""Per-pathway synaptic parameters, with the source and status of every value.

status:
  "unverified"  value or class has no checked source yet (value is None until it has one)
  "abstract"    class taken from a paper's abstract only; numbers not yet read
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


# Losonczy, Zhang, Shigemoto, Somogyi & Nusser (2002) J Physiol 542:193-210 (DOI 10.1113/jphysiol.2002.020024).
# Abstract only so far (mouse hippocampal interneurons): ~75% of O-LM cells facilitating (3/12 also
# depressing); 8/12 basket cells depression-only; O-Bi cells 2/9 facilitating, 2/9 depressing, 5/9 combined.
# Full text could not be fetched (network policy), so afferent, conditions and fitted numbers are NOT read yet.
_LOSONCZY = "Losonczy et al. 2002 J Physiol 542:193 (abstract only)"

PATHWAYS = {
    "SC_PYR": Pathway("SC_PYR", "unspecified", source="none yet",
                      conditions="to be read: Schaffer collateral -> CA1 pyramidal"),
    "SC_PV": Pathway("SC_PV", "depressing", source=_LOSONCZY,
                     conditions="basket cells; stimulated afferent not verified", status="abstract"),
    "SC_BiS": Pathway("SC_BiS", "mixed", source=_LOSONCZY,
                      conditions="O-Bi cells (nearest class to bistratified); afferent not verified",
                      status="abstract"),
    "PYR_PV": Pathway("PYR_PV", "depressing", source=_LOSONCZY,
                      conditions="basket cells; stimulated afferent not verified", status="abstract"),
    "PYR_BiS": Pathway("PYR_BiS", "mixed", source=_LOSONCZY,
                       conditions="O-Bi cells; afferent not verified", status="abstract"),
    "PYR_OLM": Pathway("PYR_OLM", "facilitating", source=_LOSONCZY,
                       conditions="O-LM cells, mouse; afferent not verified", status="abstract"),
}
