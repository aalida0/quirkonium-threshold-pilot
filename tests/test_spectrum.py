import sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from spectrum import Cornell,radial_spectrum
from shooting import refine_near
from widths import gamma_ll_photon_only,gamma_3g,gamma_gamma_2g

def test_coulomb_analytic_levels():
    p=Cornell(m_q=100,a=.12,sigma=0.)
    got=radial_spectrum(p,nlevels=3,rmax=5,h=.0015)
    want=np.array([-p.mu*p.a*p.a/(2*n*n) for n in [1,2,3]])
    np.testing.assert_allclose(got['energies'],want,atol=2e-4,rtol=2e-4)

def test_coulomb_wavefunctions():
    p=Cornell(m_q=100,a=.12,sigma=0.)
    got=radial_spectrum(p,nlevels=3,rmax=9,h=.0012)
    want=np.array([4*(p.mu*p.a)**3/n**3 for n in [1,2,3]])
    np.testing.assert_allclose(got['r0sq'],want,atol=.3,rtol=.006)

def test_published_m100_levels():
    p=Cornell(m_q=100,a=4/3*.091,sigma=.18)
    x=radial_spectrum(p,nlevels=3,rmax=4,h=.0012)
    np.testing.assert_allclose((x['energies'][1:]-x['energies'][0])*1000,[375,533],rtol=.02)

def test_published_m100_wavefunctions():
    p=Cornell(m_q=100,a=4/3*.091,sigma=.18)
    x=radial_spectrum(p,nlevels=3,rmax=4,h=.0012)
    got=x['r0sq']/(2*p.m_q)**2
    np.testing.assert_allclose(got[:2],[.025,.0059],rtol=.05)

def test_fd_numerov_independence():
    p=Cornell(m_q=100,a=4/3*.091,sigma=.18)
    x=radial_spectrum(p,nlevels=3,rmax=4,h=.0015)
    roots=np.array([refine_near(p.m_q,p.a,p.sigma,float(e),rmax=4,h=.0015) for e in x['energies']])
    np.testing.assert_allclose(x['energies'],roots,atol=3e-5,rtol=0)

def test_finite_volume_and_grid():
    p=Cornell(m_q=100,a=4/3*.091,sigma=.18)
    x=radial_spectrum(p,nlevels=3,rmax=4,h=.0012)
    y=radial_spectrum(p,nlevels=3,rmax=5,h=.0009)
    np.testing.assert_allclose(x['energies'],y['energies'],atol=1.6e-5,rtol=0)

def test_widths_positive_and_scaling():
    wfo=.025
    assert gamma_ll_photon_only(wfo)>0
    assert gamma_3g(wfo,.1)>0
    assert gamma_gamma_2g(wfo,.1)>0
    np.testing.assert_allclose(gamma_3g(wfo,.2)/gamma_3g(wfo,.1),8.)
    np.testing.assert_allclose(gamma_gamma_2g(wfo,.2)/gamma_gamma_2g(wfo,.1),4.)
