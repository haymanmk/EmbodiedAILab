---
type: source
domain: research
created: 2026-05-31
updated: 2026-05-31
source_url: https://blog.evjang.com/2018/01/nf1.html
source_path: raw/diffusion-model/Normalizing Flows Tutorial, Part 1 Distributions and Determinants.md
source_format: web
author: Eric Jang
published: 2018-01-18
chunks_indexed: false
indexed_at:
study_status: covered
tags: [normalizing-flows, change-of-variables, jacobian, generative-models, tensorflow-1x, foundations]
sources:
  - "[[Diffusion Crash Course - synthesis]]"
---

# Normalizing Flows Tutorial, Part 1 — Distributions and Determinants (Eric Jang)

> The most accessible introduction to normalizing flows. Builds the change-of-variables story from a 1D shift-and-scale example, generalizes to 2D via parallelograms (= determinants), then to arbitrary nonlinear maps via Jacobians. Closes with a TensorFlow 1.x `TransformedDistribution` / `Bijector` code example training a 6-layer MLP-bijector on a 2D toy problem.

## Raw-file caveat

The Obsidian Web Clipper for this article **dropped most inline `$...$` math expressions** (e.g., lines like *"Let $X$ be the distribution . Let random variable ."* with the variable definitions missing). The display `$$...$$` blocks survived. For the dropped inline notation, refer to the source URL — the math doesn't appear at all in `raw/diffusion-model/Normalizing Flows Tutorial, Part 1 Distributions and Determinants.md`. The cleanup script (`wiki/assets/scripts/clean-clipped-latex.py`) can't recover what was never captured.

## Summary

Jang's Part 1 is the *intuition-first* normalizing flows tutorial. The argument unfolds in four moves:

1. **Why we need more than Gaussians.** A unimodal Gaussian can't model a multimodal data distribution; the "agent crossing a lake by going either left or right but a Gaussian policy chooses straight into the water" example makes this physical. Mixture models, autoregressive factorizations, energy-based models, and **normalizing flows** are listed as the four ways out.
2. **1D change of variables.** Pick a 1D base distribution $X$ and an invertible transformation $Y = f(X)$. Probability conservation requires $p_X(x)\,dx = p_Y(y)\,dy$, so $p_Y(y) = p_X(f^{-1}(y))\,|df^{-1}/dy|$. Take logs for numerical stability.
3. **Multivariate generalization is the determinant.** A unit square deformed by a linear map becomes a parallelogram of area $|\det A|$ — the determinant *is* the local change-of-volume of a linear map. For nonlinear $f$, replace the global determinant with the local Jacobian determinant: $p_Y(y) = p_X(f^{-1}(y)) \cdot |\det J_{f^{-1}}(y)|$.
4. **Chain bijectors into a "normalizing flow."** Just like neural-net layers, you stack invertible transformations. Each has its own log-determinant; sum them in log space. Train end-to-end by max-likelihood. The cost: arbitrary determinant computation is $O(n^3)$; *the entire research direction is "design bijectors whose Jacobian determinant is cheap."*

The code example builds an "MLP bijector" (6 layers, each = `Affine` + `LeakyReLU` bijector) trained on a banana-shaped 2D dataset. It explicitly notes this MLP is *weak* (each affine is 2×2; PReLU only slowly warps the manifold) — that's the bridge to Part 2's modern architectures.

For this vault, Part 1 is the *foundational concept page* you'd write if normalizing flows had its own concept entry. It earns its place on the diffusion curriculum because **probability-flow ODE** (Yang Song's blog, the Sunday-afternoon reading) is literally a continuous normalizing flow, and the change-of-variables formula resurfaces in the exact-likelihood-via-neural-ODE derivation.

## Key claims

