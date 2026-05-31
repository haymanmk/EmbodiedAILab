---
type: concept
domain: research
created: 2026-05-31
updated: 2026-05-31
aliases: ["logistic classifier", "binary classifier with sigmoid output", "LR (classification)"]
tags: [machine-learning, classification, glm, foundations, bishop]
sources:
  - "[[Bishop and Bishop - Deep Learning Foundations and Concepts]]"
---

# Logistic Regression

## Explain like I'm 5

You want to decide: spam or not spam? Hot dog or not hot dog? Cancer or not cancer? You have some features of the input (word counts, pixel values, biomarkers) and you want a probability between 0 and 1.

**Logistic regression**: take a weighted sum of the features (just like linear regression), then squash it through a sigmoid so it becomes a probability. That probability is your prediction.

$$
y \;=\; \sigma(w^T \phi(x) + w_0) \;=\; \frac{1}{1 + \exp\!\bigl(-(w^T \phi(x) + w_0)\bigr)}.
$$

That's it. The name is misleading — it has "regression" in it but it's a *classifier* (because the output is a probability for a class).

## Bridges from

- **Voting committee with a thermometer.** Each feature $\phi_j(x)$ is a committee member with a vote weight $w_j$ that says how strongly they think the answer is "yes" (positive weight) or "no" (negative weight). The committee tallies the weighted votes into a single number (the "log-odds" or "logit"). Then the sigmoid acts as a thermometer that converts the tally into a probability between 0 and 1.

  *Where the analogy breaks down*:
  - Real committees don't have closed-form decision rules; logistic regression has a *convex* loss (binary cross-entropy) with a single global optimum. Gradient descent always finds the right weights.
  - The "thermometer" never quite reaches 0 or 1. The sigmoid asymptotes at the extremes but never touches them. (This is a feature: it prevents the model from being infinitely confident, which matters for [[Cross-Entropy Loss]] and stable training.)
  - The committee can deadlock at 50% (output $\sigma(0) = 0.5$). That's the decision boundary; on the boundary, the model is maximally uncertain.

## Definition

For binary classification with input $x$ and a basis function feature map $\phi(x)$:

$$
\boxed{\;p(C_1 \mid x) \;=\; \sigma(w^T \phi(x))\;}, \qquad \sigma(a) = \frac{1}{1 + e^{-a}}.
$$

The decision rule: predict class $C_1$ if $p(C_1 \mid x) > 0.5$, else class $C_2$. Equivalently: predict $C_1$ if $w^T \phi(x) > 0$. **The decision boundary $w^T \phi(x) = 0$ is a hyperplane in feature space** — and (because $\sigma$ is monotone) the decision surface in input space $x$ may be nonlinear, but the *feature-space* boundary is linear. That's why this is still called a "linear classifier."

## Why sigmoid? It's the log-odds formula

This is the most elegant derivation in Bishop & Bishop Ch 5. Suppose you have two classes with class-conditional densities $p(x \mid C_k)$ and priors $p(C_k)$. By Bayes' theorem:

$$
p(C_1 \mid x) \;=\; \frac{p(x \mid C_1) p(C_1)}{p(x \mid C_1) p(C_1) + p(x \mid C_2) p(C_2)}.
$$

Define $a \;:=\; \ln \frac{p(x \mid C_1)p(C_1)}{p(x \mid C_2)p(C_2)}$ — this is the **log-odds** (or "logit") of class 1 vs class 2. Divide the Bayes ratio top and bottom by $p(x \mid C_1)p(C_1)$ and you get exactly:

$$
p(C_1 \mid x) \;=\; \frac{1}{1 + e^{-a}} \;=\; \sigma(a).
$$

**The sigmoid isn't an arbitrary activation choice — it's the formula that converts a log-odds ratio into a probability.** Anywhere in ML you see a sigmoid output for binary classification, there's an implicit log-odds story behind it.

When the class-conditionals are Gaussian with shared covariance, the log-odds works out to be a *linear function* of $x$ (the quadratic terms cancel between classes), so $a = w^T x + w_0$ and the sigmoid acts on a linear function. That's the generative-model derivation. Logistic regression skips it and just *posits* $a = w^T \phi(x)$ directly, training $w$ to fit observed labels.

## Training: MLE = minimize binary cross-entropy

Given $\{(x_n, t_n)\}$ with $t_n \in \{0, 1\}$, the per-example likelihood is

$$
p(t_n \mid \phi_n, w) \;=\; y_n^{t_n} (1-y_n)^{1-t_n}, \qquad y_n = \sigma(w^T \phi_n).
$$

(This is just $y_n$ if $t_n = 1$ and $1 - y_n$ if $t_n = 0$, written as a single formula.) Taking $-\ln$ of the product gives **binary cross-entropy** (see [[Cross-Entropy Loss]]):

$$
E(w) \;=\; -\sum_n \bigl\{ t_n \ln y_n + (1 - t_n) \ln(1 - y_n) \bigr\}.
$$

The gradient — and this is the satisfying part — comes out as

$$
\nabla E(w) \;=\; \sum_n (y_n - t_n)\, \phi_n.
$$

**Prediction error times input features.** The $\sigma'(a) = \sigma(1-\sigma)$ factor that you'd expect from differentiating the sigmoid *cancels exactly* because it appears in both the numerator (from the loss) and denominator (from differentiating $\ln \sigma$). This cancellation is the *canonical-link* magic, derived in [[Generalized Linear Models]] §5.4.6.

**No closed-form solution.** Unlike linear regression, the gradient $= 0$ equation is nonlinear in $w$ (because $y_n = \sigma(\text{linear in } w)$). But the loss is **convex** in $w$, so gradient descent (or specialized methods like Iterative Reweighted Least Squares / IRLS) always converges to the global optimum.

