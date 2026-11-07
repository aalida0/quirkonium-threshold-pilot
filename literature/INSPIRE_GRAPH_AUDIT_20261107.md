# INSPIRE two-hop audit — actual uploaded results (7 November 2026)

**Evidence:** User-provided `inspire_audit_results.tar.gz`, parsed and independently counted. The collector finished, but scientific completeness remains PARTIAL. All conclusions are conditional on the archive as provided.

## Verified quantitative coverage

| Field | Value |
|---|---:|
| Original seeds | 5 |
| First-hop papers | 382 |
| Second-hop records | 77,838 |
| Total unique graph nodes | **78,225** |
| Metadata-resolved nodes | **60,519** |
| Metadata-missing nodes | **17,706** |
| Directed edges | **152,128** |
| Unlinked references | **4,625** |
| Unique parents of unlinked references | **272** |
| Failed API citation queries | **1** |
| Seed authors searched | 12 |
| Author-paper records (nonunique across coauthors) | **2,186** |
| Distinct records across author paper lists | **2,048** |

**The sole API error** was `refersto:recid:1293923` at page 101, HTTP 400. This is the **MG5_aMC@NLO** methods paper arXiv:1405.0301 with about 10,980 citing records, which hits INSPIRE's official 10,000-result-per-search limitation. A date-partitioned targeted overlay repair is in `scripts/repair_inspire_overflow.py`. It has NOT been run live and must not be called a successful graph repair. Source: [INSPIRE REST API documentation](https://github.com/inspirehep/rest-api-doc).

**Unlinked bibliography entries:** 1,162 belong to the 2024 Review of Particle Physics; 567 to the FCC 2025 feasibility volume 1; 336 to its volume 2. These three account for 2,065/4,625. Unlinked references are not missing HTTP requests and do not imply that all 4,625 represent relevant literature.

**Known author-census failure:** INSPIRE author ID 2458026 for J.L. Domenech-Garret reports one associated paper (arXiv:1112.4629), despite the same researcher coauthoring *QQ-onia package* arXiv:0805.2704 (INSPIRE record 786131), which **is** in the graph. Hence the collector's `author_census_complete=true` is NOT a verified exhaustive bibliography. Other author searches returned 2,185 records combined; the 12 lists contain 2,048 unique publications. Inspect the alternate author identifier on the 2008 paper before declaring this gate closed.

## What the novelty audit actually found

| Paper | Prior contribution | Material relevance |
|---|---|---|
| [Domenech-Garret, arXiv:1112.4629](https://arxiv.org/abs/1112.4629) | Heavy quirkonium potential spectra, wavefunctions at origin, leptonic decays; mentions LHC/ILC collider prospects | DIRECT; quirkonium spectroscopy is already done |
| [Cheung–Keung–Yuan, arXiv:0810.1524](https://arxiv.org/abs/0810.1524) | iQuarkonium photon/Z and hidden-boson annihilation widths; vectorlike **SU(2) doublet** | DIRECT for decay methodology; singlet quirk charges differ |
| [Domenech-Garret & Sanchis-Lozano, arXiv:0805.2704](https://arxiv.org/abs/0805.2704) | QQ-onia code, Numerov levels, independent force identity for S-wave WFO, `|R(0)|²=mQ*<V'(r)>` | DIRECT for validating high-mass spectrum discrepancies |
| [Hochberg–Kuflik–Murayama, arXiv:1512.07917](https://arxiv.org/abs/1512.07917) | *SIMP Spectroscopy* (JHEP 2016): confining vector resonances, `Im Pi` correlator, e+e− mono-photon spectrum, possible visible lepton pairs | HIGH: destroys broad claim of first dark spectroscopy at lepton colliders |
| [Hochberg–Kuflik–Murayama, arXiv:1706.05008](https://arxiv.org/abs/1706.05008) | *Dark Spectroscopy at Lepton Colliders* (PRD 2018): resonance structures, mono-photon recoil, energy-smearing/peak visibility | HIGH: close lepton collider observable precedent |
| [Fok–Kribs, arXiv:1106.3101](https://arxiv.org/abs/1106.3101) | Chiral quirkonium decays | DIFFERENT quirk model; method overlap |
| [Bai–Chen–Yang, arXiv:2506.14552](https://arxiv.org/abs/2506.14552) | Toponium vector states, e+e− current and resonance-continuum interference | HIGH: interference method is not itself new |
| [Tang–Fast–Rapp, arXiv:2607.14554](https://arxiv.org/abs/2607.14554) | Cornell potential T matrix and complex-energy top threshold poles | HIGH methodological overlap |
| [FASER, arXiv:2607.26195](https://arxiv.org/abs/2607.26195) | Actual quirk exclusions in very low IC tension region | Model-viability context, not an identical threshold scan |

Primary-source distinction: 2016 SIMP and 2018 Dark Spectroscopy emphasize light hidden-vector sectors and mono-photon (often invisible) final states, **not** our exact heavy stable `SU(2)L`-singlet `Q=-1`, `SU(3)IC` quirk and exclusive `e+e−→μ+μ−` coherent visible line shape. But their vector-current spectral machinery and resonance spectroscopy **do** overlap substantially.

**NO-GO:** presenting basic dark spectroscopy at e+e− colliders, or quirkonium level calculations plus established width formulas, as novel.

**Only potential narrow contribution (UNKNOWN, not yet computed):** a quantitatively new observable sensitive to heavy-quirk IC string tension after exact physical vector width, coherent gamma/Z matching, viable machine-energy benchmark, mass/width nuisance profiling and eventual realistic energy smearing. A model-label change is insufficient.

## Scientific and technical gates

1. Resolve why Table V of arXiv:1112.4629 states Delta(2S−1S)=0.850 GeV, less than its own stated *pure Coulomb* analytic Delta=0.88817 GeV at mQ=500, alpha'_IC=.073. The converged Cornell calculation gives ~0.92015 GeV. Reproduce original QQ-onia input cards; do NOT tune for table agreement.
2. Independently check singlet WW and Zh amplitudes and hard current matching; existing 56.680/129.417/478.416 keV results are **LO partonic accounted sums**, NOT defensible physical total widths.
3. Independently establish one viable heavy-quark benchmark accessible at its collider; mQ=500 GeV is NOT available at a 240/365 GeV FCC-ee machine.
4. A coherent visible resonance signal must survive profiling of threshold mass, Coulomb coupling, potential offset, unmeasured hidden widths and energy-resolution effects.
5. Only then proceed to an ISR/beam-smeared line-shape and a limited physics result. Do not initiate an arbitrary mass scan or discovery claim.

## Release verdict

**Graph coverage PARTIAL. Author bibliography completeness FAIL (one demonstrated omission). Broad novelty FAIL. Specific heavy singlet visible line shape novelty NOT CERTIFIED. Physical collider signal NOT CALCULATED.**

A full local archive-derived report with 297 heuristic title-ranked candidates (rankings are triage, not peer-reviewed novelty judgments) and 272 parent-reference counts was produced separately. The incomplete 17,706 metadata-only nodes mean title-ranking cannot exhaust the graph.
