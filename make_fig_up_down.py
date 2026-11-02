"""Documentation figures: where upscaling and downscaling act in the Tier-B circuit, and how large they are.

1. docs/figures/circuit_up_down_sites.svg: the circuit (hand-laid schematic, no data).
2. docs/figures/circuit_up_down_scale_20Hz.svg: steady-state factors at 20 Hz per pathway, from the closed form
   (analysis.tm_pi_terms, verified against NEURON in RESULTS.md section 12): facilitation fac = log(u+/U_eff),
   depletion dep = log(x-), and on SC terminals the A1R terms phasic = log(1-I), tonic = log(1-i_tonic) with
   params.PRESYN_INHIB["SC_A1R"] (Mitchell et al. 1993, kinetics and c fitted; c is per SC volley, so applying it per
   spike assumes the SC fibres fire together). Bars are log factors, so they add up to the net.
No time compression. Deterministic: no seeds.
Usage: python make_fig_up_down.py
"""
import numpy as np

import analysis as an
import protocols as pr
from params import PATHWAYS, PRESYN_INHIB

PI = PRESYN_INHIB["SC_A1R"]
RATE = 20.0
UP, DEP, PHASIC, TONIC = "#639922", "#7F77DD", "#D85A30", "#EF9F27"
ROWS = (("SC → PYR", "SC_PYR", False), ("SC → PYR, + A1R", "SC_PYR", True),
        ("SC → PV, BiS", "SC_PV", False), ("SC → PV, BiS, + A1R", "SC_PV", True),
        ("PYR → O-LM", "PYR_OLM", False), ("PYR → PV, BiS", "PYR_PV", False),
        ("PV → PYR", "PV_PYR", False), ("BiS → PYR", "BiS_PYR", False), ("O-LM → PYR", "OLM_PYR", False))
STYLE = """<style>
.t{font:14px sans-serif;fill:#2C2C2A}.ts{font:12px sans-serif;fill:#5F5E5A}.th{font:500 14px sans-serif;fill:#2C2C2A}
.box{fill:#F8F7F3;stroke:#B4B2A9}
.c-teal>rect{fill:#E1F5EE;stroke:#0F6E56}.c-teal>.th{fill:#085041}.c-teal>.ts{fill:#0F6E56}
.c-pink>rect{fill:#FBEAF0;stroke:#993556}.c-pink>.th{fill:#72243E}.c-pink>.ts{fill:#993556}
.c-gray>rect{fill:#F1EFE8;stroke:#5F5E5A}.c-gray>.th{fill:#444441}.c-gray>.ts{fill:#5F5E5A}
</style>"""


def marker(mid, col):
    return (f'<marker id="{mid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" '
            f'orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="{col}" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round"/></marker>')


def svg(h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="680" height="{h}" viewBox="0 0 680 {h}">{STYLE}'
            f'<defs>{marker("ag", UP)}{marker("ap", DEP)}</defs><rect width="680" height="{h}" fill="#FFFFFF"/>'
            f'{body}</svg>\n')


def node(cls, x, y, w, title, sub):
    return (f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w}" height="50" rx="8" stroke-width="0.5"/>'
            f'<text class="th" x="{x + w / 2}" y="{y + 18}" text-anchor="middle" dominant-baseline="central">{title}</text>'
            f'<text class="ts" x="{x + w / 2}" y="{y + 36}" text-anchor="middle" dominant-baseline="central">{sub}</text></g>')


