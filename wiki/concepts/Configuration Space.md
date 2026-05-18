---
type: concept
domain: research
created: 2026-05-16
updated: 2026-05-16
aliases: ["C-space", "configuration space", "joint space"]
tags: [robotics, kinematics, topology, manifolds, robotics-math]
---

# Configuration Space

## Bridges from

- **A house with rooms on multiple floors.** To say *exactly* where someone is standing, you need a few numbers: the floor, the (x, y) on that floor, maybe which way they're facing. The minimum count of numbers it takes to pin them down completely is the **dimension of their configuration space**, and the set of all such tuples is the configuration space itself. Where it breaks down: in the house example the floor is a discrete choice and each floor is flat. A real robot's C-space can be continuous *and* curved (a doorknob's configuration wraps around at 360°), so unlike a floor plan it can have unusual global shape — see *topology* below.

## Definition

A robot's **configuration** is a complete specification of the position of every point of the robot. The minimum number $n$ of real-valued coordinates needed to represent a configuration is the robot's **degrees of freedom (dof)**. The $n$-dimensional space whose points are all the possible configurations is the **configuration space**, abbreviated **C-space**. (see [[Modern Robotics - Lynch & Park]] Def. 2.1, p. 12.)

A configuration is one point. The C-space is the set of all such points. The dimension of the C-space equals the dof.

## Why we care (the four useful facts)

1. **Counting dof.** Tells you how many independent actuators a mechanism *can* have. A door has 1 dof; a coin on a table has 3 ($x, y, \theta$); a free rigid body in 3D has 6.
2. **Computing dof for a mechanism.** Use **Grübler's formula** below.
3. **Topology** of the C-space (its global shape — plane vs. cylinder vs. torus vs. sphere) determines whether any single coordinate chart can describe it without singularities.
4. **Constraints** on the C-space (holonomic vs. nonholonomic — see §2.4 and [[Constraint Gradients and Tangent Spaces]]) determine which directions you can actually move from a given configuration.

## Degrees of freedom

For a single rigid body:

- **Planar** ($\mathbb{R}^2$): 3 dof — two for position, one for orientation.
- **Spatial** ($\mathbb{R}^3$): 6 dof — three for position, three for orientation.

For a mechanism built from $N$ links (including ground as a link) and $J$ joints with $f_i$ freedoms each, **Grübler's formula** gives the mechanism's dof (assuming joint constraints are independent):

$$
\text{dof} = m(N - 1 - J) + \sum_{i=1}^{J} f_i,
$$

where $m = 3$ for planar mechanisms and $m = 6$ for spatial mechanisms. The reasoning: each link contributes $m$ freedoms; the ground link contributes none; each joint constrains $m - f_i$ of those freedoms. (see [[Modern Robotics - Lynch & Park]] Prop. 2.2, p. 17.)

### Joint freedom cheat sheet

| Joint                    | dof $f$ | Planar constraints $c$ | Spatial constraints $c$ |
| ------------------------ | ------- | ---------------------- | ----------------------- |
| Revolute (R, hinge)      | 1       | 2                      | 5                       |
| Prismatic (P, slider)    | 1       | 2                      | 5                       |
| Helical (H, screw)       | 1       | N/A                    | 5                       |
| Cylindrical (C)          | 2       | N/A                    | 4                       |
| Universal (U)            | 2       | N/A                    | 4                       |
| Spherical (S, ball-joint)| 3       | N/A                    | 3                       |

The constraint count is just $m - f$. (see [[Modern Robotics - Lynch & Park]] Table 2.1, p. 17.)

### Sanity checks

- **Door (planar 1R)**: $N=2$, $J=1$, $f_1=1$, $m=3$. $\text{dof} = 3(2-1-1) + 1 = 1$. ✓
- **$k$R serial planar arm**: $N = k+1$, $J = k$, $f_i = 1$. $\text{dof} = 3((k+1) - 1 - k) + k = k$. ✓ (each revolute joint adds one dof, as you'd expect from a serial chain.)
- **Stewart–Gough platform (6-UPS)**: $N=14$, $J=18$, $\sum f_i = 6\cdot 2 + 6 + 6 \cdot 3 = 36$, $m=6$. $\text{dof} = 6(14-1-18) + 36 = -30 + 36 = 6$. ✓

Grübler's formula can over-count when joint constraints are **not independent** — the parallelogram linkage gives dof $= 0$ by the formula but actually moves with 1 dof (see [[Modern Robotics - Lynch & Park]] Example 2.6, p. 21). Treat the formula as a generic-case answer; verify on suspicious mechanisms.

## Topology: the *shape* of the C-space

Dimension alone doesn't characterize a C-space. A plane and the surface of a sphere are both 2-dimensional, but they have different **topology** — you cannot continuously deform one into the other without cutting or gluing.

The canonical 1-dimensional spaces:

- $\mathbb{R}^1$ (or $\mathbb{E}^1$): the real line — infinite, flat. Topology of a prismatic joint with no joint limits.
- $S^1$: the circle — wraps around. Topology of a revolute joint angle.
- $[a, b]$: a closed interval — has endpoints. Topology of a joint with hard limits.

Products of these give 2D C-spaces of distinct shapes:

| Robot / object                 | C-space topology     |
| ------------------------------ | -------------------- |
| Point on a plane               | $\mathbb{R}^2$       |
| Spherical pendulum             | $S^2$                |
| 2R planar arm (no joint limits)| $T^2 = S^1 \times S^1$ |
| Rotating sliding knob          | $\mathbb{R}^1 \times S^1$ (cylinder) |

(see [[Modern Robotics - Lynch & Park]] Table 2.2, p. 26.)

> [!warning] $S^1 \times S^1 \ne S^2$
> The torus and the sphere are both 2-dimensional and both "closed up," but they are not topologically equivalent. Two angles always live on a torus, not on a sphere.

### Why topology matters in practice

If your representation's topology doesn't match the C-space's topology, you get **[[Singularity|representation singularities]]** — places where small motion in the world causes huge changes in the coordinates (latitude near the poles), or where the same configuration has multiple coordinate representations (longitude wrapping at ±180°). Two ways to live with this:

1. **Atlas of coordinate charts** — cover the space with several minimal-coordinate charts and switch between them so you're always far from the singularity of whichever chart you're using.
2. **Implicit representation** — embed the C-space in a higher-dimensional Euclidean space and carry a constraint. A point on $S^2$ as $(x,y,z)$ with $x^2+y^2+z^2=1$ has no representation singularities but uses an extra coordinate. This is what [[Modern Robotics - Lynch & Park]] does throughout: rotations live in $SO(3)$ embedded in $\mathbb{R}^{3\times 3}$ subject to $R^\top R = I$ and $\det R = +1$. The book consistently prefers implicit representations and reserves explicit parametrizations (Euler angles, quaternions) for the appendix.

This choice — implicit-with-constraints over minimal coordinates — is the reason Ch. 3 introduces rotation matrices and the exponential-coordinate machinery rather than starting from Euler angles. The trade-off is exactly the one [[Constraint Gradients and Tangent Spaces]] describes: working *on* a constraint surface, with feasible directions defined by the constraint Jacobian's null space.

## Holonomic and nonholonomic constraints

Constraints come in two fundamentally different flavors. Both can be written in **Pfaffian form** $A(\theta)\dot\theta = 0$, but only one restricts the reachable C-space.

**Holonomic** (a.k.a. *integrable*): can be written as $g(\theta) = 0$ for some $g$. The loop-closure equations of a closed chain are the classic example — for a planar four-bar linkage,

$$
\begin{aligned}
L_1\cos\theta_1 + L_2\cos(\theta_1{+}\theta_2) + \cdots + L_4\cos(\theta_1{+}\cdots{+}\theta_4) &= 0 \\
L_1\sin\theta_1 + L_2\sin(\theta_1{+}\theta_2) + \cdots + L_4\sin(\theta_1{+}\cdots{+}\theta_4) &= 0 \\
\theta_1 + \theta_2 + \theta_3 + \theta_4 - 2\pi &= 0
\end{aligned}
$$

reduces the C-space from $\mathbb{R}^4$ (or $T^4$ if joint angles wrap) down to a 1-dimensional curve. Holonomic constraints **reduce the dimension of the C-space itself**. Differentiating $g(\theta(t)) = 0$ gives $\partial g/\partial\theta \cdot \dot\theta = 0$ — a Pfaffian form whose $A(\theta)$ happens to be a gradient of $g$.

**Nonholonomic**: Pfaffian constraints $A(\theta)\dot\theta = 0$ that *cannot* be integrated to a configuration constraint $g(\theta) = 0$. The canonical example is a coin rolling without slipping on a plane:

$$
\begin{bmatrix}
\dot x \\ \dot y
\end{bmatrix}
= r\dot\theta
\begin{bmatrix}
\cos\phi \\ \sin\phi
\end{bmatrix}
\;\Longleftrightarrow\;
\begin{bmatrix}
1 & 0 & 0 & -r\cos\phi \\
0 & 1 & 0 & -r\sin\phi
\end{bmatrix}
\dot q = 0,
\quad q = (x, y, \phi, \theta).
$$

The C-space stays 4-dimensional — the coin can still reach any $(x, y, \phi, \theta)$ — but at any instant only 2 of those 4 velocity components are independently choosable. Nonholonomic constraints **reduce the dimension of feasible velocities** without reducing the reachable C-space. This is the regime [[Modern Robotics - Lynch & Park]] Ch. 13 lives in.

> [!example] Holonomic vs. nonholonomic — the test
> Try to find a $g(\theta)$ whose gradient gives you $A(\theta)$. For the coin: $\partial g_1/\partial q_3 = 0$ would force $g_1$ to not depend on $\phi$, but $\partial g_1/\partial q_4 = -r\cos\phi$ depends on $\phi$ — contradiction. So no $g$ exists; the constraint is nonholonomic.

This connects directly to [[Constraint Gradients and Tangent Spaces]]: holonomic constraints give a $g$ whose gradient is normal to the C-space surface, and the C-space's tangent space at a regular point is exactly $\operatorname{null}(\partial g/\partial\theta)$.

## Task space vs. workspace vs. C-space

Three related-but-distinct spaces, often confused:

- **C-space** — every point of the *robot* specified. Driven by the mechanism.
- **Task space** — a space in which the robot's task is naturally expressed (e.g., $\mathbb{R}^2$ for a 2D pen plotter; $SE(3)$ for a generic pick-and-place). Driven by the *task*, independent of the robot.
- **Workspace** — the set of end-effector configurations the robot can actually reach. Driven by the *robot's structure*, independent of the task.

Same C-space, different workspaces is possible (a planar 2R arm vs. a spherical 2R arm both have C-space $T^2$ but reach different shapes in 3D space). Different C-spaces, same workspace is also possible (a 2R and a 3R planar arm with appropriate link lengths). And a point in task space may correspond to multiple C-space points — the source of inverse-kinematics multiplicity covered later in Ch. 6.

## Visualization: 2R arm and its torus C-space

A planar 2R arm has two revolute joints, each contributing $S^1$, so its C-space is the 2-torus $T^2 = S^1 \times S^1$. Two ways to picture the same point:

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 280" width="640" height="280" font-family="sans-serif" font-size="13">
  <!-- Left: the planar 2R arm in the world -->
  <g transform="translate(20,20)">
    <text x="120" y="0" text-anchor="middle" font-weight="bold">2R arm in the world</text>
    <!-- ground -->
    <line x1="20" y1="200" x2="220" y2="200" stroke="#888" stroke-width="1"/>
    <!-- base -->
    <circle cx="60" cy="200" r="6" fill="#444"/>
    <!-- link 1 -->
    <line x1="60" y1="200" x2="140" y2="120" stroke="#1f77b4" stroke-width="5" stroke-linecap="round"/>
    <!-- joint 2 -->
    <circle cx="140" cy="120" r="5" fill="#444"/>
    <!-- link 2 -->
    <line x1="140" y1="120" x2="220" y2="100" stroke="#ff7f0e" stroke-width="5" stroke-linecap="round"/>
    <!-- end effector -->
    <circle cx="220" cy="100" r="4" fill="#d62728"/>
    <!-- angle arcs -->
    <path d="M 90 200 A 30 30 0 0 0 80 180" fill="none" stroke="#666" stroke-width="1"/>
    <text x="98" y="190" font-style="italic">θ₁</text>
    <path d="M 165 105 A 25 25 0 0 0 158 95" fill="none" stroke="#666" stroke-width="1"/>
    <text x="172" y="105" font-style="italic">θ₂</text>
    <text x="60" y="220" text-anchor="middle" fill="#666" font-size="11">base</text>
    <text x="225" y="95" fill="#d62728" font-size="11">end-effector</text>
  </g>

  <!-- Right: the torus / square-with-glued-edges -->
  <g transform="translate(340,20)">
    <text x="140" y="0" text-anchor="middle" font-weight="bold">Configuration space T²</text>
    <!-- square -->
    <rect x="40" y="20" width="200" height="200" fill="#f5f5f5" stroke="#444" stroke-width="1"/>
    <!-- gluing arrows: top/bottom (single arrowheads) -->
    <line x1="80"  y1="20" x2="120" y2="20" stroke="#1f77b4" stroke-width="2" marker-end="url(#a1)"/>
    <line x1="80"  y1="220" x2="120" y2="220" stroke="#1f77b4" stroke-width="2" marker-end="url(#a1)"/>
    <line x1="160" y1="20" x2="200" y2="20" stroke="#1f77b4" stroke-width="2" marker-end="url(#a1)"/>
    <line x1="160" y1="220" x2="200" y2="220" stroke="#1f77b4" stroke-width="2" marker-end="url(#a1)"/>
    <!-- gluing arrows: left/right (double arrowheads) -->
    <line x1="40"  y1="80"  x2="40"  y2="120" stroke="#ff7f0e" stroke-width="2" marker-end="url(#a2)"/>
    <line x1="240" y1="80"  x2="240" y2="120" stroke="#ff7f0e" stroke-width="2" marker-end="url(#a2)"/>
    <line x1="40"  y1="160" x2="40"  y2="200" stroke="#ff7f0e" stroke-width="2" marker-end="url(#a2)"/>
    <line x1="240" y1="160" x2="240" y2="200" stroke="#ff7f0e" stroke-width="2" marker-end="url(#a2)"/>
    <!-- axes labels -->
    <text x="140" y="240" text-anchor="middle" fill="#1f77b4" font-style="italic">θ₁ ∈ S¹</text>
    <text x="20"  y="125" text-anchor="middle" fill="#ff7f0e" font-style="italic">θ₂</text>
    <text x="20"  y="140" text-anchor="middle" fill="#ff7f0e" font-style="italic">∈ S¹</text>
    <!-- a sample configuration point -->
    <circle cx="120" cy="80" r="4" fill="#d62728"/>
    <text x="128" y="76" fill="#d62728" font-size="11">(θ₁, θ₂)</text>
    <text x="140" y="270" text-anchor="middle" fill="#444" font-size="11" font-style="italic">
      glue top↔bottom and left↔right → torus
    </text>
  </g>

  <defs>
    <marker id="a1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#1f77b4"/>
    </marker>
    <marker id="a2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#ff7f0e"/>
    </marker>
  </defs>
</svg>

The left picture is the arm posing in the world. The right picture is its *C-space* — a single point $(\theta_1, \theta_2)$ encodes the whole pose. The square's left edge is glued to its right edge (because $\theta_1$ wraps at $2\pi$), and the top edge is glued to the bottom edge (because $\theta_2$ wraps). Glue both pairs in 3D and you get a donut. Every full arm pose is one point on that donut.

## Variations / debates

- Some texts define dof as the dimension of the **feasible velocities**, not the dimension of the C-space. For nonholonomic systems the two disagree — a rolling coin has a 4-dimensional C-space but only 2 feasible velocity directions. [[Modern Robotics - Lynch & Park]] consistently uses the C-space dimension; this wiki follows the same convention.
- Whether to model joint limits in the topology (closed intervals) or ignore them (full $S^1$) is a modeling choice — closed intervals are the truth for real hardware but full circles are simpler for the topology discussion.

## Related concepts

- [[Modern Robotics - Lynch & Park]] — primary source, Ch. 2.
- [[Constraint Gradients and Tangent Spaces]] — the geometric story behind holonomic constraints; this page's §"Holonomic vs. nonholonomic" leans on it.
- [[Singularity]] — cross-domain explanation of representation singularities, geometric singularities, and robotics Jacobian singularities.
- [[Lagrange Multipliers]] — multipliers attach to each holonomic constraint when posing constrained optimization on the C-space.
- [[Modern Robotics - chapters]] — chapter-level progress index.
- (red link) [[SO(3) Rotation Group]] — Ch. 3 introduces this for the rotational part of a rigid body's C-space.
- (red link) [[SE(3) Rigid-Body Group]] — Ch. 3, the full pose group.

## Mentions

- [[Modern Robotics - Lynch & Park]]
- [[Modern Robotics - chapters]]
- [[Constraint Gradients and Tangent Spaces]]
