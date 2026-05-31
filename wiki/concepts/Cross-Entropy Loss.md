---
type: concept
domain: research
created: 2026-05-31
updated: 2026-05-31
aliases: ["cross entropy", "log loss", "negative log-likelihood", "binary cross-entropy", "BCE", "categorical cross-entropy"]
tags: [machine-learning, classification, loss-functions, foundations, bishop]
sources:
  - "[[Bishop and Bishop - Deep Learning Foundations and Concepts]]"
---

# Cross-Entropy Loss

## Explain like I'm 5

You have a weather forecaster. Each day they give you a probability: "70% chance of rain." Then the day actually happens — it either rained or didn't. **Cross-entropy is the bill the forecaster pays for being surprised.**

- It rained, and they predicted 90% rain → tiny bill (they were nearly certain, and they were right).
- It rained, and they predicted 10% rain → huge bill (they were nearly certain, and they were *wrong*).
- It rained, and they predicted 50% rain → medium bill (they hedged).

Specifically, if the true outcome is "rain" and they predicted probability $y$ for rain, the bill is $-\ln y$. So a 90%-rain prediction that turned out to be rain costs $-\ln 0.9 \approx 0.105$; a 10%-rain prediction that turned out to be rain costs $-\ln 0.1 \approx 2.30$ — twenty times worse. Crucially, predicting *zero* probability for the thing that actually happens costs **infinity** — the worst possible bill — because $-\ln 0 = \infty$.

Cross-entropy is the **average bill across all the days**. A classifier minimizing cross-entropy is a forecaster trying to minimize their expected bill.

## Bridges from

- **Surprise meter (extended)**. Cross-entropy is the *information cost* of using your predicted probabilities as a code for what actually happened. The more concentrated your prediction was on the truth, the cheaper the code; the more concentrated on the wrong thing, the more expensive. The mathematical name for this is "the expected number of nats (or bits) needed to encode the truth under your distribution."

  *Where the analogy breaks down*:
  - Real weather forecasters get bills measured in money or reputation; cross-entropy is measured in *log-probability units* (nats if natural log, bits if log base 2). The unit isn't intuitive — it's just a number you minimize.
  - The "bill" analogy makes it sound like a one-off transaction. Cross-entropy is computed over the entire dataset and averaged; one bad prediction can be diluted by many good ones.
  - The infinity-for-predicting-zero behaviour is a real feature, not an analogy quirk. Models that need to handle "could be anything" outputs must use distributions with support everywhere (Gaussian, softmax with finite logits) — not categorical distributions that can assign exact zero.

## Definition

For binary classification with true labels $t_n \in \{0, 1\}$ and predicted probabilities $y_n = p(\text{class 1} \mid x_n) \in (0, 1)$:

$$
\boxed{\;E(\theta) \;=\; -\sum_{n=1}^N \bigl\{\,t_n\,\ln y_n \;+\; (1-t_n)\,\ln(1-y_n)\,\bigr\}\;}
$$

This is the **binary cross-entropy** or **BCE**. Read each term: if $t_n=1$, only the $-\ln y_n$ part contributes (you get penalized for $y_n$ being far from 1); if $t_n=0$, only the $-\ln(1-y_n)$ part contributes (you get penalized for $y_n$ being far from 0).

For multi-class classification with one-hot targets $t_{nk} \in \{0,1\}$ and softmax predictions $y_{nk} = p(C_k \mid x_n)$:

$$
\boxed{\;E(\theta) \;=\; -\sum_{n=1}^N \sum_{k=1}^K t_{nk}\,\ln y_{nk}\;}
$$

This is the **categorical cross-entropy**. For each example $n$, only one $t_{nk}$ is 1 (the true class), so the sum reduces to $-\ln y_{n,k^*}$ where $k^*$ is the true class — the surprise meter, applied to the predicted probability of the correct class.

