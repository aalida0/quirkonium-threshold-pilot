"""Independent radial Numerov shooting. No shared eigensolver with spectrum.py."""
import numpy as np
from scipy.optimize import brentq

def shoot_endpoint(m_q,a,sigma,e,rmax=4.,h=.002,v0=0):
    mu=m_q/2
    n=int(round(rmax/h));h=rmax/n
    r=h*np.arange(n+1)
    r[0]=h/2
    k=2*mu*(sigma*r-a/r+v0-e)
    prev=0.
    curr=h-mu*a*h*h+(mu/3)*(mu*a*a-e+v0)*h**3
    for j in range(1,n):
        nex=(2*(1+5*h*h*k[j]/12)*curr-(1-h*h*k[j-1]/12)*prev)/(1-h*h*k[j+1]/12)
        prev,curr=curr,nex
        if abs(curr)>1e100:prev*=1e-100;curr*=1e-100
    return curr

def refine_near(m_q,a,sigma,guess,rmax=4.,h=.002,window=.035,v0=0):
    f=lambda e:shoot_endpoint(m_q,a,sigma,e,rmax,h,v0)
    left,right=guess-window,guess+window
    if f(left)*f(right)>0:raise RuntimeError(f'Cannot bracket {guess}')
    return brentq(f,left,right,xtol=1e-12,rtol=1e-13)
