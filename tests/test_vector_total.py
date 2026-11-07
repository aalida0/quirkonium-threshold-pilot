import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
from vector_current import EW,decay_ff,gamma_photon_ff,decay_ww,decay_zh
from vector_total import Inputs,compute,independent_massless_chiral_check
from three_body import phase_integral,gamma_z_2g
from widths import gamma_gamma_2g

def test_massless_chiral_current_identity():
    for f in ['e','mu','tau','u','d','s','c','b','nu_e']:
        a=decay_ff(1000,.05817,f)
        b=independent_massless_chiral_check(f,1000,.05817)
        assert abs(a/b-1)<.0002

def test_photon_limit_current():
    expected=4*(1/128)**2*.05817
    np.testing.assert_allclose(gamma_photon_ff(1000,.05817,'e'),expected,rtol=1e-10)

def test_three_body_massless():
    np.testing.assert_allclose(phase_integral(0.,144),np.pi**2-9,atol=1e-8)

def test_massive_z_threshold_and_asymptotics():
    gg=gamma_gamma_2g(.05817,.073)
    assert gamma_z_2g(90,.05817,gg)==0
    assert gamma_z_2g(1000,.05817,gg)>0
    value=gamma_z_2g(100000,.05817,gg,n=96)
    np.testing.assert_allclose(value/gg,EW().sw2/(1-EW().sw2),rtol=1e-4)

def test_sum_and_accounted_fractions():
    r=compute(Inputs(1000,.05817,.073),phase_nodes=72)
    assert len(r['partials_GeV'])==17
    np.testing.assert_allclose(sum(r['partials_GeV'].values()),r['partonic_LO_sum_GeV'])
    np.testing.assert_allclose(sum(r['fractions_within_accounted_channels'].values()),1)
    assert r['physical_total_width_GeV'] is None

def test_ww_zh_kinematic_thresholds():
    ew=EW()
    assert decay_ww(150,.05817)==0
    assert decay_ww(1000,.05817)>0
    assert decay_zh(ew.mz+ew.mh-1,.05817)==0
    assert decay_zh(1000,.05817)>0

def test_coherent_z_differs_from_photon():
    assert not np.isclose(decay_ff(1000,.05817,'e'),gamma_photon_ff(1000,.05817,'e'),rtol=1e-3)
