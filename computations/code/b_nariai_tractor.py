"""Implementation B: SageMath manifold/SR route, authored separately from A."""
from sage.all import *
from report import check

def stamp(message):
    pass

def is_zero(e):
    e=SR(e)
    for f in (lambda u:u.simplify_full(),lambda u:u.exponentialize().simplify_full(),lambda u:u.simplify_rational()):
        try:
            if bool(f(e)==0):return True
        except Exception:
            pass
    return False

def allzero(it):
    return all(is_zero(u) for u in it)

def nariai_tractor():
    stamp("Part 1: real Nariai metric (global Prop 8.1, eq nariai-real-metric)")
    a = var('a', domain='positive')
    M = Manifold(4, 'M')
    X = M.chart(r't th vt:(0,pi) ph')
    t, th, vt, ph = X[:]
    g = M.metric('g', signature=-2)
    g[0, 0] = 1
    g[1, 1] = -a**2 * cosh(t / a)**2
    g[2, 2] = -a**2
    g[3, 3] = -a**2 * sin(vt)**2
    Lam = -1 / a**2
    Ric = g.ricci()
    check('G-B-S01', "Nariai Ric = Lambda g with Lambda=-a^-2 (Sage Ricci = tr(a->R(a,b)c))",
          allzero((Ric[i, j] - Lam * g[i, j]).expr() for i in range(4) for j in range(4)))
    check('G-B-S02', "Nariai scalar curvature = 4 Lambda", is_zero(g.ricci_scalar().expr() - 4 * Lam))
    C = g.weyl()
    Wv = [C[i, 2, 0, 2].expr() for i in range(4)]  # W(v,w)w, v=d_t, w=d_vt
    check('G-B-S03', "Weyl: W(d_t,d_vt)d_vt = -(Lambda/3) g(w,w) d_t = -1/3 d_t",
          is_zero(Wv[0] + QQ(1) / 3) and allzero(Wv[1:]), str(Wv))
    check('G-B-S04', "Weyl tensor nonzero", is_zero(Wv[0] + QQ(1)/3))
    Gm = matrix(SR, 4, 4, lambda i, j: g[i, j].expr())
    Ginv = Gm.inverse()
    nab = g.connection()
    Gam = [[[nab[i, j, k].expr() for k in range(4)] for j in range(4)] for i in range(4)]
    co = [t, th, vt, ph]

    stamp("Part 1b: normal tractor connection of global eq real-ray-canonical-tractor on Nariai")
    def omega(i):
        w = matrix(SR, 6, 6, 0)
        for j in range(4):
            w[0, 1 + j] = -Gm[i, j]
            w[5, 1 + j] = -(Lam / 6) * Gm[i, j]
            for k in range(4):
                w[1 + j, 1 + k] = Gam[j][i][k]
        w[1 + i, 0] = Lam / 6
        w[1 + i, 5] = 1
        return w
    Om = [omega(i) for i in range(4)]
    Hm = matrix(SR, 6, 6, 0)
    Hm[0, 5] = Hm[5, 0] = 1
    for j in range(4):
        for k in range(4):
            Hm[1 + j, 1 + k] = Gm[j, k]
    Ivec = vector(SR, [1, 0, 0, 0, 0, -Lam / 6])
    Xvec = vector(SR, [0, 0, 0, 0, 0, 1])
    check('G-B-S05', "tractor D preserves H (d_i H - w_i^T H - H w_i = 0)",
          all(allzero((Hm.apply_map(lambda u: diff(u, co[i])) - Om[i].transpose() * Hm - Hm * Om[i]).list())
              for i in range(4)))
    check('G-B-S06', "D I = 0", all(allzero(list(Om[i] * Ivec)) for i in range(4)))
    check('G-B-S07', "H(I,I)=-Lambda/3, H(I,X)=1, H(X,X)=0",
          is_zero(Ivec * Hm * Ivec + Lam / 3) and is_zero(Ivec * Hm * Xvec - 1) and is_zero(Xvec * Hm * Xvec))
    ok = True
    for i in range(4):
        for j in range(4):
            lhs = Om[i] * vector(SR, [0] + [1 if q == j else 0 for q in range(4)] + [0])
            rhs = vector(SR, [-Gm[i, j]] + [Gam[q][i][j] for q in range(4)] + [-(Lam / 6) * Gm[i, j]])
            rhs2 = vector(SR, [0] + [Gam[q][i][j] for q in range(4)] + [0]) - Gm[i, j] * Ivec - (Lam / 3) * Gm[i, j] * Xvec
            ok = ok and allzero(list(lhs - rhs)) and allzero(list(rhs - rhs2))
    check('G-B-S08', "D_v Theta(w) = Theta(nabla_v w) - g(v,w) I - (Lambda/3) g(v,w) X (Lemma 3.3)", ok)
    stamp("tractor curvature")
    def F(i, j):
        return (Om[j].apply_map(lambda u: diff(u, co[i])) - Om[i].apply_map(lambda u: diff(u, co[j]))
                + Om[i] * Om[j] - Om[j] * Om[i])
    okX = True; okW = True; okRic = True
    for i in range(4):
        for j in range(i + 1, 4):
            Fij = F(i, j)
            okX = okX and allzero(list(Fij * Xvec))
            Wfull = matrix(SR, 6, 6, 0)
            for k in range(4):
                for l in range(4):
                    Wfull[1 + k, 1 + l] = C[k, l, i, j].expr()
            okW = okW and allzero((Fij - Wfull).list())
    check('G-B-S09', "tractor curvature kills X (F^D X = 0)", okX)
    check('G-B-S10', "tractor curvature = Weyl in middle block, 0 elsewhere (normality)", okW)
    for j in range(4):
        for l in range(4):
            sres = sum(F(k, j)[1 + k, 1 + l] for k in range(4) if k != j)
            okRic = okRic and is_zero(sres)
    check('G-B-S11', "Ricci contraction of Theta^-1 pr_W F Theta vanishes (Prop 2.2 admission)", okRic)

