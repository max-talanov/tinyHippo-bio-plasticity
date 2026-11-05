"""Documentation figure: the Tier-B circuit as implemented in circuit.py (working tree, cells="bezaire").

Every number on the figure is read from the code: generators and synapse counts from circuit.Config, peak
conductances from circuit.G_HAT_NS, STP (U, D, F) from params.PATHWAYS via circuit.STP_OF, PYR layer section counts and
lengths from cells.build_bezaire_pyr(cells.TIER_B_PYR). Receptor kinetics, reversal potentials, NetCon delay and
threshold are the constants of circuit._syn / circuit._loop, restated here (checked by the asserts below).
Usage: python make_fig_implementation.py -> docs/figures/tier_b_implementation.svg (with the projection table) and
       docs/figures/tier_b_implementation_drawing.svg (drawing only)
"""
import inspect

import cells
import circuit as cc
from params import PATHWAYS

UP, DOWN = "#639922", "#7F77DD"
STYLE = """<style>
.ts{font:12px sans-serif;fill:#5F5E5A}.th{font:500 14px sans-serif;fill:#2C2C2A}.tb{font:500 12px sans-serif;fill:#2C2C2A}
.box{fill:#F8F7F3;stroke:#B4B2A9}
.c-teal>rect{fill:#E1F5EE;stroke:#0F6E56}.c-teal>.th{fill:#085041}.c-teal>.ts{fill:#0F6E56}
.c-pink>rect{fill:#FBEAF0;stroke:#993556}.c-pink>.th{fill:#72243E}.c-pink>.ts{fill:#993556}
.c-gray>rect{fill:#F1EFE8;stroke:#5F5E5A}.c-gray>.th{fill:#444441}.c-gray>.ts{fill:#5F5E5A}
.badge{fill:#FFFFFF;stroke:#2C2C2A;stroke-width:0.8}
</style>"""
W = 1000


def marker(mid, col):
    return (f'<marker id="{mid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" '
            f'orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="{col}" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round"/></marker>')


