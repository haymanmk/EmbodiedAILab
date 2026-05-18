---
type: concept
domain: research
created: 2026-05-17
updated: 2026-05-18
aliases: ["singularities", "singular", "Jacobian singularity", "robot singularity", "geometric singularity", "representation singularity"]
tags: [linear-algebra, geometry, robotics-math, kinematics, manifolds]
---

# Singularity

## Explain like I'm 5

Imagine a toy map of your room. Most of the time the map works: take one step in your room, and your finger takes one step on the map. Everything lines up.

But pretend the map has one bad spot — maybe it got folded, or two streets got drawn on top of each other, or someone squished a corner flat. At that one spot, the map stops being helpful. Your finger doesn't know which way to go. Or two different places on the map seem to point to the same spot in your room.

That bad spot is called a **singularity**. It's just a fancy word for *a place where the usual rules suddenly stop working.*

Different things can have singularities:

- A **number machine** that turns numbers into other numbers might give the same answer for two different numbers — so you can't tell which number you started with.
- A **shape** might have a sharp point or two lines crossing, instead of being smooth all the way through.
- A **map of the Earth** gets confused at the very top: stand on the North Pole and try to point "east" — there's no good answer.
- A **robot arm** can reach a pose where, even though every motor still works, it can't push its hand sideways. One whole direction has disappeared.

The thing they all share: at this special spot, *small moves on one side stop matching up with small moves on the other side.* Everywhere else the world behaves nicely. Right here, it doesn't.

The rest of this page is the grown-up version of that idea, one domain at a time.

## Bridges from

- **A clean map with a tear, fold, or pinched point.** Away from the damaged spot, nearby points on the map behave normally: small moves on the map correspond to small moves in the place being mapped. At the tear, fold, or pinch, that local rule stops being trustworthy. Two places may collapse together, one direction may disappear, or the map may fail to show a single smooth neighborhood.

  *Where the analogy breaks down:* mathematical singularities are not always visually dramatic. Sometimes the object still looks ordinary, but a matrix inverse becomes unstable, a coordinate chart becomes ambiguous, or a Jacobian loses rank. The common signal is not "looks broken"; it is "the usual local model fails."

## Reading the analogy across domains

Across every domain on this page, the word **map** is used in the mathematical sense: a rule that pairs each point in one space with a point in another. A matrix is a map (vectors → vectors); a coordinate chart is a map (physical points → numerical coordinates); a robot's forward kinematics is a map (joint angles → end-effector poses).

The analogy is not "a matrix is like a way to look things up on a map" — that understates it. A *good* map preserves neighborhoods: take a small step in the room, take a small step on the map. That local consistency is the property that usually holds, and a singularity is exactly the point where it stops holding in some tiny neighborhood.

To read the rest of the page, here is the "room" vs. "map" split in each domain:

| Domain | The "room" (the place) | The "map" |
|---|---|---|
| Linear algebra | Input vector space | The matrix $A$ (vectors → vectors) |
| Geometric | The curve or surface itself | A local parametrization of a small patch |
| Representation | The smooth sphere | Latitude / longitude coordinates |
| Robotics | End-effector poses the arm can reach | Forward kinematics $f(\theta)$ (joint angles → poses) |

