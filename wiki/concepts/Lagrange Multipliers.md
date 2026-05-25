---
type: concept
domain: research
created: 2026-05-14
updated: 2026-05-25
aliases: ["Lagrangian multipliers", "Lagrange multiplier method"]
tags: [optimization, constrained-optimization, robotics-math]
---

# Lagrange Multipliers

## Explain like I'm 5

A Lagrange multiplier is a helper number for a problem where you want the best answer, but the answer must stay on a rule. The rule might be "stay on this line" or "keep this equation equal to zero." Instead of wandering everywhere, the method asks: "At the best allowed point, which way would the objective like to move, and how hard does the rule have to push back?"

## Bridges from

Imagine walking on a painted path in a park while trying to get to the lowest nearby ground. If the path still slopes down in the direction you are allowed to walk, you are not at the lowest point on the path yet. At the best point on that path, the downhill direction points straight off the path, so every allowed step along the paint either goes sideways or uphill. The path's "push back" is the constraint direction, and the helper number $\lambda$ tells how much of that direction is needed to balance the objective's downhill pull.

Where the analogy breaks down: a real constraint can be a high-dimensional surface, not a literal path, and the method assumes a smooth, regular point where the constraint gradient gives a meaningful normal direction. At corners, cusps, or degenerate points, the simple "path has one clean sideways direction" picture can fail.

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

The new variable $\lambda$ is the Lagrange multiplier. Plainly: $\lambda$ measures how strongly the constraint must participate in the optimum. At a constrained optimum, the objective gradient cannot have any useful component along the feasible surface, so it must be balanced by the gradients of the active constraints. Algebraically, this is the stationarity condition:

$$
\nabla_x L(x^\star,\lambda^\star)=0.
$$

For a single scalar equality constraint, this becomes:

$$
\nabla f(x^\star)+\lambda^\star \nabla h(x^\star)=0.
$$

## Geometric intuition

For one equality constraint $h(x)=0$, the feasible points form a curve or surface. At the constrained optimum, you cannot improve $f$ by moving along that surface. That means the objective's gradient is perpendicular to every feasible tangent direction.

![[lagrange-feasible-surface-no-tangent-improvement.svg]]

The constraint gradient $\nabla h(x)$ is also perpendicular to the surface $h(x)=0$; this is the basic [[Constraint Gradients and Tangent Spaces|constraint-gradient/tangent-space relation]]. Therefore, at the optimum, the objective gradient must lie in the same normal space as the constraint gradient:

![[lagrange-objective-and-constraint-gradients-parallel.svg]]

$$
\nabla f(x^\star) + \lambda^\star \nabla h(x^\star)=0.
$$

This is the geometric heart of Lagrange multipliers: **at the best feasible point, the objective gradient has no tangent component left, so a scaled constraint gradient can cancel it**.

![[lagrange-line-contour-tangency.svg]]

For the tiny example below, the objective contours are circles around the origin and the constraint is the line $x+y=1$. The closest feasible point is where a circle first touches the line. At that point, the objective gradient and constraint gradient are parallel normals.

![[lagrange-tangent-component-before-optimum.svg]]

Away from the optimum, $\nabla f$ usually has a component along the feasible tangent. That tangent component means there is still some allowed motion that changes $f$, so the Lagrange stationarity condition is not yet satisfied.

![[lagrange-stationarity-at-optimum.svg]]

At the optimum, the tangent component disappears. The objective gradient is purely normal to the feasible surface, so a scaled constraint gradient can cancel it:

$$
\nabla f(x^\star)+\lambda^\star \nabla h(x^\star)=0.
$$

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

2. Set stationarity with respect to the decision variables:

$$
\nabla_x L(x,\lambda)=0.
$$

3. Keep the original constraint:

$$
h(x)=0.
$$

4. Solve the combined equations for $x$ and $\lambda$.

The multiplier $\lambda$ is not usually the final answer. It is the bookkeeping variable that makes the constraint's influence explicit, so the constrained problem can be solved as a system of equations.

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

This example has the same pattern as the fat-Jacobian pseudoinverse derivation: minimize a norm subject to a linear equality.

## Connection to robotics

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

This is why Lagrange multipliers belong next to [[Moore-Penrose Pseudoinverse]], [[Constraint Gradients and Tangent Spaces]], and later inverse-kinematics material in [[Modern Robotics - Lynch & Park]].

## Why it can feel like a constraint push

A physical railing can stop you from stepping sideways off a path. In the math, the constraint does not literally push, but the multiplier plays a similar accounting role: it tells how much normal-direction influence is needed so the best answer stays feasible.

In inverse kinematics, the equality constraint

$$
J\dot{\theta}=\mathcal{V}_d
$$

says "the joint velocity must produce this exact end-effector twist." The multiplier $\lambda$ is the mathematical object that enforces that requirement in the optimization. It is not a physical force here, but it behaves like one in the equations: it tells how the constraint changes the optimal direction.

## Relationship to KKT

[[Karush-Kuhn-Tucker Conditions]] are the broader framework. Lagrange multipliers are the constraint variables inside that framework.

- Equality-only constrained optimization: the Lagrange multiplier method and KKT stationarity are essentially the same first-order condition.
- Inequality-constrained optimization: KKT adds nonnegative multipliers, complementary slackness, and feasibility requirements.

So "KKT multiplier" and "Lagrange multiplier" often refer to the same mathematical object, but KKT gives the complete rules for equality and inequality constraints.

## Origins / sources

- [[Modern Robotics - Lynch & Park]] App. D uses Lagrange multipliers as part of the optimization background needed for robot mechanics and inverse-kinematics derivations.
- Boyd and Vandenberghe, *Convex Optimization*, gives the broader convex-optimization treatment: https://web.stanford.edu/~boyd/cvxbook/
- [[Deriving the Pseudoinverse Where the Formulas Come From - Heptabase AI Tutor]] uses the multiplier method to expose where the pseudoinverse formula comes from.

## Variations / debates

- Sign convention: some texts write $L=f+\lambda^T h$, while others write $L=f-\lambda^T h$. The sign of $\lambda$ changes, but the optimum $x^\star$ and the geometric balance idea do not.
- Multiple equality constraints: replace the single gradient $\nabla h$ with the span of all constraint gradients, or equivalently the rows of the constraint Jacobian.
- Regularity matters: the clean geometric story assumes the active constraint gradients are independent enough to define a normal space. When this fails, first-order multiplier conditions can become ambiguous or incomplete.
- Inequalities need KKT: an inactive inequality constraint should not push on the solution, so KKT adds complementary slackness to decide which inequalities actually matter.

## Related concepts

- [[Constraint Gradients and Tangent Spaces]]
- [[Karush-Kuhn-Tucker Conditions]]
- [[Moore-Penrose Pseudoinverse]]
- [[Configuration Space]]
- [[Singularity]]

## Mentions

- [[Deriving the Pseudoinverse Where the Formulas Come From - Heptabase AI Tutor]]
- [[Modern Robotics - Lynch & Park]]

## Socratic check

> [!question]
> If $\nabla f$ still has a component along the feasible tangent, what move is still possible?
>
> In the line example $x+y=1$, why does the closest point occur where a circle contour just touches the line instead of crossing it?
>
> In $J\dot{\theta}=\mathcal{V}_d$, what is the constraint, and what is the objective being minimized?
