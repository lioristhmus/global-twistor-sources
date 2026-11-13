"""Implementation A: exact SymPy checks, extracted from a separately authored audit."""
import sympy as s
from report import passed

dot=lambda v,H,w:(v.T*H*w)[0]

def zero(expr):
    reduced=s.simplify(s.expand(expr))
    if reduced != 0:
        reduced=s.simplify(s.expand_trig(reduced).rewrite(s.exp))
    if reduced != 0:
        raise ArithmeticError(str(reduced))

def tractor():
    # Extracted calculation in a parallel metric frame, valid for arbitrary Lambda.
    lam=s.symbols('Lambda'); metric=s.diag(1,-1,-1,-1)
    vv=s.Matrix(s.symbols('v0:4')); ww=s.Matrix(s.symbols('w0:4'))
    H=s.zeros(6);H[0,5]=H[5,0]=1
    H[1:5,1:5]=metric
    A=s.zeros(6);A[0,1:5]=-(vv.T*metric)
    A[1:5,0]=lam*vv/6;A[1:5,5]=vv;A[5,1:5]=-lam*(vv.T*metric)/6
    I=s.Matrix([1,0,0,0,0,-lam/6]); X=s.Matrix([0,0,0,0,0,1])
    for e in A.T*H+H*A:zero(e)
    for e in A*I:zero(e)
    zero((I.T*H*I)[0]+lam/3);zero((I.T*H*X)[0]-1)
    ThetaW=s.Matrix([0,*ww,0]); pairing=(vv.T*metric*ww)[0]
    for e in A*ThetaW+pairing*I+lam*pairing*X/3:zero(e)
    for e in A*A*X-s.Matrix([-dot(vv,metric,vv),0,0,0,0,-lam*dot(vv,metric,vv)/6]):zero(e)
    passed('G-A-T01', 'Tractor metric, scale, solder and null-affine identities',
           'Universal algebraic identities in a parallel frame; D_k^2 X vanishes for affine null k, including Lambda=0')

