# Pilot results: only spectrum diagnostics
Seven tests PASS. Cornell finite-difference and independent Numerov agree on eigenenergies (see validation/SPECTRUM_VALIDATION.md). Benchmark III mQ=100 GeV: computed Δ21=0.377153 GeV vs published 0.375 GeV; benchmark V mQ=500 GeV: 0.920097 vs 0.850; benchmark VI mQ=500 GeV: 3.197387 vs 2.980. Heavy WFO 2S mismatches reach ~30%/45% and remain unresolved.
Selected photon-only, LO Table V control partial widths: Γ_ee^(gamma)=14.1996 keV, Γ_3gIC=3.09281 keV, Γ_gamma2gIC=2.38316 keV using alphaEM=1/128, alphaIC=.073 and M≈2mQ. These are neither full physical Γ_total nor BRs.
Code: src/spectrum.py, src/shooting.py, src/widths.py; tests/test_spectrum.py; run_pilot.py writes benchmarks/numerical_results.json and two spectrum *diagnostic* PNGs.
No complete two-hop INSPIRE citation graph; physical model constraints unknown; no matched Green function, real Γ_total, coherent muon amplitude, ISR, beam convolution, sensitivity, or exclusion. No detector simulation.
Status: numerical code PASS (7/7); published spectrum PARTIAL; novelty/physical viability/current matching UNKNOWN and therefore STOP. Use PILOT_DECISION.md for research decision.
