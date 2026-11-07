"""Offline regression tests for INSPIRE's 15 requests / rolling 5-second IP quota."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
import pytest
import inspire_two_hop as audit


def test_rate_window_is_rolling_and_conservative(tmp_path,monkeypatch):
    clock={"now":0.}
    delays=[]
    def sleeping(dt):
        delays.append(dt)
        clock["now"]+=dt
    monkeypatch.setattr(audit.time,"monotonic",lambda:clock["now"])
    monkeypatch.setattr(audit.time,"sleep",sleeping)
    api=audit.API(tmp_path,max_requests=3,window_seconds=5.2)
    for _ in range(3):
        api.rate_limit()
    assert len(api.times)==3
    assert clock["now"]==0.
    api.rate_limit()
    assert clock["now"]>=5.2
    assert len(api.times)<=3
    assert delays
    assert api.times[-1]>=5.2


def test_more_than_15_per_window_rejected(tmp_path):
    with pytest.raises(ValueError,match="1..15"):
        audit.API(tmp_path,max_requests=16)


def test_retry_after_http_429_at_least_five_seconds(tmp_path,monkeypatch):
    clock={"now":0.}
    monkeypatch.setattr(audit.time,"monotonic",lambda:clock["now"])
    monkeypatch.setattr(audit.time,"sleep",lambda x:clock.__setitem__("now",clock["now"]+x))

    class Response:
        def __init__(self,status,body,headers=None):
            self.status_code=status
            self._body=body
            self.headers=headers or {}
        def raise_for_status(self):
            if self.status_code>=400:
                raise RuntimeError("unexpected response")
        def json(self):
            return self._body

    calls=[]
    def get(url,timeout):
        calls.append(clock["now"])
        if len(calls)==1:
            return Response(429,{},{"Retry-After":"2"})
        return Response(200,{"id":42})
    api=audit.API(tmp_path,max_requests=12,window_seconds=5.2)
    monkeypatch.setattr(api.http,"get",get)
    assert api.get("/api/test")=={"id":42}
    assert len(calls)==2
    assert calls[1]-calls[0]>=5.3
    assert api.count==2
    assert api.get("/api/test")=={"id":42}
    assert len(calls)==2
    assert api.cache_hits==1


def test_uncached_api_errors_not_silent(tmp_path,monkeypatch):
    class BadResponse:
        status_code=404
        headers={}
        def raise_for_status(self):
            import requests
            response=requests.Response()
            response.status_code=404
            raise requests.HTTPError("not found",response=response)
    api=audit.API(tmp_path)
    monkeypatch.setattr(api.http,"get",lambda url,timeout:BadResponse())
    with pytest.raises(RuntimeError,match="API rejected"):
        api.get("/api/does-not-exist")


def test_search_uses_small_metadata_projection_and_preserves_it_on_next_pages(tmp_path,monkeypatch):
    from urllib.parse import parse_qs,urlsplit
    calls=[]
    class Response:
        status_code=200
        headers={}
        def __init__(self,records,next_url=None):
            self.records=records
            self.next_url=next_url
        def raise_for_status(self):pass
        def json(self):
            return {'hits':{'total':{'value':2},
                            'hits':self.records},
                    'links':({'next':self.next_url} if self.next_url else {})}
    api=audit.API(tmp_path)
    def fake_get(url,timeout):
        params=parse_qs(urlsplit(url).query)
        fields=params['fields'][0].split(',')
        # Citation queries should not pull enormous ATLAS author arrays.
        assert 'authors.record' not in fields
        assert 'arxiv_eprints' in fields
        assert 'citation_count' in fields
        assert 'abstract' not in fields
        assert 'references' not in fields
        calls.append(url)
        record=lambda i:{'id':i,'metadata':{'titles':[{'title':'Quirk'}],
                   'authors':[{'record':{'$ref':'https://inspirehep.net/api/authors/7'}}]}}
        if len(calls)==1:
            # Simulate INSPIRE accidentally omitting the field projection in links.next.
            return Response([record(1)], 'https://inspirehep.net/api/literature?page=2&q=refersto%3Arecid%3A42')
        return Response([record(2)])
    monkeypatch.setattr(api.http,'get',fake_get)
    results=list(api.search('refersto:recid:42'))
    assert [r['id'] for r in results]==[1,2]
    assert len(calls)==2
    assert 'fields=' in calls[1]


def test_author_census_opt_in_projects_author_record(tmp_path,monkeypatch):
    from urllib.parse import parse_qs,urlsplit
    api=audit.API(tmp_path)
    class Response:
        status_code=200
        def raise_for_status(self):pass
        def json(self):
            return {'hits':{'total':{'value':1},'hits':[{
                'id':21,'metadata':{'titles':[{'title':'pilot'}],
                      'authors':[{'record':{'$ref':'https://inspirehep.net/api/authors/7'}}]}}]},
                    'links':{}}
    def fake_get(url,timeout):
        fields=parse_qs(urlsplit(url).query)['fields'][0].split(',')
        assert 'authors.record' in fields
        return Response()
    monkeypatch.setattr(api.http,'get',fake_get)
    rows=list(api.search('a "Some Verified Author"',include_authors=True))
    assert len(rows)==1
