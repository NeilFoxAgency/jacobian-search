# Findings and Search Log

Last updated: July 20, 2026

## Research question

Can the explicit three-dimensional constant-Jacobian, noninjective polynomial map be reduced, sliced, or imitated to produce a two-dimensional counterexample?

No plane counterexample was found. The work below records what was verified, what was searched, and what failed.

## Evidence labels

Each item is marked with one of four labels:

- **Exact**: symbolic identity or proof over characteristic zero.
- **Finite exhaustive**: every object in a precisely declared finite ansatz was checked.
- **Sampled**: a large but nonexhaustive collection was checked.
- **Interpretive**: a mathematical conclusion or proposed direction based on the results.

## 1. The three-dimensional map

Define

\[
\begin{aligned}
a&=(1+xy)^3z+y^2(1+xy)(4+3xy),\\
b&=y+3x(1+xy)^2z+3xy^2(4+3xy),\\
c&=2x-3x^2y-x^3z.
\end{aligned}
\]

### Exact verification

The included SymPy verifier confirms

\[
\det\frac{\partial(a,b,c)}{\partial(x,y,z)}=-2.
\]

It also confirms that

\[
(0,0,-1/4),\quad (1,-3/2,13/2),\quad (-1,3/2,13/2)
\]

all map to

\[
(-1/4,0,0).
\]

This establishes noninjectivity of the displayed map by direct calculation.

## 2. The cubic fiber description

Set

\[
t=y+\frac1x.
\]

A useful cubic associated with the map is

\[
P(T)=cT^3-2T^2+bT-2a.
\]

The structural observation is that \(P(t)=0\), and the derivative at the selected root is related to \(x^{-1}\). This helps explain how a locally nonsingular map can have multiple global sheets.

The current repository does not yet formalize the full cubic reconstruction in code. It is recorded here as a high-priority exact-verification addition.

## 3. Affine slices through the known collisions

### Result

**Exact, recorded from the exploratory session.** No affine plane through any pair of the three displayed colliding points, followed by any linear two-coordinate projection of the target, produced a nonzero constant planar Jacobian.

### Method

For each collision pair, the full one-parameter family of affine planes containing the connecting line was parameterized. For tangent vectors \(v_1,v_2\), a linear target projection is controlled by a vector \(m\), and the restricted determinant can be written as

\[
m\cdot\bigl(DF(v_1)\times DF(v_2)\bigr).
\]

Requiring the result to be constant gives a symbolic linear system. Polynomial minors in the plane parameter generated the unit ideal in all three cases.

### Reproducibility status

The exploratory symbolic notebook for this calculation has not yet been converted into a clean standalone script. Contributions that package this calculation are welcome.

## 4. Pole-cancellation rings

A two-dimensional analogue was explored using

\[
s=x,\qquad t=y+\frac1{s^k}.
\]

Pole-canceling polynomial expressions can be organized in the ring

\[
R_k=\mathbb C[s,u,v]/(s^kv-u(u-1)),
\]

with

\[
u=s^kt,\qquad v=t(u-1).
\]

The basic brackets are

\[
\{s,u\}=s^k,\qquad
\{s,v\}=2u-1,\qquad
\{u,v\}=ks^{k-1}v.
\]

### The case \(k=1\)

**Exact, recorded from the exploratory session.** The direct \(y+1/x\) construction is obstructed by a period argument. If \(\{A,B\}=1\), then the relevant symplectic form would be exact, but the surface contains a compact real two-cycle with nonzero period.

This rules out the most literal two-variable imitation in the full \(k=1\) ring.

### Higher pole orders

**Finite exhaustive and sampled searches, recorded from the exploratory session.** Structured one-term, two-term, and randomized multi-term candidates were tested for \(k\ge2\), including candidates in the critical \((72,108)\) degree window. No nontrivial mate was found.

These auxiliary search programs have not yet been fully packaged in this repository.

## 5. The critical degree pair \((72,108)\)

A published 2022 analysis excludes every hypothetical plane-counterexample degree pair with maximum below 125 except \((72,108)\) and \((108,72)\).

The included code studies the ansatz

\[
A=x+H^2,
\]

where \(H\) is homogeneous of degree 36.

### Included exhaustive family

The full mode checks:

- all 37 monomial choices for \(H\),
- every two-monomial sum,
- every two-monomial difference.

This gives 1,369 candidates.

For each candidate, the program builds the linear map

\[
B\longmapsto\{A,B\}
\]

on all polynomials \(B\) of degree at most 108 and asks whether the constant polynomial 1 lies in its image over \(\mathbb F_p\).

### Result

**Finite exhaustive within the declared ansatz.** The only survivor is

