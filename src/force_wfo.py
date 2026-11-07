"""Independent S-wave |R(0)|² from the potential-force expectation identity.

For a normalized radial S-wave u(r)=r R(r) and equal quirk masses:
  |R(0)|² = 2 mu <dV/dr> = m_Q <dV/dr>
where V(r)=-a/r+sigma*r, <...>=int |u|² (...) dr.
This method does not use a polynomial extrapolation of u(r)/r to r=0.
"""
import numpy as np
from scipy.integrate import simpson

def wfo_force(cornell, spectrum):
    r=np.asarray(spectrum['r'])
    u=np.asarray(spectrum['u'])
    h=float(spectrum['h'])
    dpot=cornell.sigma+cornell.a/(r*r)
    result=[]
    for col in u.T:
        integrand=col*col*dpot
        integral=simpson(integrand,x=r)
        # The finite-difference grid starts at r=h. For an S wave,
        # u(r)/r -> R(0), so the missing [0,h] Coulomb contribution
        # is a*R(0)^2*h to leading order.
        integral+=h*cornell.a*(col[0]/r[0])**2
        result.append(cornell.m_q*integral)
    return np.asarray(result)
