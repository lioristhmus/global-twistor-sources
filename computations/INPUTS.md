# Embedded symbolic inputs

The input formulas are embedded in the named functions; no numerical dataset is loaded.

<div id="input-nariai-real"></div>

## nariai-real

- **location**: `code/a_nariai.py:nariai; code/b_nariai_tractor.py:nariai_tractor`

- **variables**: `a>0; t,theta,chi,phi real; 0<chi<pi`

- **metric**: `diag(1,-a^2 cosh(t/a)^2,-a^2,-a^2 sin(chi)^2)`

- **Lambda**: `-1/a^2`

- **signature**: `+---`

- **dimension**: `4`



<div id="input-nariai-conics"></div>

## nariai-conics

- **location**: `code/a_nariai.py:nariai; code/b_quadric_infinity.py:quadric_infinity`

- **variables**: `a>0; eta near 0 real for endpoint derivative; z nonzero complex; [S:T] in P^1; geodesic parameter complex (real segment 0..pi used in paper)`

- **H1**: `diag(1,-1,-1)`

- **H2**: `diag(-1,-1,-1)`

- **x1**: `(0,a,0)`

- **x2**: `(0,0,a)`

- **k**: `a(cosh eta,0,sinh eta)`

- **u**: `a/2 (z+z^-1,-i(z-z^-1),0)`

- **v**: `a(S^2+T^2,-i(S^2-T^2),0)`

- **side_conditions**: `(S,T)!=(0,0); sinh(pi)>0; a>0. The derivative is a sinh(pi) times the third first-factor ambient vector.`



<div id="input-nariai-sequence"></div>

## nariai-sequence

- **location**: `same nariai/conic functions`

- **variables**: `r>0 with r->0 in the paper; code A also verifies polynomial identities with symbolic r`

- **k1r**: `a/2 (1+r^2,0,1-r^2)`

- **k2r**: `r(a,0,0)`

- **sr**: `2*pi*i/r`

- **y2**: `x2*cosh(2*pi)+i*(a,0,0)*sinh(2*pi)`

- **scope**: `A checks a subset; B checks return time, endpoints and limiting null direction. Topological limits are interpreted in the manuscript.`



<div id="input-tractor-general"></div>

## tractor-general

- **location**: `code/a_tractor.py:tractor`

- **metric**: `eta=diag(1,-1,-1,-1)`

- **variables**: `arbitrary symbolic Lambda and v0..v3,w0..w3`

- **H**: `2*sigma*rho+eta(mu,mu)`

- **I**: `(1,0,0,0,0,-Lambda/6)`

- **X**: `(0,0,0,0,0,1)`

- **basis_order**: `sigma,mu0,mu1,mu2,mu3,rho`

- **normalization**: `c=Lambda/6; H(I,I)=-Lambda/3; H(I,X)=1; H(X,X)=0`



<div id="input-tractor-nariai"></div>

## tractor-nariai

- **location**: `code/b_nariai_tractor.py:nariai_tractor`

- **metric**: `nariai-real`

- **variables**: `a>0, all regular coordinates; Lambda=-1/a^2`

- **basis_order**: `sigma,mu0,mu1,mu2,mu3,rho`

- **normalization**: `same rank-six H,I,X as tractor-general; middle block includes coordinate Christoffel symbols`



<div id="input-infinity-pair"></div>

## infinity-pair

- **location**: `code/b_quadric_infinity.py:quadric_infinity, final block`

- **variables**: `symbolic c=Lambda/6; ranks only at c=1 and c=0`

- **J**: `[[0,1],[-1,0]]`

- **I_cov**: `diag(-c*J,J)`

- **I_contra**: `diag(J,-c*J)`

- **orientation**: `marked volume with Pf(diag(aJ,bJ))=a*b`



<div id="input-bianchi-normal"></div>

## bianchi-normal

- **location**: `code/a_bianchi.py:bianchi`

- **signature**: `-+++ for ghat=-g`

- **lambda**: `-Lambda; constant and absent from contracted residual derivatives`

- **variables**: `independent H,M_i and first derivatives, arbitrary symmetric 3x3 K; spatial h_ij=delta_ij, spatial Christoffels zero at the chosen point`

- **indices**: `0=time; i,j=1,2,3 spatial`

- **assumption**: `E_ij=0, E=Ric(ghat)-lambda*ghat; no evolution solution is computed`



<div id="input-gaussian-D"></div>

## gaussian-D

- **location**: `code/b_gaussian.py:hD,run_family`

- **h**: `diag((1+t)^2,(1+x)^2,1)`

- **variables**: `t>-1, x>-1; y and zz arbitrary real`

- **signature**: `ghat=-dt^2+h (-+++ where h is positive); g=-ghat (+---)`

- **lambda**: `arbitrary symbolic lam=-Lambda`

- **K**: `(1/2) d_t h; tau=tr_h K`

- **E**: `Ric(ghat)-lam*ghat`

- **scope**: `One explicit polynomial metric, not an arbitrary-function family. Input resized after the arbitrary-function implementation exceeded the fixed memory cap.`



<div id="input-gaussian-O"></div>

## gaussian-O

- **location**: `code/b_gaussian.py:hO,run_family`

- **h**: `[[ (1+t)*(1+t^2), (1+t)*t, 0 ],[(1+t)*t,1+t,0],[0,0,1+x^2]]`

- **variables**: `t>-1; x,y,zz arbitrary real`

- **signature**: `same as gaussian-D`

- **lambda**: `arbitrary symbolic lam=-Lambda`

- **K**: `(1/2) d_t h; tau=tr_h K`

- **E**: `Ric(ghat)-lam*ghat`

- **scope**: `One explicit polynomial metric, not an arbitrary-function family. Input resized after the arbitrary-function implementation exceeded the fixed memory cap.`



<div id="input-general-jet"></div>

## general-jet

[The jet input catalog](jets/inputs.json) specifies all six entries of h in all four coordinates. The independent 24 first and 60 second derivatives, plus arbitrary symmetric E and its 40 derivatives, are embedded in `jets/code/jet_gaussian.py`. See [JET-SCOPE.md](JET-SCOPE.md) for normalization, Taylor realization and the residual-versus-direct distinction.

<div id="input-third-jet"></div>

## third-jet

The same input catalog adds all 120 independent third derivatives. The executed main is `jets/code/third_gaussian.py`; it imports the hash-pinned 2jet helper. `lam=-Lambda` is constant, `ghat=-g`, and the physical metric signature is +---. All applicable files are listed in `jets/dependency-hashes.json` and the run input hashes.
