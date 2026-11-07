"""Massive Z+2 infragluon 3-body phase-space integrator, CKY Appendix A.
The xi->0 integral must reproduce pi^2-9; physical hadronization not modeled.
"""
from functools import lru_cache
import numpy as np
from numpy.polynomial.legendre import leggauss
from math import pi

def poly_integral(xv,x1,xi):
    a=2*xi**4
    b=2*xi**3*(6-4*xv+2*x1-xv*x1-x1*x1)
    c=2*xi*xi*(11-16*xv+6*xv*xv-(8-2*xv-xv*xv)*x1+(4+xv)*x1*x1)
    d=xi*(4*(1-xv)*(4-5*xv+2*xv*xv)-(32-44*xv+14*xv*xv)*x1+
        (20-18*xv+xv*xv)*x1*x1-2*(2-xv)*x1**3+x1**4)
    e=2*(2-6*xv+7*xv*xv-4*xv**3+xv**4-
        (6-13*xv+9*xv*xv-2*xv**3)*x1+
        (7-9*xv+3*xv*xv)*x1*x1-2*(2-xv)*x1**3+x1**4)
    return a+b+c+d+e

@lru_cache(maxsize=32)
def phase_integral(xi,n=144):
    xi=float(xi)
    if not 0<=xi<1:return 0.
    z,w=leggauss(n)
    xv=(z+1)/2*(1+xi-2*np.sqrt(xi))+2*np.sqrt(xi)
    wx=w*(1+xi-2*np.sqrt(xi))/2
    delta=np.sqrt(np.maximum(xv*xv-4*xi,0))
    x1=(2-xv[:,None])/2+delta[:,None]*z[None,:]/2
    x2=2-xv[:,None]-x1
    a=poly_integral(xv[:,None],x1,xi)
    return float(np.sum(a/(x1*x1*x2*x2*(xv[:,None]-2*xi)**2)*
        wx[:,None]*(delta[:,None]*w[None,:]/2)))

def gamma_z_2g(mass,wfo_over_m2,gamma_photon_2g,sw2=.23122,mz=91.1876,n=144):
    if mass<=mz:return 0.
    xi=(mz/mass)**2
    return gamma_photon_2g*(sw2/(1-sw2))*phase_integral(xi,n)/(pi*pi-9)
