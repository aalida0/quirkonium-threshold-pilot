# Published Cornell spectrum mismatch

Source: J.L. Domenech-Garret, arXiv:1112.4629 (2012), Eq.(4) and Tables III/V/VI. The quoted Table V benchmark uses mQ=500 GeV, N_IC=3, alpha'_IC=0.073 and sigma=0.18 GeV^2. The Coulomb coefficient is a=(4/3)alpha' and reduced mass mu=mQ/2.

For sigma=0, analytic Coulomb Δ(2S−1S)=3mu*a^2/8 = **0.888166667 GeV**. The published Table V value is **0.850 GeV**. At the published positive sigma our converged numerical value is **0.92015 GeV**, in agreement across two different solvers.

| sigma [GeV^2] | calculated Δ21 [GeV] | <r>2−<r>1 [GeV^-1] |
|---:|---:|---:|
| 0 | 0.888152 | 0.184932 |
| 0.045 | 0.896384 | 0.181021 |
| 0.090 | 0.904450 | 0.177505 |
| 0.180 | 0.920141 | 0.171376 |

The Hellmann–Feynman identity dΔ21/dsigma = <r>2−<r>1 is positive along these tested points. The published 0.850 GeV cannot be recovered by increasing positive confinement while retaining the stated alpha. This is evidence of an input, convention or software inconsistency, **not proof the paper has a typo**.

Pure Coulomb 1S WFO/(2mQ)^2 is 0.057632 GeV, close to the printed 0.058, while pure Coulomb 2S WFO is 0.007204 versus the printed 0.0063 and numerical confining 0.008199. For Table VI (alpha'=0.102, sigma=18), printed Δ21=2.980 GeV versus numerical ~3.19767 GeV. Table VI does not have the below-Coulomb inconsistency (Coulomb limit 1.734 GeV).

**Next decisive check:** inspect and run original QQ-onia code and its exact 2012 input cards (PAW, unit conversion fm to GeV^-1, string tension, quirk mass, radial boundary and normalization). Source identified: Domenech-Garret and Sanchis-Lozano, Comput. Phys. Commun. 180 (2009) 768–778, DOI 10.1016/j.cpc.2008.11.011, CPC dataset DOI 10.17632/zydk6xjzp8.1. Original code has NOT been run here. Do not retune alpha to fit.