Both reduce to **negative log-likelihood** under the appropriate target distribution: Bernoulli for binary, multinomial for multi-class. So minimizing cross-entropy = maximum likelihood estimation.

## Where it comes from: MLE on Bernoulli / multinomial

For a binary classifier with prediction $y_n = \sigma(w^T \phi_n)$ (logistic regression — see [[Logistic Regression]]), the per-example likelihood is

$$
p(t_n \mid \phi_n, w) \;=\; y_n^{t_n}\,(1-y_n)^{1-t_n}
$$

(this is just $y_n$ if $t_n=1$ and $1-y_n$ if $t_n=0$, written compactly). The full likelihood is the product across all $N$ examples; taking $-\ln$ turns the product into a sum and gives binary cross-entropy. **There's no other choice** if you assume your targets are Bernoulli-distributed conditional on $x$.

The multi-class case is identical with the multinomial replacing the Bernoulli: $p(t_n \mid \phi_n, w) = \prod_k y_{nk}^{t_{nk}}$; take $-\ln$, sum, get categorical cross-entropy.

## The clean-gradient miracle: $(y - t) \cdot \phi$

For both binary and multi-class cross-entropy *paired with the corresponding canonical-link activation* (sigmoid for binary, softmax for multi-class), the gradient is

$$
\nabla_w E \;=\; \sum_n (y_n - t_n)\,\phi_n.
$$

(For multi-class, $\nabla_{w_k} E = \sum_n (y_{nk} - t_{nk})\,\phi_n$.) Read: **prediction error times input features**. No sigmoid-derivative terms, no softmax-Jacobian terms — they cancel exactly because of the activation-loss pairing.

This is the same gradient form as MSE loss for linear regression. Once you see this, you understand why the same training loop (vanilla SGD) works for regression and classification interchangeably — *as long as you pair the activation and loss correctly*.

## Why pair correctly: the vanishing-gradient warning

If you instead pair **sigmoid output + MSE loss** (a common beginner mistake), the gradient picks up a $\sigma'(a) = \sigma(1-\sigma)$ factor that *does not cancel*. Near $y \approx 0$ or $y \approx 1$, $\sigma' \approx 0$, so the gradient is nearly zero and **training stalls** even though the loss is still huge. This is the [[Sigmoid Function]]-page-noted "vanishing gradient pitfall" for the wrong loss pairing.

The right rule, drilled into every Ch 5 reader:

| Output type | Activation | Loss |
|---|---|---|
| Continuous, real-valued | Linear (identity) | MSE |
| Binary {0, 1} | Sigmoid | Binary cross-entropy |
| Categorical (K classes) | Softmax | Categorical cross-entropy |

These three pairings are the **canonical link function** pairings from §5.4.6 — they give the clean $(y-t)\phi$ gradient and prevent vanishing-gradient stalls. Any deep-learning framework's defaults (`nn.MSELoss`, `nn.BCEWithLogitsLoss`, `nn.CrossEntropyLoss` in PyTorch) implement exactly these pairings, often combining activation and loss in one function for numerical stability.

## Connection to KL divergence and entropy

Cross-entropy decomposes as

$$
H(p, q) \;=\; H(p) + D_{\mathrm{KL}}(p \,\|\, q)
$$

where $p$ is the true distribution, $q$ is your predicted distribution, $H(p) = -\sum p\log p$ is the entropy of $p$ (intrinsic, irreducible), and $D_{\mathrm{KL}}$ is the Kullback-Leibler divergence (how much $q$ wastes vs the perfect coder $p$). When $p$ is fixed (e.g., a one-hot label distribution), $H(p) = 0$ and **minimizing cross-entropy = minimizing KL divergence** between predicted and true distributions. This is the link to information theory that Bishop covers in Ch 2 §2.5.

## Common confusions

