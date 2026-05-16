---
type: concept
domain: research
created: 2026-05-15
updated: 2026-05-16
aliases: ["constraint gradient", "tangent plane of a constraint", "tangent space of a level set", "level set normal"]
tags: [optimization, constrained-optimization, differential-geometry, robotics-math]
---

# Constraint Gradients and Tangent Spaces

## Bridges from

- **A hiker walking along a contour line on a topographic map.** Let
  $h(x, y)$ be elevation. A contour line is the level set $h = c$, and
  $\nabla h$ at any point on the map is the *direction of steepest
  ascent* — straight uphill, perpendicular to the contour. A hiker
  who wants to stay at the same elevation has to walk **perpendicular
  to uphill** — any step with a component along $\nabla h$ would
  change their elevation. So the tangent direction along any contour
  is exactly the direction perpendicular to $\nabla h$.

  *Where the analogy breaks down:* at a summit, saddle, or basin
  bottom, $\nabla h = 0$ — there is no well-defined "uphill," and the
  contour through that point degenerates to a single point or crosses
  itself. The perpendicularity statement requires a *regular point*
  ($\nabla h \ne 0$). And the picture is genuinely 2D-on-a-surface; in
  $n$ dimensions a single $\nabla h$ vector is perpendicular to a
  whole $(n{-}1)$-dimensional hyperplane of tangent directions, which
  the contour-map intuition can't quite render.

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

### The contour-and-gradient picture

The hiker analogy made visual. Below: contour lines of
$h(x,y) = \tfrac{1}{2}x^2 + \tfrac{3}{2}y^2 + 0.4\,xy$, with the level
set $h = 1$ highlighted in red as "the constraint." At sample points
all the way around that constraint, red gradient arrows point
**outward, perpendicular to the curve**. Blue: a tangent direction
plus a right-angle marker at one sample point.

![Gradient arrows perpendicular to the constraint level set h(x,y)=1](../assets/constraint-gradient/contour_field.png)

The gradient always points in the *uphill* direction (toward larger
$h$), and the contour is the locus where $h$ doesn't change — so
gradients and contours meet at right angles wherever $\nabla h \ne 0$.

### What "perpendicular to first order" actually means

The Taylor argument above can be visualized as two side-by-side
experiments at the same point $x$ on the contour $h = 1$. Step the
same Euclidean distance $\epsilon = 0.18$ in two different directions:

![Tangent step stays on the contour to first order; normal step leaves it linearly](../assets/constraint-gradient/tangent_decomposition.png)

- **Left (tangent step).** Move along $v$ with $\nabla h(x)^\top v = 0$.
  The endpoint sits at $h = 1.047$ — almost back on the contour. The
  small leftover drift is **second-order** in $\epsilon$ (the contour
  curves away from its tangent line). Shrink $\epsilon$ and the drift
  shrinks faster than the step.
- **Right (normal step).** Move along $\nabla h$ itself. The endpoint
  sits at $h = 1.270$ — visibly off the contour, in the higher
  level-set band. This change scales **linearly** with $\epsilon$:
  $h(x + \epsilon\,\hat{\nabla h}) \approx 1 + \epsilon\,\|\nabla h(x)\|$.

That contrast — quadratic-drift vs. linear-drift — is what
"perpendicular to first order" means concretely. Tangent steps preserve
the constraint up to a vanishing correction; any non-tangent step
violates it proportionally to its component along $\nabla h$.

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

### Two constraints in 3D: a worked schematic

