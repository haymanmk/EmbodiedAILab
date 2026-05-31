---
type: concept
domain: research
created: 2026-05-31
updated: 2026-05-31
aliases: ["least squares regression", "MSE regression", "linear regression with basis functions", "single-layer regression"]
tags: [machine-learning, regression, foundations, bishop, glm]
sources:
  - "[[Bishop and Bishop - Deep Learning Foundations and Concepts]]"
---

# Linear Regression

## Explain like I'm 5

You have noisy data points $(x_n, t_n)$ and want to fit a smooth curve through them. **Linear regression** picks a curve from a fixed *family* of curves — typically weighted sums of pre-chosen building blocks (basis functions) — by minimizing the sum of squared errors between the curve and the data points.

The "linear" doesn't mean the curve is a straight line; it means **the prediction is a linear combination of the model's parameters $w$**. Pick polynomial building blocks and you get polynomial regression. Pick Gaussian-bump building blocks and you get something that fits multimodal data. Either way, the closed-form solution is a single matrix calculation involving the [[Moore-Penrose Pseudoinverse]].

## Bridges from

- **Tuning a graphic equalizer to match a song's frequency profile.** You're given a "target sound" (the data $t$); you have a bunch of frequency sliders (the basis functions $\phi_j$); you adjust each slider's height (the weight $w_j$) to minimize how different the output sounds from the target.

  *Where the analogy breaks down*:
  - Equalizers operate on audio in real time; linear regression is a one-shot fit to a fixed dataset.
  - The "best" slider configuration in linear regression has a closed-form solution (the normal equations) — no fiddling required. Equalizers require ear-and-eye iteration.
  - Equalizers can only attenuate or boost a fixed set of bands; linear regression's basis functions can be arbitrary nonlinear functions of the input.

## Definition

Given $N$ training pairs $\{(x_n, t_n)\}_{n=1}^N$ and a vector of [[Basis Functions]] $\phi(x) = (\phi_0(x), \ldots, \phi_{M-1}(x))^T$ (with $\phi_0(x) \equiv 1$ for the bias term), the **linear regression** model is

$$
y(x, w) \;=\; \sum_{j=0}^{M-1} w_j \phi_j(x) \;=\; w^T \phi(x).
$$

The model is *linear in $w$* (not necessarily in $x$). The goal is to find $w$ that minimizes the sum-of-squared-errors

$$
E_D(w) \;=\; \tfrac{1}{2} \sum_{n=1}^N \bigl(t_n - w^T \phi(x_n)\bigr)^2.
$$

## Why MSE? The MLE story (Bishop §4.1.2)

Sum-of-squared-errors isn't an arbitrary choice — it's the maximum-likelihood estimate under a **Gaussian noise** assumption on the target. Assume:

$$
t_n \;=\; y(x_n, w) + \epsilon_n, \qquad \epsilon_n \sim \mathcal{N}(0, \sigma^2).
$$

Then the likelihood of observing the training data is

$$
p(\mathbf{t} \mid X, w, \sigma^2) \;=\; \prod_{n=1}^N \mathcal{N}(t_n \mid w^T \phi(x_n), \sigma^2).
$$

Take the log:

$$
\ln p(\mathbf{t}\mid X, w, \sigma^2) \;=\; -\frac{N}{2}\ln(2\pi\sigma^2) \;-\; \frac{1}{\sigma^2}\, E_D(w).
$$

The first term doesn't depend on $w$. So **maximizing the log-likelihood is equivalent to minimizing $E_D(w)$.** MSE = MLE under Gaussian-noise assumptions. This is a special case of the [[Generalized Linear Models]] canonical-link framework: identity activation + MSE loss is the canonical pairing for Gaussian targets.

## Closed-form solution: the normal equations

Setting $\nabla_w E_D(w) = 0$ gives the **normal equations**:

$$
\Phi^T \Phi\, w \;=\; \Phi^T \mathbf{t},
$$

where the **design matrix** $\Phi$ is $N \times M$ with $\Phi_{nj} = \phi_j(x_n)$ (one row per training example, one column per basis function). Solving:

$$
\boxed{\;w_{\text{ML}} \;=\; (\Phi^T \Phi)^{-1}\, \Phi^T\, \mathbf{t} \;=\; \Phi^\dagger\, \mathbf{t}\;}
$$

where $\Phi^\dagger = (\Phi^T \Phi)^{-1} \Phi^T$ is the [[Moore-Penrose Pseudoinverse]] (a generalization of the matrix inverse to non-square matrices). The pseudoinverse is exactly the object covered in the user's existing concept page; here it appears as the closed-form MLE for linear regression.

The maximum likelihood estimate for the noise variance $\sigma^2$ is

$$
\sigma^2_{\text{ML}} \;=\; \frac{1}{N}\sum_{n=1}^N \bigl(t_n - w_{\text{ML}}^T \phi(x_n)\bigr)^2
$$

— the residual variance around the fit.

