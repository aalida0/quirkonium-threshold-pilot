#!/usr/bin/env python3
"""Identify the missing 2008 QQ-onia publication in the 2012 seed author's bibliography.

The existing collector marked the author census complete merely because one
paper matched each seed author ID. This checks two known same-author papers
against their canonical INSPIRE author links, then writes a comparison file.
"""
import json
from pathlib import Path
from inspire_two_hop import API,recid,save

DOCS={786131:'arXiv:0805.2704 (QQ-onia package)',
      1082353:'arXiv:1112.4629 (Exotic Spectroscopy)'}
def inspect(api):
    records={}
    for literature_id,title in DOCS.items():
        doc=api.get('/api/literature/'+str(literature_id))
        matched=[]
        for a in doc.get('metadata',{}).get('authors',[]):
            full=a.get('full_name','')
            if 'domenech' in full.casefold() or 'garret' in full.casefold():
                matched.append({'full_name':full,'canonical_author_id':recid(a.get('record')),
                                'raw_author_record':a.get('record')})
        records[literature_id]={'title':title,'matched':matched}
    return records

def main():
    out=Path('output/inspire_audit_20261107')
    api=API(out/'http_cache',max_requests=12,window_seconds=5.2)
    records=inspect(api)
    selected={x['canonical_author_id'] for v in records.values()
              for x in v['matched'] if x['canonical_author_id']}
    notes=['The original 2012-seed canonical author ID is 2458026.',
           'A search returning only one paper for that ID cannot be an exhaustive author bibliography given the 2008 QQ-onia coauthorship.',
           'Do not automatically merge different ID profiles without documentary verification.']
    result={'documents':records,'author_ids':sorted(selected),
            'same_author_id':len(selected)==1 and bool(selected),
            'original_seed_author_id':2458026,'notes':notes}
    save(out/'author_identity_qqonia.json',result)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
