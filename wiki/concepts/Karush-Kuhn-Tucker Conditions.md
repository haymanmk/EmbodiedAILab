---
type: concept
domain: research
created: 2026-05-14
updated: 2026-05-14
aliases: ["KKT", "KKT conditions", "KKT optimality", "Karush-Kuhn-Tucker"]
tags: [optimization, constrained-optimization, robotics-math]
---

# Karush-Kuhn-Tucker Conditions

## Definition

Karush-Kuhn-Tucker conditions, usually abbreviated KKT, are first-order optimality conditions for constrained optimization problems. They generalize [[Lagrange Multipliers]] from equality-only constraints to problems that can also include inequality constraints.

For a minimization problem

$$
\min_x f_0(x)
$$

subject to

$$
f_i(x) \le 0,\quad h_j(x)=0,
$$

the Lagrangian is

$$
L(x,\lambda,\nu)
= f_0(x) + \sum_i \lambda_i f_i(x) + \sum_j \nu_j h_j(x).
$$

The KKT conditions are:

- Primal feasibility: the original constraints hold.
- Dual feasibility: inequality multipliers satisfy $\lambda_i \ge 0$.
- Complementary slackness: $\lambda_i f_i(x^\star) = 0$.
- Stationarity: the gradient of the Lagrangian with respect to $x$ is zero.

## How to read the four conditions

KKT looks abstract until each condition is translated into a question:

| Condition | Question it answers | Meaning |
|---|---|---|
| Primal feasibility | Is the candidate solution allowed? | $x^\star$ must satisfy the original constraints. |
| Dual feasibility | Are inequality forces pointing the right way? | For constraints $f_i(x)\le 0$, multipliers must satisfy $\lambda_i\ge 0$. |
| Complementary slackness | Which constraints are actually touching? | Either the constraint is active, $f_i(x^\star)=0$, or its multiplier is zero. |
| Stationarity | Are all first-order forces balanced? | The objective gradient plus constraint-gradient terms sums to zero. |

The most important mental model is: **constraints exert forces only when they are active**. If an inequality constraint is loose, it cannot influence the optimum, so its multiplier must be zero. If it is tight, its multiplier may be positive.

## Tiny inequality example

Consider the constrained problem:

$$
\min_x x^2
\quad \text{subject to} \quad
x \ge 1.
$$

Write the inequality in KKT's usual $\le 0$ form:

$$
1-x \le 0.
$$

The Lagrangian is:

$$
L(x,\lambda)=x^2+\lambda(1-x),
\qquad \lambda\ge 0.
$$

Stationarity gives:

$$
\frac{dL}{dx}=2x-\lambda=0,
$$

so:

$$
\lambda=2x.
$$

Complementary slackness gives:

$$
\lambda(1-x)=0.
$$

There are two possibilities:

- If the constraint is inactive, then $\lambda=0$, so $x=0$ from stationarity. But $x=0$ violates $x\ge 1$, so this is impossible.
- If the constraint is active, then $1-x=0$, so $x=1$. Then $\lambda=2$, which satisfies $\lambda\ge 0$.

Therefore:

$$
x^\star=1.
$$

This example shows the core KKT pattern: the unconstrained minimizer would be $x=0$, but the constraint blocks it, so the optimum sits on the boundary and the multiplier becomes nonzero.

## Relationship to Lagrange multipliers

Lagrange multipliers are the variables attached to constraints. KKT is the full optimality system that tells those multipliers what properties they must satisfy.

For equality-only problems, the inequality conditions disappear. KKT reduces to the classical Lagrange multiplier method:

$$
h(x^\star)=0,
\qquad
\nabla_x L(x^\star,\nu^\star)=0.
$$

So when the Heptabase pseudoinverse lesson says the stationarity equation follows from KKT optimality, it is using the equality-only KKT case. The multiplier $\lambda$ in the fat-Jacobian derivation is a KKT/Lagrange multiplier enforcing the constraint $J\dot{\theta}=\mathcal{V}_d$.

Another way to say it:

- **Lagrange multiplier method**: "I have equality constraints; set up a Lagrangian and solve stationarity plus feasibility."
- **KKT conditions**: "I may have equality and inequality constraints; solve stationarity, feasibility, sign constraints, and complementary slackness."

