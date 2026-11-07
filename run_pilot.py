"""Generate spectrum-level diagnostics only; never physical collider cross sections."""
from pathlib import Path
import json,sys
import numpy as np
import scipy,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from spectrum import Cornell,radial_spectrum
from shooting import refine_near
from widths import gamma_ll_photon_only,gamma_3g,gamma_gamma_2g
benchmarks=[
 ('DG_Table_III_diagnostic',Cornell(100,4/3*.091,.18),[.375,.533],[.025,.0059]),
 ('DG_Table_V_diagnostic',Cornell(500,4/3*.073,.18),[.850,1.054],[.058,.0063]),
 ('DG_Table_VI_diagnostic',Cornell(500,4/3*.102,18.),[2.98,4.64],[.187,.048])]
output={'schema':'spectrum-only pilot; no observed cross section','units':{'m_q':'GeV','energy':'GeV','sigma':'GeV^2','r':'GeV^-1','r0sq':'GeV^3'},'software':{'numpy':np.__version__,'scipy':scipy.__version__,'matplotlib':matplotlib.__version__},'model_validation':'UNKNOWN','reference':'Domenech-Garret arXiv:1112.4629 Tables III/V/VI','benchmarks':{}}
for name,p,refdelta,refwfo in benchmarks:
    h=.0012 if p.m_q==100 else .0006
    rmax=4 if p.sigma==.18 else 1.5
    x=radial_spectrum(p,3,rmax,h)
    roots=np.array([refine_near(p.m_q,p.a,p.sigma,float(e),rmax,h) for e in x['energies']])
    d=(x['energies'][1:]-x['energies'][0]).tolist()
    w=(x['r0sq']/(2*p.m_q)**2).tolist()
    entry={'parameters':{'m_q':p.m_q,'a_CF_alpha':p.a,'sigma':p.sigma,'N_IC':3,'rmax':rmax,'h':h,'V0':p.v0},'levels_E_GeV':x['energies'].tolist(),'splittings_GeV':[0]+d,'WFO_over_4mq2_GeV':w,'published_delta_GeV':refdelta,'published_WFO_GeV':refwfo,'rel_delta_disagreement':[(v-r)/r for v,r in zip(d,refdelta)],'rel_WFO_disagreement':[(v-r)/r for v,r in zip(w[:2],refwfo)],'numerov_energy_GeV':roots.tolist(),'max_abs_shoot_difference_GeV':float(np.max(np.abs(roots-x['energies'])))}
    if name=='DG_Table_V_diagnostic':
        entry['partial_widths_LO_diagnostic']={'gamma_ee_photon_only_GeV':gamma_ll_photon_only(w[0]),'gamma_3_infragluons_GeV':gamma_3g(w[0],.073),'gamma_2_infragluons_GeV':gamma_gamma_2g(w[0],.073),'alpha_em_assumed':1/128,'alpha_ic_hard_scale_assumed':.073,'Gamma_total':'UNKNOWN'}
    output['benchmarks'][name]=entry
(ROOT/'benchmarks').mkdir(exist_ok=True)
(ROOT/'figures').mkdir(exist_ok=True)
(ROOT/'benchmarks'/'numerical_results.json').write_text(json.dumps(output,indent=2))
p=benchmarks[0][1]
x=radial_spectrum(p,nlevels=4,rmax=4,h=.0012)
fig,ax=plt.subplots(figsize=(7,4.5))
for n,e in enumerate(x['energies']):
    ax.plot(x['r'],e+.035*x['u'][:,n]/np.max(abs(x['u'][:,n])),label=f'{n+1}S E={e:+.3f} GeV')
ax.plot(x['r'],p.sigma*x['r']-p.a/x['r'],ls='--',label='Cornell potential')
ax.set(xlim=(0,2.5),ylim=(-.8,1),xlabel=r'r [GeV$^{-1}$]',ylabel='E and V [GeV]',title='Potential and spectrum only, mQ=100 GeV diagnostic')
ax.legend(fontsize=8);fig.tight_layout();fig.savefig(ROOT/'figures'/'spectrum_m100.png',dpi=180);plt.close(fig)
fig,ax=plt.subplots(figsize=(6.8,4.2))
idx=np.arange(3);our=[output['benchmarks'][n]['splittings_GeV'][1] for n,*_ in benchmarks]
ref=[b[2][0] for b in benchmarks]
ax.bar(idx-.18,our,.36,label='Numerical FD');ax.bar(idx+.18,ref,.36,label='Published')
ax.set(xticks=idx,xticklabels=['Table III','Table V','Table VI'],ylabel='2S−1S splitting [GeV]',title='Published reference comparison: mismatches are retained')
ax.legend();fig.tight_layout();fig.savefig(ROOT/'figures'/'published_spectrum_comparison.png',dpi=180)
print(json.dumps({k:{'delta21_GeV':v['splittings_GeV'][1],'published_GeV':v['published_delta_GeV'][0]} for k,v in output['benchmarks'].items()},indent=2))
