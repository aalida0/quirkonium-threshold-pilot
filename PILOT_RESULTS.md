# Results ledger — 7 November 2026

## Spectrum and independent numerical checks

mQ=100 GeV, alpha'=0.091, sigma=0.18 GeV^2: published Delta21=0.375 GeV, ours 0.37716.
mQ=500 GeV, alpha'=0.073, sigma=0.18: published 0.850, ours 0.92015.
mQ=500 GeV, alpha'=0.102, sigma=18: published 2.980, ours 3.19765.
Published Table V 0.850 is below analytic pure Coulomb Delta21=0.8881667 using the printed inputs. Local independent finite-difference and Numerov solvers agree. Original QQ-onia PAW code identified, not executed; exact source-card provenance UNKNOWN. See validation/HIGH_MASS_DIAGNOSTIC.md.

## Electroweak and hidden-channel LO vector width

Consistent with one **singlet** Q~(1,1,-1;3_IC), rather than CKY's SU(2) doublet, code now includes tree coherent gamma/Z to 12 SM fermion flavors, WW s-channel, Zh, 3gIC, gamma2gIC, Z2gIC. Photon vector-current prefactor and chiral-current decomposition checked. Z2gIC massive phase space has the correct I(0)=pi^2−9 analytic limit.

At diagnostic control 1S wavefunctions M=2mQ+E1, LO partonic accounted sums are 56.680, 129.417, 478.416 keV for Tables III/V/VI respectively; respective ee partial rates 6.733, 15.072, 52.369 keV. These are **not physical total widths**: hard-current matching, NLO corrections, hidden hadronization, missing loop channels, external WW/Zh normalization and model viability unresolved. See theory/VECTOR_CURRENT_LO_MATCHING.md and scripts/run_vector_widths.py.

## Test evidence

The complete local package was executed and passed 19 tests (7 spectrum, 8 vector, 4 offline INSPIRE parser/graph tests). GitHub includes a slightly leaner test subset; do not label its tests as independently executed in this tool environment.

## Citation graph

Live INSPIRE is unreachable in model execution environment: *zero canonical API graph results collected*. The reproducible, cached and paginated local runner lives at scripts/inspire_two_hop.py; see literature/INSPIRE_LOCAL_RUN.md. A complete novel-observable audit must wait for returned source records and close full-text review.

Status: numerical spectrum PASS, published exact replication PARTIAL, leading photon/fermion current checked, LO channel sum provisional, physical width UNKNOWN, citation audit UNKNOWN, observable line shape NOT RUN, novelty UNKNOWN. This is a conditional feasibility investigation, NOT paper readiness.
