# Quirkonium threshold spectroscopy — physically gated pilot

**Research status (7 November 2026): active numerical and literature feasibility work; NOT cleared for a collider line-shape, parameter scan or manuscript.**

This is a detector-simulation-free study of a neutral vector bound state of one vectorlike SU(2)L-singlet, electrically charged Dirac quirk in SU(3)_IC. The core scientific question is whether a properly normalized and machine-smeared e+e− to mu+mu− excitation curve contains confinement information beyond previous spectroscopy and top-threshold methods.

## Immediate results

- Analytic Coulomb and independent Cornell finite-difference/Numerov solver tests: PASS.
- Published Domenech-Garret 2012 mass splitting comparison: mQ100 0.375 vs ours 0.37716 GeV; mQ500 (sigma .18) 0.850 vs ours 0.92015; mQ500 (sigma 18) 2.980 vs ours 3.19765.
- **New insight:** published mQ500 (alpha'=0.073) Table V Delta21=0.850 GeV is **below the 0.88817 GeV analytic pure-Coulomb limit** for its stated alpha and mQ. This suggests a published input/convention/software mismatch. The original QQ-onia software archive has been located, but not run.
- Implemented coherent photon+Z SM fermion channels and the explicit LO partonic vector width sum including WW, Zh, 3 infragluons, gamma+2 infragluons and Z+2 infragluons; all are **conditional on the frozen singlet model**. Accounted LO sums at three diagnostic controls: 56.680, 129.417, 478.416 keV. **Physical total widths and BRs remain UNKNOWN** pending external amplitude matching and missing theoretical effects.
- INSPIRE full two-hop citation network and all seed-author publications: **NOT DONE** because the execution environment cannot resolve inspirehep.net. Run the cached, paginated scripts/inspire_two_hop.py on an internet-connected host; instructions in literature/INSPIRE_LOCAL_RUN.md.
- **19 tests passed in the local full package**; the GitHub subset includes spectroscopy, LO-width and INSPIRE parsing tests. All results are diagnostic; no physical model viability, collider sensitivity, or novelty certification has been established.

## Reproduction

    python3 -m pip install -r requirements.txt
    python3 -m pytest -q
    python3 run_pilot.py
    python3 scripts/run_vector_widths.py

For INSPIRE on a locally networked machine:

    python3 scripts/inspire_two_hop.py --second-hop all --hydrate-all --output output/inspire_audit_20261107

See PILOT_DECISION.md, validation/HIGH_MASS_DIAGNOSTIC.md, theory/VECTOR_CURRENT_LO_MATCHING.md and literature/INSPIRE_LOCAL_RUN.md.

No detector simulation, ISR, beam-energy convolution, mass scan, discovery reach, exclusion limits or manuscript is included.
