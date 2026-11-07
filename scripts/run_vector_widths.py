#!/usr/bin/env python3
"""Write LO partonic channel accounting at published diagnostic potential inputs."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from spectrum import Cornell,radial_spectrum
from vector_total import Inputs,compute

cards=[('Table_III_m100',Cornell(100,4/3*.091,.18),4,.0003,.091),
       ('Table_V_m500',Cornell(500,4/3*.073,.18),4,.0003,.073),
       ('Table_VI_m500',Cornell(500,4/3*.102,18.),1.5,.0003,.102)]
res={'status':'DIAGNOSTIC, no physical model viability certified',
     'source':'CKY arXiv:0810.1524 and Domenech-Garret arXiv:1112.4629',
     'calculations':{}}
for name,p,rmax,h,alpha in cards:
    eig=radial_spectrum(p,3,rmax,h)
    mass=2*p.m_q+float(eig['energies'][0])
    w=float(eig['r0sq'][0])/(mass*mass)
    report=compute(Inputs(mass,w,alpha))
    report['spectrum']={'mQ_GeV':p.m_q,'sigma_GeV2':p.sigma,
                        'E1_GeV':float(eig['energies'][0]),
                        'dE21_GeV':float(eig['energies'][1]-eig['energies'][0])}
    res['calculations'][name]=report
    print(name,report['partonic_LO_sum_keV'],'keV partonic LO accounted')
out=ROOT/'benchmarks'/'partonic_vector_widths.json'
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(res,indent=2))
print(out)
