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

lam = var('lam')
def run_family(label, hfun):
    stamp("family %s" % label)
    N = Manifold(4, 'N_' + label)
    Y = N.chart(r't x y zz')
    t, x, y, zz = Y[:]
    sp = [x, y, zz]
    hm = hfun(t, x, y)
    hinv = hm.inverse()
    gh = N.metric('gh', signature=2)
    gh[0, 0] = -1
    for i in range(3):
        for j in range(3):
            gh[1 + i, 1 + j] = hm[i, j]
    Ricg = gh.ricci()
    R4 = [[Ricg[i, j].expr() for j in range(4)] for i in range(4)]
    stamp("  4D Ricci done")
    # 3D Levi-Civita of h_t (t is a parameter)
    Gam = [[[sum(hinv[i, l] * (diff(hm[l, j], sp[k]) + diff(hm[l, k], sp[j]) - diff(hm[j, k], sp[l]))
                 for l in range(3)) / 2 for k in range(3)] for j in range(3)] for i in range(3)]
    def Ric3(j, k):
        return sum(diff(Gam[i][j][k], sp[i]) - diff(Gam[i][j][i], sp[k])
                   + sum(Gam[i][i][p] * Gam[p][j][k] - Gam[i][k][p] * Gam[p][j][i] for p in range(3))
                   for i in range(3))
    Rh = matrix(SR, 3, 3, lambda j, k: Ric3(j, k))
    Kt = hm.apply_map(lambda u: diff(u, t) / 2)
    tau = sum(hinv[i, j] * Kt[i, j] for i in range(3) for j in range(3))
    KK = Kt * hinv * Kt
    Kup = hinv * Kt * hinv
    K2 = sum(Kt[i, j] * Kup[i, j] for i in range(3) for j in range(3))
    def covK(k, i, j):
        return diff(Kt[i, j], sp[k]) - sum(Gam[l][k][i] * Kt[l, j] + Gam[l][k][j] * Kt[i, l] for l in range(3))
    divK = [sum(hinv[j, k] * covK(k, i, j) for j in range(3) for k in range(3)) for i in range(3)]
    # second fundamental form sign: ghat(nabla_i d_t, d_j) = Gamma^k_{i0} h_kj
    nab = gh.connection()
    check(f"G-B-{label}01", "%s: K(v,w) = ghat(nabla_v d_t, w) = (1/2) d_t h" % label,
          allzero(sum(nab[1 + k, 1 + i, 0].expr() * hm[k, j] for k in range(3)) - Kt[i, j]
                  for i in range(3) for j in range(3)))
    check(f"G-B-{label}02", "%s: Ric_ij = Ric(h)_ij + d_t K_ij + tau K_ij - 2 K_iq K^q_j" % label,
          allzero(R4[1 + i][1 + j] - (Rh[i, j] + diff(Kt[i, j], t) + tau * Kt[i, j] - 2 * KK[i, j])
                  for i in range(3) for j in range(3)))
    check(f"G-B-{label}03", "%s: Ric_00 = -d_t tau - |K|^2" % label, is_zero(R4[0][0] + diff(tau, t) + K2))
    check(f"G-B-{label}04", "%s: Ric_0i = div_h K_i - d_i tau" % label,
          allzero(R4[0][1 + i] - (divK[i] - diff(tau, sp[i])) for i in range(3)))
    stamp("  Gaussian formulas done")
    # E = Ric(ghat) - lam ghat, H = E_00, M_i = E_0i
    E = [[R4[i][j] - lam * (gh[i, j].expr()) for j in range(4)] for i in range(4)]
    H = E[0][0]; Mv = [E[0][1 + i] for i in range(3)]
    Es = matrix(SR, 3, 3, lambda i, j: E[1 + i][1 + j])
    e = sum(hinv[i, j] * Es[i, j] for i in range(3) for j in range(3))
    scal_h = sum(hinv[i, j] * Rh[i, j] for i in range(3) for j in range(3))
    check(f"G-B-{label}05", "%s: E_00 + h^ij E_ij = Scal(h) + tau^2 - |K|^2 - 2 lam" % label,
          is_zero(H + e - (scal_h + tau**2 - K2 - 2 * lam)))
    divM = sum(hinv[i, j] * (diff(Mv[i], sp[j]) - sum(Gam[k][j][i] * Mv[k] for k in range(3)))
               for i in range(3) for j in range(3))
    Kupl = Kup
    lhs_a = (-diff(H, t) / 2 + divM - tau * H - diff(e, t) / 2
             - sum(Kupl[i, k] * Es[i, k] for i in range(3) for k in range(3)))
    stamp("  Bianchi identity (a) assembled")
    check(f"G-B-{label}06", "%s: Bianchi(a): -dH/2 + div M - tau H - de/2 - K^ik E_ik = 0" % label, is_zero(lhs_a))
    Sm = Es - (-H + e) / 2 * hm
    def covS(k, j, i):
        return diff(Sm[j, i], sp[k]) - sum(Gam[l][k][j] * Sm[l, i] + Gam[l][k][i] * Sm[j, l] for l in range(3))
    okb = True
    for i in range(3):
        divS = sum(hinv[j, k] * covS(k, j, i) for j in range(3) for k in range(3))
        okb = okb and is_zero(-diff(Mv[i], t) + divS - tau * Mv[i])
    check(f"G-B-{label}07", "%s: Bianchi(b): -dM_i/dt + (div_h S)_i - tau M_i = 0" % label, okb)
    stamp("  family %s done" % label)

def hD(t,x,y):
    # Explicit polynomial example: t>-1, x>-1, y and zz arbitrary real.
    return diagonal_matrix(SR,[(1+t)**2,(1+x)**2,1])

def hO(t,x,y):
    # Positive definite for t>-1; determinant=(1+t)^2*(1+x^2).
    return matrix(SR,[[(1+t)*(1+t*t),(1+t)*t,0],[(1+t)*t,1+t,0],[0,0,1+x*x]])
