"""Implementation A: exact SymPy checks, extracted from a separately authored audit."""
import sympy as s
from report import passed

def zero(expr):
    reduced=s.simplify(s.expand(expr))
    if reduced != 0:
        reduced=s.simplify(s.expand_trig(reduced).rewrite(s.exp))
    if reduced != 0:
        raise ArithmeticError(str(reduced))

def nariai():
    # Extracted calculation R(d,c,a,b) is [R(partial_a,partial_b)partial_c]^d.
    t, th, ch, ph = x = s.symbols('t theta chi phi', real=True)
    a = s.symbols('a', positive=True)
    g = s.diag(1, -a*a*s.cosh(t/a)**2, -a*a, -a*a*s.sin(ch)**2)
    gi = s.diag(*[1/g[i,i] for i in range(4)])
    G = [[[s.simplify(sum(gi[d,e]*(s.diff(g[e,b],x[c])+
             s.diff(g[e,c],x[b])-s.diff(g[b,c],x[e])) for e in range(4))/2)
           for c in range(4)] for b in range(4)] for d in range(4)]
    R = {}
    for d in range(4):
        for c in range(4):
            for u in range(4):
                for v in range(4):
                    R[d,c,u,v] = s.simplify(s.diff(G[d][v][c],x[u])-
                        s.diff(G[d][u][c],x[v])+sum(G[d][u][e]*G[e][v][c]-
                        G[d][v][e]*G[e][u][c] for e in range(4)))
    Ric = s.Matrix(4,4,lambda b,c:s.simplify(sum(R[u,c,u,b] for u in range(4))))
    for e in Ric + g/a**2: zero(e)
    zero(R[0,2,0,2]-(-1/a**2)/3*g[2,2]+s.Rational(1,3))
    passed('G-A-N01', 'Nariai coordinate Ricci and mixed Weyl',
           'All 16 Ricci entries and a nonzero Weyl component, on the regular coordinate chart',
           Lambda='-1/a^2', Weyl_t_chi_t_chi='-1/3',
           Ricci_diagonal=[str(Ric[i,i]) for i in range(4)])

    # Quadric geodesics and compact direction conics.
    eta, z, u, S, T, r = s.symbols('eta z u S T r')
    H1=s.diag(1,-1,-1); H2=-s.eye(3)
    dot=lambda v,H,w:(v.T*H*w)[0]
    x1=s.Matrix([0,a,0]); x2=s.Matrix([0,0,a])
    k=s.Matrix([a*s.cosh(eta),0,a*s.sinh(eta)])
    uz=a*s.Matrix([(z+1/z)/2,-s.I*(z-1/z)/2,0])
    zero(dot(x1,H1,k)); zero(dot(x2,H2,uz))
    zero(dot(k,H1,k)-a*a); zero(dot(uz,H2,uz)+a*a)
    c1=x1*s.cosh(u)+k*s.sinh(u)
    c2=x2*s.cos(u)+uz*s.sin(u)
    zero(dot(c1,H1,c1)+a*a); zero(dot(c2,H2,c2)+a*a)
    zero(dot(c1.diff(u),H1,c1.diff(u))+dot(c2.diff(u),H2,c2.diff(u)))
    for e in c1.diff(u,2)-c1:zero(e)
    for e in c2.diff(u,2)+c2:zero(e)
    v=a*s.Matrix([S*S+T*T,-s.I*(S*S-T*T),0])
    zero(dot(2*S*T*k,H1,2*S*T*k)+dot(v,H2,v))
    zero((v[0]+s.I*v[1])/(2*a)-S*S)
    zero((v[0]-s.I*v[1])/(2*a)-T*T)
    for e in v.subs({S:z,T:1})/(2*z)-uz:zero(e)
    for e in c2.subs(u,s.pi)+x2:zero(e)
    y1=(x1*s.cosh(s.pi)+k*s.sinh(s.pi))
    dy=y1.diff(eta).subs(eta,0)
    assert dy == s.Matrix([0,0,a*s.sinh(s.pi)])
    assert a*s.sinh(s.pi) != 0
    passed('G-A-N02', 'Nariai quadric, geodesic, conic and kernel-contradiction formulas',
           'Exact symbolic identities; nonvanishing of v on P1 follows from S^2=T^2=0 only at the forbidden zero pair',
           transverse_base_derivative=str(dy.T),
           degenerate_leaf_first_factor='zero; therefore cannot contain this derivative')
    k1r=a*s.Matrix([(1+r*r)/2,0,(1-r*r)/2]); u2=s.Matrix([a,0,0])
    zero(dot(k1r,H1,k1r)-a*a*r*r)
    y2=x2*s.cosh(2*s.pi)+s.I*u2*s.sinh(2*s.pi)
    zero(dot(y2,H2,y2)+a*a)
    assert y2[0] == s.I*a*s.sinh(2*s.pi) != 0
    passed('G-A-N03', 'Nariai nonclosed-relation sequence formulas',
           'Initial energy, limiting endpoint quadric and distinct second point; properness and quotient topology require hand proof')

