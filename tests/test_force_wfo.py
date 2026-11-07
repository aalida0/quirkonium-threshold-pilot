import sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from spectrum import Cornell,radial_spectrum
from force_wfo import wfo_force

def test_wfo_force_identity_independent_of_origin_extrapolation():
    for mass,alpha,sigma,rmax in [(100,.091,.18,4.),(500,.073,.18,4.),(500,.102,18.,1.5)]:
        p=Cornell(mass,4/3*alpha,sigma)
        result=radial_spectrum(p,nlevels=3,rmax=rmax,h=.0003)
        force=wfo_force(p,result)
        fit=result['r0sq']
        np.testing.assert_allclose(force,fit,rtol=4e-4)

def test_wfo_force_coulomb_analytic():
    p=Cornell(100,.12,0.)
    result=radial_spectrum(p,nlevels=3,rmax=9,h=.0005)
    force=wfo_force(p,result)
    mu=p.m_q/2
    analytic=np.array([4*(mu*p.a)**3/n**3 for n in (1,2,3)])
    np.testing.assert_allclose(force,analytic,rtol=2e-3)
