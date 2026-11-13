"""Exact finite-jet Gaussian identities. Import and execute only in the container.

At the chosen point h=Id; all 24 first and 60 second derivatives of its six
entries are independent symbols, modulo metric and mixed-partial symmetry.
The Bianchi reduction uses an independent symmetric residual E and its first
derivatives. It does not derive contracted Bianchi from third metric jets.
"""
from functools import lru_cache
import sympy as s
from report import check

HALF=s.Rational(1,2)
eps=(-1,1,1,1)

@lru_cache(None)
def dg(i,j,a):
    if i==0 or j==0:return s.S.Zero
    i,j=sorted((i,j))
    return s.Symbol(f'h{i}{j}_{a}')

@lru_cache(None)
def ddg(i,j,a,b):
    if i==0 or j==0:return s.S.Zero
    i,j=sorted((i,j));a,b=sorted((a,b))
    return s.Symbol(f'h{i}{j}_{a}{b}')

def gi(i,j):return eps[i] if i==j else s.S.Zero
def dgi(i,j,a):return -eps[i]*eps[j]*dg(i,j,a)

@lru_cache(None)
def gam(i,j,k):
    return HALF*sum(gi(i,l)*(dg(l,j,k)+dg(l,k,j)-dg(j,k,l)) for l in range(4))

@lru_cache(None)
def dgam(i,j,k,a):
    return HALF*sum(
        dgi(i,l,a)*(dg(l,j,k)+dg(l,k,j)-dg(j,k,l))
        +gi(i,l)*(ddg(l,j,k,a)+ddg(l,k,j,a)-ddg(j,k,l,a))
        for l in range(4))

@lru_cache(None)
def ric4(i,j):
    return sum(dgam(k,i,j,k)-dgam(k,k,j,i)
        +sum(gam(k,k,l)*gam(l,i,j)-gam(k,i,l)*gam(l,k,j) for l in range(4))
        for k in range(4))

@lru_cache(None)
def ric3(i,j):
    return sum(dgam(k,i,j,k)-dgam(k,k,j,i)
        +sum(gam(k,k,l)*gam(l,i,j)-gam(k,i,l)*gam(l,k,j) for l in range(1,4))
        for k in range(1,4))

def zero(expr):return s.expand(expr)==0
def allzero(expressions):return all(zero(e) for e in expressions)

def run():
    K=s.Matrix(3,3,lambda i,j:HALF*dg(i+1,j+1,0))
    Kdot=s.Matrix(3,3,lambda i,j:HALF*ddg(i+1,j+1,0,0))
    tau=s.trace(K);Ksq=s.trace(K*K)
    tau_t=s.trace(Kdot)-2*Ksq
    check('GG-JET-K','K from the four-dimensional Christoffel symbols',
          allzero(gam(j+1,i+1,0)-K[i,j] for i in range(3) for j in range(3)),
          metric_jet='general symmetric h; h(p)=Id; 24 first + 60 second derivatives')
    check('GG-JET-RIJ','All spatial Gaussian Ricci components',
          allzero(ric4(i+1,j+1)-ric3(i+1,j+1)-Kdot[i,j]-tau*K[i,j]+2*(K*K)[i,j]
                  for i in range(3) for j in range(3)))
    check('GG-JET-R00','Gaussian time-time Ricci component',zero(ric4(0,0)+tau_t+Ksq))

    def divK(i):
        return sum(HALF*ddg(j+1,i+1,0,j+1)
            -sum(gam(l+1,j+1,j+1)*K[l,i]+gam(l+1,j+1,i+1)*K[j,l] for l in range(3))
            for j in range(3))
    def dtau(i):
        return HALF*sum(ddg(j+1,j+1,0,i+1) for j in range(3))\
             -sum(dg(j+1,k+1,i+1)*K[j,k] for j in range(3) for k in range(3))
    check('GG-JET-R0I','All Gaussian time-space Ricci components',
          allzero(ric4(0,i+1)-divK(i)+dtau(i) for i in range(3)))
    lam=s.Symbol('lam')
    H=ric4(0,0)+lam
    trace_E=sum(ric4(i,i)-lam for i in range(1,4))
    scal3=sum(ric3(i,i) for i in range(1,4))
    check('GG-JET-CONSTRAINT','Hamiltonian trace identity for arbitrary constant lam',
          zero(H+trace_E-scal3-tau*tau+Ksq+2*lam))

    @lru_cache(None)
    def E(i,j):
        i,j=sorted((i,j));return s.Symbol(f'E{i}{j}')
    @lru_cache(None)
    def dE(i,j,a):
        i,j=sorted((i,j));return s.Symbol(f'E{i}{j}_{a}')
    def nabE(a,i,j):
        return dE(i,j,a)-sum(gam(l,a,i)*E(l,j)+gam(l,a,j)*E(i,l) for l in range(4))
    def dtrace(a):
        return sum(eps[i]*dE(i,i,a) for i in range(4))\
             +sum(dgi(i,j,a)*E(i,j) for i in range(4) for j in range(4))
    def B(i):return sum(eps[a]*nabE(a,a,i) for a in range(4))-HALF*dtrace(i)
    def de(a):
        return sum(dE(i,i,a) for i in range(1,4))\
             +sum(dgi(i,j,a)*E(i,j) for i in range(1,4) for j in range(1,4))
    divM=sum(dE(0,i,i)-sum(gam(l,i,i)*E(0,l) for l in range(1,4)) for i in range(1,4))
    time_target=-HALF*dE(0,0,0)+divM-tau*E(0,0)-HALF*de(0)\
        -sum(K[i-1,j-1]*E(i,j) for i in range(1,4) for j in range(1,4))
    check('GG-BIANCHI-TIME','Full time residual: contracted Bianchi in Gaussian coordinates',
          zero(B(0)-time_target),residual='arbitrary symmetric E and its 40 first derivatives')
    tr=-E(0,0)+sum(E(i,i) for i in range(1,4))
    def S(i,j):return E(i,j)-HALF*tr*(1 if i==j else 0)
    def dS(i,j,a):return dE(i,j,a)-HALF*dtrace(a)*(1 if i==j else 0)-HALF*tr*dg(i,j,a)
    def spatial_target(i):
        divS=sum(dS(j,i,j)-sum(gam(l,j,j)*S(l,i)+gam(l,j,i)*S(j,l) for l in range(1,4))
                 for j in range(1,4))
        return -dE(0,i,0)+divS-tau*E(0,i)
    check('GG-BIANCHI-SPACE','All three full spatial contracted-Bianchi residuals',
          allzero(B(i)-spatial_target(i) for i in range(1,4)))
