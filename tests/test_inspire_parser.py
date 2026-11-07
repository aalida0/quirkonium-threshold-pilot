import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from inspire_two_hop import recid,compact,cutoff_ok

def test_resolve_identity_urls():
    assert recid({'record':{'$ref':'https://inspirehep.net/api/literature/1234'}})==1234
    assert recid({'$ref':'https://inspirehep.net/api/authors/56'})==56
    assert recid({'name':'unresolved'}) is None

def test_canonical_paper_metadata():
    r={'id':12,'metadata':{'titles':[{'title':'Quirkonium'}],
       'arxiv_eprints':[{'value':'1112.4629'}], 'earliest_date':'2012-01-01'}}
    x=compact(r)
    assert x['id']==12 and x['arxiv']=='1112.4629'

def test_cutoff_status():
    assert cutoff_ok({'id':1,'metadata':{'earliest_date':'2026-11-08'}},'2026-11-07') is False
    assert cutoff_ok({'id':1,'metadata':{'earliest_date':'2026-11-07'}},'2026-11-07') is True
