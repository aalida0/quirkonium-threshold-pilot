"""Selected LO ^3S_1 partial-rate probes; NOT a physical Gamma_total or branching ratio."""
import numpy as np
def gamma_ll_photon_only(wfo_over_m2,n_ic=3,alpha_em=1/128,q_quark=-1):
    return (4*n_ic/3)*alpha_em**2*q_quark**2*wfo_over_m2
def gamma_3g(wfo_over_m2,alpha_ic,n_ic=3):
    return alpha_ic**3/(9*np.pi)*((n_ic**2-1)*(n_ic**2-4)/n_ic**2)*(np.pi**2-9)*wfo_over_m2
def gamma_gamma_2g(wfo_over_m2,alpha_ic,n_ic=3,alpha_em=1/128,q_quark=-1):
    return 4*alpha_ic**2*q_quark**2*alpha_em/(3*np.pi)*(n_ic**2-1)/n_ic*(np.pi**2-9)*wfo_over_m2
