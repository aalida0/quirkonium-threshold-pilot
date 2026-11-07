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
