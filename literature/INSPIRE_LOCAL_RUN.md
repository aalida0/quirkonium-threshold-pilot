## Live progress and rate-limiting update

INSPIRE's documented per-IP limit is **15 HTTP requests in each rolling five-second window**, with rejected HTTP 429 requests also counted. The collector defaults to the more conservative **12 requests / rolling 5.2 seconds** and imposes at least **5.3 seconds** of backoff after a 429 (or the server's longer `Retry-After` value). Every HTTP attempt, including retries, consumes a rate slot.

If an older version produces an empty log for minutes, interrupt it with `Ctrl+C`. Already saved cached JSON responses remain reusable. Update your clone and run:

```bash
git pull --ff-only
python3 -m py_compile scripts/inspire_two_hop.py
python3 -u scripts/check_inspire_api.py
python3 -u scripts/inspire_two_hop.py \
    --second-hop all --hydrate-all \
    --requests-per-window 12 --window-seconds 5.2 \
    --output output/inspire_audit_20261107 \
    2>&1 | tee inspire_audit.log
```

New logging prints immediately: START, SEED, DEPTH, per-paper progress, each REQUEST, each search PAGE with totals, HYDRATE, AUTHOR, rate-limit sleeps and 429/5xx retries. Use `tail -f inspire_audit.log` from another terminal to follow the log. The complete unfiltered two-hop crawl may include a very large number of records; its output is **not** valid until `coverage.json` is produced and checked.

## November 7 hotfix: external arXiv ID vs INSPIRE recid

The first release incorrectly did `int(record['id'])` on a response from `/api/arxiv/1112.4629`. Per the INSPIRE REST schema, `id` can be the *requested external identifier*, whereas the numeric literature record is under `metadata.control_number`. Fixed in `scripts/inspire_two_hop.py`, with a regression test and a fast preflight.

From your existing clone:

```bash
git pull --ff-only
python3 scripts/check_inspire_api.py
```

The preflight should print five `OK arXiv=... INSPIRE_recid=...` rows. Only then run the full audit:

```bash
python3 scripts/inspire_two_hop.py --second-hop all --hydrate-all --output output/inspire_audit_20261107 2>&1 | tee inspire_audit.log
```

The `uno 0.3.3 requires pytest==2.6.0` warning is a pre-existing package dependency conflict and unrelated to this ID failure. For future installations, prefer `python3 -m venv .venv`, `source .venv/bin/activate`, then `python -m pip install -r requirements.txt` rather than modifying the global environment.

# INSPIRE two-hop and seed-author publication census

The execution environment has no DNS access to inspirehep.net. **The live audit is NOT run or certified.** An offline test fixture verifies parsing and traversal logic only.

## Local run

Connectivity test:

    python3 -c "import requests; r=requests.get('https://inspirehep.net/api/arxiv/1112.4629',timeout=30); print(r.status_code,r.json().get('id'))"

Then run:

    cd ~/quirkonium-threshold-pilot
    python3 -m pip install --user requests
    python3 scripts/inspire_two_hop.py --second-hop all --hydrate-all --output output/inspire_audit_20261107 2>&1 | tee inspire_audit.log

The default seed list contains arXiv 1112.4629, 0810.1524, 1106.3101, 0812.0843, 2506.14552. The program resolves canonical author IDs from the seed records and attempts a complete bibliography search for each *seed author*, rejecting papers that do not match the canonical ID. Author-name matching without identity verification is not sufficient.

The two-hop graph is: seed papers (depth zero), all papers they cite and all papers citing them (depth one), then all references and citations of every depth-one paper (depth two). All seed authors' publication lists are recorded separately. Expanding two hops from every author publication would create a different, much larger graph and is not this audit.

Resume works because HTTP pages are cached by URL hash. The collector respects the official 15 requests per five seconds rule and paginates with links.next. The no-cap full mode can touch thousands of papers. Diagnostic options such as second-hop relevant, limit-depth1 and max-nodes invalidate any claim of completeness.

Output includes: coverage.json, seed_authors.json, author_coverage.json, authors/*.json, nodes.csv, edges.csv, topic_candidates.json, http_cache/*.json. Read coverage.json before making novelty claims. An unlinked author, missing reference record, failed API page, metadata not hydrated or undated paper means an unresolved coverage gap. Topic-filtered titles are useful for prioritization, not proof that papers were fully examined.

Share the generated outputs as a zip, optionally excluding the large HTTP cache. No sensitive author email data is exported. The actual novelty decision still requires reading close-match equations and figures.

Official documentation: https://github.com/inspirehep/rest-api-doc
