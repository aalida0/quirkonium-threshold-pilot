# INSPIRE audit ledger: not yet executed

Cutoff: 7 November 2026. Seeds:
- Domenech-Garret arXiv:1112.4629 (quirkonium spectroscopy).
- Cheung–Keung–Yuan arXiv:0810.1524 (vectorlike iquarkonium widths).
- Fok–Kribs arXiv:1106.3101 (chiral quirkonium decays).
- Cai–Cheng–Terning arXiv:0812.0843 (quirky little Higgs).
- Bai–Chen–Yang arXiv:2506.14552 (toponium threshold and interference).

**No live INSPIRE API result was obtained in this environment**: direct DNS lookup failed, so forward/backward graph, two-hop edges, author publication counts and DOI/arXiv deduplication remain UNKNOWN.

A complete, paginated and resumable **local request** has now been implemented in scripts/inspire_two_hop.py. It extracts every seed's canonical author IDs, seeks all papers of each seed author, traverses both citation directions to depth two, caches every HTTP JSON response, and exports nodes, edges, author census, topic-title triage and coverage-status records. Before declaring an audit complete, inspect coverage.json, manually reconcile unlinked records and read full texts of close matches.

Run instructions: literature/INSPIRE_LOCAL_RUN.md.

Related source **not yet compared against the exact published inputs**: J.-L. Domenech-Garret and M.-A. Sanchis-Lozano, QQ-onia package, arXiv:0805.2704, CPC 180 (2009) 768, DOI 10.1016/j.cpc.2008.11.011, numerical package archived at DOI 10.17632/zydk6xjzp8.1.

An automated author-paper search through an unrelated system earlier returned false matches for multiple authors. It is not legitimate evidence of an INSPIRE author census; canonical author record matching is mandatory.
