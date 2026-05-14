---
type: concept
domain: research
created: 2026-05-14
updated: 2026-05-14
aliases: ["Lagrangian multipliers", "Lagrange multiplier method"]
tags: [optimization, constrained-optimization, robotics-math]
---

# Lagrange Multipliers

## Definition

Lagrange multipliers are auxiliary variables used to solve constrained optimization problems. For an equality-constrained problem

$$
\min_x f(x)
\quad \text{subject to} \quad
h(x)=0,
$$

the Lagrangian is:

$$
L(x,\lambda)=f(x)+\lambda^T h(x).
$$

At an optimum, the gradient of the objective cannot point in an arbitrary direction: it must be balanced by the gradients of the active constraints. Algebraically, this is the stationarity condition:

$$
\nabla_x L(x^\star,\lambda^\star)=0.
$$

## Geometric intuition

For one equality constraint $h(x)=0$, the feasible points form a curve or surface. At the constrained optimum, you cannot improve $f$ by moving along that surface. That means the objective's gradient is perpendicular to the feasible surface.

The constraint gradient $\nabla h(x)$ is also perpendicular to the surface $h(x)=0$. Therefore, at the optimum, these two gradients must be parallel:

$$
\nabla f(x^\star) + \lambda^\star \nabla h(x^\star)=0.
$$

This is the geometric heart of Lagrange multipliers: **at the best feasible point, the objective gradient is balanced by the constraint gradient**.

## Step-by-step method

For an equality-constrained problem:

$$
\min_x f(x)
\quad \text{subject to} \quad
h(x)=0,
$$

use this procedure:

1. Build the Lagrangian:

$$
L(x,\lambda)=f(x)+\lambda h(x).
$$

2. Set stationarity:

$$
\nabla_x L(x,\lambda)=0.
$$

3. Keep the original constraint:

$$
h(x)=0.
$$

4. Solve the combined equations for $x$ and $\lambda$.

The multiplier $\lambda$ is not the main object you usually care about. It is the variable that makes the constraint's influence explicit, so the constrained problem can be solved as a system of equations.

## Tiny example

Find the point on the line $x+y=1$ closest to the origin. This is:

$$
\min_{x,y}\frac{1}{2}(x^2+y^2)
\quad \text{subject to} \quad
x+y-1=0.
$$

The Lagrangian is:

$$
L(x,y,\lambda)
=\frac{1}{2}(x^2+y^2)+\lambda(x+y-1).
$$

Stationarity gives:

$$
\frac{\partial L}{\partial x}=x+\lambda=0,
\qquad
\frac{\partial L}{\partial y}=y+\lambda=0.
$$

So:

$$
x=-\lambda,\qquad y=-\lambda.
$$

Use the constraint:

$$
x+y=1.
$$

Substitute:

$$
-\lambda-\lambda=1,
$$

so:

$$
\lambda=-\frac{1}{2}.
$$

Therefore:

$$
x=y=\frac{1}{2}.
$$

The closest feasible point is:

$$
\left(\frac{1}{2},\frac{1}{2}\right).
$$

This example is the same pattern as the fat-Jacobian pseudoinverse derivation: minimize a norm subject to a linear equality.

## Relationship to KKT

[[Karush-Kuhn-Tucker Conditions]] are the broader framework. Lagrange multipliers are the constraint variables inside that framework.

- Equality-only constrained optimization: Lagrange multiplier method and KKT stationarity are essentially the same first-order condition.
- Inequality-constrained optimization: KKT adds nonnegative multipliers, complementary slackness, and feasibility requirements.

So "KKT multiplier" and "Lagrange multiplier" often refer to the same mathematical object, but KKT gives the complete rules for equality and inequality constraints.

## Pseudoinverse example

In the minimum-norm inverse-kinematics problem

$$
\min_{\dot{\theta}} \frac{1}{2}\|\dot{\theta}\|^2
\quad \text{subject to} \quad
J\dot{\theta}=\mathcal{V}_d,
$$

the Lagrange multiplier $\lambda$ enforces the velocity constraint. The stationarity equation gives:

$$
\dot{\theta}=J^T\lambda.
$$

This says the minimum-norm joint velocity has no null-space component. It lives in the row space of $J$; any extra null-space motion would increase norm without changing the end-effector twist.

## Why it feels like a "constraint force"

In mechanics, constraints restrict motion. A bead on a wire cannot move off the wire because the wire supplies a constraint force. Lagrange multipliers play a similar mathematical role: they measure how strongly the constraint must push back to keep the optimum feasible.

In inverse kinematics, the equality constraint

$$
J\dot{\theta}=\mathcal{V}_d
$$

says "the joint velocity must produce this exact end-effector twist." The multiplier $\lambda$ is the mathematical object that enforces that requirement in the optimization. It is not a physical force here, but it behaves like one in the equations: it tells how the constraint changes the optimal direction.

## Related concepts

- [[Karush-Kuhn-Tucker Conditions]]
- [[Moore-Penrose Pseudoinverse]]
- [[Robotics Development Stack]]

## Mentions

- [[Deriving the Pseudoinverse Where the Formulas Come From - Heptabase AI Tutor]]

## External sources

- Boyd and Vandenberghe, *Convex Optimization*: https://web.stanford.edu/~boyd/cvxbook/