- **"Cross-entropy" vs "log loss" vs "negative log-likelihood".** All the same object under different names. *Cross-entropy* is the information-theoretic name (its definition as $-\sum p \log q$); *log loss* is the ML-engineering nickname; *negative log-likelihood* is the statistical name (since under Bernoulli/multinomial assumptions, the loss equals $-\ln p(\text{data} \mid \text{model})$).
- **"Binary cross-entropy" vs "categorical cross-entropy".** Same object, different number of classes. BCE handles 2 classes (one output between 0 and 1, paired with sigmoid). CCE handles $K \geq 2$ classes (a vector of $K$ outputs that sum to 1, paired with softmax). Both reduce to $-\sum_n \ln y_{n,k^*}$ for true-class index $k^*$.
- **"Cross-entropy" with hard vs soft labels.** With *hard* one-hot labels, $t_{nk} \in \{0, 1\}$ and only the true-class term survives. With *soft* labels (e.g., from label smoothing or teacher-student distillation), $t_{nk}$ can be a smooth probability distribution and cross-entropy generalizes naturally — it's still $-\sum t_{nk} \ln y_{nk}$, just with more non-zero $t$ terms.
- **"Numerical stability".** Computing $\sigma(z)$ then $\ln \sigma(z)$ separately overflows for negative $z$ (the $\sigma$ underflows to 0). Frameworks combine into a single $\text{log-sum-exp}$-based formula (e.g., PyTorch's `BCEWithLogitsLoss` and `CrossEntropyLoss` take *logits* not probabilities for this reason).
- **The "perfect classifier" gives loss zero, not infinity.** When $y_n = t_n$ for all $n$, cross-entropy = $-\sum_n 1 \cdot \ln 1 = 0$. Loss is minimized at perfection. The infinity only shows up when the model is *confident and wrong*.

## Worked example: a 3-class classifier

Say true class is $C_2$, so $t = (0, 1, 0)$. The model predicts probabilities $y = (0.1, 0.7, 0.2)$. The cross-entropy for this single example is

$$
-(0 \cdot \ln 0.1 + 1 \cdot \ln 0.7 + 0 \cdot \ln 0.2) \;=\; -\ln 0.7 \;\approx\; 0.357.
$$

If instead $y = (0.7, 0.1, 0.2)$ (model very confident it's class $C_1$, but actually $C_2$), the cross-entropy is $-\ln 0.1 \approx 2.30$ — about 6.5× higher. If the model predicted $y = (0.45, 0.45, 0.10)$ (genuine uncertainty between $C_1$ and $C_2$), the loss is $-\ln 0.45 \approx 0.799$ — penalized for not being more confident in the truth, but much less than for being confidently wrong.

## Origins / sources

- **Bishop & Bishop, *Deep Learning: Foundations and Concepts* (2024)**, §5.4.3 (binary) and §5.4.4 (multi-class) — the canonical derivation from MLE on Bernoulli/multinomial.
- The general information-theoretic concept dates to Shannon (1948), *A Mathematical Theory of Communication*.
- The application to neural-network classification was popularized in the 1980s–90s (Hinton et al., Bishop's *Neural Networks for Pattern Recognition* 1995) as the replacement for MSE on classification problems.

## Related concepts

- [[Logistic Regression]] — the canonical use case for binary cross-entropy (sigmoid output).
- [[Softmax]] — the canonical use case for categorical cross-entropy (softmax output).
- [[Sigmoid Function]] — sigmoid + BCE is the canonical-link pairing for binary classification.
- [[Generalized Linear Models]] — the broader framework that explains *why* the activation-loss pairing rule works.
- [[Normalizing Constant]] — softmax's denominator is a normalizing constant; cross-entropy is the negative log-likelihood the normalization makes possible.
- [[Bishop and Bishop - Deep Learning Foundations and Concepts]] — the source.
- (red link) [[KL Divergence]] — cross-entropy = entropy + KL.

## Mentions

- [[Logistic Regression]]
- [[Softmax]]
- [[Generalized Linear Models]]
- [[Bishop and Bishop - chapters]] — Ch 5
