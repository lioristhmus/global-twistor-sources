# Universal Gaussian identities and their finite-jet reduction

The eleven `GG-...` checks augment the 57 checks retained from candidate rc.1.
They concern the differential-algebraic input to Proposition A.2 of the fixed
manuscript v0.9.2. The two explicit polynomial metrics `hD` and `hO` and all
fourteen SageMath checks on them remain as a separate implementation route.

## Coordinates and independent inputs

Write

$$
\widehat g=-\mathrm dt^2+h_{ij}(t,x^1,x^2,x^3)\,\mathrm dx^i\mathrm dx^j,
\qquad h=h^T>0.
$$

Fix any point $p$. Choose a constant real invertible matrix $L$ with
$L^Th(p)L=\operatorname{Id}$ and use $x=x(p)+Ly$, leaving time unchanged
(up to a translation). The transformed spatial metric is $L^Th(t,x(p)+Ly)L$.
This preserves Gaussian gauge, $K=\partial_t h/2$, and each tested tensor,
covector or scalar equation. Since $L$ is constant, time derivatives and spatial
covariant derivatives acquire only their usual tensor transformations.
No first spatial derivative is set to zero.

The six symmetric entries of $h$ have 24 independent first derivatives,
$6\binom{5}{2}=60$ independent second derivatives and
$6\binom{6}{3}=120$ independent third derivatives in the four coordinates.
The symbol maps sort only the pair of metric indices and the derivative
multi-index. Each resulting index has its own indeterminate. Thus metric
symmetry and commutation of mixed partials are the only imposed relations.
The container checks symbol cardinality, disjointness between orders, Gaussian
time-component constancy and Ricci symmetry before the recorded identities.

Any real assignment to these jets is realized by a symmetric Taylor polynomial

$$
h(x)=\operatorname{Id}
 +\sum_{1\le |\alpha|\le m}\frac{H_\alpha}{\alpha!}(x-p)^\alpha,
\qquad m=2\ \text{or}\ 3.
$$

Its value at $p$ is positive definite, so continuity preserves positive
definiteness in a sufficiently small neighborhood. Consequently the normalized
jets have no additional realizability constraint. The neighborhood may depend
on the coefficients; no uniform radius is required.

## Inverse metric and curvature derivatives

The normalization is imposed only on zeroth-order values. Differentiating the
inverse before evaluating at $p$ gives

$$
\partial_a h^{-1}=-h^{-1}h_a h^{-1},
\qquad
\partial_{ab}h^{-1}
 =h^{-1}h_a h^{-1}h_b h^{-1}
 +h^{-1}h_b h^{-1}h_a h^{-1}
 -h^{-1}h_{ab}h^{-1}.
$$

Both terms quadratic in first derivatives and the second-derivative term are
retained by `dgi` and `ddgi`. The functions `dgam`, `ddgam` and `dric4` apply the
product rule to these expressions, including both first-inverse-derivative terms
in the second connection derivative. For indices from zero to three,
`gam(i,j,k)` represents $\Gamma^i_{jk}$, and `ric4(i,j)` uses

$$
\operatorname{Ric}_{ij}
 =\sum_k\left(\partial_k\Gamma^k_{ij}-\partial_i\Gamma^k_{kj}
 +\sum_l\bigl(\Gamma^k_{kl}\Gamma^l_{ij}
                 -\Gamma^k_{il}\Gamma^l_{kj}\bigr)\right).
$$

This is the manuscript convention
$R(a,b)=[\nabla_a,\nabla_b]-\nabla_{[a,b]}$ and
$\operatorname{Ric}(b,c)=\operatorname{tr}(a\mapsto R(a,b)c)$.
The spatial-only sums in `ric3` give the Ricci tensor of $h_t$.
The derivative of $\tau=\operatorname{tr}_hK$ includes
$\partial_t\tau=\operatorname{tr}(\partial_tK)-2\operatorname{tr}(K^2)$
at the normalized point.

