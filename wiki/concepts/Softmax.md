---
type: concept
domain: research
created: 2026-05-31
updated: 2026-05-31
aliases: ["softmax function", "normalized exponential", "softmax regression", "multinomial logistic regression", "multi-class logistic regression"]
tags: [machine-learning, classification, glm, foundations, bishop]
sources:
  - "[[Bishop and Bishop - Deep Learning Foundations and Concepts]]"
---

# Softmax

## Explain like I'm 5

You have a multi-class problem — say "is this image of a dog, a cat, a bird, or a fish?" — and your network produces four numbers $(a_1, a_2, a_3, a_4)$, one per class. These numbers can be anything: positive, negative, big, small. You want to turn them into a probability distribution: four numbers between 0 and 1 that sum to 1.

**Softmax** is the trick:

1. **Exponentiate** each $a_k$ so they're all positive: $e^{a_1}, e^{a_2}, e^{a_3}, e^{a_4}$.
2. **Divide each by the total** so they sum to 1: $y_k = e^{a_k} / (e^{a_1} + e^{a_2} + e^{a_3} + e^{a_4})$.

That's it. The denominator $\sum_j e^{a_j}$ is the [[Normalizing Constant]] for the resulting distribution — the same gluing trick that turns "raw cake-slice weights" into "fractions of cake" in your existing vault concept page.

## Bridges from

