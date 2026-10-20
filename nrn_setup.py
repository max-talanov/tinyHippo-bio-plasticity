"""Compile (if needed) and load the NMODL mechanisms in mod/."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MOD_DIR = ROOT / "mod"
_ARCHS = ("x86_64", "arm64", "aarch64")


def _find_lib():
    for arch in _ARCHS:
        for sub in ("", ".libs"):
            lib = MOD_DIR / arch / sub / "libnrnmech.so"
            if lib.exists():
                return lib
    return None


def load_mechanisms():
    """Run nrnivmodl on mod/ when the build is missing or older than a .mod file, then load it."""
    from neuron import h

    lib = _find_lib()
    newest_mod = max(p.stat().st_mtime for p in MOD_DIR.glob("*.mod"))
    if lib is None or lib.stat().st_mtime < newest_mod:
        nrnivmodl = Path(sys.executable).parent / "nrnivmodl"
        subprocess.run([str(nrnivmodl) if nrnivmodl.exists() else "nrnivmodl"],
                       cwd=MOD_DIR, check=True, capture_output=True)
        lib = _find_lib()
    if lib is None or not h.nrn_load_dll(str(lib)):
        raise RuntimeError(f"could not load NMODL library from {MOD_DIR}")
    return h
