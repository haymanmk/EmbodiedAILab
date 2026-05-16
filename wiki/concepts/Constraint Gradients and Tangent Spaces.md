---
type: concept
domain: research
created: 2026-05-15
updated: 2026-05-16
aliases: ["constraint gradient", "tangent plane of a constraint", "tangent space of a level set", "level set normal"]
tags: [optimization, constrained-optimization, differential-geometry, robotics-math]
---

# Constraint Gradients and Tangent Spaces

## Definition

For an equality constraint

$$
h(x)=0,
$$

the feasible set is a level set of $h$. At a regular point $x$ where $\nabla h(x)\ne 0$, the gradient $\nabla h(x)$ is normal to the tangent line, tangent plane, or tangent space of that feasible set.

The tangent directions are exactly the directions $v$ that do not change the constraint to first order:

$$
\nabla h(x)^T v = 0.
$$

So the tangent space is:

$$
T_x = \{v : \nabla h(x)^T v = 0\}.
$$

This is the core geometric fact behind [[Lagrange Multipliers]]: if a constrained optimum has no improving direction along the tangent space, then the objective gradient must also be normal to the feasible set.

## Why the gradient is normal

Take a small feasible step from $x$ in direction $v$. A first-order Taylor expansion gives:

$$
h(x+\epsilon v)
\approx h(x)+\epsilon \nabla h(x)^T v.
$$

If $x$ is feasible, then $h(x)=0$. To remain feasible to first order, the change in $h$ must vanish:

$$
\nabla h(x)^T v = 0.
$$

That equation says every feasible tangent direction is perpendicular to $\nabla h(x)$. Therefore $\nabla h(x)$ is a normal vector to the constraint surface.

## Dimensions

- In 2D, $h(x,y)=0$ usually forms a curve. The gradient $\nabla h(x,y)$ is perpendicular to the tangent line.
- In 3D, $h(x,y,z)=0$ usually forms a surface. The gradient $\nabla h(x,y,z)$ is perpendicular to the tangent plane.
- In $n$ dimensions, $h(x)=0$ usually forms an $(n-1)$-dimensional hypersurface. The gradient $\nabla h(x)$ spans the normal direction, and the tangent space contains all vectors orthogonal to it.

## Multiple equality constraints

For multiple equality constraints

$$
h(x)=0,\qquad h:\mathbb{R}^n\to\mathbb{R}^m,
$$

the Jacobian $J_h(x)$ stacks the constraint gradients. Tangent directions must satisfy:

$$
J_h(x)v=0.
$$

So the tangent space is the null space of the constraint Jacobian:

$$
T_x = \operatorname{null}(J_h(x)).
$$

The normal space is spanned by the rows of $J_h(x)$, equivalently by the individual constraint gradients. This is why equality-constrained stationarity has the form:

$$
\nabla f(x^\star) + J_h(x^\star)^T \lambda^\star = 0.
$$

The objective gradient is balanced by a linear combination of constraint normals.

## Variations / debates

This picture assumes a regular point: $\nabla h(x)\ne 0$ for one constraint, or full row rank of $J_h(x)$ for multiple independent constraints. If the constraint gradient vanishes or the constraint Jacobian loses rank, the feasible set can have singularities, and the usual tangent-plane intuition may break down.

## Connection to robotics: holonomic constraints

In [[Modern Robotics - Lynch & Park]] §2.4 (p. 28) this same picture
shows up under a different name. A closed-chain robot's
**loop-closure equations** $g(\theta) = 0$ are equality constraints on
the joint vector $\theta \in \mathbb{R}^n$, and they reduce the
[[Configuration Space]] from $\mathbb{R}^n$ to the level set of $g$ —
an $(n-k)$-dimensional surface, exactly the situation this page
describes.

Differentiating $g(\theta(t)) = 0$ along a trajectory gives the
velocity-level form:

$$
\frac{\partial g}{\partial\theta}(\theta)\,\dot\theta = 0,
$$

i.e., feasible joint velocities $\dot\theta$ lie in the null space of
the constraint Jacobian — the tangent space at $\theta$. Constraints
expressible this way (as the gradient of some $g$) are called
**holonomic** or **integrable** in the robotics literature.

The contrast is **nonholonomic constraints** $A(\theta)\dot\theta = 0$
where no such $g$ exists (a rolling coin is the canonical example).
These give a tangent-space-like restriction on velocities at every
configuration but do *not* reduce the C-space's dimension. The "test"
is exactly the integrability check: try to find a function whose
gradient is $A(\theta)$; if you can't, the constraint is nonholonomic.

## Related concepts

- [[Lagrange Multipliers]]
- [[Karush-Kuhn-Tucker Conditions]]
- [[Moore-Penrose Pseudoinverse]]
- [[Configuration Space]]
- [[Modern Robotics - Lynch & Park]]

## Mentions

- [[Lagrange Multipliers]]
- [[Configuration Space]]