When two equality constraints $h_1(x) = 0$ and $h_2(x) = 0$ meet at a
regular point in $\mathbb{R}^3$, each is a surface and the feasible set
is the curve where the surfaces intersect. The feasible *tangent
direction* must lie in **both** surfaces' tangent planes — that is, it
must be perpendicular to **both** gradients $\nabla h_1$ and
$\nabla h_2$. The normal space (the space of "constraint pressures") is
the plane spanned by those two gradients.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 320" width="560" height="320" font-family="sans-serif" font-size="13">
  <defs>
    <marker id="cg-arr-1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#d62728"/>
    </marker>
    <marker id="cg-arr-2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#9467bd"/>
    </marker>
    <marker id="cg-arr-t" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#1f77b4"/>
    </marker>
  </defs>

  <!-- surface 1 (drawn as a tilted parallelogram) -->
  <polygon points="60,180 240,90 380,150 200,240" fill="#fde2e2" stroke="#d62728" stroke-width="1.5" opacity="0.7"/>
  <text x="80" y="200" fill="#a01818" font-size="12" font-style="italic">h₁(x) = 0</text>

  <!-- surface 2 (other tilted parallelogram, intersecting surface 1) -->
  <polygon points="160,60 440,90 520,240 240,210" fill="#ece6f5" stroke="#9467bd" stroke-width="1.5" opacity="0.65"/>
  <text x="450" y="115" fill="#5e3b8a" font-size="12" font-style="italic">h₂(x) = 0</text>

  <!-- intersection curve (drawn as a straight line through both shapes) -->
  <line x1="200" y1="225" x2="380" y2="135" stroke="#1f77b4" stroke-width="2.5"/>
  <text x="135" y="260" fill="#1f77b4" font-size="12" font-style="italic">feasible set: h₁ = 0 AND h₂ = 0</text>

  <!-- point on the intersection -->
  <circle cx="290" cy="180" r="5" fill="#222"/>
  <text x="295" y="200" fill="#222" font-size="11">x</text>

  <!-- gradient of h1 (perpendicular to surface 1 — roughly upward-left) -->
  <line x1="290" y1="180" x2="240" y2="120" stroke="#d62728" stroke-width="2.4" marker-end="url(#cg-arr-1)"/>
  <text x="200" y="115" fill="#d62728" font-weight="bold">∇h₁</text>

  <!-- gradient of h2 (perpendicular to surface 2 — roughly upward-right) -->
  <line x1="290" y1="180" x2="370" y2="100" stroke="#9467bd" stroke-width="2.4" marker-end="url(#cg-arr-2)"/>
  <text x="378" y="95" fill="#9467bd" font-weight="bold">∇h₂</text>

  <!-- tangent direction (along the intersection curve, both ways) -->
  <line x1="290" y1="180" x2="350" y2="150" stroke="#1f77b4" stroke-width="2.4" marker-end="url(#cg-arr-t)"/>
  <line x1="290" y1="180" x2="230" y2="210" stroke="#1f77b4" stroke-width="2.4" marker-end="url(#cg-arr-t)"/>

  <!-- Side panel: explanatory text -->
  <g transform="translate(20,275)">
    <text fill="#444" font-size="11">
      <tspan x="0" dy="0">Tangent space at x: directions v with</tspan>
      <tspan x="0" dy="14">∇h₁(x)·v = 0  AND  ∇h₂(x)·v = 0</tspan>
      <tspan x="320" dy="-14">Normal space at x: span(∇h₁, ∇h₂)  ⊂  ℝ³</tspan>
      <tspan x="320" dy="14">(a 2D plane of "constraint pressures")</tspan>
    </text>
  </g>
</svg>

In 3D with two constraints, $\operatorname{null}(J_h)$ is 1-dimensional
(the blue tangent line) and the row space of $J_h$ is 2-dimensional
(the red-and-purple plane). Together they span all of $\mathbb{R}^3$ —
every direction can be decomposed into "stay on the constraint set" +
"violate the constraints." [[Karush-Kuhn-Tucker Conditions]] uses this
decomposition: stationarity says $\nabla f$ has no component in the
tangent space, equivalently $\nabla f$ lies entirely in the normal
space, equivalently $\nabla f$ is a linear combination of the
$\nabla h_i$ — those coefficients are the Lagrange multipliers.

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
