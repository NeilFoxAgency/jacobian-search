#!/usr/bin/env python3
"""Reproducible experiments around the plane Jacobian conjecture.

This script:
  1. Exactly verifies the July 2026 C^3 counterexample.
  2. Exactly verifies the factorization produced by the target cut b = a*c.
  3. Searches modulo a large prime for a degree <=108 mate B satisfying
         {A,B} = A_x B_y - A_y B_x = 1
     for degree-72 candidates A = x + H(x,y)^2, where H is homogeneous
     of degree 36.

The modular test is a rigorous rejection over F_p. A candidate that fails
mod p cannot be a solution with coefficients whose denominators are nonzero
mod p. A survivor must then be checked exactly over Q/C.

Usage:
    python plane_jacobian_search.py --quick
    python plane_jacobian_search.py --full

The full mode tests all 1,369 monomial/binomial H choices and should find only
the triangular coordinate A=x+y^72, B=y.
"""

from __future__ import annotations

import argparse
import itertools
import time
from collections import Counter

import sympy as sp

PRIME = 1_000_003


def exact_verification() -> None:
    x, y, z = sp.symbols("x y z")
    u = 1 + x*y
    a = sp.expand(u**3*z + y**2*u*(4 + 3*x*y))
    b = sp.expand(y + 3*x*u**2*z + 3*x*y**2*(4 + 3*x*y))
    c = sp.expand(2*x - 3*x**2*y - x**3*z)

    determinant = sp.factor(sp.Matrix([a, b, c]).jacobian([x, y, z]).det())
    assert determinant == -2

    points = [
        (sp.Integer(0), sp.Integer(0), -sp.Rational(1, 4)),
        (sp.Integer(1), -sp.Rational(3, 2), sp.Rational(13, 2)),
        (-sp.Integer(1), sp.Rational(3, 2), sp.Rational(13, 2)),
    ]
    target = (-sp.Rational(1, 4), sp.Integer(0), sp.Integer(0))
    for point in points:
        image = tuple(sp.expand(f.subs(dict(zip((x, y, z), point)))) for f in (a, b, c))
        assert image == target

    f1 = x**2*y*z + 3*x*y**2 + x*z + y
    f2 = x**4*y**2*z + 3*x**3*y**3 + 2*x**3*y*z + 4*x**2*y**2 + x**2*z + x*y + 1
    assert sp.expand(b - a*c - f1*f2) == 0

    q = x*y
    inverse_u = -x**2*z*u - q*(3*q + 1)
    # On f2=0, (1+xy)*inverse_u = 1.
    assert sp.expand(u*inverse_u - 1 + f2) == 0

    print("Exact checks passed:")
    print("  det DF = -2")
    print("  all three listed source points have image (-1/4, 0, 0)")
    print("  b-a*c factors as f1*f2")
    print("  1+xy is a nonconstant unit on f2=0")


Poly = dict[tuple[int, int], int]


def clean(poly: Poly, p: int = PRIME) -> Poly:
    return {m: c % p for m, c in poly.items() if c % p}


def add(a: Poly, b: Poly, scale: int = 1, p: int = PRIME) -> Poly:
    out = dict(a)
    for mon, coeff in b.items():
        out[mon] = (out.get(mon, 0) + scale*coeff) % p
        if out[mon] == 0:
            del out[mon]
    return out


def mul(a: Poly, b: Poly, p: int = PRIME) -> Poly:
    out: Poly = {}
    for (i, j), ca in a.items():
        for (k, ell), cb in b.items():
            mon = (i+k, j+ell)
            out[mon] = (out.get(mon, 0) + ca*cb) % p
    return clean(out, p)


def derivative_x(a: Poly, p: int = PRIME) -> Poly:
    return {(i-1, j): (i*c) % p for (i, j), c in a.items() if i and (i*c) % p}


