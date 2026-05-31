---
type: source
domain: research
created: 2026-05-30
updated: 2026-05-30
source_url: https://lilianweng.github.io/posts/2021-07-11-diffusion-models/
source_path: raw/diffusion-model/What are Diffusion Models?.md
source_format: web
author: Lilian Weng
published: 2021-07-11
chunks_indexed: false
indexed_at:
study_status: covered
tags: [diffusion, ddpm, ncsn, ddim, classifier-free-guidance, latent-diffusion, distillation, consistency-models, u-net, dit, controlnet, reading-notes]
---

# What are Diffusion Models? — Lilian Weng (Lil'Log)

> Canonical secondary source for diffusion models. The post starts from the DDPM formulation (Ho et al. 2020), derives the variational bound and the simplified MSE noise-prediction loss step by step, and then expands outward through every major follow-up: noise schedules (linear / cosine), reverse-process variance learning, the NCSN / score-matching connection (Song & Ermon), classifier and classifier-free guidance, faster sampling (DDIM, strided), distillation (progressive, consistency models), latent-space diffusion (LDM / Stable Diffusion), cascaded super-resolution, unCLIP, Imagen, and the U-Net / ControlNet / DiT architecture options. The 2024 update adds the architecture section and the consistency-models walkthrough.

## Summary

Weng's post is *the* most-cited single-page tour of DDPM-style diffusion, written first in 2021 and incrementally extended through 2024. It is organized around the **DDPM perspective first**: forward Gaussian Markov chain, closed-form $q(x_t \mid x_0)$, ELBO decomposition into $L_T + \sum L_{t-1} + L_0$, ε-parameterization that reduces the per-step KL to the simplified MSE objective $\mathbb{E}\|\epsilon - \epsilon_\theta(\sqrt{\bar\alpha_t}x_0 + \sqrt{1-\bar\alpha_t}\epsilon, t)\|^2$. Each follow-up paper is then layered onto that spine — Nichol & Dhariwal's cosine schedule and learned $\Sigma_\theta$, Dhariwal & Nichol's classifier guidance, Ho & Salimans' classifier-free guidance, Song et al.'s DDIM (deterministic, fewer sampling steps, latent interpolation), Salimans & Ho's progressive distillation, Song et al. 2023's consistency models (single-step generation via the *consistency function* $f(x_t, t) \mapsto x_\epsilon$), Rombach et al.'s LDM (run diffusion on a VAE latent for 4–16× speedup), Ho et al.'s cascaded super-resolution with noise-conditioning augmentation, Ramesh et al.'s unCLIP and Saharia et al.'s Imagen (text-to-image via CLIP image-embedding prior vs. frozen T5-XXL), and the architecture menu of U-Net, ControlNet (zero-conv trainable copies for additional conditioning), and DiT (transformer on latent patches with adaLN-Zero conditioning). The piece also makes the **NCSN ↔ DDPM bridge** explicit via $s_\theta(x_t, t) \approx -\epsilon_\theta(x_t, t)/\sqrt{1-\bar\alpha_t}$, which is the same identity the user's existing [[Diffusion Models]] page uses to motivate score additivity for [[Compositional Diffusion Constraint Solvers]].

For this vault, the post is canonical secondary reference material: it justifies every equation already on the [[Diffusion Models]] concept page, and it backfills the queued [[Diffusion Policy]] deep-read with the menu of design choices (variance schedule, $T$, sampler, parameterization, architecture, guidance scale) that Diffusion Policy makes specific picks within.

## Key claims

