---
type: source
domain: research
created: 2026-05-14
updated: 2026-05-14
source_url: heptabase://card/13cfb60d-4dcc-4dbb-8aed-ad773ef0b70c
source_path: raw/heptabase-deriving-pseudoinverse-kkt-snapshot.md
author: Heptabase AI Tutor
published: 2026-05-14
tags: [robotics, inverse-kinematics, pseudoinverse, kkt, lagrange-multipliers]
---

# Deriving the Pseudoinverse Where the Formulas Come From - Heptabase AI Tutor

## Summary

This Heptabase AI Tutor card derives the two familiar Jacobian pseudoinverse formulas from optimization problems rather than treating them as algebraic recipes. For a fat Jacobian, the right pseudoinverse $J^T(JJ^T)^{-1}$ comes from minimizing joint-velocity norm subject to exactly achieving the desired task-space velocity. For a tall Jacobian, the left pseudoinverse $(J^T J)^{-1}J^T$ comes from minimizing least-squares task-space error. The card mentions KKT optimality in the fat-Jacobian case because the stationarity equation of the equality-constrained Lagrangian gives the key structural result: the minimum-norm solution lies in the row space of $J$.

## Key claims

- The pseudoinverse formulas come from optimization, not from visual symmetry.
- In the fat-Jacobian case, the problem is equality-constrained: minimize $\frac{1}{2}\|\dot{\theta}\|^2$ subject to $J\dot{\theta}=\mathcal{V}_d$.
- The Lagrange multiplier stationarity condition gives $\dot{\theta}=J^T\lambda$, meaning the minimum-norm solution lives in the row space of $J$.
- Substituting the stationarity result into the constraint produces $JJ^T\lambda=\mathcal{V}_d$, which explains why $JJ^T$ appears.
- In the tall-Jacobian case, there is usually no exact solution, so the least-squares normal equations produce $(J^T J)^{-1}J^T$.
- Near singularities, the SVD-based [[Moore-Penrose Pseudoinverse]] is the reliable unified construction.

## Reader's guide

The easiest way to read the lesson is to keep three questions separate:

1. **Is an exact solution possible?** If $J$ has full row rank in the fat case, every task velocity in $\mathbb{R}^m$ is reachable.
2. **If many exact solutions exist, which one should we choose?** The pseudoinverse chooses the minimum-norm joint velocity.
3. **If no exact solution exists, what does "best" mean?** The pseudoinverse chooses the least-squares closest task velocity.

The KKT/Lagrange step appears only in the second question: exact solutions exist, but there are infinitely many, so an optimization criterion is needed to choose one.

## Expanded derivation map

For the fat Jacobian:

$$
\min_{\dot{\theta}}\frac{1}{2}\|\dot{\theta}\|^2
\quad \text{subject to}\quad
J\dot{\theta}=\mathcal{V}_d
$$

leads to:

$$
\dot{\theta}=J^T\lambda
$$

by stationarity. This places $\dot{\theta}$ in $\operatorname{Row}(J)$. Substitution into the constraint gives:

$$
JJ^T\lambda=\mathcal{V}_d,
$$

and therefore:

$$
\dot{\theta}^\star=J^T(JJ^T)^{-1}\mathcal{V}_d.
$$

For the tall Jacobian:

$$
\min_{\dot{\theta}}\|J\dot{\theta}-\mathcal{V}_d\|^2
$$

leads to:

$$
J^TJ\dot{\theta}=J^T\mathcal{V}_d,
$$

and therefore:

$$
\dot{\theta}^\star=(J^TJ)^{-1}J^T\mathcal{V}_d.
$$

The two formulas look similar, but they answer different questions.

## Notable quotes

- "The formulas come from optimization, not algebra."
- "The optimal joint velocity is a linear combination of the rows of $J$."
- "KKT optimality conditions" appear in the lesson as the general constrained-optimization frame behind the Lagrange multiplier step.

## Connections

- [[Karush-Kuhn-Tucker Conditions]]
- [[Lagrange Multipliers]]
- [[Moore-Penrose Pseudoinverse]]
- [[Robotics Development Stack]]

## Open questions

- Should the vault later ingest the relevant Modern Robotics and Lay textbook sections as proper source pages?
- How should damped least squares be filed: under pseudoinverse, singularity handling, or numerical inverse kinematics?
