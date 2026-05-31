---
type: source
domain: research
created: 2026-05-31
updated: 2026-05-31
source_url: https://www.bishopbook.com
source_path: "raw/Christopher M. Bishop, Hugh Bishop - Deep Learning_ Foundations and Concepts-Springer (2024).pdf"
source_format: pdf
total_pages: 656
author: Christopher M. Bishop, Hugh Bishop
published: 2024
chunks_indexed: false
indexed_at:
study_status: in-progress
tags: [textbook, deep-learning, foundations, bishop, classification, regression, neural-networks]
---

# Deep Learning: Foundations and Concepts — Bishop & Bishop (Springer 2024)

> The successor to Bishop's *Neural Networks for Pattern Recognition* (1995) and the deep-learning-era companion to *Pattern Recognition and Machine Learning* (2006). Self-contained introduction with probability theory, linear algebra appendix, and a chapter-per-topic structure. Top textbook recommendation in the diffusion crash course's "probability fundamentals" block.

## Summary

656-page Springer textbook organized into 20+ "bite-sized" chapters, each depending only on earlier ones. Bishop & Bishop deliberately avoid trying to survey the latest research, instead distilling the *foundational concepts* that have remained stable for decades (transformers, attention, MLE, ELBO, MSE, cross-entropy) plus the modern deep-learning machinery built on them. The book is structured so a reader can use it as either a one-semester or two-semester course, and is equally suited to self-study (free digital edition at bishopbook.com).

Three areas of mathematics are assumed at the level the book provides: probability theory (covered self-contained in Ch 2), linear algebra (appendix), multivariate calculus (assumed; appendix covers calculus-of-variations + Lagrange multipliers). The treatment is **non-Bayesian** — that's the major scope choice vs PRML (2006). Coverage of generative models (Ch 18–20) includes VAEs, normalizing flows, GANs, and diffusion (Ch 20) — so the book itself is the natural anchor for a generative-modeling thread.

For this vault, the textbook is the **central deep-learning reference** going forward — every concept page that touches a foundational ML idea (MLE, cross-entropy, basis functions, regularization, bias-variance, sigmoid, softmax, logistic regression) should cite back here. The diffusion crash course ([[Diffusion Crash Course - synthesis]]) recommends Ch 16 (latent-variable models) and Ch 20 (diffusion) as primary readings.

## Key claims (chapter-level)

- **Ch 1 *The Deep Learning Revolution***: motivating tour through impact areas (medical, AlphaFold, image synthesis, LLMs), a tutorial example on polynomial curve fitting that introduces error functions, regularization, and bias-variance, and a brief history.
- **Ch 2 *Probabilities***: self-contained probability fundamentals — sum/product rules, Bayes' theorem, expectations, Gaussian distribution, transformation of densities, information theory (entropy, KL divergence), Bayesian probabilities. The probability prerequisites for everything that follows.
- **Ch 3 *Standard Distributions***: discrete (Bernoulli, binomial, multinomial), multivariate Gaussian (with full conditional/marginal/Bayes derivations and the exponential-family generalization), periodic distributions (von Mises), nonparametric methods (histograms, KDE, k-NN).
- **Ch 4 *Single-layer Networks: Regression***: linear regression with basis functions; MLE under Gaussian noise → sum-of-squares; closed-form solution via [[Moore-Penrose Pseudoinverse]]; geometric interpretation as orthogonal projection; sequential learning (SGD / LMS); L2 regularization / weight decay; decision theory (squared loss → conditional mean); bias-variance decomposition.
- **Ch 5 *Single-layer Networks: Classification***: linear discriminants; three-approaches taxonomy (generative / discriminative / discriminant function); decision theory with loss matrices and reject option; classifier metrics (precision, recall, F-score, ROC/AUC); **sigmoid as the log-odds → probability formula**; **softmax as the K-class generalization**; generative classifiers with Gaussian class-conditionals (linear vs quadratic discriminants); logistic regression + cross-entropy MLE; multi-class logistic = softmax regression; canonical link functions (activation-loss pairing rule).
- **Ch 6 *Deep Neural Networks***: motivates multi-layer networks via the limitations of fixed basis functions and the curse of dimensionality; introduces feed-forward networks / multi-layer perceptrons and the case for learned features.
- **Ch 7 *Gradient Descent***: training algorithms — vanilla SGD, momentum, Adam, learning-rate schedules, etc.
- **Ch 8 *Backpropagation***: the chain-rule machinery that makes Ch 6 networks trainable.
- *(...and onward through CNNs, RNNs, transformers, attention, normalization, regularization, sequence models, VAEs, NFs, GANs, diffusion, RL, structured prediction. Full chapter index lives at [[Bishop and Bishop - chapters]].)*

