#!/usr/bin/env python3
"""INSPIRE two-hop citation audit + canonical seed-author publication census.

Run from a networked host. Stores all public metadata and HTTP cache locally.
A graph traversal is *not* a substitute for reading full-text novelty matches.
"""
import argparse, csv, hashlib, json, re, sys, time
from pathlib import Path
from urllib.parse import urlencode
import requests

SEEDS = ['1112.4629','0810.1524','1106.3101','0812.0843','2506.14552']
REF = re.compile(r'/(?:api/)?(?:literature|authors)/(\d+)(?:$|[/?#])')
TOPIC = re.compile(r'quirk|infracolo|hidden.{0,15}confin|onium|quarkoni|threshold|spectroscop|green.function|beam.spread|line.shape|resonan', re.I)
URL = 'https://inspirehep.net'

def save(path, obj):
    path = Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False))

def recid(v):
    if isinstance(v,dict):
        return recid(v.get('$ref') or v.get('record') or (v.get('reference',{}).get('record') if isinstance(v.get('reference'),dict) else None))
    m = REF.search(v) if isinstance(v,str) else None
    return int(m.group(1)) if m else None

def compact(r):
    m=r.get('metadata',{})
    return dict(id=int(r['id']), title=(m.get('titles') or [{}])[0].get('title',''),
       date=m.get('earliest_date') or m.get('preprint_date') or '',
       arxiv=(m.get('arxiv_eprints') or [{}])[0].get('value',''),
       doi=[x.get('value','') for x in m.get('dois',[])], citations=m.get('citation_count'))

def cutoff_ok(r, date):
    d=compact(r)['date']
    return not d or d[:10]<=date[:len(d[:10])]

class API:
    def __init__(self, cache, base=URL, delay=.4):
        self.cache=Path(cache); self.cache.mkdir(parents=True,exist_ok=True)
        self.base=base; self.delay=delay; self.last=0; self.count=0
        self.http=requests.Session(); self.http.headers['User-Agent']='quirkonium-threshold-pilot/audit'
    def get(self,path,params=None):
        url=(path if path.startswith('http') else self.base+path)
        if params:url+='?'+urlencode(params)
        h=hashlib.sha256(url.encode()).hexdigest(); location=self.cache/(h+'.json')
        if location.exists(): return json.loads(location.read_text())
        for attempt in range(7):
            time.sleep(max(0,self.delay-(time.monotonic()-self.last)))
            try:
                r=self.http.get(url,timeout=40); self.count+=1; self.last=time.monotonic()
                if r.status_code in (429,500,502,503,504):
                    time.sleep(min(40,5*(attempt+1)));continue
                r.raise_for_status(); obj=r.json();save(location,obj);return obj
            except Exception as e:
                if attempt==6:raise RuntimeError(f'API unavailable: {url}: {e}') from e
                time.sleep(min(20,2**attempt))
        raise RuntimeError('retry budget exhausted for '+url)
    def search(self,query):
        path='/api/literature';params=dict(q=query,size=100,page=1)
        seen=set();returned=0;total=None
        while True:
            obj=self.get(path,params); hits=obj.get('hits',{})
            num=hits.get('total',0);total=num.get('value',0) if isinstance(num,dict) else num
            for row in hits.get('hits',[]):
                returned+=1;yield row
            nxt=obj.get('links',{}).get('next')
            if not nxt:break
            if nxt in seen:raise RuntimeError('Cyclic page in '+query)
            seen.add(nxt); path=nxt;params=None
        if total is not None and returned!=int(total):
            raise RuntimeError(f'Incomplete pagination: {query} {returned}/{total}')

