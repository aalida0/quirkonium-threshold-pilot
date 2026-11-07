# Quirkonium threshold pilot — gated scientific feasibility study

**Status 7 November 2026: spectrum diagnostic; NO-GO for a physical collider line-shape or publication claim on present evidence.**

This project tests the potential-model prerequisites to a future electron–positron vector quirkonium threshold calculation, without detector simulation. The prior art contains quirkonium spectroscopy, electroweak widths, and established top-threshold Green-function/interference techniques. No novelty claim is made.

## Run
```sh
python -m pip install -r requirements.txt
python -m pytest -q tests/test_spectrum.py
python run_pilot.py
```

Numerical reference: Domenech-Garret [arXiv:1112.4629](https://arxiv.org/abs/1112.4629), Tables III, V, VI. For the 100 GeV benchmark, computed Δ(2S−1S)=0.377153 GeV against published 0.375 GeV. At 500 GeV, 0.920097 versus 0.850 GeV (unresolved 8.25% mismatch). Independent Numerov agrees with the eigensolver. Seven scoped tests passed. Selected photon-only and IC widths do **not** constitute a physical total width.

All mass points are **diagnostic, not experimentally validated viable**. In particular, mQ=500 GeV is inaccessible at a √s=240–365 GeV collider. No ISR, beam convolution, Green-function cross section, interference, discovery reach or exclusion limits are provided.

See PILOT_DECISION.md, MODEL_CARD.md and validation/SPECTRUM_VALIDATION.md for status/limitations. Research prompt scope: a full citation-network and physical-current audit must pass *before* an observable line-shape computation.
