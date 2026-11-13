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

def quadric_infinity():
    a=var('a', domain='positive')
    stamp("Part 2: complex product quadric, Theorem 8.2 / 8.6 directions and conics")
    eta, s, S, T, z, r = var('eta s S T z r')
    phi = var('phi', domain='real')
    H1 = diagonal_matrix(SR, [1, -1, -1]); H2 = diagonal_matrix(SR, [-1, -1, -1])
    B1 = lambda u, v: u * H1 * v
    B2 = lambda u, v: u * H2 * v
    e1 = vector(SR, [1, 0, 0]); e2 = vector(SR, [0, 1, 0]); e3 = vector(SR, [0, 0, 1])
    x1 = vector(SR, [0, a, 0]); x2 = a * e3
    k = vector(SR, [a * cosh(eta), 0, a * sinh(eta)])
    u = (a / 2) * ((z + 1 / z) * e1 - I * (z - 1 / z) * e2)
    check('G-B-S12', "x1 in Q1, x2 in Q2", is_zero(B1(x1, x1) + a**2) and is_zero(B2(x2, x2) + a**2))
    check('G-B-S13', "H1(k,k)=a^2, H1(x1,k)=0", is_zero(B1(k, k) - a**2) and is_zero(B1(x1, k)))
    check('G-B-S14', "H2(u,u)=-a^2, H2(x2,u)=0", is_zero(B2(u, u) + a**2) and is_zero(B2(x2, u)))
    check('G-B-S15', "u(z) real for |z|=1",
          allzero([imag_part(c.subs(z=exp(I * phi))).simplify_full() for c in u]) if True else False)
    g1 = x1 * cosh(s) + k * sinh(s); g2 = x2 * cos(s) + u * sin(s)
    d1 = diff(g1, s); d2 = diff(g2, s)
    check('G-B-S16', "gamma stays on Q1 x Q2", is_zero(B1(g1, g1) + a**2) and is_zero(B2(g2, g2) + a**2))
    check('G-B-S17', "gamma tangent to quadrics", is_zero(B1(g1, d1)) and is_zero(B2(g2, d2)))
    check('G-B-S18', "gamma null", is_zero(B1(d1, d1) + B2(d2, d2)))
    check('G-B-S19', "gamma geodesic: x_i''=(eps_i/a^2)x_i",
          allzero(list(diff(g1, s, 2) - (B1(d1, d1) / a**2) * g1) + list(diff(g2, s, 2) - (B2(d2, d2) / a**2) * g2)))
    y1 = x1 * cosh(pi) + k * sinh(pi); kp = x1 * sinh(pi) + k * cosh(pi)
    check('G-B-S20', "endpoint at s=pi is (y1,-x2) with velocity (k',-u)",
          allzero(list(g1.subs(s=pi) - y1) + list(g2.subs(s=pi) + x2) + list(d1.subs(s=pi) - kp) + list(d2.subs(s=pi) + u)))
    v = a * (S**2 + T**2) * e1 - I * a * (S**2 - T**2) * e2
    check('G-B-S21', "2ST*u(S/T) = v(S,T)", allzero(list(2 * S * T * u.subs(z=S / T) - v)))
    check('G-B-S22', "conic alpha: H1(2STk,2STk)=4a^2S^2T^2, H2(v,v)=-4a^2S^2T^2 (null)",
          is_zero(B1(2 * S * T * k, 2 * S * T * k) - 4 * a**2 * S**2 * T**2) and is_zero(B2(v, v) + 4 * a**2 * S**2 * T**2))
    check('G-B-S23', "conic alpha tangent at x; conic beta tangent at y",
          is_zero(B1(x1, k)) and is_zero(B2(x2, v)) and is_zero(B1(y1, kp)) and is_zero(B2(-x2, -v)) and is_zero(B1(kp, kp) - a**2))
    R2 = PolynomialRing(QQ, 'S,T'); SS, TT = R2.gens()
    check('G-B-S24', "v(S,T)=0 only at S=T=0 (radical of (S^2+T^2,S^2-T^2) is (S,T))",
          R2.ideal([SS**2 + TT**2, SS**2 - TT**2]).radical() == R2.ideal([SS, TT]))
    vp = a * (e1 - I * e2)
    check('G-B-S25', "[1:0]: v(1,0)=v_+, null and tangent at x2 and at -x2",
          allzero(list(v.subs(S=1, T=0) - vp)) and is_zero(B2(vp, vp)) and is_zero(B2(x2, vp)))
    leaf = -x2 + s * vp
    check('G-B-S26', "leaf through (y,[0,v_+]) stays in Q2 with constant first factor (eps=0 line)",
          is_zero(B2(leaf, leaf) + a**2))
    dpw = diff(y1, eta).subs(eta=0)
    check('G-B-S27', "dp(w) = (a sinh(pi) e_3, 0) != 0", allzero(list(dpw - a * sinh(pi) * e3)) and is_zero(dpw[2]/(a*sinh(pi))-1))
    Mrank = matrix(SR, [list(dpw) + [0, 0, 0], [0, 0, 0] + list(vp)])
    check('G-B-S28', "dp(w) not in C*(0,v_+): rank 2", Mrank.rank() == 2)

    # ---------------------------------------------------------------- Part 3
    stamp("Part 3: Prop 8.3 nonclosed sequence")
    rr = var('rr', domain='positive')
    u2 = a * e1
    k1 = (a / 2) * vector(SR, [1 + rr**2, 0, 1 - rr**2]); k2 = rr * u2
    check('G-B-S29', "k1 tangent at x1 with H1(k1,k1)=a^2 r^2; k2=r u2 tangent at x2; null",
          is_zero(B1(x1, k1)) and is_zero(B1(k1, k1) - a**2 * rr**2) and is_zero(B2(x2, k2)) and is_zero(B1(k1, k1) + B2(k2, k2)))
    G1 = x1 * cosh(rr * s) + (1 / rr) * k1 * sinh(rr * s)
    G2 = x2 * cos(rr * s) + (1 / rr) * k2 * sin(rr * s)
    check('G-B-S30', "general solution is a null geodesic on Q1 x Q2",
          is_zero(B1(G1, G1) + a**2) and is_zero(B2(G2, G2) + a**2)
          and allzero(list(diff(G1, s, 2) - rr**2 * G1) + list(diff(G2, s, 2) + rr**2 * G2)))
    sr = 2 * pi * I / rr
    y2 = x2 * cosh(2 * pi) + I * u2 * sinh(2 * pi)
    check('G-B-S31', "at s_r: first factor and tangent return to (x1,k1)",
          allzero(list(G1.subs(s=sr) - x1) + list(diff(G1, s).subs(s=sr) - k1)))
    check('G-B-S32', "at s_r: second factor = x2 cosh 2pi + i u2 sinh 2pi, tangent r(u2 cosh2pi - i x2 sinh 2pi)",
          allzero(list(G2.subs(s=sr) - y2) + list(diff(G2, s).subs(s=sr) - rr * (u2 * cosh(2 * pi) - I * x2 * sinh(2 * pi)))))
    check('G-B-S33', "limiting second endpoints are distinct: y2 != x2", not allzero(list(y2 - x2)))
    check('G-B-S34', "limit direction k1(0) is H1-null (pure first-factor leaf)", is_zero(B1(k1.subs(rr=0), k1.subs(rr=0))))
    zz = var('zz')
    yy1 = x1 * cosh(zz) + (1 / rr) * k1 * sinh(zz)
    yy2 = x2 * cos(zz) + (1 / rr) * k2 * sin(zz)
    check('G-B-S35', "Prop 8.4: cosh z = -a^-2 H1(x1,y1), cos z = -a^-2 H2(x2,y2)",
          is_zero(cosh(zz) + B1(x1, yy1) / a**2) and is_zero(cos(zz) + B2(x2, yy2) / a**2))

    # ---------------------------------------------------------------- Part 4
    stamp("Part 4: Prop 6.1 infinity pair normalization")
    c = var('c')
    J2 = matrix(SR, [[0, 1], [-1, 0]])
    Icov = block_diagonal_matrix(-c * J2, J2); Icon = block_diagonal_matrix(J2, -c * J2)
    check('G-B-S36', "I_cov I_contra = c * Id", allzero((Icov * Icon - c * identity_matrix(SR, 4)).list()))
    check('G-B-S37', "2 Pf(I_cov) = -2c = -Lambda/3 for c=Lambda/6", is_zero(2 * Icov.pfaffian() + 2 * c))
    check('G-B-S38', "rank 4 at c=1, rank 2 at c=0", Icov.subs(c=1).rank() == 4 and Icov.subs(c=0).rank() == 2)

