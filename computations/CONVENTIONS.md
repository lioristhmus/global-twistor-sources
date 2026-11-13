# Mathematical conventions

All current manuscript locators refer to v1.0 and its source/PDF hashes in MANUSCRIPT-LOCATORS.json. Historical execution versions are recorded in provenance.json.

- Curvature: `R(a,b)=[nabla_a,nabla_b]-nabla_[a,b]`;
  `Ric(b,c)=trace(a -> R(a,b)c)`. A stores
  `R[d,c,u,v]=[R(partial_u,partial_v)partial_c]^d` and contracts
  `Ric[b,c]=sum_u R[u,c,u,b]`. Sage B uses its `(1,3)` curvature/Weyl arrays
  in the corresponding order, with its convention checked on the stated metric.
- Coordinates: Python arrays are zero based. Real Nariai order is
  `(t,theta,chi,phi)` in A and `(t,th,vt,ph)` in B; `vt=chi`.
  Signature is `+---`, dimension four and `Lambda=-1/a^2`, `a>0`.
- Ambient quadrics: `H1=diag(1,-1,-1)`, `H2=-Id_3`;
  both quadric equations are `H_i(x_i,x_i)=-a^2`.
  Script `e3=(0,0,1)` is the third first-factor vector called `e_2`
  in the zero-based first-factor convention in the proof of Theorem 8.2.
- Tractor basis: `(sigma,mu0,mu1,mu2,mu3,rho)`,
  `H=2*sigma*rho+g(mu,mu)`, `X=(0,0,0,0,0,1)`,
  `I=(1,0,0,0,0,-Lambda/6)`. Normalization is
  `H(I,I)=-Lambda/3`, `H(I,X)=1`, `H(X,X)=0`.
  In A the Levi-Civita frame is parallel at the point. B retains coordinate
  Christoffels on Nariai and differentiates the connection matrices.
- Infinity pair: `c=Lambda/6`, `J=[[0,1],[-1,0]]`,
  `I_cov=diag(-c*J,J)`, `I_contra=diag(J,-c*J)` in the marked volume.
  Thus the exact target is `I_cov*I_contra=c*Id` and `2 Pf(I_cov)=-2c`.
  The implemented rank samples are c=1 and c=0.
- Gaussian calculation: `ghat=-dt^2+h_t`, of signature `-+++` for positive h;
  the physical metric is `g=-ghat`, and `lam=-Lambda`.
  `K=(1/2)partial_t h`, `tau=tr_h K`, `E=Ric(ghat)-lam*ghat`.
  This is the paper's `K(v,w)=-g(nabla_v n,w)` convention.
  A sets spatial Christoffels to zero at one normal point and `E_ij=0`.
  B checks full Bianchi residuals before this specialization in the two
  explicit polynomial metrics specified in inputs.json.
- Scalar constants are integers/rationals or exact symbolic constants.
  No random seed, tolerance or floating point sampling enters a mathematical test.
  CAS simplification tests exact equality; the declared positive-factor side
  conditions for nonvanishing are recorded explicitly in the input profiles.

The universal-jet checks use the same curvature and Gaussian sign conventions. Their spatial normalization and all inverse-metric derivatives are detailed in [JET-SCOPE.md](JET-SCOPE.md). No first spatial derivatives are suppressed.