- **Unimodal Gaussian limitations are not academic.** RL continuous-control policies modeled as diagonal-covariance Gaussians fail on simple bimodal tasks (the cross-the-lake example). The same failure mode is why **diffusion** displaces [[Action Chunking Transformer]] on multimodal manipulation — different fix to the same problem.
- **Change-of-variables formula in 1D.** $p_Y(y) = p_X(f^{-1}(y)) \cdot |df^{-1}/dy|$ — conservation of probability mass, taken in log-space for stability.
- **Determinant = local volume distortion.** A linear map's determinant is the area-ratio of "unit square in → parallelogram out." For nonlinear $f$, the Jacobian $J(f^{-1})$ plays the same role pointwise. *"Determinants are nothing more than the amount (and direction) of volume distortion of a linear transformation, generalized to any number of dimensions."*
- **Multivariate change of variables.** $p_Y(y) = p_X(f^{-1}(y)) \cdot |\det J_{f^{-1}}(y)|$. The absolute-value handles orientation-reversing maps.
- **TensorFlow's `TransformedDistribution` API.** A `Bijector` exposes `forward`, `inverse`, and `inverse_log_det_jacobian` (ILDJ). Sampling: `bijector.forward(base.sample())`. Log-density: `base.log_prob(bijector.inverse(x)) + bijector.inverse_log_det_jacobian(x)`. This is the practical abstraction every NF library inherits.
- **Stacking bijectors = a flow.** Composing $K$ bijectors gives a flow with log-density = base log-density + $\sum_k \log|\det J_{f_k^{-1}}|$. Train with max-likelihood SGD.
- **Why this is hard.** Computing $\det J$ for an arbitrary neural net is $O(n^3)$. *"Much of the current research on Normalizing Flows focuses on how to design expressive Bijectors that exploit GPU parallelism during forward and inverse computations, all while maintaining computationally efficient ILDJs."* — the entire research direction in one sentence.
- **LeakyReLU bijector**: the toy nonlinearity Jang implements. Invertible (because $\alpha > 0$), element-wise (so Jacobian is diagonal), ILDJ trivially the sum of log-diagonal entries. PReLU is the parameterized version with learnable $\alpha$.
- **Sigmoid/tanh are bad bijectors.** Their saturation makes inversion numerically unstable (small output changes near $\pm 1$ correspond to massive input changes). *"In my experiments I could not chain 2 saturating nonlinearities together without gradients exploding."*

## Notable quotes

- *"Normalizing flows transform simple densities (like Gaussians) into rich complex distributions that can be used for generative models, RL, and variational inference."* — the one-sentence pitch.
- *"Determinants are nothing more than the amount (and direction) of volume distortion of a linear transformation, generalized to any number of dimensions."* — the geometric intuition that the rest of the post leans on. (Change of Variables section.)
- *"When I learned about determinants in middle & high school I was very confused at the seemingly arbitrary definition of determinants. We were only taught how to compute a determinant, instead of what a determinant meant: the local, linearized rate of volume change of a transformation."* — pedagogical aside that's worth keeping; explains why the determinant feels arbitrary until you see this.
- *"Much of the current research on Normalizing Flows focuses on how to design expressive Bijectors that exploit GPU parallelism during forward and inverse computations, all while maintaining computationally efficient ILDJs."* — frames the entire NF research program.

## Connections

- [[Diffusion Crash Course - synthesis]] — Part 1 is the Saturday-afternoon-optional / Sunday-bridge reading. The change-of-variables formula reappears in probability-flow ODE Sunday afternoon.
- [[Normalizing Flows Tutorial Part 2 - Eric Jang]] — direct follow-up; same author, immediately after.
- [[Diffusion Models]] — diffusion's "probability-flow ODE" reverse-time formulation IS a continuous normalizing flow; the determinant-of-Jacobian appears there as the instantaneous-change-of-variables formula (Chen et al. *Neural ODEs* 2018).
- [[Generative Modeling by Estimating Gradients of the Data Distribution - Yang Song]] — Song's blog references normalizing flows several times when discussing exact-likelihood computation via probability-flow ODE.
- [[Normalizing Constant]] — normalizing flows are the *one* likelihood-based generative model family where the normalizing constant is trivially $Z = 1$ (because invertibility + change-of-variables gives a proper density without dividing by anything). This is precisely the "tractability strategy" row in [[Normalizing Constant]]'s escape-routes table.
- [[Sigmoid Function]] — Jang explicitly notes sigmoid/tanh are *bad* bijectors due to saturation. Connects back to the vanishing-gradient theme.
- [[Singularity]] — the matrix determinant lemma Jang invokes (for low-rank-updated triangular affine bijectors) becomes singular exactly when the affine is rank-deficient. Same "rank loss" concept.

## Open questions

- **Are normalizing flows still competitive in 2026?** Jang's piece is from 2018. By now, diffusion models dominate image generation and Flow Matching / Rectified Flow have emerged as a hybrid (continuous-time flows trained without invertibility constraints, leveraging score-matching ideas). Where does NF research stand today? Probably mostly subsumed into flow matching for generative modeling, still alive in density estimation + Bayesian inference. Worth a synthesis pass if NF becomes a thread.
- **Could normalizing flows model robot policies?** Jang's lake-crossing example is explicitly an RL motivation. NF-based policies were briefly explored (e.g., 2019–2020) but never displaced Gaussian-mixture or autoregressive policies in practice. Diffusion Policy is now the default. Why did NF policies fade — engineering cost, sample efficiency, or wall-clock at inference?

## Mentions

- [[Diffusion Crash Course - synthesis]] — auxiliary cluster reading.
- (to be added on next pass: [[Diffusion Policy]] when deep-read.)
