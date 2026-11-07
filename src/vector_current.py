"""Leading electroweak widths of a vectorlike SU(2)L-singlet quirkonium.

Adapt tree level current structure from CKY arXiv:0810.1524 Eq.(7),
but DO NOT borrow their SU(2)-doublet quirk charges. Not a physical total width.
"""
from dataclasses import dataclass
from math import sqrt,pi
@dataclass(frozen=True)
class EW:
    alpha:float=1/128
    sw2:float=.23122
    mz:float=91.1876
    mh:float=125.25
    @property
    def cw2(self):return 1-self.sw2
    @property
    def mw(self):return self.mz*sqrt(self.cw2)
    @property
    def v(self):return 2*self.mz*sqrt(self.sw2*self.cw2)/sqrt(4*pi*self.alpha)

F_F={'e':(-1,-.5,1,.000511),'mu':(-1,-.5,1,.105658),'tau':(-1,-.5,1,1.77686),
'nu_e':(0,.5,1,0),'nu_mu':(0,.5,1,0),'nu_tau':(0,.5,1,0),
'u':(2/3,.5,3,.0022),'c':(2/3,.5,3,1.27),'t':(2/3,.5,3,172.76),
'd':(-1/3,-.5,3,.0047),'s':(-1/3,-.5,3,.096),'b':(-1/3,-.5,3,4.18)}

def decay_ff(mass,wfo_over_m2,name,ew=EW(),n_ic=3,qQ=-1):
    """Coherent photon+Z vector/axial CKY Eq.(7), mass and width in GeV."""
    q,t3,ncf,mf=F_F[name]
    if mass<=2*mf:return 0.
    rf=(mf/mass)**2; beta=sqrt(1-4*rf);rz=(ew.mz/mass)**2
    vQ=-qQ*ew.sw2
    gV=t3/2-q*ew.sw2;gA=t3/2
    A=qQ*q+vQ*gV/(ew.sw2*ew.cw2*(1-rz))
    B=vQ*gA/(ew.sw2*ew.cw2*(1-rz))
    return 4*n_ic*ncf*ew.alpha**2*beta/3*wfo_over_m2*((1+2*rf)*A*A+beta**2*B*B)

def gamma_photon_ff(mass,wfo_over_m2,name,ew=EW(),n_ic=3,qQ=-1):
    q,t3,ncf,mf=F_F[name]
    if mass<=2*mf:return 0.
    beta=sqrt(1-4*(mf/mass)**2)
    return (4*n_ic*ncf/3)*ew.alpha**2*wfo_over_m2*(qQ*q)**2*beta*(1+2*(mf/mass)**2)

def decay_ww(mass,wfo_over_m2,ew=EW(),n_ic=3,qQ=-1):
    """SU(2) singlet has only s-channel gamma+Z, no quirk t-channel.
    Adapt CKY Eqs.(13-15); absolute rate needs independent amplitude audit.
    """
    if mass<=2*ew.mw:return 0.
    rw=(ew.mw/mass)**2;rz=(ew.mz/mass)**2
    beta=sqrt(1-4*rw);alphaw=ew.alpha/ew.sw2
    G=(-2*qQ*ew.sw2*rz)/(1-rz)
    return n_ic*alphaw**2*beta**3/(48*rw*rw)*wfo_over_m2*G**2*(1+20*rw+12*rw*rw)

def decay_zh(mass,wfo_over_m2,ew=EW(),n_ic=3,qQ=-1):
    """On-shell Z,h, tree Z*->Zh with f_V current; external amplitude audit pending."""
    mz,mh=ew.mz,ew.mh
    if mass<=mz+mh:return 0.
    k=sqrt((mass*mass-(mz+mh)**2)*(mass*mass-(mz-mh)**2))/(2*mass)
    f2=n_ic*wfo_over_m2*mass/pi
    e=sqrt(4*pi*ew.alpha)
    gzq=e*(-qQ*ew.sw2)/sqrt(ew.sw2*ew.cw2)
    gzzh=2*mz*mz/ew.v
    amp2=(gzq*sqrt(f2)*mass*gzzh/(mass*mass-mz*mz))**2
    return k/(8*pi*mass*mass)*amp2*(1+k*k/(3*mz*mz))