def arrow(d, kind):
    col, mk, dash = (UP, "ag", "") if kind == "up" else (DEP, "ap", ' stroke-dasharray="5 3"')
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.5"{dash} marker-end="url(#{mk})"/>'


def sites():
    b = ['<rect class="box" x="220" y="40" width="180" height="320" rx="16" stroke-width="0.5"/>',
         '<text class="th" x="310" y="62" text-anchor="middle" dominant-baseline="central">PYR (Bezaire, 34 °C)</text>']
    for y, t, s in ((80, "Distal tuft", "SLM"), (150, "Proximal apical", "SR"), (220, "Soma, axon", "SP"),
                    (290, "Basal", "SO")):
        b.append(node("c-teal", 240, y, 140, t, s))
    for y, t, s in ((80, "O-LM", "inhibits distal tuft"), (150, "Bistratified", "inhibits SR"),
                    (220, "PV basket", "inhibits soma")):
        b.append(node("c-pink", 470, y, 150, t, s))
    b.append(node("c-gray", 40, 80, 150, "T pathway", "300 syn, silent"))
    b.append(node("c-gray", 40, 160, 150, "Schaffer coll.", "600 SR + 300 SO"))
    b.append('<rect x="34" y="154" width="162" height="62" rx="10" fill="none" stroke="#BA7517" stroke-width="1.2" '
             'stroke-dasharray="4 3"/>')
    b += [arrow("M190 105 H210 V163 H238", "up"), arrow("M196 185 H238", "up"), arrow("M120 216 V315 H238", "up"),
          arrow("M80 216 V400 H648 V177 H622", "up"), arrow("M648 247 H622", "up"),
          arrow("M400 95 H468", "up"), arrow("M400 165 H468", "down"), arrow("M400 235 H468", "down")]
    b += [arrow(f"M470 {y} H382", "down") for y in (115, 185, 255)]
    b += [f'<line x1="40" y1="440" x2="80" y2="440" stroke="{UP}" stroke-width="1.5"/>',
          '<text class="ts" x="92" y="440" dominant-baseline="central">Facilitating: up and down both act, '
          'net up below f* (22–75 Hz)</text>',
          f'<line x1="40" y1="466" x2="80" y2="466" stroke="{DEP}" stroke-width="1.5" stroke-dasharray="5 3"/>',
          '<text class="ts" x="92" y="466" dominant-baseline="central">Depressing: depletion only (down at every rate)</text>',
          '<rect x="40" y="484" width="40" height="16" rx="4" fill="none" stroke="#BA7517" stroke-width="1.2" '
          'stroke-dasharray="4 3"/>',
          '<text class="ts" x="92" y="492" dominant-baseline="central">Presynaptic A1R inhibition of release '
          '(down #2), SC terminals only</text>',
          '<text class="ts" x="92" y="516" dominant-baseline="central">Upper arrow of each pair: PYR → interneuron; '
          'lower: interneuron → PYR</text>']
    return svg(530, "".join(b))


def factors(path, a1r):
    p = PATHWAYS[path]
    n = int(np.ceil(8 * max(p.tau_rec, p.tau_fac, PI.tau_d) * RATE / 1000.0)) + 20
    sp = np.round((10.0 + np.arange(n) * 1000.0 / RATE) / pr.DT_FIXED) * pr.DT_FIXED
    inh = dict(i_tonic=PI.i_tonic, i_max=PI.i_max, c=PI.c, tau_r=PI.tau_r, tau_d=PI.tau_d) if a1r else {}
    r = an.tm_pi_terms(sp, sp + PI.lag if a1r else [], p.U, p.tau_rec, p.tau_fac, **inh)
    return {k: float(r[k][-1]) for k in ("fac", "dep", "phasic", "tonic")}


def scale():
    x0, k, b = 390.0, 85.0, []
    b += ['<text class="ts" x="380" y="30" text-anchor="end" dominant-baseline="central">← downscaling</text>',
          '<text class="ts" x="400" y="30" dominant-baseline="central">upscaling →</text>',
          '<text class="ts" x="640" y="30" text-anchor="end" dominant-baseline="central">net</text>']
    ticks = (0.25, 0.5, 1, 2, 4)
    for f in ticks:
        x = x0 + k * np.log(f)
        if f != 1:
            b.append(f'<line x1="{x:.1f}" y1="48" x2="{x:.1f}" y2="340" stroke="#D3D1C7" stroke-width="0.5" '
                     'stroke-dasharray="2 3"/>')
        b.append(f'<text class="ts" x="{x:.1f}" y="356" text-anchor="middle" dominant-baseline="central">×{f:g}</text>')
    lo = x0
    for i, (lab, path, a1r) in enumerate(ROWS):
        y = 60 + 32 * i
        t = factors(path, a1r)
        b.append(f'<text class="ts" x="40" y="{y + 9}" dominant-baseline="central">{lab}</text>')
        b.append(f'<rect x="{x0}" y="{y}" width="{k * t["fac"]:.1f}" height="18" fill="{UP}"/>')
        left = x0
        for key, col in (("dep", DEP), ("phasic", PHASIC), ("tonic", TONIC)):
            w = -k * t[key]
            if w > 0.05:
                b.append(f'<rect x="{left - w:.1f}" y="{y}" width="{w:.1f}" height="18" fill="{col}"/>')
                left -= w
        lo = min(lo, left)
        net = sum(t.values())
        xn = x0 + k * net
        b.append(f'<line x1="{xn:.1f}" y1="{y - 4}" x2="{xn:.1f}" y2="{y + 22}" stroke="#2C2C2A" stroke-width="2"/>')
        b.append(f'<text class="ts" x="640" y="{y + 9}" text-anchor="end" dominant-baseline="central">'
                 f'×{np.exp(net):.2f}</text>')
        print(f"  {lab:22s} up x{np.exp(t['fac']):.2f}  dep x{np.exp(t['dep']):.2f}  phasic x{np.exp(t['phasic']):.2f}"
              f"  tonic x{np.exp(t['tonic']):.2f}  net x{np.exp(net):.2f}")
    assert lo > 200, "bars run into the labels; reduce k"
    b.append(f'<line x1="{x0}" y1="48" x2="{x0}" y2="340" stroke="#5F5E5A" stroke-width="1"/>')
    for x, col, lab in ((40, UP, "Facilitation"), (150, DEP, "Vesicle depletion"), (290, PHASIC, "Phasic A1R"),
                        (400, TONIC, "Tonic A1R")):
        b.append(f'<rect x="{x}" y="384" width="14" height="14" fill="{col}"/>'
                 f'<text class="ts" x="{x + 20}" y="391" dominant-baseline="central">{lab}</text>')
    b.append('<line x1="510" y1="384" x2="510" y2="398" stroke="#2C2C2A" stroke-width="2"/>'
             '<text class="ts" x="520" y="391" dominant-baseline="central">Net factor</text>')
    b.append(f'<text class="ts" x="40" y="420" dominant-baseline="central">Steady state at {RATE:g} Hz; '
             'bar length = log factor, so bars add up to the net</text>')
    return svg(440, "".join(b))


def main():
    with open("docs/figures/circuit_up_down_sites.svg", "w") as fh:
        fh.write(sites())
    print(f"steady-state factors at {RATE:g} Hz:")
    with open("docs/figures/circuit_up_down_scale_20Hz.svg", "w") as fh:
        fh.write(scale())


if __name__ == "__main__":
    main()