def derivative_y(a: Poly, p: int = PRIME) -> Poly:
    return {(i, j-1): (j*c) % p for (i, j), c in a.items() if j and (j*c) % p}


def poisson(a: Poly, b: Poly, p: int = PRIME) -> Poly:
    return add(mul(derivative_x(a, p), derivative_y(b, p), p),
               mul(derivative_y(a, p), derivative_x(b, p), p),
               scale=-1, p=p)


def monomial(i: int, j: int, coefficient: int = 1, p: int = PRIME) -> Poly:
    coefficient %= p
    return {} if coefficient == 0 else {(i, j): coefficient}


def monomial_basis(max_degree: int, p: int = PRIME) -> list[Poly]:
    return [monomial(i, degree-i, p=p)
            for degree in range(max_degree+1)
            for i in range(degree+1)]


def pivot_key(mon: tuple[int, int]) -> tuple[int, int, int]:
    return (mon[0]+mon[1], mon[0], mon[1])


def span_contains(columns: list[Poly], target: Poly, p: int = PRIME) -> tuple[bool, int]:
    """Sparse incremental Gaussian elimination over F_p."""
    echelon: dict[tuple[int, int], Poly] = {}
    for column in columns:
        vector = clean(column, p)
        while vector:
            pivot = max(vector, key=pivot_key)
            if pivot in echelon:
                vector = add(vector, echelon[pivot], scale=-vector[pivot], p=p)
            else:
                inv = pow(vector[pivot], -1, p)
                vector = {m: (c*inv) % p for m, c in vector.items()}
                echelon[pivot] = vector
                break

    vector = clean(target, p)
    while vector:
        pivot = max(vector, key=pivot_key)
        if pivot not in echelon:
            return False, len(echelon)
        vector = add(vector, echelon[pivot], scale=-vector[pivot], p=p)
    return True, len(echelon)


def has_mate(a: Poly, b_basis: list[Poly], p: int = PRIME) -> tuple[bool, int]:
    columns = [poisson(a, basis_element, p) for basis_element in b_basis]
    return span_contains(columns, {(0, 0): 1}, p)


def degree_72_search(full: bool) -> None:
    p = PRIME
    degree_36_monomials = [monomial(i, 36-i, p=p) for i in range(37)]
    b_basis = monomial_basis(108, p)

    specs: list[tuple[int, int | None, int]] = []
    for i in range(37):
        specs.append((i, None, 1))
    for i, j in itertools.combinations(range(37), 2):
        specs.append((i, j, 1))
        specs.append((i, j, -1))

    if not full:
        # Deterministic representative sample, including the trivial survivor.
        specs = specs[:200]

    survivors = []
    ranks = Counter()
    start = time.time()
    for index, (i, j, sign) in enumerate(specs, start=1):
        h = dict(degree_36_monomials[i])
        if j is not None:
            h = add(h, degree_36_monomials[j], scale=sign, p=p)
        a = add(monomial(1, 0, p=p), mul(h, h, p), p=p)
        possible, rank = has_mate(a, b_basis, p)
        ranks[rank] += 1
        if possible:
            survivors.append((i, j, sign))
        if full and index % 200 == 0:
            print(f"  tested {index}/{len(specs)}")

    print("Degree-(72,108) modular search:")
    print(f"  candidates tested: {len(specs)}")
    print(f"  prime: {p}")
    print(f"  survivors: {survivors}")
    print(f"  ranks: {dict(ranks)}")
    print(f"  elapsed: {time.time()-start:.2f} seconds")
    if full:
        assert survivors == [(0, None, 1)], (
            "Expected only H=y^36, giving the triangular coordinate A=x+y^72."
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--quick", action="store_true", help="Run a representative 200-candidate search")
    mode.add_argument("--full", action="store_true", help="Run all 1,369 homogeneous monomial/binomial H cases")
    args = parser.parse_args()

    exact_verification()
    degree_72_search(full=args.full)


if __name__ == "__main__":
    main()
