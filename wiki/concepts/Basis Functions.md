---
type: concept
domain: research
created: 2026-05-31
updated: 2026-05-31
aliases: ["basis function", "feature function", "fixed features", "feature extractor"]
tags: [machine-learning, linear-models, foundations, bishop]
sources:
  - "[[Bishop and Bishop - Deep Learning Foundations and Concepts]]"
---

# Basis Functions

## Explain like I'm 5

A piano has 88 keys. Each key plays one fixed sound — middle C, high A, low E. To play a melody, you don't change what each key sounds like; you just decide **how loudly to press each one**. The melody is the *sum* of all those key-presses, weighted by how hard you pressed.

A **basis function** is one of those piano keys for machine learning. Each one is a fixed little function $\phi_j(x)$ that produces some pattern in input space — a bump near a certain spot, a polynomial curve, an S-shape. The model doesn't change what each basis function does; it just learns *how much weight* $w_j$ to put on each one. The prediction is the weighted sum:

$$
y(x, w) \;=\; w_0 + w_1\phi_1(x) + w_2\phi_2(x) + \cdots + w_{M-1}\phi_{M-1}(x) \;=\; w^T \phi(x).
$$

## Bridges from

- **Piano keys (extended)**. Each basis function $\phi_j(x)$ is a pre-built "sound" — its output for any input $x$ is fixed by the function form. The model learns the *volumes* $w_j$ (one per key). The melody (the model's prediction) is the weighted sum of all the sounds.

  *Where the analogy breaks down*:
  - A piano's keys are chosen by the piano-maker. In ML, *you choose the keys themselves* — polynomial keys, Gaussian-bump keys, sigmoidal keys, wavelet keys. The choice of basis-function family is a modeling decision, not a fixed property of the universe.
  - Real piano keys don't interact. Basis functions sit on top of each other in input space, and the way they overlap matters — closely-spaced Gaussian bumps mean a small change to one weight visibly affects predictions near that bump's centre, but a small change to a polynomial weight shifts predictions *everywhere*.
  - The deepest gap: pianos are 1D (input = "which key"). ML basis functions take vector inputs $x \in \mathbb{R}^D$ and produce a scalar. Spatial structure matters in ways pianos don't capture.

## Definition

A **basis function** is any function $\phi_j : \mathbb{R}^D \to \mathbb{R}$ chosen *before* seeing data, used as a feature in a linear model

$$
y(x, w) \;=\; \sum_{j=0}^{M-1} w_j\,\phi_j(x) \;=\; w^T \phi(x).
$$

The convention is $\phi_0(x) \equiv 1$ so that $w_0$ acts as the **bias parameter** (constant offset). The model is "linear" in $w$ (which is what lets us solve it in closed form), but $y(x, w)$ can be wildly *non*linear in $x$ if the $\phi_j$ are.

## Three standard families (from Bishop & Bishop §4.1.1)

| Family | Form | Locality | Where it shines |
|---|---|---|---|
| **Polynomial** | $\phi_j(x) = x^j$ | Global — every basis function is non-zero everywhere | Smooth low-dim functions; small $M$ |
| **Gaussian** ("RBF") | $\phi_j(x) = \exp\!\left(-\frac{(x-\mu_j)^2}{2s^2}\right)$ | Local — peaks at $\mu_j$, decays fast | Functions with spatial structure (bumps, peaks) |
| **Sigmoidal** | $\phi_j(x) = \sigma\!\left(\frac{x-\mu_j}{s}\right)$ | Soft step at $\mu_j$ | Functions that "turn on" at certain thresholds; the [[Sigmoid Function]] |

Also common: **Fourier basis** (sines and cosines at different frequencies — global, frequency-localized) and **wavelets** (localized in both space and frequency).

## Worked example: 1D polynomial regression as a basis function model

Polynomial curve fitting $y(x, w) = w_0 + w_1 x + w_2 x^2 + \cdots + w_M x^M$ is literally a linear model with $\phi_j(x) = x^j$. The model is *linear in $w$* — that's why we can solve it with the normal equations / [[Moore-Penrose Pseudoinverse]] — even though the predictions trace out arbitrary-order polynomial curves in $x$.

## The "linear in $w$, possibly nonlinear in $x$" trick

This is the deepest insight in §4.1. **"Linear model" does not mean "the prediction is a straight line."** It means *the prediction is a linear combination of the parameters*. The basis functions are allowed to do arbitrary nonlinear preprocessing of $x$ first; we just demand that the *combination step* be a simple weighted sum. That linearity in $w$ is what gives us:

- Closed-form MLE via the pseudoinverse (one matrix inverse, done).
- Convex loss (single global minimum, no local minima to worry about).
- Clean geometric interpretation as orthogonal projection.

The cost: you have to pick the basis functions yourself, *before* seeing the data. For low-dimensional problems with clear structure, this is fine. For high-dimensional problems (images, audio, text), it's hopeless.

## The pivot to deep learning: learned basis functions

**The single most important sentence in Bishop & Bishop Chapter 4:**

> *"Before the advent of deep learning it was common practice in machine learning to use some form of fixed pre-processing of the input variables x, also known as feature extraction, expressed in terms of a set of basis functions $\{\phi_j(x)\}$. The goal was to choose a sufficiently powerful set of basis functions that the resulting learning task could be solved using a simple network model. Unfortunately, it is very difficult to hand-craft suitable basis functions for anything but the simplest applications. Deep learning avoids this problem by learning the required nonlinear transformations of the data from the data set itself."* (§4.1.1)

That paragraph is the conceptual bridge to Ch 6. **A hidden layer in a deep network IS a learned basis function** — one per hidden unit. The output layer is then a linear-in-$w$ combination of those learned features. Every modern deep network is the basis-function template with the basis functions trained jointly with the output weights.

**Concretely:** when you see a 1-hidden-layer MLP $y(x, w, W) = w^T h(W x)$, read it as "linear regression in the basis $\phi_j(x) = h(W_j^T x)$ — except $W_j$ is learnable too." Stack more layers → richer learned features. The basis-function template never goes away; it just gets recursive.

## Single-layer network diagram

Bishop & Bishop's Figure 4.1: the basis-function model drawn as a one-layer neural network.

```
  φ_{M-1}(x)  ────── w_{M-1} ──┐
       :                       │
   φ_1(x)  ──────── w_1 ───────┼─── Σ ─── y(x, w)
       :                       │
   φ_0(x)=1 ────── w_0 ────────┘
```

Each basis function is an *input node*; each weight is an *edge*; the output is the weighted sum. Multiple outputs (regression for $K$ targets) → $K$ output nodes, sharing the basis functions but with their own weight vectors.

This is the picture Ch 6 generalizes by **adding layers between the inputs and the basis-function-output nodes** — i.e., letting the network *compute* the $\phi_j$ rather than taking them pre-baked.

## Common confusions

- **"Basis function" vs "feature".** These are the same thing under different academic dialects. ML papers often say "features"; statistics + Bishop say "basis functions". The vector $\phi(x) = (\phi_0(x), \ldots, \phi_{M-1}(x))^T$ is the "feature vector".
- **"Linear model" vs "linear function".** Linear *model* means linear in $w$. Linear *function* (of $x$) means a straight line / hyperplane. A polynomial basis-function model is a linear *model* whose prediction is a nonlinear function of $x$.
- **The bias term.** Setting $\phi_0(x) \equiv 1$ folds the bias parameter $w_0$ into the basis-function framework cleanly. Without that convention you'd write $y = w^T \phi(x) + b$; with the convention you just write $y = w^T \phi(x)$. Same content, less notation.
- **Why hand-picking basis functions fails in high dimensions.** The curse of dimensionality: if you want to tile a $D$-dimensional input space with Gaussian bumps, you need $O(K^D)$ bumps to cover the space at resolution $K$ — exponentially many. Ch 6 §6.1 makes this explicit and uses it as the launchpad for hidden layers.

## Where you'll meet basis functions in Ch 6+ (translation guide)

| When Ch 6 says... | Translate to... |
|---|---|
| "Linear models with fixed basis functions" | Ch 4–5 single-layer models |
| "Hidden units" | Learned basis functions, one per unit |
| "Feature map $\phi(x)$" | The vector of basis-function values $(\phi_1(x), \ldots, \phi_{M-1}(x))^T$ |
| "Feature extraction" | The whole $x \mapsto \phi(x)$ transformation |
| "Hand-crafted features" | $\phi_j$ chosen by the modeler from a fixed family |
| "Learned representations" | $\phi_j$ trained jointly with the output weights |

## Origins / sources

- **Bishop & Bishop, *Deep Learning: Foundations and Concepts* (2024)**, §4.1.1 — the canonical modern treatment; cited for the "linear in $w$" trick and the three standard families.
- **Bishop, *Pattern Recognition and Machine Learning* (2006)**, Ch 3 — fuller historical treatment with more families (Fourier, splines, wavelets).
- The framework is much older: dates to early-20th-century statistics (Galton, Pearson) and was the workhorse of pre-deep-learning ML through the 1980s–2000s.

## Related concepts

- [[Linear Regression]] — the canonical use case for basis functions (regression head on top).
- [[Logistic Regression]] — basis functions plus sigmoid + cross-entropy = single-layer classification.
- [[Sigmoid Function]] — one of the three standard basis-function families.
- [[Moore-Penrose Pseudoinverse]] — solves the closed-form MLE problem for linear-in-$w$ models with basis functions.
- [[Bishop and Bishop - Deep Learning Foundations and Concepts]] — the source.
- (red link) [[Hidden Units]] — the deep-learning generalization: learned basis functions.
- (red link) [[Feature Extraction]] — the umbrella term for the pre-processing step.

## Mentions

- [[Bishop and Bishop - chapters]] — Ch 4 + Ch 5 + Ch 6 all use the basis-function frame.
- [[Bishop and Bishop - Deep Learning Foundations and Concepts]] — source page.
