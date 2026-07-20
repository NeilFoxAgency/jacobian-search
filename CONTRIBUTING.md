# Contributing

Contributions are welcome, especially those that improve reproducibility or turn an exploratory calculation into an exact, reviewable result.

## Standards for mathematical claims

Every pull request should label each substantive claim as one of the following:

- exact over characteristic zero,
- exact over a stated finite field,
- exhaustive within a fully specified finite family,
- sampled or heuristic.

Do not describe a modular rejection as a proof over the complex numbers. Do not describe a sampled search as exhaustive.

## Reproducibility requirements

A computational contribution should include:

- a deterministic command,
- dependency information,
- the precise search space,
- any prime or random seed used,
- expected output or a machine-readable result,
- and a test for short exact identities when practical.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[test]
pytest
python plane_jacobian_search.py --quick
```

## Pull requests

Keep each pull request focused. Explain:

1. the mathematical question,
2. the ansatz or theorem being tested,
3. what the code proves or screens,
4. what remains unproved,
5. the runtime and hardware used.

Code should be readable before it is clever. Sparse algorithms are welcome, but include comments explaining the mathematical representation.

## Responsible disclosure

A plausible plane counterexample should not be announced from a floating-point result. Before making a public claim, provide exact polynomial coefficients, an exact constant-Jacobian verification, distinct colliding points or another exact noninvertibility certificate, and independent reproduction.
