---
type: concept
domain: research
created: 2026-05-14
updated: 2026-05-14
aliases: ["pseudoinverse", "Moore-Penrose inverse", "Jacobian pseudoinverse"]
tags: [linear-algebra, robotics, inverse-kinematics, jacobian]
---

# Moore-Penrose Pseudoinverse

## Definition

The Moore-Penrose pseudoinverse $J^\dagger$ generalizes the inverse of a matrix to rectangular or rank-deficient matrices. In robotics, it is used to solve velocity inverse kinematics:

$$
J\dot{\theta}=\mathcal{V}_d.
$$

Depending on the shape and rank of $J$, the pseudoinverse gives either an exact minimum-norm solution or a least-squares best approximation.

## Origins / sources

[[Deriving the Pseudoinverse Where the Formulas Come From - Heptabase AI Tutor]] derives the two common full-rank formulas:

$$
J^\dagger = J^T(JJ^T)^{-1}
$$

for a fat full-row-rank Jacobian, and

$$
J^\dagger = (J^TJ)^{-1}J^T
$$

for a tall full-column-rank Jacobian.

The fat formula comes from a constrained minimum-norm problem solved with [[Lagrange Multipliers]], which is the equality-only case of [[Karush-Kuhn-Tucker Conditions]]. The tall formula comes from least squares and the normal equations.

## Three regimes for inverse kinematics

For velocity IK, the core equation is:

$$
J\dot{\theta}=\mathcal{V}_d.
$$

If $J\in\mathbb{R}^{m\times n}$:

| Shape | Robotics meaning | Linear algebra situation | Desired solution |
|---|---|---|---|
| $m=n$ | same number of joints and task dimensions | square system | ordinary inverse if full rank |
| $n>m$ | more joints than task dimensions | underdetermined / redundant | exact solution with minimum joint norm |
| $n<m$ | fewer joints than task dimensions | overdetermined / insufficient DOF | least-squares best approximation |

The pseudoinverse is valuable because it expresses all three cases using one symbol:

$$
\dot{\theta}^\star=J^\dagger\mathcal{V}_d.
$$

## Fat Jacobian derivation

Assume $J\in\mathbb{R}^{m\times n}$ with $n>m$ and full row rank. There are more joint variables than task equations, so if the desired task velocity is achievable, there are infinitely many exact solutions.

Choose the shortest joint velocity:

$$
\min_{\dot{\theta}}\frac{1}{2}\|\dot{\theta}\|^2
\quad \text{subject to}\quad
J\dot{\theta}=\mathcal{V}_d.
$$

Build the Lagrangian:

$$
L(\dot{\theta},\lambda)
=\frac{1}{2}\dot{\theta}^T\dot{\theta}
-\lambda^T(J\dot{\theta}-\mathcal{V}_d).
$$

Different sign conventions are possible. This sign choice makes the next equation come out as $\dot{\theta}=J^T\lambda$.

Take the derivative with respect to $\dot{\theta}$:

$$
\nabla_{\dot{\theta}}L
=\dot{\theta}-J^T\lambda.
$$

Set it to zero:

$$
\dot{\theta}-J^T\lambda=0.
$$

Therefore:

$$
\dot{\theta}=J^T\lambda.
$$

Now substitute this into the constraint:

$$
J\dot{\theta}=\mathcal{V}_d
$$

$$
J(J^T\lambda)=\mathcal{V}_d
$$

$$
JJ^T\lambda=\mathcal{V}_d.
$$

Because $J$ has full row rank, $JJ^T$ is invertible. Solve for $\lambda$:

$$
\lambda=(JJ^T)^{-1}\mathcal{V}_d.
$$

Substitute back:

$$
\dot{\theta}^\star
=J^T(JJ^T)^{-1}\mathcal{V}_d.
$$

So:

$$
J^\dagger=J^T(JJ^T)^{-1}.
$$

This is called a right inverse because:

$$
JJ^\dagger
=J J^T(JJ^T)^{-1}
=I_m.
$$

## Why the fat solution has no null-space motion

For a fat $J$, the complete set of exact solutions is:

$$
\dot{\theta}
=J^\dagger\mathcal{V}_d+(I-J^\dagger J)z.
$$

The term $(I-J^\dagger J)z$ lies in the null space of $J$. It moves joints without changing the end-effector velocity:

$$
J(I-J^\dagger J)z=0.
$$

The pseudoinverse solution chooses $z=0$. That is why it is minimum norm. It performs only the joint motion needed for the task and excludes extra self-motion.

For a redundant arm, this is both useful and limiting:

- Useful: it gives the smallest joint-velocity command that achieves the requested twist.
- Limiting: it ignores secondary goals such as avoiding joint limits unless you intentionally add a null-space term.

## Tall Jacobian derivation

Assume $J\in\mathbb{R}^{m\times n}$ with $n<m$ and full column rank. There are fewer joint variables than task-space equations. Usually, no exact solution exists.

So solve the least-squares problem:

$$
\min_{\dot{\theta}}
\|J\dot{\theta}-\mathcal{V}_d\|^2.
$$

Let:

$$
r(\dot{\theta})=J\dot{\theta}-\mathcal{V}_d.
$$

The objective is:

