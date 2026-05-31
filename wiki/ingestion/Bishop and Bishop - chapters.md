---
type: ingestion-index
source: "[[Bishop and Bishop - Deep Learning Foundations and Concepts]]"
created: 2026-05-31
updated: 2026-05-31
last_chapter_studied: 5
---

# Bishop & Bishop, *Deep Learning: Foundations and Concepts* — chapter index

> Chapter-level coverage tracker for the 2024 Springer textbook. PDF page = book page + 19 (front-matter offset). Use the *PDF pages* column for `pdftotext -f X -l Y` extraction; the *book pages* column matches the printed page numbers in the textbook itself.

Status values: `not started` | `queued` | `next` | `partial` | `covered`

| # | Title | Book pages | PDF pages | Concepts | Status |
|---|---|---|---|---|---|
| 1 | The Deep Learning Revolution | 1–22 | 20–41 | tutorial example (polynomial curve fitting, error function, model complexity, regularization, model selection); brief history of ML | not started |
| 2 | Probabilities | 23–64 | 42–83 | sum/product rules, Bayes, probability densities, Gaussian, transformation of densities, information theory (entropy, KL divergence), Bayesian probabilities | not started |
| 3 | Standard Distributions | 65–110 | 84–129 | Bernoulli/binomial/multinomial, multivariate Gaussian (conditional/marginal/Bayes/MLE), periodic distributions (von Mises), exponential family, nonparametric methods (histograms, KDE, k-NN) | not started |
| 4 | Single-layer Networks: Regression | 111–129 | 130–148 | [[Basis Functions]], [[Linear Regression]] (MLE = MSE under Gaussian noise), [[Moore-Penrose Pseudoinverse]] (closed-form solution + orthogonal-projection geometry), sequential learning / [[Stochastic Gradient Descent]] (LMS), [[L2 Regularization]] / weight decay, decision theory (squared loss → conditional mean), [[Bias-Variance Trade-off]] | covered |
| 5 | Single-layer Networks: Classification | 131–167 | 150–186 | linear discriminants + hyperplane geometry, multi-class (one-vs-rest gotcha), 1-of-K coding, three-approaches taxonomy (generative/discriminative/discriminant), classifier metrics (precision/recall/F/ROC/AUC), generative classifiers with Gaussian class-conditionals → [[Sigmoid Function]] and [[Softmax]] emerge as log-odds formulas, [[Logistic Regression]] + [[Cross-Entropy Loss]] (MLE on Bernoulli/multinomial), [[Generalized Linear Models]] + canonical link functions (activation-loss pairing rule) | covered |
| 6 | Deep Neural Networks | 169–198 | 188–217 | limitations of fixed basis functions, curse of dimensionality, data manifolds, multi-layer perceptrons, feed-forward networks, universal approximation | next |
| 7 | Gradient Descent | — | — | gradient descent variants, momentum, Adam, learning rate schedules, mini-batch SGD | queued |
| 8 | Backpropagation | — | — | chain rule, computational graphs, automatic differentiation | queued |
| 9 | Regularization | — | — | early stopping, dropout, data augmentation, batch normalization, layer normalization | queued |
| 10 | Convolutional Networks | — | — | convolutions, pooling, architectures (LeNet → ResNet) | queued |
| 11 | Structured Distributions | — | — | graphical models (directed/undirected), conditional independence | queued |
| 12 | Transformers | — | — | self-attention, multi-head attention, encoder-decoder, decoder-only | queued |
| 13 | Graph Neural Networks | — | — | message passing, graph convolutions | queued |
| 14 | Sampling | — | — | rejection sampling, importance sampling, MCMC, Gibbs, Hamiltonian Monte Carlo | queued |
| 15 | Discrete Latent Variables | — | — | k-means, EM, mixtures, hidden variables | queued |
| 16 | Continuous Latent Variables | — | — | PCA, probabilistic PCA, factor analysis, **VAE + ELBO + reparameterization trick** | queued — **prereq for Diffusion Crash Course Block A** |
| 17 | Generative Adversarial Networks | — | — | GANs, mode collapse, Wasserstein GANs | queued |
| 18 | Normalizing Flows | — | — | change of variables, coupling flows (RealNVP), autoregressive flows | queued — complements [[Normalizing Flows Tutorial Part 1 - Eric Jang]] |
| 19 | Autoencoders | — | — | denoising autoencoders, sparse autoencoders | queued |
| 20 | Diffusion Models | — | — | DDPM, score-based, SDEs, classifier-free guidance, applications | queued — **complements [[Diffusion Models]] vault page** |
| 21+ | Reinforcement Learning, Structured Prediction, etc. | — | — | TBD | queued |

*Page ranges for chapters 7+ to be filled in as those chapters are studied.*

## Recommended reading order

- **Foundation thread** (for users at the user's current level): Ch 4 → Ch 5 → Ch 6 → Ch 7 → Ch 8. Builds the regression-classification-deep-network-training core in five chapters.
- **Diffusion thread**: Ch 2 (probability prereq if not solid) → Ch 16 (VAE / ELBO / reparameterization) → Ch 20 (diffusion). Aligns with [[Diffusion Crash Course - synthesis]] Saturday-morning block.
- **Generative-models thread**: Ch 16 (VAE) → Ch 17 (GAN) → Ch 18 (NF) → Ch 19 (autoencoder) → Ch 20 (diffusion). The full generative-modeling tour as a 5-chapter arc.
- **Transformers / LLM thread**: Ch 8 (backprop) → Ch 12 (transformers, self-attention). Smallest path to reading modern LLM papers.

## Appendices

- **A**: Linear Algebra
- **B**: Calculus of Variations
- **C**: Lagrange Multipliers — *covered* via [[Lagrange Multipliers]] (independently from textbook)
- **D**: (TBD — verify on next read)