## Geometry: orthogonal projection (Bishop §4.1.4, Fig 4.3)

Think of the $N$ targets as a single vector $\mathbf{t} \in \mathbb{R}^N$. Each basis function $\phi_j$ evaluated at the $N$ training inputs is also a vector $\boldsymbol\varphi_j \in \mathbb{R}^N$. The $M$ such vectors span an $M$-dimensional subspace $S \subset \mathbb{R}^N$. The model prediction $\mathbf{y} = \Phi w$ lives somewhere in $S$ (it's an arbitrary linear combination of the $\boldsymbol\varphi_j$).

The least-squares loss is $\tfrac{1}{2}\|\mathbf{t} - \mathbf{y}\|^2$ — the *squared Euclidean distance* from the target vector to the model prediction. **Minimizing this distance over all $\mathbf{y} \in S$ is, by elementary geometry, the orthogonal projection of $\mathbf{t}$ onto $S$.** The pseudoinverse $\Phi^\dagger$ is the operator that performs this projection.

This is the same projection-onto-subspace geometry that shows up in the user's existing [[Singularity]] page (when the basis vectors $\boldsymbol\varphi_j$ are nearly collinear, the subspace $S$ is poorly conditioned and the projection becomes numerically unstable).

## Sequential learning (SGD / LMS)

For large datasets, the closed-form solution is expensive (an $M \times M$ matrix inverse). The **least-mean-squares (LMS)** algorithm processes one example at a time:

$$
w^{(\tau+1)} \;=\; w^{(\tau)} \;+\; \eta\, (t_n - w^{(\tau)T} \phi_n)\, \phi_n.
$$

Read: "for each training example, nudge the weights in the direction that would reduce *this example's* squared error." The learning rate $\eta$ controls step size. This is **stochastic gradient descent** in its simplest form, 1960s-vintage, and it is structurally identical to the SGD-with-MSE training loop you'd write in PyTorch today.

For deep networks (Ch 6+ in Bishop & Bishop), the same update form applies — just with the gradient computed via backpropagation through hidden layers instead of being immediately readable from the basis-function inputs.

## Regularized least squares (weight decay / L2)

Add an L2 penalty on the weights to discourage overfitting:

$$
E(w) \;=\; E_D(w) \;+\; \frac{\lambda}{2}\|w\|^2.
$$

The closed-form solution becomes

$$
w \;=\; (\lambda I + \Phi^T \Phi)^{-1}\, \Phi^T\, \mathbf{t}.
$$

The $\lambda I$ inside the inverse:
- **Improves numerical conditioning** — even when $\Phi^T \Phi$ is singular (e.g., when $M > N$ or columns of $\Phi$ are collinear), adding $\lambda I$ for any $\lambda > 0$ makes it invertible.
- **Shrinks weights toward zero** — discouraging the model from relying on any single basis function too heavily.
- **Trades bias for variance** — see the bias-variance discussion below.

Three names for the same thing: **L2 regularization**, **weight decay**, **ridge regression** (in statistics). Bishop §4.1.6 calls it "parameter shrinkage."

In deep learning, the *exact same* L2 penalty is applied to each layer's weights; the closed-form solution disappears (no closed form for non-convex losses) but the regularization effect is the same.

## Decision theory: when is $E[t \mid x]$ the right thing to predict?

After training, you have $p(t \mid x) = \mathcal{N}(y(x, w_{\text{ML}}), \sigma^2_{\text{ML}})$ — a *distribution* over $t$, not just a single prediction. For a real-valued decision under squared loss, the optimal prediction is the conditional mean $\mathbb{E}[t \mid x] = y(x, w_{\text{ML}})$. For absolute loss, it'd be the conditional median; for 0/1 loss, the mode. (Bishop §4.2.)

This decision-theory framing matters because it makes explicit when MSE is the "right" loss: only when (a) the target distribution is Gaussian-shaped and (b) you'll be evaluated on squared-error performance downstream. For heavy-tailed targets or asymmetric loss, MSE is the wrong choice; use Huber loss, quantile regression, or a non-Gaussian likelihood.

## Bias-variance trade-off (Bishop §4.3)

The expected squared loss decomposes as

$$
\mathbb{E}[L] \;=\; \underbrace{(\text{bias})^2}_{E_D[f(x;D)] \text{ vs } h(x)} \;+\; \underbrace{\text{variance}}_{\text{wobble of } f(x;D) \text{ across data sets}} \;+\; \underbrace{\text{noise}}_{\text{irreducible}}.
$$

Where $h(x) = \mathbb{E}[t \mid x]$ is the true regression function and $f(x; D)$ is the trained model on dataset $D$.

The trade-off picture:
- **Large $\lambda$** (heavy regularization): the trained model is rigid → low variance (similar across datasets) but high bias (its average misses $h$).
- **Small $\lambda$** (no regularization): the trained model overfits each dataset → high variance (different on every dataset) but low bias (the average is close to $h$).
- **Optimal $\lambda$**: minimizes $\text{bias}^2 + \text{variance}$.

The bias-variance decomposition is "of limited practical value" (Bishop's words — it requires averaging over hypothetical datasets) but is foundational for understanding why model complexity matters at every scale, including deep networks.

## Common confusions

- **"Linear regression" means linear in $w$, not linear in $x$.** A polynomial regression $y = w_0 + w_1 x + w_2 x^2 + \cdots + w_M x^M$ is a *linear model* whose prediction is nonlinear in $x$. The closed-form solution machinery applies because the model is linear in $w$.
- **MSE is a *consequence* of assuming Gaussian noise, not a default.** If you suspect heavy-tailed errors, use a different likelihood; if you have asymmetric costs, use a different loss. MSE isn't sacred.
- **The pseudoinverse and the matrix inverse.** $\Phi^\dagger = (\Phi^T\Phi)^{-1}\Phi^T$ only when $\Phi^T\Phi$ is invertible (i.e., the columns of $\Phi$ are linearly independent). When they're not — too few data points, collinear basis functions — $\Phi^T\Phi$ is singular and you need either L2 regularization or the SVD-based pseudoinverse (which handles the singular case via "Moore-Penrose conditions"). The user's existing [[Moore-Penrose Pseudoinverse]] page covers this in depth.
- **Multiple outputs decouple.** If $t$ has $K$ components, the K-target regression problem decomposes into $K$ independent single-target problems, each sharing the same pseudoinverse $\Phi^\dagger$. (Bishop §4.1.7.)
- **"Linear regression is too simple for real problems."** True for raw $x$, false for engineered $\phi(x)$. The whole point of the basis-function framework is that linear-in-$w$ models can fit arbitrarily complex curves *given the right $\phi$*. The "too simple" critique is really an indictment of hand-engineered $\phi$ in high dimensions — which is what Ch 6 fixes via learned representations.

## Worked example: 1D polynomial regression

Fit a 3rd-order polynomial $y = w_0 + w_1 x + w_2 x^2 + w_3 x^3$ to data points $\{(x_n, t_n)\}$. The design matrix is:

$$
\Phi \;=\; \begin{pmatrix} 1 & x_1 & x_1^2 & x_1^3 \\ 1 & x_2 & x_2^2 & x_2^3 \\ \vdots & \vdots & \vdots & \vdots \\ 1 & x_N & x_N^2 & x_N^3 \end{pmatrix}.
$$

Compute $w = (\Phi^T\Phi)^{-1} \Phi^T \mathbf{t}$. That's the full algorithm. Three lines of NumPy:

```python
Phi = np.vstack([np.ones_like(x), x, x**2, x**3]).T   # design matrix, shape (N, 4)
w   = np.linalg.lstsq(Phi, t, rcond=None)[0]          # solves the normal equations stably
y_pred = Phi @ w                                       # model predictions
```

(Use `np.linalg.lstsq` rather than computing $\Phi^\dagger$ explicitly — it's numerically safer because it uses SVD under the hood.)

## In a deep-learning context (Ch 6+ preview)

A 1-hidden-layer neural network for regression is:

$$
y(x, w, W) \;=\; w^T h(W x).
$$

The hidden layer $h(W x)$ produces a learned feature vector — this is exactly the "linear regression with basis functions" structure, where the basis functions $\phi_j(x) = h(W_j^T x)$ are *trained* rather than hand-picked. The output is still a linear combination $w^T \phi(x)$; the loss is still MSE (if targets are Gaussian); the canonical-link argument still holds. The closed-form pseudoinverse solution disappears because $\phi$ depends on $W$ which depends on $w$ through SGD, so the joint problem is non-convex. But the structural template — linear regression at the output, with whatever features you've got — never goes away.

## Origins / sources

- **Bishop & Bishop, *Deep Learning: Foundations and Concepts* (2024)**, §4.1 (linear regression with basis functions), §4.2 (decision theory), §4.3 (bias-variance).
- **Gauss (1809)** is traditionally credited with introducing least-squares regression, though Legendre published it first in 1805.
- The probabilistic interpretation (MLE under Gaussian noise) is standard mid-20th-century statistics.

## Related concepts

- [[Basis Functions]] — the feature framework linear regression sits on top of.
- [[Moore-Penrose Pseudoinverse]] — the closed-form solution operator.
- [[Generalized Linear Models]] — linear regression is the identity-link GLM; explains why MSE is the "right" loss.
- [[Logistic Regression]] — the binary-classification analog (sigmoid + cross-entropy).
- [[Singularity]] — the failure mode when the design matrix is ill-conditioned.
- [[Sigmoid Function]] — appears as the basis-function family choice (§4.1.1 sigmoidal basis functions).
- [[L2 Regularization]] (red link) — the weight-decay penalty.
- [[Bias-Variance Trade-off]] (red link) — the model-complexity framework.
- [[Bishop and Bishop - Deep Learning Foundations and Concepts]] — the source.

## Mentions

- [[Bishop and Bishop - chapters]] — Ch 4
