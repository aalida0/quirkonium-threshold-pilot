"""S-wave Cornell radial Schrödinger solver (natural units, GeV and GeV^-1)."""
from dataclasses import dataclass
import numpy as np
from scipy.linalg import eigh_tridiagonal

@dataclass(frozen=True)
class Cornell:
    m_q: float = 500.
    a: float = (4/3)*.073
    sigma: float = .18
    v0: float = 0.
    @property
    def mu(self):
        return self.m_q/2

def radial_spectrum(p, nlevels=4, rmax=4., h=.002):
    n=int(round(rmax/h))-1
    h=rmax/(n+1)
    r=h*np.arange(1,n+1)
    diag=1/(p.mu*h*h)+p.sigma*r-p.a/r+p.v0
    off=np.full(n-1,-.5/(p.mu*h*h))
    e,u=eigh_tridiagonal(diag,off,select='i',select_range=(0,nlevels-1))
    u=u/np.sqrt(h)
    nr=min(10,len(r))
    coeff=np.polynomial.polynomial.polyfit(r[:nr],u[:nr,:]/r[:nr,None],deg=3)
    return {'energies':e,'r0sq':coeff[0]**2,'r':r,'u':u,'h':h}