## Notable quotes

- *"Conceptually, this book is perhaps most naturally viewed as a successor to Neural Networks for Pattern Recognition (Bishop, 1995b)... It can also be considered as a companion volume to Pattern Recognition and Machine Learning (Bishop, 2006), which covered a broader range of topics in machine learning although it predated the deep learning revolution."* — positioning vs Bishop's earlier books. (Preface.)
- *"There are many interesting topics in machine learning discussed in Bishop (2006) that remain of interest today but which have been omitted from this new book. For example, Bishop (2006) discusses Bayesian methods in some depth, whereas this book is almost entirely non-Bayesian."* — explicit scope tradeoff. (Preface.)
- *"Deep learning avoids this problem by learning the required nonlinear transformations of the data from the data set itself."* — the conceptual pivot that motivates the entire post-Ch-5 arc. (§4.1.1.)
- *"As we have seen, for both Gaussian distributed and discrete inputs, the posterior class probabilities are given by generalized linear models with logistic sigmoid (K = 2 classes) or softmax (K ≥ 2 classes) activation functions."* — the unification Ch 5 is built around. (§5.3.4.)
- *"We have seen that there is a natural pairing between the choice of error function and the choice of output-unit activation function. Although we have derived this result in the context of single-layer network models, the same considerations apply to deep neural networks discussed in later chapters."* — **the most important paragraph in Ch 5 for everything that follows**. (§5.4.6.)

## Connections

- [[Bishop and Bishop - chapters]] — chapter-level ingestion index (page ranges, status, planned concept pages).
- [[Diffusion Crash Course - synthesis]] — Ch 16 (§16.1–16.3) is the top recommended reading for the Saturday-morning probability/ELBO block; Ch 20 covers diffusion models directly.
- [[Diffusion Models]] — Ch 20 is the canonical textbook treatment; complements [[What are Diffusion Models - Lilian Weng]] and [[Generative Modeling by Estimating Gradients of the Data Distribution - Yang Song]].
- [[Moore-Penrose Pseudoinverse]] — §4.1.3 derives $\Phi^\dagger = (\Phi^T\Phi)^{-1}\Phi^T$ as the closed-form MLE for linear regression.
- [[Sigmoid Function]] — §5.3 derives the sigmoid as the log-odds → probability formula; §5.4.6 derives why pairing it with binary cross-entropy gives the clean $(y-t)\phi$ gradient (canonical link).
- [[Normalizing Constant]] — §5.3's softmax derivation makes the denominator $\sum_j e^{a_j}$ explicit as a normalizing constant; tracks back to the same trick in Boltzmann distributions.
- [[Constraint Gradients and Tangent Spaces]] — §5.1.1's hyperplane decision boundary geometry uses the same "gradient is perpendicular to the level set" picture.
- [[Singularity]] — §4.1.4's closed-form least squares solution becomes ill-defined when columns of $\Phi$ are nearly collinear (same "rank loss" theme).
- [[learning-tracker]] — covers progress on this textbook.

## Open questions

- **Should later chapter studies be done in tutor-mode chunks, or in a focused multi-chapter run?** Chapters 4-5 covered in one tutor session worked well (they're tightly coupled). Ch 6-8 (deep networks + gradient descent + backprop) are similarly coupled; might benefit from the same combined treatment.
- **Is the book's "almost entirely non-Bayesian" stance a gap for the diffusion-models chapter?** Ch 20 must engage with the ELBO derivation which is Bayesian-flavored — worth checking whether the treatment is self-contained or whether PRML 2006 needs to be a companion for that one chapter.

## Mentions

- [[Diffusion Crash Course - synthesis]] — cites this textbook as the top reading recommendation for probability/ELBO and diffusion.
- (to be added on next pass: every concept page that touches Ch 4-5 content.)
