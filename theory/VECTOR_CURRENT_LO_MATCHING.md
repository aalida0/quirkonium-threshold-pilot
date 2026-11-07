# Singlet-vector current and LO partonic annihilation channels

Minimal candidate: a single stable vectorlike SU(2)L-singlet Dirac quirk Q of charge −1, fundamental SU(3)_IC and no QCD color. This is a different EW representation from the doublet in Cheung–Keung–Yuan (CKY), arXiv:0810.1524.

Normalize <0|bar Q gamma_mu Q|V>=fV*M*epsilon_mu, with fV^2=N_IC*|R(0)|^2/(pi*M). The pure-photon leptonic width is Gamma_ee=4*N_IC*alphaEM^2*Q_Q^2*|R(0)|^2/(3*M^2), checked against CKY Eq.(7). A second left/right chiral current representation reproduces the coherent photon+Z vector/axial result for light fermions.

LO partonic channels included: 12 SM fermion-antifermion pairs (e, mu, tau, 3 neutrinos, 6 quarks), WW (s-channel gamma/Z with no t-channel quirk), Zh (Z* and SM ZZh coupling), 3 infragluons, gamma+2 infragluons, Z+2 infragluons. The massive-Z three-body integral reproduces its massless analytic limit I(0)=pi^2−9. CKY source formulas: Eqs.(7),(13–18), Appendix A. The WW and Zh absolute normalizations still need independent amplitude-generator checks.

With frozen Cornwall-model 1S inputs, M=2mQ+E1S rather than 2mQ, alphaEM=1/128 and sin^2(thetaW)=0.23122:

| Diagnostic spectrum | Gamma_ee [keV] | LO accounted partonic sum [keV] | Gamma_mumu / sum |
|---|---:|---:|---:|
| Table III mQ100, sigma=.18 | 6.733 | **56.680** | 0.118788 |
| Table V mQ500, sigma=.18 | 15.072 | **129.417** | 0.116462 |
| Table VI mQ500, sigma=18 | 52.369 | **478.416** | 0.109464 |

These controls have NOT passed collider viability checks. The fractions are within an explicitly limited LO partonic sum, NOT physical branching ratios. The physical total width is **UNKNOWN** pending current hard matching, higher-order corrections, radiative/hidden glueball channels, omitted loop modes, possible additional interactions and model-exclusion review. Excited states require radiative transition widths.

Reproduce with: python3 scripts/run_vector_widths.py (writes benchmarks/partonic_vector_widths.json). No Green-function line shape, ISR, beam convolution, or mass scan has been performed.
