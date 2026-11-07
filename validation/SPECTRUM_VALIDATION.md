# External/independent validation (2026-11-07)
Original reference: J.L. Domenech-Garret, arXiv:1112.4629, Eq.(4) and Tables III, V, VI.
Two independent methods implemented: finite-difference symmetric tridiagonal matrix eigensolver and Numerov shooting with Coulomb cusp. Agreement between these is independent numerical confirmation, not proof that the potential matches publication conventions.
| Control | Published Δ21 [GeV] | Ours [GeV] | Relative disagreement | Published WFO 1S [GeV] | Ours 1S [GeV] | Published WFO 2S [GeV] | Ours 2S [GeV] |
|---|---:|---:|---:|---:|---:|---:|---:|
| Table III m100 | .375 | .377153 | +0.57% | .025 | .0248075 | .0059 | .0061233 |
| Table V m500 | .850 | .920097 | **+8.25%** | .058 | .0581617 | .0063 | .0081988 |
| Table VI m500 | 2.980 | 3.197387 | **+7.29%** | .187 | .201918 | .048 | .0696345 |
Here WFO=|R_nS(0)|²/M², M≈2m_Q; unit GeV. Paper Δ31: III 0.533 vs ours 0.535536; V 1.054 vs ours 1.131124; VI 4.640 vs ours 4.898290 GeV.
Numerov/FD maximum eigenvalue differences: III 9.13e−6 GeV; V 1.04e−4 GeV; VI 5.28e−4 GeV. The heavy published benchmarks disagree, especially 2S WFO (~30% and ~45%). Do not tune parameters to hide mismatch. Need original source-input convention and WFO extraction checks.
Analytic pure Coulomb test verifies E_n=−mu a²/(2n²) and |R_n(0)|²=4(mu a)³/n³. Seven tests passed. Initial Coulomb 3S WFO test failed due to small radial box; increased rmax to 9 GeV^-1 and retested. Hardware/versions for original run: Python 3.13; NumPy 2.3.5, SciPy 1.17.0, Matplotlib 3.10.8, pytest 9.0.2.