$$
\phi(\dot{\theta})=r^Tr.
$$

Expand it:

$$
\phi(\dot{\theta})
=(J\dot{\theta}-\mathcal{V}_d)^T(J\dot{\theta}-\mathcal{V}_d).
$$

$$
\phi(\dot{\theta})
=\dot{\theta}^TJ^TJ\dot{\theta}
-2\mathcal{V}_d^TJ\dot{\theta}
+\mathcal{V}_d^T\mathcal{V}_d.
$$

Differentiate and set to zero:

$$
\nabla_{\dot{\theta}}\phi
=2J^TJ\dot{\theta}-2J^T\mathcal{V}_d=0.
$$

This gives the normal equations:

$$
J^TJ\dot{\theta}=J^T\mathcal{V}_d.
$$

Because $J$ has full column rank, $J^TJ$ is invertible. Therefore:

$$
\dot{\theta}^\star=(J^TJ)^{-1}J^T\mathcal{V}_d.
$$

So:

$$
J^\dagger=(J^TJ)^{-1}J^T.
$$

This is called a left inverse because:

$$
J^\dagger J
=(J^TJ)^{-1}J^TJ
=I_n.
$$

## Projection interpretation

In the tall case, $J\dot{\theta}$ can only land inside the column space of $J$. If $\mathcal{V}_d$ is outside that column space, no exact joint velocity can produce it.

Least squares finds the closest achievable velocity:

$$
J\dot{\theta}^\star
=\operatorname{proj}_{\operatorname{Col}(J)}(\mathcal{V}_d).
$$

The residual is:

$$
r^\star=\mathcal{V}_d-J\dot{\theta}^\star.
$$

At the least-squares optimum, the residual is orthogonal to every column of $J$:

$$
J^T r^\star=0.
$$

Substituting $r^\star=\mathcal{V}_d-J\dot{\theta}^\star$ gives:

$$
J^T(\mathcal{V}_d-J\dot{\theta}^\star)=0,
$$

which is the normal equation again:

$$
J^TJ\dot{\theta}^\star=J^T\mathcal{V}_d.
$$

This is the geometric meaning of the tall formula.

## Variations / debates

- Full row rank, fat $J$: infinitely many exact solutions exist; the pseudoinverse returns the minimum-norm joint velocity.
- Full column rank, tall $J$: exact solutions usually do not exist; the pseudoinverse returns the least-squares best joint velocity.
- Square full-rank $J$: the pseudoinverse equals the ordinary inverse.
- Rank-deficient or near-[[Singularity|singular]] $J$: the SVD-based pseudoinverse is the unified tool, but near-zero singular values can produce very large joint velocities. Robotics controllers often use damped least squares near singularities.

## Robotics interpretation

For a redundant robot, null-space motion can be added without changing the task-space velocity:

$$
\dot{\theta}
= J^\dagger \mathcal{V}_d + (I - J^\dagger J)z.
$$

The first term is the minimum-norm task solution. The second term lies in the null space of $J$, so it can be used for secondary objectives such as avoiding joint limits or obstacles.

## SVD unification

The most general and numerically important definition uses the singular value decomposition:

$$
J=U\Sigma V^T.
$$

The pseudoinverse is:

$$
J^\dagger=V\Sigma^\dagger U^T.
$$

Here $\Sigma^\dagger$ is made by taking the reciprocal of each nonzero singular value and transposing the rectangular diagonal matrix:

$$
\sigma_i \mapsto \frac{1}{\sigma_i}.
$$

If a singular value is zero, its reciprocal is treated as zero:

$$
0 \mapsto 0.
$$

This single construction handles square, fat, tall, and rank-deficient matrices. It also explains why singularities are dangerous in robotics: if a singular value $\sigma_i$ is very small, then $\frac{1}{\sigma_i}$ is very large. A small desired end-effector velocity in a hard-to-move direction can require a huge joint velocity.

## Mecharm interpretation

The Mecharm 270 Pi has a nominally square $6\times 6$ Jacobian when controlling a 6D end-effector twist. Away from singularities, the ordinary inverse may exist:

$$
\dot{\theta}=J^{-1}\mathcal{V}_d.
$$

Near a singularity, $J$ loses rank or becomes ill-conditioned. Then the ordinary inverse is unsafe, and the SVD-based pseudoinverse or damped least squares is more appropriate.

The conceptual rule:

- $J^{-1}$ says "solve exactly."
- $J^\dagger$ says "solve exactly if possible; otherwise give the minimum-norm least-squares best answer."
- Damped least squares says "solve approximately, but avoid explosive joint velocities near singularities."

## Related concepts

- [[Karush-Kuhn-Tucker Conditions]]
- [[Lagrange Multipliers]]
- [[Singularity]]
- [[Robotics Development Stack]]

## Mentions

- [[Deriving the Pseudoinverse Where the Formulas Come From - Heptabase AI Tutor]]

## External sources

- Modern Robotics numerical IK page: https://modernrobotics.northwestern.edu/nu-gm-book-resource/6-2-numerical-inverse-kinematics-part-1-of-2/
- Boyd and Vandenberghe, *Convex Optimization*: https://web.stanford.edu/~boyd/cvxbook/
