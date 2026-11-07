#!/usr/bin/env python3
"""INSPIRE two-hop citation audit + canonical seed-author publication census.

Run from a networked host. Stores all public metadata and HTTP cache locally.
A graph traversal is *not* a substitute for reading full-text novelty matches.
"""
import argparse, csv, hashlib, json, re, sys, time
from collections import deque
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

def canonical_literature_id(record):
    """Resolve the numeric INSPIRE recid from a literature response.

    /api/arxiv/<eprint> returns the eprint in top-level 'id', not a
    numeric INSPIRE recid. Literature search hits usually have numeric
    'id'. The canonical metadata.control_number works for both.
    """
    meta = record.get('metadata') or {}
    for candidate in (meta.get('control_number'), record.get('id')):
        if candidate is None:
            continue
        try:
            return int(candidate)
        except (TypeError, ValueError):
            pass
    for key in ('json', 'self', 'citations'):
        candidate = recid((record.get('links') or {}).get(key))
        if candidate is not None:
            return candidate
    raise ValueError(
        'Numeric INSPIRE literature recid unavailable: top-level id=%r, metadata.control_number=%r'
        % (record.get('id'), meta.get('control_number'))
    )

def compact(r):
    m=r.get('metadata',{})
    return dict(id=canonical_literature_id(r), title=(m.get('titles') or [{}])[0].get('title',''),
       date=m.get('earliest_date') or m.get('preprint_date') or '',
       arxiv=(m.get('arxiv_eprints') or [{}])[0].get('value',''),
       doi=[x.get('value','') for x in m.get('dois',[])], citations=m.get('citation_count'))

def cutoff_ok(r, date):
    d=compact(r)['date']
    return not d or d[:10]<=date[:len(d[:10])]