- **Forward kernel is a Gaussian Markov chain with a closed-form cumulative.** $q(x_t \mid x_{t-1}) = \mathcal{N}(\sqrt{1-\beta_t}\,x_{t-1}, \beta_t I)$ composes via the Gaussian-merge identity into $q(x_t \mid x_0) = \mathcal{N}(\sqrt{\bar\alpha_t}\,x_0, (1-\bar\alpha_t)I)$, so a single training example $(x_0, t, \epsilon)$ yields the noisy input in one shot. This is the "nice property" the loss leans on.
- **The ELBO decomposes into $T$ tractable KL terms plus an endpoint.** $L_{\text{VLB}} = L_T + \sum_{t=1}^{T-1} L_t + L_0$ where each $L_t$ (for $t \ge 1$) is a KL between two Gaussians — computable in closed form. $L_T$ is constant (no learnable parameters); $L_0$ uses a discrete decoder in Ho 2020.
- **ε-prediction collapses each KL to MSE.** Parameterize $\mu_\theta(x_t, t) = \frac{1}{\sqrt{\alpha_t}}(x_t - \frac{1-\alpha_t}{\sqrt{1-\bar\alpha_t}}\epsilon_\theta(x_t, t))$; the per-step KL becomes $\|\epsilon - \epsilon_\theta\|^2$ with a $t$-dependent weight; Ho et al. drop the weight entirely and use $L_{\text{simple}} = \mathbb{E}\|\epsilon - \epsilon_\theta\|^2$. Empirically this works better than keeping the weight.
- **The denoising network is the same one across all timesteps; $t$ is an explicit input.** Time-conditioning (sinusoidal embedding → MLP → injected into U-Net) is what lets one model handle the entire noise spectrum.
- **The NCSN connection is exact for Gaussian-perturbed data.** $s_\theta(x_t, t) \approx \nabla_{x_t} \log q(x_t) = -\epsilon_\theta(x_t, t)/\sqrt{1-\bar\alpha_t}$. So an ε-prediction network *is* a noise-conditional score network up to a scalar.
- **Cosine $\beta_t$ schedule beats linear.** Nichol & Dhariwal's $\bar\alpha_t = \cos^2(\frac{t/T + s}{1 + s} \cdot \frac{\pi}{2})/\cos^2(\frac{s}{1+s} \cdot \frac{\pi}{2})$ keeps SNR near-linear in $t$ and avoids the rapid information destruction of linear schedules.
- **Learning $\Sigma_\theta$ as a $[\beta_t, \tilde\beta_t]$ interpolation needs a hybrid loss.** $L_{\text{simple}}$ doesn't depend on $\Sigma_\theta$, so Nichol & Dhariwal add $L_{\text{hybrid}} = L_{\text{simple}} + \lambda L_{\text{VLB}}$ (with $\lambda = 0.001$ and stop-grad on $\mu_\theta$ in the VLB term) so $L_{\text{VLB}}$ only updates the variance interpolation.
- **Classifier guidance.** Train classifier $f_\phi(y \mid x_t, t)$ on noisy images; modify the ε-prediction as $\bar\epsilon_\theta = \epsilon_\theta - \sqrt{1-\bar\alpha_t}\,w\,\nabla_{x_t}\log f_\phi(y \mid x_t)$. The $w$ scales classifier strength.
- **Classifier-free guidance (CFG) removes the separate classifier.** Train the same network on conditional $\epsilon_\theta(x_t, t, y)$ and unconditional $\epsilon_\theta(x_t, t, \emptyset)$ examples (drop $y$ at some rate during training). At inference, $\tilde\epsilon = (1+w)\epsilon_\theta(x_t, t, y) - w\,\epsilon_\theta(x_t, t, \emptyset)$. GLIDE found CFG beats CLIP-guidance because CLIP guidance "exploits the model with adversarial examples toward the CLIP model."
- **DDIM makes sampling deterministic and skippable.** Same training objective, different sampling formula: $\sigma_t^2 = \eta\,\tilde\beta_t$ with $\eta = 0$ ⇒ deterministic, $\eta = 1$ ⇒ DDPM-style stochastic. Deterministic DDIM allows sub-sequences $\tau_1 < \cdots < \tau_S$ of the original $T$ steps with $S \ll T$ at small quality cost, plus latent-space "consistency" / interpolation.
- **Progressive distillation halves sampling steps per iteration.** Salimans & Ho 2022 — student initialized from teacher, one student DDIM step targets two teacher steps; iterate.
- **Consistency models do single-step generation.** Song et al. 2023 learn $f(x_t, t) \mapsto x_\epsilon$ (consistency function) with $f(x_t, t) = c_{\text{skip}}(t)\,x + c_{\text{out}}(t)\,F_\theta(x, t)$; can be trained by distillation (CD, requires teacher score) or independently (CT, uses unbiased score estimator $-(x_t - x)/t^2$). Heun ODE solver + LPIPS distance + $N=18$ is the empirical sweet spot for CD.
- **Latent Diffusion Model (LDM) runs the chain on VAE latents, not pixels.** Two-stage decomposition: autoencoder for *perceptual* compression (KL-reg or VQ-reg), diffusion for *semantic* generation. Cross-attention on a per-modality conditioning encoder $\tau_\theta(y)$ lets the same architecture take class labels, semantic maps, blurred images, or text. This is the Stable Diffusion architecture.
- **Cascaded super-resolution with noise-conditioning augmentation.** Ho et al. 2021 — pipeline of multiple diffusion models at increasing resolutions; *noise-conditioning augmentation* (corrupt the upsampling-stage condition with Gaussian noise at low-res / Gaussian blur at high-res) reduces compounding error and is critical for final quality.
- **unCLIP (DALL·E 2) is a two-stage CLIP-mediated pipeline.** Prior model $P(c^i \mid y)$ predicts CLIP image embedding from text; decoder $P(x \mid c^i, [y])$ generates pixels from that embedding. Image-variation generation falls out of the second stage.
- **Imagen replaces CLIP with frozen T5-XXL.** Scaling the *text encoder* matters more than scaling the U-Net. *Dynamic thresholding* (clip $x_0$ predictions per-sample to a high-percentile range, then divide) closes the train-test mismatch caused by high CFG scales.
- **U-Net is the default backbone; DiT scales better.** U-Net (Ronneberger 2015) with downsampling/upsampling stacks and skip connections is the standard. Diffusion Transformer (DiT; Peebles & Xie 2023) patchifies the latent, applies transformer blocks with adaLN-Zero conditioning (scale/shift regressed from $t$ and $c$), and scales cleanly with compute — now the architecture choice for large-scale image diffusion.
- **ControlNet adds dense conditioning via trainable copies + zero convs.** Freeze original block weights; clone trainable copy $\theta_c$ with extra conditioning input $c$; connect via 1×1 zero convolutions (init to zero so initial output is unchanged). Enables Canny / Hough / pose / depth / segmentation conditioning without destabilizing the base model.

