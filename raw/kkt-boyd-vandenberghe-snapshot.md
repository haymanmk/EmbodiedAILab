---
title: Convex Optimization - KKT and Lagrange duality notes
source_url: https://web.stanford.edu/~boyd/cvxbook/
book_pdf: https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf
authors: Stephen Boyd, Lieven Vandenberghe
saved: 2026-05-14
---

# Convex Optimization - KKT and Lagrange duality notes

Local research snapshot for KKT conditions and their relationship to Lagrange multipliers.

## Relevant source

Stephen Boyd and Lieven Vandenberghe, *Convex Optimization*, Chapter 5, especially section 5.5 "Optimality conditions."

## Standard constrained problem form

```math
\begin{aligned}
\text{minimize} \quad & f_0(x) \\
\text{subject to} \quad & f_i(x) \le 0, \quad i = 1,\dots,m \\
& h_i(x) = 0, \quad i = 1,\dots,p.
\end{aligned}
```

The Lagrangian is:

```math
L(x,\lambda,\nu)
= f_0(x) + \sum_{i=1}^{m}\lambda_i f_i(x)
+ \sum_{i=1}^{p}\nu_i h_i(x).
```

## KKT conditions

The KKT conditions are:

```math
f_i(x^\star) \le 0
```

```math
h_i(x^\star) = 0
```

```math
\lambda_i^\star \ge 0
```

```math
\lambda_i^\star f_i(x^\star) = 0
```

```math
\nabla f_0(x^\star)
+ \sum_i \lambda_i^\star \nabla f_i(x^\star)
+ \sum_i \nu_i^\star \nabla h_i(x^\star) = 0.
```

These correspond to primal feasibility, dual feasibility, complementary slackness, and stationarity.

## Key interpretation

Inequality multipliers must be nonnegative. Complementary slackness means an inequality multiplier can be nonzero only when its constraint is active. Equality multipliers are unrestricted in sign.

For equality-only problems, the inequality pieces disappear and KKT reduces to the ordinary Lagrange multiplier equations: satisfy the equality constraints and make the gradient of the Lagrangian with respect to the primal variables vanish.

## Convexity note

For differentiable convex optimization problems with suitable regularity, KKT conditions are sufficient for global optimality. In nonconvex problems, they are generally first-order necessary conditions under assumptions, not a guarantee of global optimality.