class API:
    """Cached, rate-limited and observable INSPIRE REST client.

    INSPIRE documents 15 requests / rolling five seconds / IP address.
    The default deliberately leaves headroom: 12 / 5.2 seconds.
    Every attempt, including HTTP 429 and retries, consumes a slot.
    """
    def __init__(self, cache, base=URL, max_requests=12,
                 window_seconds=5.2, read_timeout=20):
        if not 1 <= max_requests <= 15:
            raise ValueError("requests per five-second window must be 1..15")
        if window_seconds < 5.0:
            raise ValueError("rolling rate window must be at least five seconds")
        self.cache=Path(cache)
        self.cache.mkdir(parents=True, exist_ok=True)
        self.base=base
        self.max_requests=max_requests
        self.window_seconds=window_seconds
        self.read_timeout=read_timeout
        self.times=deque()
        self.count=0
        self.cache_hits=0
        self.http=requests.Session()
        self.http.headers['User-Agent']='quirkonium-threshold-pilot/audit'
    @staticmethod
    def progress(message):
        print(f"[{time.strftime('%H:%M:%S')}] {message}",
              file=sys.stderr, flush=True)
    def rate_limit(self):
        while True:
            now=time.monotonic()
            while self.times and now-self.times[0]>=self.window_seconds:
                self.times.popleft()
            if len(self.times)<self.max_requests:
                self.times.append(now)
                return
            delay=max(.01,self.window_seconds-(now-self.times[0])+.01)
            self.progress(f"RATE_LIMIT waiting {delay:.1f}s "
                          f"(max {self.max_requests} requests / "
                          f"{self.window_seconds:.1f}s rolling window)")
            time.sleep(delay)
    def get(self,path,params=None):
        url=(path if path.startswith('http') else self.base+path)
        if params:
            url+='?'+urlencode(params)
        key=hashlib.sha256(url.encode()).hexdigest()
        location=self.cache/(key+'.json')
        if location.exists():
            self.cache_hits+=1
            return json.loads(location.read_text())
        for attempt in range(1,8):
            self.rate_limit()
            self.count+=1
            self.progress(f"REQUEST {self.count}: {url[:190]} "
                          f"(attempt {attempt}/7, cached={self.cache_hits})")
            try:
                response=self.http.get(url,timeout=(10,self.read_timeout))
                if response.status_code==429:
                    value=response.headers.get('Retry-After','')
                    try: retry=float(value)
                    except (ValueError,TypeError): retry=0.
                    delay=max(5.3,retry)
                    self.progress(f"HTTP 429: waiting {delay:.1f}s "
                                  "before next request; failed requests count")
                    time.sleep(delay)
                    continue
                if response.status_code in (500,502,503,504):
                    delay=min(45.,5.0*attempt)
                    self.progress(f"HTTP {response.status_code}: "
                                  f"waiting {delay:.1f}s before retry")
                    time.sleep(delay)
                    continue
                response.raise_for_status()
                obj=response.json()
                save(location,obj)
                return obj
            except (requests.RequestException,ValueError) as error:
                if isinstance(error,requests.HTTPError) and error.response is not None:
                    # Irrecoverable record/parameter failures should surface promptly.
                    if error.response.status_code in (400,401,403,404,422):
                        raise RuntimeError(f"API rejected {url}: {error}") from error
                if attempt==7:
                    raise RuntimeError(f"API failed after 7 attempts: "
                                       f"{url}: {error}") from error
                delay=min(30.,2.0*attempt)
                self.progress(f"ERROR {type(error).__name__}: {error}; "
                              f"retry in {delay:.1f}s")
                time.sleep(delay)
        raise RuntimeError("Retry budget exhausted: "+url)
    def search(self,query):
        path='/api/literature'
        # INSPIRE's 'fields' cuts huge author/affiliation/abstract and
        # reference payloads from citation-search results. It is part of
        # the cache key and is retained by links.next pagination.
        # authors.record is needed to verify author-ID membership.
        fields=('control_number,titles,arxiv_eprints,dois,earliest_date,'
                'citation_count,authors.record')
        params=dict(q=query,size=100,page=1,fields=fields)
        seen=set()
        returned=0
        total=None
        page=0
        while True:
            obj=self.get(path,params)
            page+=1
            hits=obj.get('hits',{})
            total_raw=hits.get('total',0)
            total=(total_raw.get('value',0) if isinstance(total_raw,dict)
                   else total_raw)
            rows=hits.get('hits',[])
            returned+=len(rows)
            self.progress(f"SEARCH {query[:75]!r}: page {page}, "
                          f"page_results={len(rows)}, received={returned}, "
                          f"reported_total={total}")
            for row in rows:
                yield row
            nxt=obj.get('links',{}).get('next')
            # Defensive: next-page URLs should preserve the projection.
            # If omitted by an upstream version, retain fields explicitly.
            if nxt and 'fields=' not in nxt:
                from urllib.parse import urlsplit,parse_qsl,urlunsplit
                parts=urlsplit(nxt)
                qp=dict(parse_qsl(parts.query))
                qp['fields']=fields
                nxt=urlunsplit((parts.scheme,parts.netloc,parts.path,
                                urlencode(qp),parts.fragment))
            if not nxt:
                break
            if nxt in seen:
                raise RuntimeError("Cyclic pagination link for "+query)
            seen.add(nxt)
            path=nxt
            params=None
        if total is not None and returned!=int(total):
            raise RuntimeError(f"Incomplete pagination for {query}: "
                               f"{returned}/{total}")

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
    p.add_argument('--requests-per-window',type=int,default=12,
                   help='Conservative IP-wide limit; INSPIRE permits 15 per 5s')
    p.add_argument('--window-seconds',type=float,default=5.2,
                   help='Rolling window for the request limiter (minimum 5s)')
    p.add_argument('--read-timeout',type=int,default=20,
                   help='HTTP response read timeout in seconds')
    args=p.parse_args()
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    api=API(out/'http_cache',base=args.base,
            max_requests=args.requests_per_window,
            window_seconds=args.window_seconds,
            read_timeout=args.read_timeout)
    api.progress('START: resolving 5 seed papers; '
                 f'limit {api.max_requests}/{api.window_seconds}s, '
                 f'cache={api.cache}')
    nodes={};depth={};edges=set();problems=[];authors={}
    try:
        for arxiv in SEEDS:
            api.progress(f'SEED resolving arXiv:{arxiv}')
            record=api.get('/api/arxiv/'+arxiv); ident=canonical_literature_id(record)
            nodes[ident]=compact(record);depth[ident]=0
            api.progress(f'SEED OK arXiv:{arxiv} -> INSPIRE {ident}')
            for a in record.get('metadata',{}).get('authors',[]):
                aid=recid(a.get('record'))
                if aid:authors[aid]=a.get('full_name','')
                else:problems.append({'paper':ident,'unresolved_author':a.get('full_name')})
        for level in (0,1):
            todo=sorted([ident for ident,d in depth.items() if d==level])
            api.progress(f'DEPTH {level}: {len(todo)} papers to inspect')
            for index,ident in enumerate(todo,1):
                api.progress(f'DEPTH {level} paper {index}/{len(todo)}: '
                             f'INSPIRE {ident}; graph_nodes={len(depth)}')
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
                        rid=canonical_literature_id(citing);nodes[rid]=compact(citing)
                        edges.add((rid,ident,level+1,'citation'));depth.setdefault(rid,level+1)
                except Exception as ex:
                    api.progress(f'INCOMPLETE paper={ident} depth={level}: {type(ex).__name__}: {ex}')
                    problems.append({'paper':ident,'depth':level,'error':str(ex)})
                api.progress(f'DEPTH {level} completed {index}/{len(todo)}; '
                             f'graph_nodes={len(depth)}, edges={len(edges)}, '
                             f'errors={len(problems)}, requests={api.count}')
                if args.max_nodes and len(depth)>=args.max_nodes:
                    problems.append({'truncated_max_nodes':args.max_nodes});break
                if args.limit_depth1 and level==1 and index>=args.limit_depth1:
                    problems.append({'truncated_depth1':args.limit_depth1});break
        if args.hydrate_all:
            api.progress('HYDRATE: retrieving missing node metadata')
            missing=[ident for ident in depth if ident not in nodes]
            for index,ident in enumerate(missing,1):
                if index==1 or index%10==0:
                    api.progress(f'HYDRATE {index}/{len(missing)} INSPIRE {ident}')
                try:
                    record=api.get('/api/literature/'+str(ident))
                    if cutoff_ok(record,args.cutoff):nodes[ident]=compact(record)
                    else:problems.append({'record_after_cutoff':ident})
                except Exception as ex:problems.append({'hydration_failed':ident,'error':str(ex)})
                if index%100==0:
                    api.progress(f'HYDRATE completed {index}/{len(missing)}')
        save(out/'node_metadata.json',nodes);save(out/'seed_authors.json',authors)
        export_csv(out/'edges.csv',['source','target','hop','type'],
             (dict(source=s,target=t,hop=h,type=k) for s,t,h,k in sorted(edges)))
        export_csv(out/'nodes.csv',['id','title','date','arxiv','hop'],
             (dict(**r,hop=depth.get(i)) for i,r in nodes.items()))
        author_result={}
        if not args.skip_authors:
            for ix,(aid,name) in enumerate(authors.items(),1):
                api.progress(f'AUTHOR {ix}/{len(authors)} INSPIRE {aid}: {name}')
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
        api.progress(f'FINISHED: requests={api.count}, cached={api.cache_hits}, '
                     f'graph_nodes={len(depth)}, problems={len(problems)}')
        return 0 if summary['graph_complete'] and summary['author_census_complete'] else 2
    except KeyboardInterrupt:
        api.progress('INTERRUPTED: cached HTTP responses are preserved; rerun safely')
        save(out/'interrupted.json',{'requests':api.count,'cached':api.cache_hits,
                                   'discovered_nodes':len(depth),'edges':len(edges)})
        raise
    except Exception as ex:
        api.progress(f'FATAL: {ex}')
        save(out/'fatal.json',{'error':str(ex),'partial_node_count':len(depth)})
        raise

if __name__=='__main__':
    sys.exit(main())