- **Voting with megaphone-power.** Each class has a "raw vote" $a_k$ (the network's logit). To turn raw votes into a probability distribution, you (a) take the exponential of each — which acts like a *megaphone*, amplifying any positive vote much more than any negative one — then (b) normalize so the megaphone-amplified votes sum to 100%. The class with the biggest $a_k$ ends up with most of the probability mass; the smallest with nearly none.

  *Where the analogy breaks down*:
  - There's no actual voting; the $a_k$ are just network outputs (called "logits" or "pre-activations").
  - The exponential isn't just for positivity — it has a specific information-theoretic meaning (see "log-odds generalization" below) that's load-bearing.
  - Softmax is often called the "soft" max because if one $a_k$ is *much* bigger than the others, the output looks almost like a hard one-hot (almost all probability on the largest); but for similar $a_k$'s, the output is genuinely diffuse.

## Definition

For $K$ classes with pre-activations (logits) $a_1, \ldots, a_K \in \mathbb{R}$:

$$
\boxed{\;y_k \;=\; \text{softmax}(a)_k \;=\; \frac{\exp(a_k)}{\sum_{j=1}^K \exp(a_j)}\;}
$$

Properties:
- $y_k \in (0, 1)$ for all $k$ (positivity from exp; strictly less than 1 since the denominator includes $e^{a_k}$ plus the other terms).
- $\sum_k y_k = 1$ (by construction; the normalizing constant).
- Translation-invariant: $\text{softmax}(a + c) = \text{softmax}(a)$ for any scalar $c$. (Adding a constant to all logits doesn't change the output.)
- Reduces to the sigmoid when $K=2$: $y_1 = \sigma(a_1 - a_2)$.

## Why softmax? The log-odds generalization (Bishop §5.3)

The same Bayes-theorem argument that derives the sigmoid as the log-odds → probability formula for two classes generalizes to $K$ classes. For class-conditionals $p(x \mid C_k)$ and priors $p(C_k)$:

$$
p(C_k \mid x) \;=\; \frac{p(x \mid C_k) p(C_k)}{\sum_j p(x \mid C_j) p(C_j)}.
$$

Define $a_k := \ln(p(x \mid C_k) p(C_k))$. Then

$$
p(C_k \mid x) \;=\; \frac{e^{a_k}}{\sum_j e^{a_j}}.
$$

**Softmax is the formula that converts a vector of log-probabilities into a probability distribution.** Wherever you see softmax in machine learning, there's an implicit "these inputs are unnormalized log-probabilities" story.

When the class-conditionals are exponential-family with shared scale, the $a_k$ work out to be linear functions of $x$: $a_k = w_k^T x + w_{k0}$. That's why "softmax of a linear function" is the canonical multi-class generalized linear model.

## Connection to [[Normalizing Constant]]

The denominator $Z := \sum_j e^{a_j}$ is *literally* a normalizing constant — it's the same role $Z_\theta$ plays in your existing concept page. The whole softmax is

$$
y_k = \frac{e^{a_k}}{Z}, \qquad Z = \sum_j e^{a_j}.
$$

This is the **discrete Boltzmann distribution** with energies $-a_j$. In statistical physics it's called the *partition function*; in ML it's the *normalizer*; in either case it's the gluing factor that makes the outputs a valid probability distribution. Softmax is the small-discrete tractable case where the sum is finite (over $K$ classes) so $Z$ is trivially computable — by contrast to the intractable integrals over continuous $x$ that motivated score-based generative modeling (see [[Diffusion Models]]).

## Softmax regression: multi-class classifier

Use softmax as the output activation of a single-layer network and pair with **categorical cross-entropy** loss for the canonical-link pairing:

$$
y_k = \text{softmax}(w_k^T \phi(x))_k, \qquad E(w) = -\sum_n \sum_k t_{nk} \ln y_{nk}.
$$

This is **softmax regression** (also called *multinomial logistic regression* or *multi-class logistic regression*). It's the $K$-class generalization of [[Logistic Regression]] in exactly the way softmax generalizes sigmoid.

**Training**: gradient comes out as

$$
\nabla_{w_j} E \;=\; \sum_n (y_{nj} - t_{nj})\, \phi_n.
$$

The same clean (prediction − target) × features form as binary cross-entropy and as MSE. **The softmax's Jacobian cancels exactly** with the cross-entropy's $1/y$ — the canonical-link miracle (see [[Generalized Linear Models]]). This is the reason every multi-class deep-learning classifier ever written uses *exactly* softmax + categorical cross-entropy as the output head.

## Watch out: numerical stability

Computing $e^{a_k}$ directly overflows for large $a_k$ (e.g., $e^{1000}$ is infinity in float32). Always implement softmax with the **log-sum-exp trick**:

$$
\text{softmax}(a)_k \;=\; \frac{e^{a_k - \max_j a_j}}{\sum_i e^{a_i - \max_j a_j}}.
$$

Subtracting the max from every $a$ is valid (softmax is translation-invariant) and prevents the exponential from overflowing. Frameworks (PyTorch, TensorFlow) implement this automatically — *don't* hand-roll softmax in production code.

## The PyTorch idiom: combine with cross-entropy

```python
import torch.nn as nn

# Multi-class classifier with K=10 classes
model = nn.Linear(input_dim, 10)         # outputs raw logits, shape (batch, 10)
loss_fn = nn.CrossEntropyLoss()          # combines log-softmax + NLL for numerical stability
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# Training step
logits = model(x)                        # shape (batch, 10)
loss = loss_fn(logits, t)                # t is integer class indices, shape (batch,)
loss.backward()
optimizer.step()

# At inference, apply softmax to get probabilities
probs = torch.softmax(model(x), dim=-1)
```

`nn.CrossEntropyLoss` does log-softmax + negative log-likelihood internally; **it expects raw logits as input, NOT softmax probabilities**. Common beginner gotcha: passing `softmax(logits)` to `CrossEntropyLoss` applies softmax twice and produces incorrect gradients. Pass the logits directly.

## Common confusions

- **Softmax is not "hard" max.** It's a *smoothed* max. For $a = (10, 1, 1)$ the softmax is approximately $(0.9999, 0.00005, 0.00005)$ — nearly one-hot but not exactly. For $a = (1, 1, 1)$ it's $(\tfrac{1}{3}, \tfrac{1}{3}, \tfrac{1}{3})$ — fully diffuse. The "temperature" of a softmax (how peaked vs spread) is controlled by scaling the logits: $\text{softmax}(a/T)$ gets sharper as $T \to 0$, more uniform as $T \to \infty$.
- **Softmax in attention vs softmax in classification.** Same function, different role. Attention layers in transformers use softmax to compute *attention weights* over keys — they're not class probabilities, they're weights for a weighted sum. The math is identical; the interpretation is different.
- **Softmax regression vs $K$ separate logistic regressions.** A softmax regression with $K$ classes uses $K$ weight vectors but is constrained by the one-hot/softmax framework so the predictions sum to 1. $K$ separate one-vs-rest logistic regressions are *not* constrained this way and can produce inconsistent predictions (multiple classes assigned probability > 0.5, or none). Softmax regression is the "right" framework.
- **The translation-invariance.** Because $\text{softmax}(a + c) = \text{softmax}(a)$, the absolute logit scale doesn't matter — only the *relative* gaps between $a_k$ values. This is why softmax outputs *don't* tell you whether the model is confident in absolute terms; they tell you the relative ranking + sharpness.
- **One-of-K vs binary case.** For $K = 2$ classes, softmax reduces to sigmoid: $\text{softmax}(a_1, a_2)_1 = \sigma(a_1 - a_2)$. So you can implement binary classification with either a single-output sigmoid + BCE loss or a two-output softmax + categorical cross-entropy — they're mathematically equivalent. Most practitioners use sigmoid + BCE for binary because it's slightly more compact.

## Origins / sources

- **Bishop & Bishop, *Deep Learning: Foundations and Concepts* (2024)**, §5.3 (derivation as multi-class log-odds), §5.4.4 (softmax regression as discriminative model with categorical cross-entropy MLE).
- The function dates to Boltzmann (statistical physics) and Gibbs (canonical distribution); brought into ML as the "normalized exponential" by Bridle (1990) and applied to neural-network outputs.
- The term "softmax" was popularized by Bridle's 1990 paper *Probabilistic Interpretation of Feedforward Classification Network Outputs*.

## Related concepts

- [[Sigmoid Function]] — the $K=2$ special case (softmax reduces to sigmoid).
- [[Logistic Regression]] — the binary analog; softmax regression is its $K$-class generalization.
- [[Cross-Entropy Loss]] — the canonical-link partner for softmax (categorical cross-entropy).
- [[Normalizing Constant]] — the denominator $\sum_j e^{a_j}$ is a normalizing constant; same structural role as $Z_\theta$ in EBMs.
- [[Generalized Linear Models]] — explains the softmax+CE pairing as the canonical link for multinomial targets.
- [[Bishop and Bishop - Deep Learning Foundations and Concepts]] — the source.
- (red link) [[Attention Mechanism]] — softmax-over-keys is the computational core of transformer attention; Ch 12 in Bishop & Bishop.

## Mentions

- [[Logistic Regression]] — references the multi-class generalization here.
- [[Cross-Entropy Loss]] — references the categorical case.
- [[Bishop and Bishop - chapters]] — Ch 5
