"""Direct contracted Bianchi from all 204 first/second/third Gaussian metric jets.

All symbolic generation and expansion occur only in the resource-limited
container. The source copy of jet_gaussian.py is part of this job's input.
"""
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import sympy as s
from report import check

BASE=Path(__file__).with_name('jet_gaussian.py')
# The driver records inputs.json, which pins the helper's exact file hash.
import json
expected=json.loads((BASE.parents[1]/'inputs.json').read_text())['helper_sha256']
if sha256(BASE.read_bytes()).hexdigest()!=expected:
    raise RuntimeError('Metric-jet helper hash mismatch')
from jet_gaussian import HALF,eps,dg,ddg,gi,dgi,gam,dgam,ric4,zero

@lru_cache(None)
def dddg(i,j,a,b,c):
    if i==0 or j==0:return s.S.Zero
    i,j=sorted((i,j));a,b,c=sorted((a,b,c))
    return s.Symbol(f'h{i}{j}_{a}{b}{c}')

@lru_cache(None)
def ddgi(i,j,a,b):
    return sum(eps[i]*eps[k]*eps[j]*(dg(i,k,a)*dg(k,j,b)+dg(i,k,b)*dg(k,j,a))
               for k in range(4))-eps[i]*eps[j]*ddg(i,j,a,b)

@lru_cache(None)
def ddgam(i,j,k,a,b):
    return HALF*sum(
        ddgi(i,l,a,b)*(dg(l,j,k)+dg(l,k,j)-dg(j,k,l))
        +dgi(i,l,a)*(ddg(l,j,k,b)+ddg(l,k,j,b)-ddg(j,k,l,b))
        +dgi(i,l,b)*(ddg(l,j,k,a)+ddg(l,k,j,a)-ddg(j,k,l,a))
        +gi(i,l)*(dddg(l,j,k,a,b)+dddg(l,k,j,a,b)-dddg(j,k,l,a,b))
        for l in range(4))

@lru_cache(None)
def dric4(i,j,a):
    return sum(ddgam(k,i,j,k,a)-ddgam(k,k,j,i,a)
        +sum(dgam(k,k,l,a)*gam(l,i,j)+gam(k,k,l)*dgam(l,i,j,a)
             -dgam(k,i,l,a)*gam(l,k,j)-gam(k,i,l)*dgam(l,k,j,a)
             for l in range(4)) for k in range(4))

lam=s.Symbol('lam')

# Covariant metric value at h(p)=Id. Its derivative is dg, not dgi.
def g0(i,j):return eps[i] if i==j else s.S.Zero
@lru_cache(None)
def E(i,j):return ric4(i,j)-lam*g0(i,j)
@lru_cache(None)
def dE(i,j,a):return dric4(i,j,a)-lam*dg(i,j,a)

def contracted_bianchi(i):
    divergence=sum(eps[a]*(dE(a,i,a)
        -sum(gam(l,a,a)*E(l,i)+gam(l,a,i)*E(a,l) for l in range(4)))
        for a in range(4))
    trace_derivative=sum(eps[a]*dE(a,a,i) for a in range(4))\
        +sum(dgi(a,b,i)*E(a,b) for a in range(4) for b in range(4))
    return divergence-HALF*trace_derivative

def time_component():
    check('GG-THIRD-TIME','Direct time contracted Bianchi from the Ricci definition',
          zero(contracted_bianchi(0)),
          scope='all 24 first, 60 second, 120 third metric derivatives; h(p)=Id; constant lam')

def space_components():
    for i in range(1,4):
        check(f'GG-THIRD-SPACE-{i}',f'Direct spatial contracted Bianchi, component {i}',
              zero(contracted_bianchi(i)),
              scope='all 204 metric derivatives independent modulo metric/partial symmetries')