## Single-layer neural network = logistic regression

The architecture diagram:

```
  φ_{M-1}(x)  ────── w_{M-1} ──┐
       :                       │
   φ_1(x)  ──────── w_1 ───────┼─── Σ ─── σ(·) ─── y = p(C_1|x)
       :                       │
   φ_0(x)=1 ────── w_0 ────────┘
```

Same as [[Basis Functions]]' single-layer regression diagram, with a sigmoid stuck on the output. This is the structural template Ch 6+ generalizes by **adding hidden layers between the inputs and the sigmoid output**. The output unit of any binary-classification deep neural network is, at its heart, a logistic regression on top of learned features.

## Watch out: linearly-separable data leads to weight blow-up

If your training data is **linearly separable** (no class overlap in feature space), MLE has no unique solution — the optimal $w$ has unbounded magnitude. Why? You can keep scaling $w$ up; the decision boundary stays the same, but the predicted probabilities sharpen toward exact 0 or 1, driving the cross-entropy toward 0 asymptotically. There's no finite minimizer.

Symptoms in practice:
- Weight magnitudes grow without bound during training
- Predictions become overconfident (0 or 1 with no uncertainty)
- Test-set generalization suffers

**Fix**: add L2 regularization ($+\frac{\lambda}{2}\|w\|^2$ to the loss). This is exactly the [[L2 Regularization|weight-decay]] pattern from regression. Bishop & Bishop §5.4.3 calls this out explicitly.

## Logistic regression vs linear-Gaussian classifier (parameter counts)

For an $M$-dimensional feature space:
- **Logistic regression** has $M$ learnable parameters (the $w$ vector).
- **Generative Gaussian classifier with shared covariance** has $2M$ (two means) + $M(M+1)/2$ (shared covariance) + $1$ (class prior) = $M(M+5)/2 + 1$ parameters.

So logistic regression scales **linearly** with $M$ while the generative alternative scales **quadratically**. For high-dimensional features (images, text embeddings), this is a decisive advantage of the discriminative approach. (Bishop & Bishop §5.4.3.)

## Common confusions

- **"Logistic regression" is a classifier, not a regressor.** The name is historical (it's a *generalized linear regression* with a logistic link function), but the task is binary classification.
- **Probability output vs hard label.** The model's output $y \in (0, 1)$ is a *probability*. To get a hard label, threshold at 0.5 (or another threshold to trade off precision/recall). The probability is what's useful for downstream — for [[Cross-Entropy Loss]] training, for the reject option, for combining with other model outputs.
- **Logistic regression vs softmax regression.** Logistic regression handles 2 classes; **softmax regression** (also called "multinomial logistic regression" or "multi-class logistic regression") handles $K \geq 2$ classes with [[Softmax]] output and categorical cross-entropy loss. Same canonical-link template, more outputs.
- **"Linear classifier" doesn't mean "linear function".** Logistic regression's decision boundary is linear *in feature space* $\phi$; in raw input space $x$ it can be highly nonlinear (depending on how $\phi$ is constructed). Pre-deep-learning practice: hand-pick nonlinear $\phi$; post-deep-learning: learn $\phi$ via hidden layers.
- **"It's just an MLP without hidden layers."** Yes! And every binary-classification deep network's output unit is a logistic regression on top of learned features. The structural template never changes.

## In code (PyTorch idiom)

```python
import torch.nn as nn

# Bare logistic regression — no hidden layers
model = nn.Linear(input_dim, 1)        # outputs raw logit w^T x
loss_fn = nn.BCEWithLogitsLoss()       # combines sigmoid + BCE for numerical stability
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# Training step
logits = model(x)                      # shape (batch,)
loss = loss_fn(logits, t.float())      # t in {0, 1}
loss.backward()
optimizer.step()

# At inference, apply sigmoid manually if you want a probability
probs = torch.sigmoid(model(x))
```

`BCEWithLogitsLoss` does sigmoid + binary cross-entropy in one numerically-stable formula. Don't do `sigmoid` then `BCELoss` separately; that's less stable and is the source of the "NaN loss after a few epochs" beginner gotcha.

## Origins / sources

- **Bishop & Bishop, *Deep Learning: Foundations and Concepts* (2024)**, §5.3 (sigmoid as log-odds derivation), §5.4.3 (logistic regression as discriminative model with cross-entropy MLE), §5.4.6 (canonical link).
- Classical statistics dating to Berkson (1944) and Cox (1958), introduced to handle binary outcomes in epidemiology and quantal bioassay.
- The "sigmoid as squashing function" terminology comes from McCulloch & Pitts (1943) — the first artificial neuron.

## Related concepts

- [[Sigmoid Function]] — the output activation; the log-odds → probability mapping.
- [[Cross-Entropy Loss]] — the loss function paired with the sigmoid output (binary cross-entropy).
- [[Generalized Linear Models]] — the framework that explains the sigmoid+BCE pairing as the *canonical link* for Bernoulli targets.
- [[Softmax]] — the multi-class generalization.
- [[Basis Functions]] — the feature map $\phi(x)$ that logistic regression sits on top of.
- [[L2 Regularization]] (red link if missing) — the standard fix for linearly-separable data weight blow-up.
- [[Bishop and Bishop - Deep Learning Foundations and Concepts]] — the source.

## Mentions

- [[Bishop and Bishop - chapters]] — Ch 5
- [[Cross-Entropy Loss]], [[Softmax]], [[Generalized Linear Models]], [[Sigmoid Function]]
