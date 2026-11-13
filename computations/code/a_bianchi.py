"""Implementation A: exact SymPy checks, extracted from a separately authored audit."""
import sympy as s
from report import passed

def zero(expr):
    reduced=s.simplify(s.expand(expr))
    if reduced != 0:
        reduced=s.simplify(s.expand_trig(reduced).rewrite(s.exp))
    if reduced != 0:
        raise ArithmeticError(str(reduced))

def polzero(expr):
    if s.expand(expr)!=0:
        raise ArithmeticError(str(expr))

def bianchi():
    mt=s.diag(-1,1,1,1)
    # Extracted calculation contracted Bianchi in a spatial normal frame, E_ij=0.
    HH=s.symbols('H'); MM=list(s.symbols('M1:4')); dHH=list(s.symbols('dH0:4'))
    dMM=s.Matrix(4,3,lambda i,j:s.Symbol('d%dM%d'%(i,j+1)))
    KK=s.Matrix(3,3,lambda i,j:s.Symbol('K%d%d'%(min(i,j),max(i,j))))
    conn=[[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for i in range(3):
        for j in range(3):
            conn[0][i+1][j+1]=KK[i,j]
            conn[i+1][0][j+1]=conn[i+1][j+1][0]=KK[i,j]
    EE=s.zeros(4);EE[0,0]=HH
    for i in range(3):EE[0,i+1]=EE[i+1,0]=MM[i]
    def partialE(d,b,c):
        if b==c==0:return dHH[d]
        if b==0 and c>0:return dMM[d,c-1]
        if c==0 and b>0:return dMM[d,b-1]
        return 0
    def nablaE(d,b,c):return partialE(d,b,c)-sum(conn[e][d][b]*EE[e,c]+conn[e][d][c]*EE[b,e] for e in range(4))
    divE=[sum(mt[i,i]*nablaE(i,i,b) for i in range(4)) for b in range(4)]
    polzero(divE[0]+dHH[0]-sum(dMM[i+1,i] for i in range(3))+s.trace(KK)*HH)
    for i in range(3):polzero(divE[i+1]+dMM[0,i]+s.trace(KK)*MM[i])
    passed('G-A-C01', 'Global Appendix A constraint propagation',
           'Universal contracted-Bianchi algebra at an arbitrary spatial-normal point with general symmetric K and residual E_ij=0; yields the two displayed propagation equations')