So Lagrange multipliers are not replaced by KKT. They are one part of KKT.

## Pseudoinverse connection

In [[Deriving the Pseudoinverse Where the Formulas Come From - Heptabase AI Tutor]], the fat-Jacobian case solves:

$$
\min_{\dot{\theta}} \frac{1}{2}\|\dot{\theta}\|^2
\quad \text{subject to} \quad
J\dot{\theta} = \mathcal{V}_d.
$$

The Lagrangian can be written as:

$$
L(\dot{\theta}, \lambda)
= \frac{1}{2}\dot{\theta}^T\dot{\theta}
- \lambda^T(J\dot{\theta} - \mathcal{V}_d).
$$

Stationarity gives:

$$
\dot{\theta} - J^T\lambda = 0,
$$

so:

$$
\dot{\theta}=J^T\lambda.
$$

Substituting into the constraint gives:

$$
JJ^T\lambda=\mathcal{V}_d.
$$

When $J$ has full row rank, $JJ^T$ is invertible, so:

$$
\dot{\theta}^*
= J^T(JJ^T)^{-1}\mathcal{V}_d.
$$

This is the right-pseudoinverse formula. The important point is that $JJ^T$ appears because the KKT/Lagrange stationarity equation puts the solution into the row space of $J$, and the original equality constraint then determines the multiplier.

## Why stationarity means "row space"

In the fat-Jacobian problem, $J$ has shape $m\times n$, so $J^T$ has shape $n\times m$. The equation

$$
\dot{\theta}=J^T\lambda
$$

means $\dot{\theta}$ is a linear combination of the columns of $J^T$. Those columns are exactly the rows of $J$ written as vectors in joint-velocity space.

Therefore:

$$
\dot{\theta}\in \operatorname{Row}(J).
$$

This is why the KKT step is not just algebra. It says the minimum-norm exact solution has no null-space component. If $\eta\in\operatorname{Null}(J)$, then:

$$
J(\dot{\theta}+\eta)=J\dot{\theta}.
$$

So adding $\eta$ does not change the end-effector twist. But if $\dot{\theta}$ is already in the row space, then $\dot{\theta}$ is orthogonal to every null-space vector, and

$$
\|\dot{\theta}+\eta\|^2
=\|\dot{\theta}\|^2+\|\eta\|^2.
$$

Any nonzero null-space addition only makes the joint velocity longer. That is the geometric reason the minimum-norm solution lives in the row space.

## Necessary vs sufficient

KKT conditions are first-order optimality conditions. For convex problems with suitable regularity assumptions, satisfying KKT is enough to prove global optimality. For nonconvex problems, KKT usually identifies candidate local optima, not guaranteed global optima.

The pseudoinverse minimum-norm problem is friendly: the objective $\frac{1}{2}\|\dot{\theta}\|^2$ is convex, the constraint $J\dot{\theta}=\mathcal{V}_d$ is linear, and the solution is unique when the problem is feasible. That is why the KKT/Lagrange derivation gives the answer cleanly.

## Robotics relevance

KKT conditions matter in robotics whenever constraints are explicit:

- inverse kinematics with equality constraints;
- joint limits and velocity limits;
- contact constraints;
- constrained dynamics;
- trajectory optimization with obstacle and actuator constraints.

The pseudoinverse derivation is the simplest useful example because it has only equality constraints. Later robotics problems add inequalities, where complementary slackness becomes physically meaningful: a contact force or joint-limit multiplier is nonzero only when the corresponding constraint is active.

## Related concepts

- [[Lagrange Multipliers]]
- [[Moore-Penrose Pseudoinverse]]
- [[Robotics Development Stack]]

## Mentions

- [[Deriving the Pseudoinverse Where the Formulas Come From - Heptabase AI Tutor]]

## External sources

- Boyd and Vandenberghe, *Convex Optimization*: https://web.stanford.edu/~boyd/cvxbook/
- MIT OCW 15.093J recitation on KKT necessary conditions: https://ocw.mit.edu/courses/15-093j-optimization-methods-fall-2009/resources/mit15_093j_f09_rec10/
