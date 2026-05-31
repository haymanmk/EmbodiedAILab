---
type: concept
domain: research
created: 2026-05-31
updated: 2026-05-31
aliases: ["GLM", "generalized linear model", "canonical link function", "link function", "activation function (statistics)", "activation-loss pairing"]
tags: [machine-learning, statistics, foundations, glm, bishop]
sources:
  - "[[Bishop and Bishop - Deep Learning Foundations and Concepts]]"
---

# Generalized Linear Models

## Explain like I'm 5

You take a linear regression model $y = w^T x$ and put a **squashing function** on the output:

$$
y = f(w^T x).
$$

That's a **generalized linear model**. The squashing function $f$ depends on what kind of output you want:
- Continuous real numbers → no squash (identity).
- A probability between 0 and 1 → sigmoid.
- A probability distribution over $K$ classes → softmax.

The genius of the framework: **there's a "right" pair of squash + loss function for each output type**, and when you pair them correctly, the gradient comes out clean: $(\text{prediction} - \text{target}) \times \text{features}$ — no awkward derivative factors. Pair them wrongly and you get the dreaded vanishing-gradient problem.

## Bridges from

- **Plumbing fittings.** A linear regression model is a pipe carrying a number from input to output. To attach a different *type* of output — a probability faucet, a class-label faucet — you need a fitting (the activation function $f$). Different fitting types need different connector types (the link function); using the wrong connector means leaks (vanishing gradients).

  *Where the analogy breaks down*:
  - Real plumbing fittings are physical and one-way; activation functions are mathematical and invertible.
  - The "right" pairings aren't arbitrary preferences — they're derived from the *probability distribution* you're assuming for the target (Gaussian, Bernoulli, multinomial). This is the *canonical-link* insight, not just a heuristic.

## Definition

A **generalized linear model** (GLM) takes the form

$$
\boxed{\;y \;=\; f(w^T \phi(x))\;}
$$

where:
- $\phi(x)$ is a feature vector ([[Basis Functions]]) — possibly $\phi(x) = x$ in the trivial case
- $w$ is a learnable weight vector
- $f$ is a **nonlinear activation function** (the *inverse* of the **link function** in statistics)

The decision surface $\{x : w^T \phi(x) = \text{constant}\}$ is a hyperplane in feature space, even though $f$ is nonlinear — that's why it's still a "linear" model.

## The three standard pairings (Bishop §5.4.6, *canonical link*)

| Target distribution | Activation $f$ | Loss (negative log-likelihood) | Gradient |
|---|---|---|---|
| Gaussian (real-valued) | Identity (linear) | $\tfrac{1}{2}\sum_n (y_n - t_n)^2$ — [[Linear Regression\|MSE]] | $\sum_n (y_n - t_n)\,\phi_n$ |
| Bernoulli (binary) | Sigmoid $\sigma$ | $-\sum_n \{t_n \ln y_n + (1-t_n)\ln(1-y_n)\}$ — [[Cross-Entropy Loss\|BCE]] | $\sum_n (y_n - t_n)\,\phi_n$ |
| Multinomial ($K$-class) | [[Softmax]] | $-\sum_n \sum_k t_{nk} \ln y_{nk}$ — categorical CE | $\sum_n (y_{nk} - t_{nk})\,\phi_n$ |

**Read down the gradient column: same form every time** — prediction error times features. This is the *canonical-link miracle*: when you pair the activation with the natural loss for the target's distribution, the activation's derivative cancels exactly with the loss's $1/y$ (or $1/(1-y)$ for negative targets), leaving a beautifully clean gradient.

## Why the pairings work: cancellation in the chain rule

For binary classification, the loss per example is $E_n = -[t_n \ln y_n + (1-t_n)\ln(1-y_n)]$ and $y_n = \sigma(a_n)$ with $a_n = w^T \phi_n$. Compute $\partial E_n / \partial w$:

