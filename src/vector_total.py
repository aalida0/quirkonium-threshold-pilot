"""LO partonic annihilation sum of one stable vectorlike SU(2)L singlet quirk.
This is NOT a certified physical total width or experimental branching ratio.
"""
from dataclasses import dataclass
from vector_current import EW,F_F,decay_ff,decay_ww,decay_zh
from widths import gamma_3g,gamma_gamma_2g
from three_body import gamma_z_2g

@dataclass(frozen=True)
class Inputs:
    mass:float
    wfo_over_m2:float
    alpha_ic:float
    n_ic:int=3
    charge:float=-1.
    ew:EW=EW()

def compute(i,phase_nodes=144):
    m,w,a,nic,q=(i.mass,i.wfo_over_m2,i.alpha_ic,i.n_ic,i.charge)
    if m<=0 or w<0 or a<0 or nic<2:raise ValueError('Bad input')
    parts={'fermions/'+f:decay_ff(m,w,f,i.ew,nic,q) for f in F_F}
    pgg=gamma_gamma_2g(w,a,nic,i.ew.alpha,q)
    parts.update({'WW':decay_ww(m,w,i.ew,nic,q),
        'Zh':decay_zh(m,w,i.ew,nic,q),
        'gIC_gIC_gIC':gamma_3g(w,a,nic),
        'gamma_gIC_gIC':pgg,
        'Z_gIC_gIC':gamma_z_2g(m,w,pgg,i.ew.sw2,i.ew.mz,phase_nodes)})
    accounted=sum(parts.values())
    ratios={n:v/accounted if accounted>0 else 0 for n,v in parts.items()}
    return {'inputs':{'mass_GeV':m,'wfo_over_m2_GeV':w,'alpha_ic':a,'n_ic':nic,
        'charge':q,'alpha_em':i.ew.alpha,'sw2':i.ew.sw2},
        'partials_GeV':parts,'partonic_LO_sum_GeV':accounted,
        'partonic_LO_sum_keV':accounted*1e6,
        'accounted_fraction_mumu':ratios['fermions/mu'],
        'fractions_within_accounted_channels':ratios,
        'physical_total_width_GeV':None,'physical_BR':None,
        'scope':'LO partonic only; unknown physical total width and branching fractions'}

def independent_massless_chiral_check(name,mass,w,ew=EW(),n_ic=3,charge=-1.):
    """Check coherent vector+axial result using independent chiral L/R currents."""
    q,t3,ncf,mf=F_F[name]
    rz=(ew.mz/mass)**2
    gQ=-charge*ew.sw2
    z=gQ/(ew.sw2*ew.cw2*(1-rz))
    l=charge*q+z*(t3-q*ew.sw2)
    r=charge*q+z*(-q*ew.sw2)
    return (4*n_ic*ncf/3)*ew.alpha**2*w*(l*l+r*r)/2
