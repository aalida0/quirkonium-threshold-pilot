# Independent force-expectation WFO check (7 Nov 2026)

The original QQ-onia software paper (Domenech-Garret & Sanchis-Lozano, arXiv:0805.2704 Eq.(34)) uses the S-wave identity

|R_n(0)|² = m_Q * <V'(r)>.

For equal masses mu=mQ/2, V(r)=-a/r+sigma*r, <V'>=integral dr |u_n(r)|² (a/r²+sigma). The implemented method evaluates the force expectation integral by Simpson quadrature with the near-origin Coulomb sub-cell term, **without reusing the polynomial fit** that supplies `r0sq` in the finite-difference solver.

At h=0.0003 GeV^-1 the maximum relative differences between polynomial R(0) and independent force are:

| Published-control input | max relative difference |
|---|---:|
| mQ=100 GeV, alpha'=.091, sigma=.18 GeV² | 7e-6 |
| mQ=500 GeV, alpha'=.073, sigma=.18 GeV² | 1.06e-4 |
| mQ=500 GeV, alpha'=.102, sigma=18 GeV² | 2.32e-4 |

The 2S WFO/(2mQ)² for Table V approaches about 0.0081986 GeV, versus printed 0.0063 GeV. For Table VI it approaches 0.06962 GeV, versus 0.048 GeV. Thus the old high-mass *published* WFO discrepancy does not arise from our R(0) extrapolation. This is an independent numerical-method check only. The original QQ-onia full 2012 parameter cards and PAW code still have **not** been executed.

A new tested module is `src/force_wfo.py`, with `tests/test_force_wfo.py`. This does not validate any collider width or bound-state production rate.
