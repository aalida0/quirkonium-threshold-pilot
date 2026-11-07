# Decision (7 November 2026): CONDITIONAL CONTINUATION, no paper or scan authorization

**Do not discard this project, but do not claim a publishable result or build collider sensitivity machinery yet.** The user-defined goal is a genuinely new, physically meaningful quirkonium e+e− threshold observable probing hidden confinement without detector simulation.

## What is now established

- Cornell spectrum solvers and analytic Coulomb validation pass.
- The printed Table V high-mass splitting is below the Coulomb-only value computed from its stated mass and coupling: published 0.850 vs analytic 0.88817 GeV, converged Cornell 0.92015 GeV. Input, software or convention mismatch is supported, but the reason has not been located because original QQ-onia software inputs were not run.
- A leading-order singlet vector-current implementation sums 12 SM f fbar modes, WW, Zh, three infragluons, photon+2 infragluons and Z+2 infragluons at diagnostic 1S inputs. LO partonic accounted sums: 56.680, 129.417, 478.416 keV. The physical total width and experimental BR remain UNKNOWN.
- INSPIRE authors and full two-hop citation audit are NOT completed because API calls could not be made from this execution environment. The local runner has been committed and must be run on a connected machine.
- Quirkonium potential spectroscopy and leptonic rates exist already (Domenech-Garret 2012), and quirkonium decay methods (Cheung–Keung–Yuan 2009), top Green functions and interference (Bai–Chen–Yang 2026) are established methods. Mere transplantation is not novelty.

## Priority order — stop at failed gates

1. Run scripts/inspire_two_hop.py locally, resolve incomplete citations/ambiguous author identities, read the exact equations and compare observable overlap for every close paper.
2. Inspect original QQ-onia CPC code and input card; diagnose the 500 GeV table discrepancy without retuning the physics.
3. Validate WW/Zh and full singlet vector current against an independently derived/generator amplitude; quantify alphaIC running, matching, glueballs and omitted channels and turn LO accounting into a defensible physical width.
4. Identify one experimentally and machine-energy viable benchmark (mQ500 requires sqrt(s) near 1 TeV, not FCC-ee 240/365).
5. Only after explicit PASS: compute ONE Green-function matched spectral observable; then consider ISR, realistic beam spread and parameter degeneracies.

## Referee risks

1. Novelty gap not certified; quirk spectroscopy already studied.
2. Direct vector spectral signal and physical total width not closed.
3. Published high-mass reference mismatch unaccounted and experimental viability unspecified.

**Status:** CONDITIONAL GO for gate-closing calculations; NO-GO for manuscript, mass grid, ISR/beam plots or sensitivity claims.
