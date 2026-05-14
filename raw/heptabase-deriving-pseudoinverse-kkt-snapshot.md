---
title: Deriving the Pseudoinverse: Where the Formulas Come From
source: Heptabase AI Tutor
course: Robot Kinematics and Control
lesson: Inverse Kinematics in Practice
card_id: 13cfb60d-4dcc-4dbb-8aed-ad773ef0b70c
saved: 2026-05-14
---

# Deriving the Pseudoinverse: Where the Formulas Come From

Local research snapshot from the user's Heptabase AI Tutor lesson.

## Context

The lesson explains why the two common Jacobian pseudoinverse formulas arise:

```math
J^\dagger = J^T(JJ^T)^{-1}
```

for a fat Jacobian with full row rank, and

```math
J^\dagger = (J^TJ)^{-1}J^T
```

for a tall Jacobian with full column rank.

## KKT-related passage summary

For a fat Jacobian `J in R^{m x n}` with `n > m`, the IK velocity equation

```math
J\dot{\theta} = \mathcal{V}_d
```

has infinitely many exact solutions when `J` has full row rank. The lesson chooses the minimum-norm solution:

```math
\min_{\dot{\theta}} \frac{1}{2}\|\dot{\theta}\|^2
\quad \text{subject to} \quad
J\dot{\theta} = \mathcal{V}_d.
```

Introducing a Lagrange multiplier `lambda in R^m` gives:

```math
L(\dot{\theta}, \lambda)
= \frac{1}{2}\dot{\theta}^T\dot{\theta}
- \lambda^T(J\dot{\theta} - \mathcal{V}_d).
```

The stationarity condition is:

```math
\dot{\theta} - J^T\lambda = 0,
```

so:

```math
\dot{\theta} = J^T\lambda.
```

The lesson notes that this is the structural result: the optimal joint velocity is a linear combination of the rows of `J`, so it lives in the row space of `J`. It explicitly connects this to KKT optimality conditions and orthogonality.

Substituting back into the constraint gives:

```math
JJ^T\lambda = \mathcal{V}_d,
```

and therefore:

```math
\dot{\theta}^* = J^T(JJ^T)^{-1}\mathcal{V}_d.
```

## Main interpretation

The pseudoinverse formulas are optimization results, not arbitrary algebraic tricks. The fat-Jacobian formula comes from an equality-constrained minimum-norm problem solved with Lagrange multipliers; this is the equality-only special case of the KKT framework. The tall-Jacobian formula comes from an unconstrained least-squares problem and its normal equations.

## Heptabase sources cited by the lesson

- Modern Robotics, Ch. 6, section 6.2.2: Numerical IK and the pseudoinverse.
- Lay, Linear Algebra and Its Applications: null spaces, rank-nullity, orthogonal projections, least squares, and SVD.
