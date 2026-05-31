---
type: source
domain: research
created: 2026-05-31
updated: 2026-05-31
source_url: https://blog.evjang.com/2018/01/nf2.html
source_path: raw/diffusion-model/Normalizing Flows Tutorial, Part 2 Modern Normalizing Flows.md
source_format: web
author: Eric Jang
published: 2018-01-18
chunks_indexed: false
indexed_at:
study_status: covered
tags: [normalizing-flows, maf, iaf, real-nvp, made, parallel-wavenet, batchnorm-bijector, tensorflow-1x]
sources:
  - "[[Diffusion Crash Course - synthesis]]"
---

# Normalizing Flows Tutorial, Part 2 — Modern Normalizing Flows (Eric Jang)

> Follow-up to [[Normalizing Flows Tutorial Part 1 - Eric Jang|Part 1]]. Surveys the four NF architectures that mattered in 2017–2018 — **MAF** (Masked Autoregressive Flow), **IAF** (Inverse Autoregressive Flow), **Real-NVP** (Real-valued Non-Volume-Preserving), and **Parallel WaveNet** (MAF teacher → IAF student distillation) — and explains how their design choices trade off training speed vs sampling speed vs expressiveness. The story is "autoregressive density estimators ARE normalizing flows in disguise."

## Raw-file caveat

Same as Part 1: the Obsidian Web Clipper dropped most inline `$...$` math (variable names, subscripts) — refer to the source URL for full notation. Display `$$...$$` blocks survived.

## Summary

Jang's Part 2 argues that **autoregressive models** (WaveNet, PixelRNN) ARE normalizing flows when you reinterpret them as deterministic transformations of Gaussian noise. Once you accept that framing, the four-architecture menu falls out naturally as trade-offs in the trio "fast forward / fast inverse / cheap Jacobian":

1. **MAF (Masked Autoregressive Flow, Papamakarios et al. 2017)**. Each conditional $p(x_i \mid x_{<i})$ is a univariate Gaussian whose mean $\mu_i = f_{\mu_i}(x_{<i})$ and log-scale $\alpha_i = f_{\alpha_i}(x_{<i})$ are predicted by a neural net. Sampling: $x_i = u_i \exp(\alpha_i) + \mu_i$. The inverse is trivial ($u_i = (x_i - \mu_i)\exp(-\alpha_i)$) — the architecture is *designed* so the inverse only requires forward evaluation of $f_\mu$ and $f_\alpha$, never their inverses. **Fast density evaluation (parallel), slow sampling (sequential, $D$ steps).**
2. **MADE (Germain et al. 2015)** — efficiency hack used inside MAF. Instead of $D$ separate networks computing $\mu_i$ and $\alpha_i$, use a *single* network with masked weights that enforces the autoregressive ordering. One forward pass → all $\mu_i, \alpha_i$ at once.
3. **IAF (Inverse Autoregressive Flow, Kingma et al. 2016)**. Same structure as MAF, but the shift-and-scale statistics depend on previous *noise* variates $u_{<i}$ instead of previous data $x_{<i}$. **Fast sampling (parallel), slow density evaluation (sequential)** — opposite trade-off from MAF. In TensorFlow Distributions, MAF and IAF are literally the same Bijector class with a `tfb.Invert(...)` wrapper.
4. **Parallel WaveNet (van den Oord et al. 2017)** — combines both. Train MAF as the slow-sampling teacher, then train an IAF student to maximize likelihood under the teacher. IAF can cheaply compute density of *its own* samples (cached noise variates), so the student is trainable. End result: fast training (MAF) + fast sampling (IAF). Deployed in Google Assistant for real-time TTS — *the* impactful NF production system.
5. **Real-NVP (Dinh et al. 2017)** — a special case of IAF where you fix an integer $d$ and only the second half $x_{d+1:D}$ depends on the first half $x_{1:d}$ via the shift-and-scale; the first half is passed through unchanged. Both forward and inverse complete in a single parallel pass — *fast both ways*. The cost: less expressive than full MAF/IAF; empirically Jang reports it underperforms on 2D toys. **NICE** (Dinh et al. 2014) was the predecessor with shift-only (no scale), giving constant ILDJ.
6. **BatchNorm bijector** — Real-NVP's contribution to stabilizing training. Apply BatchNorm as an invertible operation in `bijector.inverse` during training; accumulate running mean/std via EMA; use those at "test" (`bijector.forward`) to de-normalize.

The piece closes with two observations that are worth keeping in mind: (1) **NFs are reversible computation** — useful for memory-bounded backprop (RevNets, Gomez et al. 2017, inspired by NICE); (2) **NFs can be drop-in replacements for any Gaussian** — VAE priors, GAN latent codes, RL policies.

