## 7 November 20:53 log diagnosis and API payload fix

The supplied user log showed 382 depth-one candidates after the five seeds. It reached only 17/382 by 20:53 with about 13,818 discovered graph nodes and 15,322 citation edges. Record 296528 had 2,354 citing papers; its page 24 failed repeatedly with JSON decoding errors after decoding 56–88 MB of payload. The environment also intermittently failed to resolve inspirehep.net, and its current 12-per-5.2s rate limit was NOT the throughput bottleneck.

**Root cause addressed:** generic `/api/literature` citation searches previously downloaded full metadata for up to 100 papers each—including thousands of authors of large collaborations. They now request only `control_number,titles,arxiv_eprints,dois,earliest_date,citation_count`, omitting large author and affiliation arrays; the separate canonical author census explicitly opts in to `authors.record`. This is supported by INSPIRE's `fields` search parameter. Pagination preserves the projection, and the URL-hash cache keeps the old and slim query representations separate. No existing cached pages need deleting.

The API preflight now also tests a three-record filtered citing query for problematic recid 296528. Run it first after pulling the fix.

**Important:** a literally unbounded two-hop graph through generic high-citation papers is extremely broad and can collect tens of thousands of mostly irrelevant HEP records. The complete crawl may still be expensive; do not assume that having a larger citation graph certifies novelty. In particular `--hydrate-all` individually looks up every referenced record not already seen in search results. For a first scientifically useful analysis, a separately labeled `--second-hop relevant` run is available, but it is **not** a full all-papers two-hop graph. Neither mode can be declared complete while page failures and unmatched INSPIRE reference links remain.

The run previously reported 96 `errors` by depth 1 paper 17. Many were unlinked bibliographic references, and the saved count alone does not distinguish them from transport failures. The updated collector logs per-paper API failures as `INCOMPLETE` and keeps them in `coverage.json`, rather than silently treating them as successful.

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
