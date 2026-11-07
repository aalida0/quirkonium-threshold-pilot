#!/usr/bin/env python3
"""Quick preflight: verify INSPIRE resolves all arXiv seeds to numeric literature IDs."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from inspire_two_hop import API, SEEDS, canonical_literature_id

def main():
    cache = Path("output/inspire_audit_20261107/http_cache")
    api = API(cache)
    failed = False
    for arxiv in SEEDS:
        try:
            r = api.get("/api/arxiv/" + arxiv)
            cid = canonical_literature_id(r)
            declared = ((r.get("metadata") or {}).get("arxiv_eprints") or [{}])[0].get("value")
            print(f"OK arXiv={arxiv} INSPIRE_recid={cid} metadata_arxiv={declared}")
        except Exception as e:
            failed = True
            print(f"ERROR arXiv={arxiv}: {e}", file=sys.stderr)
    # Exercise the actual projected citation-search response (without
    # traversing a full citation graph), including the problematic recid.
    if not failed:
        try:
            from urllib.parse import urlencode
            fields='control_number,titles,arxiv_eprints,dois,earliest_date,citation_count'
            probe=api.get('/api/literature', {
                'q':'refersto:recid:296528','size':3,'page':1,'fields':fields
            })
            rows=probe.get('hits',{}).get('hits',[])
            if not rows:
                raise ValueError('INSPIRE returned zero citation records for smoke test')
            print(f"OK filtered citation probe: {len(rows)} results, "
                  f"first recid={canonical_literature_id(rows[0])}, "
                  f"fields={fields}")
        except Exception as e:
            failed=True
            print(f"ERROR projected citation probe: {e}",file=sys.stderr)
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