$$
\frac{\partial E_n}{\partial w} \;=\; \frac{\partial E_n}{\partial y_n}\cdot\frac{\partial y_n}{\partial a_n}\cdot\frac{\partial a_n}{\partial w}
$$

The three factors:
- $\partial E_n / \partial y_n = -t_n / y_n + (1-t_n)/(1-y_n) = (y_n - t_n)/[y_n(1-y_n)]$
- $\partial y_n / \partial a_n = \sigma'(a_n) = y_n(1-y_n)$
- $\partial a_n / \partial w = \phi_n$

The $y_n(1-y_n)$ factor in $\sigma'$ **cancels exactly** with the $y_n(1-y_n)$ in the denominator of $\partial E_n/\partial y_n$, leaving $\partial E_n/\partial w = (y_n - t_n)\phi_n$. Magic — but it's not actually magic, it's the canonical-link choice. (Bishop §5.4.6 derives the general result from the exponential family structure.)

## What goes wrong with the wrong pairing

**Sigmoid output + MSE loss** is the classic beginner mistake. The gradient becomes:

$$
\frac{\partial E_n}{\partial w} \;=\; (y_n - t_n) \cdot \sigma'(a_n) \cdot \phi_n \;=\; (y_n - t_n) \cdot y_n(1-y_n) \cdot \phi_n.
$$

The $\sigma'(a_n) = y_n(1-y_n)$ factor **does not cancel**. Now look at what happens near a saturated output:
- If $y_n \approx 0$ (predicted "no" confidently): $y_n(1-y_n) \approx 0$ → gradient ≈ 0.
- If $y_n \approx 1$ (predicted "yes" confidently): $y_n(1-y_n) \approx 0$ → gradient ≈ 0.

So **when the model is confident and wrong**, the gradient is tiny, and the model can't learn fast enough to fix its mistake. This is the **vanishing gradient problem** for the wrong activation-loss pairing. The [[Sigmoid Function]] vault page already notes this; the canonical-link framework is the *reason* it happens and the *cure*.

The same problem happens with softmax + MSE, tanh + MSE for classification, and any "off-canonical" combination.

## The exponential-family derivation (sketch)

If the target distribution $p(t \mid \eta)$ is a member of the exponential family

$$
p(t \mid \eta, s) = \tfrac{1}{s} h(t/s) g(\eta) \exp(\eta t / s),
$$

then the conditional mean is $\mathbb{E}[t \mid \eta] = -s\, \tfrac{d}{d\eta} \ln g(\eta)$. Define this relationship $\eta = \psi(y)$. The **canonical link function** is $f^{-1}(y) = \psi(y)$, equivalently the canonical activation is $f(\psi(y)) = y$. When you train by MLE under this distribution and use the canonical activation, the gradient simplifies to $\sum_n (y_n - t_n)\phi_n$. (Bishop §5.4.6.)

The exponential family contains essentially every distribution you'll meet: Gaussian, Bernoulli, multinomial/categorical, Poisson, exponential, beta, gamma, Dirichlet. Each has its own canonical link, and the GLM template gives you the corresponding regression model.

## The framework transfers to deep networks

Bishop & Bishop §5.4.6 ends with the most important pointer for Ch 6+:

> *"We have seen that there is a natural pairing between the choice of error function and the choice of output-unit activation function. Although we have derived this result in the context of single-layer network models, the same considerations apply to deep neural networks discussed in later chapters."*

A deep network's output layer is, structurally, a GLM on top of learned features (the hidden layers). The canonical-link rule transfers directly:

- **Regression head** (predicting any real number): final layer is linear (no activation), loss is MSE.
- **Binary head** (predicting probability of one class): final layer is sigmoid (or, in practice, *no* sigmoid + `BCEWithLogitsLoss`), loss is binary cross-entropy.
- **Multi-class head** (predicting probability over $K$ classes): final layer is softmax (or, in practice, *no* softmax + `CrossEntropyLoss`), loss is categorical cross-entropy.