For this vault, Part 2 is the *architecture menu* that the diffusion world also has (DDPM / DDIM / DiT / LDM / ControlNet are diffusion's equivalent menu). Once you see MAF vs IAF vs Real-NVP, the analogous diffusion-world trade-offs (DDPM stochastic-and-slow vs DDIM deterministic-and-fast vs consistency-models one-step) parse more cleanly.

## Key claims

- **Autoregressive density models ARE normalizing flows.** $p(x_{1:D}) = \prod_i p(x_i \mid x_{<i})$ with each conditional a univariate Gaussian = a deterministic transformation of standard-Gaussian noise. This reinterpretation is what unlocks the whole NF taxonomy.
- **MAF trains fast, samples slow.** Density evaluation parallelizes over $D$ dimensions (one forward pass); sampling is sequential because $x_i$ depends on $x_{<i}$.
- **IAF samples fast, evaluates density slow.** Sampling parallelizes ($x_i$ depends only on $u_{<i}$ which are known at sampling time); density evaluation is sequential (must recover $u_{<i}$ from $x$ recursively).
- **MAF and IAF are inverses of each other** — same Bijector class with `tfb.Invert(...)`. Choice depends on whether you need fast training (use MAF) or fast inference (use IAF).
- **For neural network *training*, MAF is usually the right choice** — you call density evaluation millions of times per epoch, sampling rarely.
- **Parallel WaveNet pattern: MAF teacher distills into IAF student.** Teacher trains fast on data; student matches teacher (KL divergence between student-and-teacher distributions, evaluated on student samples whose noise is cached) → fast sampling at deployment. Real-time audio synthesis, deployed in Google Assistant.
- **Real-NVP coupling layers are a degenerate IAF.** Partition variables into two halves; one half stays fixed, the other half gets scaled and shifted by a function of the first half. Fast both ways, less expressive. **NICE** is the shift-only predecessor (constant ILDJ).
- **Variable ordering matters.** Within a single autoregressive flow, the ordering is fixed; if you stack multiple flows, **permute the ordering between layers** so different orderings get a shot. Without permutation, the flow can't model dependency patterns that violate the chosen ordering.
- **Architecture trade-offs reduce to two questions.** (1) Is forward (sampling) fast? (2) Is inverse (density eval) fast? Pick a flow architecture by your workload's answer.
- **BatchNorm as a bijector** — straightforward to implement once you realize BatchNorm itself is invertible (subtract mean, divide by std → multiply by std, add mean).

## Notable quotes

- *"The procedure of autoregressive sampling is a deterministic transformation of the underlying noise variates (sampled from $\mathcal{N}(0,I)$) into a new distribution, so autoregressive samples can actually be interpreted as a TransformedDistribution of the standard Normal!"* — the unification claim. Once you see this, MAF / IAF / WaveNet all collapse into one framework.
- *"IAF and MAF make opposite computational tradeoffs — MAF trains quickly but samples slowly, while IAF trains slowly but samples quickly. For training neural networks, we usually demand way more throughput with density evaluation than sampling, so MAF is usually a more appropriate choice when learning distributions."* — the practitioner's takeaway.
- *"This is an incredibly impactful application of normalizing flows research — the end result is a real-time audio synthesis model that is 20 times faster to sample, and is already deployed in real-world products like the Google Assistant."* — Parallel WaveNet, the production payoff.
- *"One of the most intriguing properties of normalizing flows is that they implement reversible computation (i.e. have a defined inverse of an expressive function). This means that if we want to perform a backprop pass, we can re-compute the forward activation values without having to store them in memory during the forward pass."* — the unexpected memory-efficiency angle (RevNets). Likely the second-most-impactful NF idea after the change-of-variables formula itself.

## Connections

- [[Normalizing Flows Tutorial Part 1 - Eric Jang]] — the prerequisite tutorial; same author, immediately before.
- [[Diffusion Crash Course - synthesis]] — auxiliary cluster reading.
- [[Diffusion Models]] — diffusion's architecture menu (DDPM ↔ MAF, DDIM ↔ IAF in spirit, consistency models ↔ Parallel WaveNet distillation) is the *same structural trade-off* in different clothing. The pattern "fast forward vs fast inverse" maps to "stochastic sampling vs deterministic sampling" in diffusion-land.
- [[Generative Modeling by Estimating Gradients of the Data Distribution - Yang Song]] — Song's probability-flow ODE is itself a continuous normalizing flow with the change-of-variables formula in its instantaneous form (neural ODEs).
- [[Action Chunking Transformer]] — ACT predicts a full action chunk in one forward pass; that's an *autoregressive-over-chunk-index* model in spirit. The MAF "fast density eval, slow sampling" trade-off is exactly why ACT can be trained efficiently but inference still needs the full chunk before any action goes out.
- [[Imitation Learning]] — NF-based policies were briefly explored for IL/RL but never displaced Gaussian-mixture or Diffusion Policy. Worth understanding why.
- (red link) [[Diffusion Policy]] — diffusion's answer to the same "fast sampling" question is DDIM with 10 steps; NF's answer is Parallel WaveNet distillation. Different strategies, same goal.

## Open questions

- **Are coupling-layer flows (RealNVP / Glow) still in active use?** They're the basis of Stable Diffusion's latent autoencoder regularization, but as standalone generative models they've been displaced by diffusion. Likely still alive in density estimation + Bayesian posterior approximation.
- **Why didn't NF policies win for robotics?** Diffusion Policy displaced ACT on multimodal tasks. NF policies were briefly attempted (e.g., Mazoure et al. 2020) but never reached the same prominence. Likely reasons: (1) coupling layers' restricted expressiveness, (2) Jacobian-tractability constraints make architecture design painful, (3) diffusion's MSE loss is more forgiving than NF's max-likelihood. Worth checking the post-2022 literature.
- **Flow Matching (Lipman et al. 2022) — successor or sibling?** Flow Matching trains a *continuous-time* flow without invertibility constraints, using a score-matching-style objective. It's a "best of both worlds" pitch: NF's deterministic flow + diffusion's training simplicity. Worth a deep-read if NF becomes a thread.

## Mentions

- [[Diffusion Crash Course - synthesis]] — auxiliary cluster reading.
