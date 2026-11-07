import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from inspire_two_hop import recid,compact,cutoff_ok,canonical_literature_id

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

def test_arxiv_external_id_resolves_to_inspire_control_number():
    """Regression: /api/arxiv/1112.4629 has nonnumeric top-level id."""
    arxiv_response = {
        'id':'1112.4629',
        'metadata':{'control_number':1082779,
                    'titles':[{'title':'Exotic spectroscopy and decays'}],
                    'arxiv_eprints':[{'value':'1112.4629'}]},
        'links':{}
    }
    assert canonical_literature_id(arxiv_response)==1082779
    assert compact(arxiv_response)['id']==1082779

def test_search_hit_numeric_id_fallback():
    hit={'id':'12345','metadata':{'titles':[{'title':'test'}]}}
    assert canonical_literature_id(hit)==12345

def test_arxiv_error_does_not_silently_invent_id():
    import pytest
    with pytest.raises(ValueError,match='Numeric INSPIRE'):
        canonical_literature_id({'id':'1112.4629','metadata':{}})
