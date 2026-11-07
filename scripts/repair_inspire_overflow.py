#!/usr/bin/env python3
"""Repair the sole 10,000-result INSPIRE pagination cap in the 2026-11-07 audit.

This script performs targeted year-partitioned citation searches for recid 1293923
(MG5_aMC@NLO paper) only, without re-crawling the entire quirk graph or hydrating
unrelated records. It writes an auditable overlay, leaving the original run intact.

INSPIRE REST maximum 10,000 results/search. Conservative 12 requests / 5.2 s.
"""
import csv
import json
import sys
from pathlib import Path
from argparse import ArgumentParser
sys.path.insert(0,str(Path(__file__).resolve().parent))
from inspire_two_hop import API,cutoff_ok,canonical_literature_id,compact,save

PARENT=1293923

def read_existing_edges(path):
    found=set()
    with open(path,newline='') as f:
        for row in csv.DictReader(f):
            if (int(row['target'])==PARENT and
                    row['type']=='citation'):
                found.add(int(row['source']))
    return found

def collect(api, years, cutoff):
    union={}
    rows=[]
    failures=[]
    for year in years:
        q=f"refersto:recid:{PARENT} and date {year}"
        api.progress(f"REPAIR query={q}")
        try:
            found={}
            for paper in api.search(q):
                if cutoff_ok(paper,cutoff):
                    found[canonical_literature_id(paper)]=compact(paper)
            union.update(found)
            rows.append({"year":year,"matched":len(found),"success":True})
        except Exception as error:
            failures.append({"year":year,"error":str(error)})
            rows.append({"year":year,"matched":None,"success":False})
            api.progress(f"INCOMPLETE repair partition={year}: {error}")
    return union,rows,failures

def main():
    parser=ArgumentParser()
    parser.add_argument('--audit-dir',default='output/inspire_audit_20261107')
    parser.add_argument('--cutoff',default='2026-11-07')
    parser.add_argument('--year-start',type=int,default=2013)
    parser.add_argument('--year-end',type=int,default=2026)
    args=parser.parse_args()
    root=Path(args.audit_dir)
    api=API(root/'http_cache',max_requests=12,window_seconds=5.2)
    existing=read_existing_edges(root/'edges.csv')
    q=f'refersto:recid:{PARENT}'
    # Only one small response requested to inspect the API's reported total.
    first=api.get('/api/literature',{
        'q':q,'page':1,'size':1,
        'fields':'control_number,titles,arxiv_eprints,earliest_date'})
    total=first['hits']['total']
    if isinstance(total,dict):total=total.get('value',0)
    total=int(total)
    api.progress(f"CAP query={q} total={total}; existing_cached_citations={len(existing)}")
    extra,partitions,failures=collect(api,range(args.year_start,args.year_end+1),args.cutoff)
    new=sorted(set(extra)-existing)
    output=root/'overflow_repair_1293923'
    output.mkdir(exist_ok=True)
    save(output/'year_partitions.json',partitions)
    save(output/'new_citation_metadata.json',{str(k):extra[k] for k in new})
    with (output/'new_edges.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['source','target','hop','type'])
        writer.writeheader()
        for ident in new:
            writer.writerow({'source':ident,'target':PARENT,'hop':2,'type':'citation'})
    union=existing|set(extra)
    report={'parent':PARENT,'api_reported_total_unfiltered':total,
            'existing_cached_citations':len(existing),
            'year_partition_in_cutoff':len(extra),
            'new_citations_after_dedup':len(new),
            'combined_unique_citations':len(union),
            'year_start':args.year_start,'year_end':args.year_end,
            'cutoff':args.cutoff,
            'unresolved_year_queries':failures,
            'coverage_uncertainties':[
                'INSPIRE date-year search may match several dates for the same paper',
                'Some records may have unknown or unusual year metadata',
                'Dates later than the audit cutoff were excluded',
                'INSPIRE query totals can change as records are revised'],
            'repair_certified':(
                not failures and len(union)>=total and
                args.year_end>=int(args.cutoff[:4]))}
    save(output/'report.json',report)
    print(json.dumps(report,indent=2))
    api.progress(f"REPAIR FINISHED overlay={output}; no original file modified")
    return 0 if report['repair_certified'] else 2

if __name__=='__main__':sys.exit(main())