In the direct code, `g0` denotes the covariant metric value. It equals the
inverse value at this point, but `dE` uses the covariant derivative data `dg`,
not `dgi`. The Einstein residual is
$E=\operatorname{Ric}(\widehat g)-\lambda\widehat g$, with constant
$\lambda=-\Lambda$. The physical metric is $g=-\widehat g$.

## The two calculations and their combination

`jets/code/jet_gaussian.py` checks $K$, the complete Gaussian Ricci decomposition
and the Hamiltonian trace identity using general 2jets. It also takes an
independent symmetric residual $E$ with ten entries and forty independent first
derivatives. It computes

$$
B_b=\nabla^aE_{ab}-\tfrac12\partial_b\operatorname{tr}_{\widehat g}E
$$

and compares it with the full Gaussian residual expressions. With
$H=E_{00}$, $M_i=E_{0i}$, $e=\operatorname{tr}_h(E_{ij})$ and
$S_{ij}=E_{ij}-(-H+e)h_{ij}/2$, these expressions are

$$
B_0=-\tfrac12\partial_tH+\operatorname{div}_hM-\tau H
       -\tfrac12\partial_t e-K^{ij}E_{ij},
\qquad
B_i=-\partial_tM_i+(\operatorname{div}_h S)_i-\tau M_i.
$$

This comparison alone does not assert $B=0$ for an arbitrary residual.
`jets/code/third_gaussian.py` separately differentiates the Ricci definition,
substitutes $E=\operatorname{Ric}(\widehat g)-\lambda\widehat g$ and its
actual derivatives, and directly checks all four components $B_b=0$ using
3jets. It does not substitute the desired Gaussian propagation equations.
The time component and the three spatial components run as two bounded jobs.

Combining the general residual rearrangement with this direct curvature
identity gives the Gaussian Bianchi identities. When the spatial residual field
$E_{ij}$ vanishes on a neighborhood, its derivatives vanish as well; hence
$e=0$, $S=Hh/2$, and the identities become

$$
\partial_tH=2\operatorname{div}_hM-2\tau H,
\qquad
\partial_tM_i=\tfrac12\partial_iH-\tau M_i.
$$

The inverse, connection and Ricci formulas have finite differential order.
At $h(p)=\operatorname{Id}$, their tested residuals are polynomials over the
rationals in the independent jet indeterminates and constant $\lambda$.
SymPy's exact expansion returns the zero polynomial. The coordinate argument
and arbitrary Taylor-jet realization therefore transfer these identities to
arbitrary positive-definite $C^3$ spatial metrics in Gaussian coordinates,
including the analytic metrics of Proposition A.2. This is a universal
finite-jet identity check, rather than a finite list of numerical metric samples.
It uses exact CAS arithmetic together with the mathematical reduction above;
it is not a proof checked by a formal proof kernel.

The analytic Cauchy existence/uniqueness theorem, constraint uniqueness,
global hyperbolicity, source descent and maximal-development statements remain
the mathematical arguments of the paper.

## Shared code and provenance

The 3jet code imports the 2jet helper for inverse first derivatives,
connection, connection first derivatives and Ricci values. Its direct
calculation adds inverse second derivatives, connection second derivatives and
Ricci first derivatives. These are complementary calculations with shared
implementation, not two independent implementations. All helpers are pinned in
`jets/dependency-hashes.json`, checked before import, and included in each
applicable run's input hashes. The 2jet parent helper is retained byte for byte;
the direct module clarifies the covariant metric value as `g0`.

The original Sage route treated three diagonal or four partly off-diagonal
functions of $(t,x,y)$. The retained rc.1 Sage examples instead use two explicit
polynomial metrics. The universal-jet route retains all six symmetric entries
and all four coordinate directions. The separate Sage examples provide concrete
checks by a different curvature implementation; they do not establish the
universal input coverage by themselves.