A singularity is always a failure of the *map* in some tiny neighborhood. But there is a subtler split — sometimes only the map is broken (the room is fine), and sometimes the room itself has the damage. That distinction is exactly the geometric-vs.-representation bullet under [Variations / debates](#variations--debates).

> [!question] Check yourself
> In the table above, which row is the case where the room is fine and only the map is broken? Which row is the case where the room itself has the damage?

## Definition

A **singularity** is a point or configuration where the usual local description of an object stops behaving normally. The word appears in several domains, but the shared pattern is:

> something that is normally invertible, smooth, rank-stable, or locally well-approximated stops having that property.

The object that becomes singular depends on the domain:

| Domain | What becomes singular? | What fails? |
|---|---|---|
| Linear algebra | A matrix or linear map | Full rank, invertibility, unique recovery |
| Geometry | A curve, surface, constraint set, or coordinate chart | A clean tangent space or smooth local model |
| Robotics | A robot configuration through its Jacobian | Controllable task-space directions or stable inverse kinematics |

## Linear algebra singularity

In linear algebra, a square matrix is **singular** when it is not invertible. Equivalently, it has less than full rank, so at least one input direction is collapsed or lost.

For example,

$$
A =
\begin{bmatrix}
1 & 0 \\
0 & 0
\end{bmatrix}
$$

maps every vector $(x,y)$ to $(x,0)$. The whole vertical direction disappears. Since many different inputs produce the same output, the map cannot be reversed uniquely.

Plain meaning: **some direction or information has been lost.**

This is the sense behind [[Moore-Penrose Pseudoinverse]]: when a Jacobian is rank-deficient, the ordinary inverse may not exist; near rank deficiency, tiny singular values can make inverse computations numerically explosive.

## Geometric singularity

In geometry, a singularity is a place where a curve, surface, or constraint set does not look locally like one clean smooth object.

A simple example is:

$$
h(x,y)=x^2-y^2=0.
$$

Factoring gives:

$$
(x-y)(x+y)=0,
$$

so the feasible set is two crossing lines:

$$
y=x
\qquad\text{or}\qquad
y=-x.
$$

Away from the origin, each branch has a clean tangent line. At the origin, there is no single tangent line for the whole feasible set; two branches cross there. The gradient also vanishes:

$$
\nabla h(x,y)=(2x,-2y),
\qquad
\nabla h(0,0)=(0,0).
$$

This is why [[Constraint Gradients and Tangent Spaces]] assumes a **regular point**. When the constraint gradient vanishes, or the constraint Jacobian loses rank, the usual "constraint surface + tangent space" picture may stop being valid.

Plain meaning: **the shape no longer has one clean local tangent model.**

## Representation singularity

A representation singularity is different: the underlying geometric object may be smooth, but the chosen coordinates fail.

For example, the surface of a sphere is smooth, but latitude-longitude coordinates behave badly at the poles. Longitude becomes ambiguous there, and small physical motion near a pole can cause a large coordinate change. [[Configuration Space]] uses this idea when explaining why topology matters: if the coordinates do not match the space's global shape, singularities or duplicated representations appear.

Plain meaning: **the object is fine; the coordinate system is the thing that breaks.**

This distinction matters for robotics because a robot's actual configuration space can be smooth while one chosen coordinate chart, such as Euler angles, has singularities.

## Robotics singularity

In robotics, a singularity usually means a robot's velocity Jacobian loses rank at a configuration. For a serial manipulator,

$$
V = J(\theta)\dot{\theta},
$$

where $\dot{\theta}$ is joint velocity and $V$ is the end-effector twist. If $J(\theta)$ loses rank, some task-space velocity directions become unreachable instantaneously. The inverse problem also becomes unstable: a small desired end-effector motion in a hard direction may require enormous joint velocities.

This is the robotics meaning previewed in [[Modern Robotics - Lynch & Park]] Ch. 5 and used by [[Moore-Penrose Pseudoinverse]]. Near a singularity, controllers often replace the ordinary inverse or raw pseudoinverse with damped least squares to avoid explosive commands.

Plain meaning: **the robot loses an instantaneous motion capability, or inverse kinematics becomes ill-conditioned.**

## How the meanings connect

These meanings are not identical, but they sit on the same stack:

1. A robot has a nonlinear forward-kinematics map.
2. The Jacobian is the local linear approximation of that map.
3. If the Jacobian loses rank, that local linear map has a linear-algebra singularity.
4. That rank loss changes the local geometry of reachable end-effector velocities.
5. An inverse-kinematics solver then feels the singularity as numerical instability or impossible motion.

So in robotics, "singularity" is often a **linear algebra singularity of a Jacobian** that expresses a **geometric change in local motion ability**.

## Variations / debates

- **Rank loss is a warning, not always a visible catastrophe.** A constraint Jacobian can lose rank because constraints are redundant, while the feasible set is still smooth.
- **Singular vs. ill-conditioned.** A matrix is singular when a singular value is exactly zero. It is ill-conditioned when a singular value is very small, causing practical instability even if the inverse technically exists.
- **Geometric singularity vs. representation singularity.** A crossing curve is geometrically singular; longitude at a pole is a coordinate failure on an otherwise smooth sphere.

## Related concepts

- [[Moore-Penrose Pseudoinverse]]
- [[Constraint Gradients and Tangent Spaces]]
- [[Configuration Space]]
- [[Modern Robotics - Lynch & Park]]
- [[Karush-Kuhn-Tucker Conditions]]

## Mentions

- [[Moore-Penrose Pseudoinverse]]
- [[Constraint Gradients and Tangent Spaces]]
- [[Configuration Space]]
- [[Modern Robotics - Lynch & Park]]