def node(cls, x, y, w, h, lines):
    out = [f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" stroke-width="0.5"/>']
    y0 = y + h / 2 - 9 * (len(lines) - 1)
    for i, s in enumerate(lines):
        out.append(f'<text class="{"th" if i == 0 else "ts"}" x="{x + w / 2}" y="{y0 + 18 * i}" text-anchor="middle" '
                   f'dominant-baseline="central">{s}</text>')
    return "".join(out) + "</g>"


def edge(d, stp, inhibitory=False):
    col, mk = (UP, "ag") if stp == "F" else (DOWN, "ap")
    dash = ' stroke-dasharray="6 3"' if inhibitory else ""
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.6"{dash} marker-end="url(#{mk})"/>'


def badge(x, y, n):
    return (f'<circle class="badge" cx="{x}" cy="{y}" r="9"/>'
            f'<text class="tb" x="{x}" y="{y}" text-anchor="middle" dominant-baseline="central">{n}</text>')


def stp_class(name):
    p = PATHWAYS[cc.STP_OF.get(name, name)]
    return ("F" if p.expected_class == "facilitating" else "D"), p


def main():
    c = cc.Config()
    src_syn, src_loop = inspect.getsource(cc._syn), inspect.getsource(cc.TierB._loop)
    assert "s.tau1, s.tau2 = 0.5, 8.0" in src_syn and "nc.threshold, nc.delay = 0.0, 1.0" in src_loop
    assert (cc.E_EXC, cc.E_INH) == (0.0, -80.0) and c.cells == "bezaire"
    pyr = cells.build_bezaire_pyr(cells.TIER_B_PYR)
    lay = {k: (len(pyr[k]), sum(s.L for s in pyr[k]) / 1000.0) for k in ("dist", "prox", "basal")}
    n_sc_int = c.n_sc_int
    n_sc_total = c.n_sc_prox + c.n_sc_basal + 2 * n_sc_int
    tp = cells.TIER_B_PYR

    # projections: (no, name, label, source, target, n, k, receptor)
    exc, inh = "AMPA 0.5/3 ms, 0 mV", "GABA_A 0.5/8 ms, −80 mV"
    rows = [
        (1, "T_PYR", "T → PYR", "T generator", f"SR ({lay['prox'][0]} sec)", c.n_t, 1, exc, "event time"),
        (2, "SC_PYR", "SC → PYR", "SC generator", f"SR ({lay['prox'][0]} sec)", c.n_sc_prox, 1, exc, "event time"),
        (3, "SC_PYR_basal", "SC → PYR", "SC generator", f"SO ({lay['basal'][0]} sec)", c.n_sc_basal, 1, exc,
         "event time"),
        (4, "SC_BiS", "SC → BiS", "SC generator", "apical trees", n_sc_int, 1, exc, "event time"),
        (5, "SC_PV", "SC → PV", "SC generator", "apical trees", n_sc_int, 1, exc, "event time"),
        (6, "PYR_OLM", "PYR → O-LM", "PYR soma", "O-LM soma", 1, c.k_pyr_int, exc, "1 ms"),
        (7, "PYR_BiS", "PYR → BiS", "PYR soma", "BiS soma", 1, c.k_pyr_int, exc, "1 ms"),
        (8, "PYR_PV", "PYR → PV", "PYR soma", "PV soma", 1, c.k_pyr_int, exc, "1 ms"),
        (9, "OLM_PYR", "O-LM → PYR", "O-LM soma", f"SLM ({lay['dist'][0]} sec)", 1, c.k_int_pyr, inh, "1 ms"),
        (10, "BiS_PYR", "BiS → PYR", "BiS soma", f"SR ({lay['prox'][0]} sec)", 1, c.k_int_pyr, inh, "1 ms"),
        (11, "PV_PYR", "PV → PYR", "PV soma", "PYR soma", 1, c.k_int_pyr, inh, "1 ms"),
    ]
    S = {r[0]: stp_class(r[1])[0] for r in rows}
    b = []
    # generators
    b.append(node("c-gray", 30, 140, 210, 90, ["T generator", f"{c.n_t} Poisson trains", "1 per synapse",
                                               f"rate_t = {c.rate_t:g} Hz (off)"]))
    b.append(node("c-gray", 30, 290, 210, 110, ["SC generator (CA3)", f"{n_sc_total} Poisson trains",
                                                "1 per synapse", f"{c.rate_bg:g} Hz background",
                                                f"{c.rate_volley:g} Hz in {c.t_volley[0]:g}–{c.t_volley[1]:g} ms"]))
    # PYR
    b.append('<rect class="box" x="320" y="50" width="280" height="500" rx="16" stroke-width="0.5"/>')
    b.append('<text class="th" x="460" y="74" text-anchor="middle" dominant-baseline="central">PYR: Bezaire poolosyncell</text>')
    b.append('<text class="ts" x="460" y="94" text-anchor="middle" dominant-baseline="central">202 sections, 34 °C, refit</text>')
    b.append(node("c-teal", 350, 110, 220, 64, ["Apical dist (SLM)", f"{lay['dist'][0]} sec, {lay['dist'][1]:.1f} mm"]))
    b.append(node("c-teal", 350, 210, 220, 64, ["Apical prox (SR)", f"{lay['prox'][0]} sec, {lay['prox'][1]:.1f} mm"]))
    b.append(node("c-teal", 350, 310, 220, 64, ["Soma + axon (SP)", "Na, Kdr, KA, HCN, leak"]))
    b.append(node("c-teal", 350, 410, 220, 64, ["Basal (SO)", f"{lay['basal'][0]} sec, {lay['basal'][1]:.1f} mm"]))
    b.append(f'<text class="ts" x="460" y="500" text-anchor="middle" dominant-baseline="central">scales: leak {tp.leak_scale:.2f}, '
             f'Na {tp.na_scale:.2f}, Kdr {tp.k_scale:.2f}</text>')
    b.append(f'<text class="ts" x="460" y="520" text-anchor="middle" dominant-baseline="central">HCN {tp.h_scale:.2f}, '
             f'KA {tp.ka_scale:.2f}, e_pas {tp.e_pas:.1f} mV</text>')
    # interneurons
    b.append(node("c-pink", 720, 110, 240, 64, ["O-LM (published)", "soma, 2 dend, axon; eh −32.9"]))
    b.append(node("c-pink", 720, 210, 240, 64, ["Bistratified (refit)", "soma, 2 apical + 2 basal trees"]))
    b.append(node("c-pink", 720, 310, 240, 64, ["PV basket (published)", "soma, 2 apical + 2 basal trees"]))
    # generator edges
    b += [edge("M240 170 H285 V232 H348", S[1]), badge(285, 200, 1),
          edge("M240 320 H300 V252 H348", S[2]), badge(300, 290, 2),
          edge("M240 370 H300 V442 H348", S[3]), badge(300, 410, 3),
          edge("M80 400 V590 H985 V242 H962", S[4]), edge("M985 342 H962", S[5]),
          badge(985, 290, 4), badge(985, 400, 5)]
    # PYR <-> interneuron pairs
    for (y_out, y_in), (n_out, n_in) in zip(((130, 156), (230, 256), (330, 356)), ((6, 9), (7, 10), (8, 11))):
        b += [edge(f"M600 {y_out} H718", S[n_out]), badge(660, y_out, n_out),
              edge(f"M720 {y_in} H572", S[n_in], inhibitory=True), badge(660, y_in, n_in)]
    # legend
    b += [f'<line x1="40" y1="622" x2="80" y2="622" stroke="{UP}" stroke-width="1.6"/>',
          '<text class="ts" x="88" y="622" dominant-baseline="central">facilitating STP</text>',
          f'<line x1="220" y1="622" x2="260" y2="622" stroke="{DOWN}" stroke-width="1.6"/>',
          '<text class="ts" x="268" y="622" dominant-baseline="central">depressing STP</text>',
          '<line x1="400" y1="622" x2="440" y2="622" stroke="#5F5E5A" stroke-width="1.6"/>',
          '<text class="ts" x="448" y="622" dominant-baseline="central">excitatory (AMPA)</text>',
          '<line x1="590" y1="622" x2="630" y2="622" stroke="#5F5E5A" stroke-width="1.6" stroke-dasharray="6 3"/>',
          '<text class="ts" x="638" y="622" dominant-baseline="central">inhibitory (GABA_A)</text>',
          badge(800, 622, "n"), '<text class="ts" x="816" y="622" dominant-baseline="central">projection, table</text>']
    write("docs/figures/tier_b_implementation_drawing.svg", b, 646)
    # table
    cols = (40, 70, 175, 290, 410, 545, 715, 800)
    heads = ("#", "projection", "source", "target", "synapses × ĝ", "receptor", "delay", "STP: class U / D / F (ms)")
    y = 660
    b.append(f'<line x1="40" y1="{y + 12}" x2="{W - 20}" y2="{y + 12}" stroke="#B4B2A9" stroke-width="0.5"/>')
    for x, s in zip(cols, heads):
        b.append(f'<text class="tb" x="{x}" y="{y}" dominant-baseline="central">{s}</text>')
    for no, name, lab, src, tgt, n, k, rec, dl in rows:
        y += 22
        cls, p = stp_class(name)
        g = cc.G_HAT_NS["SC_PYR" if name == "SC_PYR_basal" else name]
        syn = f"{n} × {g:g} nS" if k == 1 else f"1 × {k:g}·{g:g} = {k * g:g} nS"
        cells_ = (str(no), lab, src, tgt, syn, rec, dl,
                  f"{cls}  {p.U:g} / {p.tau_rec:g} / {p.tau_fac:g}" + ("  (as SC)" if name == "T_PYR" else ""))
        for x, s in zip(cols, cells_):
            b.append(f'<text class="ts" x="{x}" y="{y}" dominant-baseline="central">{s}</text>')
    notes = ["SC and T: every synapse is a TMSyn with its own resource pool and its own Poisson train; "
             "events are delivered at their times (NetCon.event).",
             "PYR ↔ interneuron (6–11; 6–8 leave from the PYR soma): one TMSyn per projection, weight K·ĝ (K = "
             f"{c.k_pyr_int:g} out of PYR, {c.k_int_pyr:g} into PYR)",
             "standing in for a population; spike detection at the presynaptic soma(0.5), threshold 0 mV.",
             "ĝ: Ecker et al. 2019 Table 1 (PYR ↔ interneuron); SC and T ĝ assumed. STP: params.PATHWAYS "
             "(secondary sources). Fixed step 0.025 ms after 20 s rest at dt 10 ms.",
             "Not in the circuit yet: NMDA, presynaptic A1R (mod/TMSynPI, verified alone), tag and capture. "
             "Synapse placement on PYR layers waits on circuit._place."]
    y += 30
    for s in notes:
        b.append(f'<text class="ts" x="40" y="{y}" dominant-baseline="central">{s}</text>')
        y += 18
    write("docs/figures/tier_b_implementation.svg", b, int(y + 12))


def write(path, body, hgt):
    out = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{hgt}" viewBox="0 0 {W} {hgt}">{STYLE}'
           f'<defs>{marker("ag", UP)}{marker("ap", DOWN)}</defs><rect width="{W}" height="{hgt}" fill="#FFFFFF"/>'
           + "".join(body) + "</svg>\n")
    with open(path, "w") as fh:
        fh.write(out)
    print("wrote", path, W, "x", hgt)


if __name__ == "__main__":
    main()