\[
H=y^{36},\qquad A=x+y^{72},
\]

with the obvious mate

\[
B=y.
\]

This is a triangular polynomial automorphism, not a counterexample.

Every other monomial/binomial \(H\) in the declared family fails the modular system.

### Important limitation

The finite-field calculation does not eliminate all rational or complex polynomial maps. It eliminates the explicitly declared candidates modulo the chosen prime. Repeating a calculation over independent primes can reduce concern about exceptional modular behavior, but it is still not a universal characteristic-zero theorem.

## 6. The target surface \(b=ac\)

The pullback factors exactly as

\[
b-ac=f_1f_2,
\]

where

\[
f_1=x^2yz+3xy^2+xz+y
\]

and

\[
f_2=x^4y^2z+3x^3y^3+2x^3yz+4x^2y^2+x^2z+xy+1.
\]

The two finite colliding points lie on the component \(f_2=0\).

This is a real near-hit: a simple target surface has a reducible pullback, and one component retains a collision.

### Unit obstruction

On \(f_2=0\), the polynomial \(1+xy\) is invertible. An explicit inverse is represented by

\[
-x^2z(1+xy)-xy(3xy+1).
\]

The identity checked by the script is

\[
(1+xy)\left[-x^2z(1+xy)-xy(3xy+1)\right]-1=-f_2.
\]

Therefore \(1+xy\) becomes a nonconstant unit in the coordinate ring of the component.

Because \(\mathbb C[r,s]\), the coordinate ring of \(\mathbb A^2\), has only constant units, the component \(f_2=0\) cannot be isomorphic to an affine plane.

So this restriction is noninjective but is not a counterexample to the plane Jacobian conjecture.

## 7. Search summary from the exploratory session

The broader session tested more than 30,000 structured candidates across several ansatz families. The main groups were:

- affine source slices and linear target projections,
- canonical one-term and two-term candidates in pole-cancellation rings,
- randomized sparse candidates,
- critical-degree sparse candidates for pole orders \(k=2,3,4,5\) and beyond,
- leading-form candidates resembling \(H^2\) and \(H^3\),
- arbitrary degree-at-most-108 mates for selected degree-72 first coordinates,
- primitive target hyperplanes,
- sparse quadratic and cubic target cuts.

No plane counterexample was found.

Only the central exact verifier and homogeneous critical-degree screen are currently packaged as clean reproducible code. The remaining counts are a research log, not a claim that every exploratory script is preserved here.

## 8. What appears unpromising

**Interpretive.** The following direct routes now look weak:

- taking an affine slice through the known collision points,
- using only a linear projection of the three outputs,
- copying the \(y+1/x\) pole trick in two variables,
- sparse monomial perturbations,
- bare \(H^2/H^3\) leading-form constructions,
- low-degree target graph cuts.

## 9. Most promising next direction

The target-surface method still appears structurally interesting.

Seek a polynomially parameterized target surface

\[
(a,b,c)=\bigl(A(r,s),B(r,s),C(r,s)\bigr)
\]

such that:

1. the target surface is isomorphic to \(\mathbb A^2\),
2. its pullback under the three-dimensional map is reducible,
3. one source component is also isomorphic to \(\mathbb A^2\),
4. that component contains at least two points in one fiber,
5. no nonconstant-unit obstruction survives.

The factorization at \(b=ac\) is a concrete seed for this program. A nonlinear coefficient solver could perturb that relation while simultaneously imposing a polynomial parameterization and controlling the cubic fiber factorization.

## 10. Suggested reproducibility roadmap

- Package the affine-slice elimination as an exact SymPy script.
- Add the cubic identity \(P(t)=0\) and derivative relation to the exact tests.
- Add command-line selection of multiple primes.
- Preserve search manifests and machine-readable result files.
- Add deterministic randomized-search seeds.
- Implement sparse rank calculations with SciPy or a dedicated finite-field library.
- Add SageMath verification for independent symbolic confirmation.
- Formalize the short exact identities in Lean or another proof assistant.

## References

1. J. A. Guccione, J. J. Guccione, R. Horruitiner, and C. Valqui, "Increasing the degree of a possible counterexample to the Jacobian Conjecture from 100 to 108," arXiv:2204.14178. https://arxiv.org/abs/2204.14178
2. Zihan Zhang, "Direct Consequences of the Three-Dimensional Counterexample to the Jacobian Conjecture," July 20, 2026. https://zzhang-iu.github.io/papers/direct-consequences-jacobian/
3. MathOverflow, "Galois structure of the new counterexample to the Jacobian conjecture." https://mathoverflow.net/questions/513387/