def export_csv(filename,headers,rows):
    with Path(filename).open('w',newline='') as fh:
        w=csv.DictWriter(fh,fieldnames=headers,extrasaction='ignore')
        w.writeheader();w.writerows(rows)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output',default='output/inspire_audit_20261107')
    p.add_argument('--cutoff',default='2026-11-07')
    p.add_argument('--second-hop',choices=['all','relevant'],default='all')
    p.add_argument('--hydrate-all',action='store_true')
    p.add_argument('--skip-authors',action='store_true')
    p.add_argument('--max-nodes',type=int,default=0)
    p.add_argument('--limit-depth1',type=int,default=0)
    p.add_argument('--base',default=URL)
    args=p.parse_args()
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    api=API(out/'http_cache',base=args.base)
    nodes={};depth={};edges=set();problems=[];authors={}
    try:
        for arxiv in SEEDS:
            record=api.get('/api/arxiv/'+arxiv); ident=int(record['id'])
            nodes[ident]=compact(record);depth[ident]=0
            for a in record.get('metadata',{}).get('authors',[]):
                aid=recid(a.get('record'))
                if aid:authors[aid]=a.get('full_name','')
                else:problems.append({'paper':ident,'unresolved_author':a.get('full_name')})
        for level in (0,1):
            todo=sorted([ident for ident,d in depth.items() if d==level])
            for index,ident in enumerate(todo,1):
                if level==1 and args.second_hop=='relevant' and not TOPIC.search(nodes.get(ident,{}).get('title','')):
                    continue
                try:
                    record=api.get('/api/literature/'+str(ident))
                    nodes[ident]=compact(record)
                    for ref in record.get('metadata',{}).get('references',[]):
                        rid=recid(ref)
                        if rid:
                            edges.add((ident,rid,level+1,'reference'));depth.setdefault(rid,level+1)
                        else:problems.append({'paper':ident,'unresolved_reference':True})
                    for citing in api.search('refersto:recid:'+str(ident)):
                        if not cutoff_ok(citing,args.cutoff):continue
                        rid=int(citing['id']);nodes[rid]=compact(citing)
                        edges.add((rid,ident,level+1,'citation'));depth.setdefault(rid,level+1)
                except Exception as ex:
                    problems.append({'paper':ident,'depth':level,'error':str(ex)})
                if index%25==0:
                    print('depth',level,'processed',index,'/',len(todo),'nodes',len(depth),file=sys.stderr)
                if args.max_nodes and len(depth)>=args.max_nodes:
                    problems.append({'truncated_max_nodes':args.max_nodes});break
                if args.limit_depth1 and level==1 and index>=args.limit_depth1:
                    problems.append({'truncated_depth1':args.limit_depth1});break
        if args.hydrate_all:
            missing=[ident for ident in depth if ident not in nodes]
            for index,ident in enumerate(missing,1):
                try:
                    record=api.get('/api/literature/'+str(ident))
                    if cutoff_ok(record,args.cutoff):nodes[ident]=compact(record)
                    else:problems.append({'record_after_cutoff':ident})
                except Exception as ex:problems.append({'hydration_failed':ident,'error':str(ex)})
                if index%100==0:print('hydration',index,'/',len(missing),file=sys.stderr)
        save(out/'node_metadata.json',nodes);save(out/'seed_authors.json',authors)
        export_csv(out/'edges.csv',['source','target','hop','type'],
             (dict(source=s,target=t,hop=h,type=k) for s,t,h,k in sorted(edges)))
        export_csv(out/'nodes.csv',['id','title','date','arxiv','hop'],
             (dict(**r,hop=depth.get(i)) for i,r in nodes.items()))
        author_result={}
        if not args.skip_authors:
            for aid,name in authors.items():
                try:
                    profile=api.get('/api/authors/'+str(aid)).get('metadata',{})
                    inspire=[x.get('value') for x in profile.get('ids',[]) if 'INSPIRE' in x.get('schema','').upper()]
                    preferred=profile.get('name',{}).get('value',name) if isinstance(profile.get('name'),dict) else name
                    queries=['a '+v for v in inspire if v]+['a "'+preferred+'"']
                    matched=[];tries=[]
                    for q in queries:
                        papers=list(api.search(q))
                        matched=[compact(x) for x in papers if cutoff_ok(x,args.cutoff)
                            and aid in [recid(a.get('record')) for a in x.get('metadata',{}).get('authors',[])]]
                        tries.append(dict(query=q,returned=len(papers),verified=len(matched)))
                        if matched:break
                    author_result[aid]=dict(name=name,profile=preferred,papers=matched,queries=tries,
                        complete=bool(matched),note='Identity-checked; unlinked publications may be missed')
                except Exception as ex:
                    author_result[aid]=dict(name=name,complete=False,error=str(ex),papers=[])
                    problems.append({'author_id':aid,'error':str(ex)})
                save(out/'authors'/f'{aid}.json',author_result[aid])
        save(out/'author_coverage.json',
             {aid:dict(name=d['name'],count=len(d['papers']),complete=d.get('complete',False))
              for aid,d in author_result.items()})
        relevant=[dict(v,hop=depth.get(i)) for i,v in nodes.items() if TOPIC.search(v['title'])]
        save(out/'topic_candidates.json',relevant)
        summary=dict(date=args.cutoff,seeds=SEEDS,depth_zero=sum(x==0 for x in depth.values()),
             depth_one=sum(x==1 for x in depth.values()),depth_two=sum(x==2 for x in depth.values()),
             graph_nodes=len(depth),metadata_nodes=len(nodes),edges=len(edges),authors=len(authors),
             author_records=len(author_result),requests=api.count,second_hop=args.second_hop,
             graph_complete=(len(depth)==len(nodes) and not problems and args.second_hop=='all'),
             author_census_complete=(len(author_result)==len(authors) and
                  all(d.get('complete') for d in author_result.values()) and not args.skip_authors),
             problems=problems)
        save(out/'coverage.json',summary)
        print(json.dumps(summary,indent=2))
        return 0 if summary['graph_complete'] and summary['author_census_complete'] else 2
    except Exception as ex:
        save(out/'fatal.json',{'error':str(ex),'partial_node_count':len(depth)})
        raise

if __name__=='__main__':
    sys.exit(main())