Every modern deep-learning library (PyTorch, TensorFlow, JAX) makes these the default choices. When you write `nn.MSELoss()`, `nn.BCEWithLogitsLoss()`, `nn.CrossEntropyLoss()` in PyTorch, you're picking a canonical-link pairing.

## Common confusions

- **"Activation function" vs "link function".** ML calls $f$ the activation function; statistics calls $f^{-1}$ the link function. Same idea, inverses of each other.
- **"Generalized linear model" vs "linear model" vs "general linear model".** Confusing terminology zoo:
  - *Linear model* — $y = w^T x$, no activation. Just linear regression.
  - *General linear model* (singular) — multi-output linear regression. Less common term.
  - *Generalized linear model* (singular) — $y = f(w^T x)$ with an activation. The GLM framework discussed here.
- **"GLM" in older statistics literature.** The classical 1970s–80s GLM framework (Nelder & Wedderburn 1972) is exactly the same idea Bishop generalizes — Bishop's contribution is showing it's the foundation for *output layers* in deep networks.
- **Convexity of the loss.** GLMs with canonical links have *convex* loss functions in $w$ — single global minimum, gradient descent always converges. Deep networks break this because adding hidden layers makes the loss non-convex; but the per-output-layer GLM step is still convex conditional on the learned features.
- **The pairing matters *only at the output layer*.** Inside the network (hidden layers), activations like ReLU, GELU, SiLU dominate — they have nothing to do with canonical links because they're not connected to a loss directly. The canonical-link rule applies to the *final* layer paired with the *training* loss.

## Quick decision table for the user's future PyTorch code

| Task | Final layer (no activation; let the loss handle it) | Loss function |
|---|---|---|
| Regression to any real value | `nn.Linear(in, 1)` (or `(in, K)` for multi-output) | `nn.MSELoss()` |
| Regression with non-negative output | `nn.Linear(in, 1)` → apply $\exp$ or softplus in the model, or use a Poisson likelihood | `nn.PoissonNLLLoss()` |
| Binary classification | `nn.Linear(in, 1)` (raw logit, no sigmoid) | `nn.BCEWithLogitsLoss()` |
| Multi-class classification | `nn.Linear(in, K)` (raw logits, no softmax) | `nn.CrossEntropyLoss()` |
| Multi-label classification | `nn.Linear(in, K)` (raw logits, no sigmoid) | `nn.BCEWithLogitsLoss()` applied per-label |

The pattern: **let the loss function combine the activation and the loss internally** for numerical stability. Hand-rolling sigmoid before BCELoss is the source of NaN gradients in beginner code.

## Origins / sources

- **Bishop & Bishop, *Deep Learning: Foundations and Concepts* (2024)**, §5.4.1 (activation/link functions), §5.4.6 (canonical link derivation from exponential family).
- **Nelder & Wedderburn (1972)**, *Generalized Linear Models* — the foundational statistics paper that introduced the framework.
- **McCullagh & Nelder (1989)**, *Generalized Linear Models* (textbook) — the canonical statistical reference.

## Related concepts

- [[Linear Regression]] — the identity-link GLM (Gaussian targets).
- [[Logistic Regression]] — the sigmoid-link GLM (Bernoulli targets).
- [[Softmax]] — the softmax-link GLM (multinomial targets); "softmax regression".
- [[Cross-Entropy Loss]] — the canonical-link partner for sigmoid and softmax outputs.
- [[Sigmoid Function]] — the activation; its pairing with BCE is canonical.
- [[Basis Functions]] — what $\phi(x)$ is, in the GLM template.
- [[Bishop and Bishop - Deep Learning Foundations and Concepts]] — the source.
- (red link) [[Exponential Family]] — the broader probability framework that justifies the canonical-link rule.

## Mentions

- [[Logistic Regression]], [[Softmax]], [[Cross-Entropy Loss]] all cite this page as the framework that explains their activation-loss pairing.
- [[Bishop and Bishop - chapters]] — Ch 5
