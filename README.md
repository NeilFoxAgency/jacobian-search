# Jacobian Search

[![CI](https://github.com/NeilFoxAgency/jacobian-search/actions/workflows/ci.yml/badge.svg)](https://github.com/NeilFoxAgency/jacobian-search/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Reproducible symbolic and finite-field experiments related to the Jacobian conjecture, with a particular focus on whether the recent three-dimensional construction can illuminate the still-open plane case.

## Status

This is an experimental research repository, not a claimed proof or disproof of the plane Jacobian conjecture.

The included code does two different kinds of work:

1. **Exact symbolic verification** over the rationals for explicitly stated polynomial identities.
2. **Finite-field screening** of structured candidate families. These searches can rigorously reject candidates modulo the selected prime, but they do not prove the plane conjecture and they do not exhaust all polynomial maps over the complex numbers.

## What is verified exactly

For the polynomial map \(F=(a,b,c):\mathbb C^3\to\mathbb C^3\),

\[
\begin{aligned}
a&=(1+xy)^3z+y^2(1+xy)(4+3xy),\\
b&=y+3x(1+xy)^2z+3xy^2(4+3xy),\\
c&=2x-3x^2y-x^3z,
\end{aligned}
\]

the verifier confirms:

- \(\det DF=-2\).
- The three distinct points
  \[
  (0,0,-1/4),\quad (1,-3/2,13/2),\quad (-1,3/2,13/2)
  \]
  all map to \((-1/4,0,0)\).
- The target cut \(b=ac\) pulls back as an exact factorization \(b-ac=f_1f_2\).
- On the component \(f_2=0\), the polynomial \(1+xy\) is a nonconstant unit, which rules out that component being isomorphic to \(\mathbb A^2\).

These identities are independently checkable by running the script.

## Critical-degree experiment

Known degree restrictions leave \((72,108)\), and its reversal, as the only hypothetical degree pair below 125 not excluded by the cited 2022 analysis. This repository tests the structured family

\[
A=x+H(x,y)^2,
\]

where \(H\) is homogeneous of degree 36 and is either a monomial or a binomial with coefficients \(\pm1\). For each fixed \(A\), the program asks whether there is any polynomial \(B\) of degree at most 108 satisfying

\[
\{A,B\}=A_xB_y-A_yB_x=1
\]

modulo a large prime.

The complete family contains 1,369 candidates. The expected sole survivor is the triangular coordinate

\[
A=x+y^{72},\qquad B=y.
\]

All other candidates in this ansatz fail the modular linear system.

## Quick start

```bash
git clone https://github.com/NeilFoxAgency/jacobian-search.git
cd jacobian-search
python -m venv .venv
source .venv/bin/activate
pip install -e .[test]
python plane_jacobian_search.py --quick
```

Run the full 1,369-case homogeneous search:

```bash
python plane_jacobian_search.py --full
```

Run the test suite:

```bash
pytest
```

## Expected quick-mode output

```text
Exact checks passed:
  det DF = -2
  all three listed source points have image (-1/4, 0, 0)
  b-a*c factors as f1*f2
  1+xy is a nonconstant unit on f2=0
Degree-(72,108) modular search:
  candidates tested: 200
  survivors: [(0, None, 1)]
```

Timing depends on hardware. Quick mode takes only a few seconds on a typical modern laptop. Full mode is intentionally more expensive.

## Repository layout

```text
.
├── plane_jacobian_search.py   # Exact verifier and modular search engine
├── docs/FINDINGS.md           # Detailed mathematical and computational log
├── tests/test_exact.py        # Exact regression tests
├── pyproject.toml             # Package and dependency metadata
├── CITATION.cff               # Citation metadata
├── CONTRIBUTING.md            # Contribution standards
└── .github/workflows/ci.yml   # Automated verification
```

## Reading the evidence correctly

A failed modular test means the selected candidate does not admit the requested mate over that finite field. This is powerful for eliminating explicit candidates, but it must not be generalized into a theorem about every characteristic-zero map.

A modular survivor is only a lead. It must be reconstructed and checked exactly over \(\mathbb Q\) or \(\mathbb C\). The included triangular survivor passes because it is already an obvious polynomial automorphism.

The detailed search log distinguishes:

- exact symbolic results,
- exhaustive searches within a declared finite ansatz,
- sampled exploratory searches,
- and proposed next directions.

See [docs/FINDINGS.md](docs/FINDINGS.md).

## Sources and context

- J. A. Guccione, J. J. Guccione, R. Horruitiner, and C. Valqui, "Increasing the degree of a possible counterexample to the Jacobian Conjecture from 100 to 108," arXiv:2204.14178: https://arxiv.org/abs/2204.14178
- Zihan Zhang, "Direct Consequences of the Three-Dimensional Counterexample to the Jacobian Conjecture," July 20, 2026: https://zzhang-iu.github.io/papers/direct-consequences-jacobian/
- MathOverflow discussion of the cubic structure of the construction: https://mathoverflow.net/questions/513387/

The public three-dimensional example is extremely recent. The code in this repository verifies the displayed algebra directly and does not rely on social-media authority.

## Contributing

Counterexamples, improved rejection lemmas, exact reformulations, faster sparse linear algebra, and independent verification are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

Every claimed result should state whether it is:

- exact over characteristic zero,
- exact over a finite field,
- exhaustive within a specified finite family,
- or heuristic/sampled.

## License

Code and original documentation in this repository are released under the [MIT License](LICENSE). Mathematical formulas and facts are not owned by this repository, and cited sources retain their own licenses and attribution requirements.