## Notable quotes

- *"It is noteworthy that the reverse conditional probability is tractable when conditioned on $x_0$"* — the algebraic hinge that turns the intractable $q(x_{t-1} \mid x_t)$ into a closed-form Gaussian and gives DDPM its trainable target $\tilde\mu_t$. (Reverse diffusion process section.)
- *"Empirically, Ho et al. (2020) found that training the diffusion model works better with a simplified objective that ignores the weighting term."* — why the canonical loss is plain MSE on $\epsilon$, not the variance-weighted KL the derivation produces. (Simplification.)
- *"They hypothesized that it is because CLIP guidance exploits the model with adversarial examples towards the CLIP model, rather than optimize the better matched images generation."* — GLIDE's takeaway on why classifier-free guidance is preferred over CLIP guidance. (Classifier-Free Guidance.)
- *"DDIM ($\eta = 0$) can produce the best quality samples when $S$ is small, while DDPM ($\eta = 1$) performs much worse on small $S$."* — the quality-vs-speed trade-off that motivates DDIM for inference; the headline reason every modern diffusion deployment uses DDIM or DPM-Solver sampling rather than the original DDPM Markov chain. (Speed up Diffusion Models.)
- *"They are both analytically tractable and flexible."* — Weng's summary of *why* diffusion ended up displacing GANs and VAEs: it dissolves the classical tractability-vs-flexibility trade-off in generative modeling. (Quick Summary.)

## Connections

- [[Diffusion Models]] — this source is the canonical derivation behind every equation on the concept page; the ε-loss, the score identity, the cosine schedule, the CFG formula, the DDIM stochasticity knob, the LDM/DiT architecture notes all trace here.
- [[Generative Modeling by Estimating Gradients of the Data Distribution - Yang Song]] — Yang Song's blog is the *complementary* view (score-based first, DDPM second). Weng connects the two via the NCSN identity in §"Connection with noise-conditioned score networks (NCSN)"; Song's blog establishes the equivalence from the opposite direction.
- [[Compositional Diffusion Constraint Solvers]] — score additivity ($\nabla \log \prod p_k = \sum \nabla \log p_k$) only makes sense if you accept the score interpretation Weng derives from the ε-prediction; CDCS uses it directly.
- [[Action Chunking Transformer]] — Diffusion Policy displaces ACT on multimodal tasks for exactly the reason Weng spells out: GANs/regression collapse to averages over multimodal targets; diffusion's noise-injecting forward process covers modes by construction.
- [[Imitation Learning]] — Diffusion Policy is one of the two dominant IL architectures in 2026; Weng's piece is the prerequisite reading for the deep-read.
- [[Constraint Gradients and Tangent Spaces]] — the score function $\nabla \log p(x)$ is the same gradient-field mental object as $\nabla h(x)$; cross-linked from [[Diffusion Models]].
- [[Vision-Language-Action Models]] — VLA models built on diffusion (e.g., Octo, RDT) inherit the architecture menu Weng catalogs (DiT for large-scale, classifier-free guidance for conditioning strength).

## Open questions

- **Is Weng's NCSN-bridge identity ($s_\theta = -\epsilon_\theta/\sqrt{1-\bar\alpha_t}$) exact, or only approximate up to expectations over $q(x_0)$?** The derivation in §"Connection with noise-conditioned score networks (NCSN)" inserts an $\mathbb{E}_{q(x_0)}[\cdot]$ inside the gradient; for finite ε-network capacity the equality is approximate, but the post is loose on when this matters. Worth checking against Song's blog ([[Generative Modeling by Estimating Gradients of the Data Distribution - Yang Song]]) — Song treats it as part of the "same model family in two formulations" claim.
- **For Diffusion Policy specifically, why DDIM with $\approx 10$ inference steps instead of consistency models with 1 step?** Weng's consistency-model walkthrough makes the latter sound strictly dominant; the empirical answer in robotics may be that consistency-model training cost or stability rules it out at small dataset sizes. Resolve on deep-read of Chi et al. 2023 + any consistency-policy follow-ups.
- **Does the dynamic-thresholding trick from Imagen apply to action chunks in Diffusion Policy?** Imagen needed it because high CFG values push $x_0$ predictions outside $[-1, 1]$ on pixels; actions live in a bounded joint-space already, so the analogous "clip to action limits" may or may not buy anything. Open until the deep-read.
- **Are ControlNet-style "zero conv trainable copies" a useful pattern for adapting a base policy to a new robot embodiment without retraining the backbone?** Speculative — the architectural pattern is general enough that a robot-learning analogue should exist.

## Mentions

(none yet — this source will be cited from [[Diffusion Models]] after the next pass; [[Diffusion Policy]] deep-read will add an inbound link.)
