---
type: synthesis
domain: research
created: 2026-05-31
updated: 2026-05-31
tags: [curriculum, diffusion, crash-course, generative-models, study-plan]
aliases: ["Diffusion Weekend Crash Course", "Diffusion Models curriculum"]
---

# Diffusion Crash Course — Weekend Edition

> A bounded-scope weekend curriculum to go from "I have read the Modern Robotics intro chapters, KKT/Lagrange, sigmoid, normalizing constants" to "I can read any diffusion paper with the right map in my head, then dive deeper wherever I want." Designed for ~12–16 active hours over Saturday + Sunday.

## Premise

You're not going to *master* diffusion in a weekend. Nobody does. What you can do is acquire **the complete map** — every major concept named, every major derivation seen at least once, every major design decision placed in context — so that future deep dives load cheaply. Think of it as building the index in your head; the volumes can be filled in over months.

The curriculum is deliberately **map-first**: at every step you'll see the simplest version of an idea first (often via an analogy already in your vault), then the canonical formal version, then where it sits in the bigger picture. Where time is tight, **skim** rather than skip — every named object should at least register, even if its full derivation doesn't land.

## Where you are on day 0

You already have, in this vault:

- **Optimization math**: [[Lagrange Multipliers]], [[Karush-Kuhn-Tucker Conditions]], [[Constraint Gradients and Tangent Spaces]], [[Moore-Penrose Pseudoinverse]] — fluent enough to recognize gradient-of-a-scalar arguments instantly.
- **Linear algebra geometry**: [[Singularity]], [[Configuration Space]], [[Numerical Inverse Kinematics]] — comfortable with manifolds, tangent spaces, Jacobians, $SE(3)$.
- **A working ML concept set**: [[Sigmoid Function]], [[Normalizing Constant]] (the cake-fraction page and the $\nabla_x \log Z_\theta = 0$ trick), [[Imitation Learning]], [[Action Chunking Transformer]] (overview), [[Diffusion Models]] (building — the dust-on-photograph page).

The curriculum below extends this base with the **probability + score-matching + DDPM derivation + SDE big-picture** spine. No PyTorch coding, no GPU work — pure understanding.

## What you'll have on day 2 evening

- Be able to read **Ho et al. 2020 (DDPM)** end-to-end and follow every step.
- Be able to read **Yang Song's SDE paper (ICLR 2021)** at the level of "I get every section."
- Be able to read **Chi et al. 2023 (Diffusion Policy)** and understand the design choices.
- Have a *named* mental model for every major modern variation: DDIM, classifier-free guidance, latent diffusion, U-Net vs DiT, consistency models, normalizing flows.
- Know exactly where to dig deeper for any sub-topic.

## The four-block weekend plan

### Day 1 — Saturday

#### Block A (Saturday morning, ~3 hours): Probabilistic ML fundamentals

You need a tighter grip on a handful of probability + variational-inference ideas that DDPM rests on. Most of these are 30-minute concepts each.

**Goals**

- [ ] KL divergence between two Gaussians has a closed form — recognize it on sight.
- [ ] Maximum likelihood as $\theta^* = \arg\max_\theta \sum_i \log p_\theta(x_i)$ — fluent.
- [ ] The "intractable $Z$" trap (you have this — re-read [[Normalizing Constant]] if dusty).
- [ ] **ELBO / variational bound** via Jensen's inequality — see it derived once.
- [ ] **Reparameterization trick**: why sampling $x \sim \mathcal{N}(\mu, \sigma^2)$ is non-differentiable but $x = \mu + \sigma\epsilon,\ \epsilon \sim \mathcal{N}(0, 1)$ is.

**Readings (pick one path)**

| Reading | Time | What it gives you |
|---|---|---|
| **Bishop & Bishop, *Deep Learning: Foundations and Concepts* (2024), Ch. 16 §16.1–16.3** | 1.5h | The cleanest modern presentation of latent-variable models, ELBO, reparameterization. The *one* textbook chapter to read if you only read one. |
| **Doersch, *Tutorial on Variational Autoencoders* (2016)** [[https://arxiv.org/abs/1606.05908]] | 1h | The original ELBO-from-Jensen derivation, very accessible. ~14 pages. Free PDF. |
| **Murphy, *Probabilistic Machine Learning: Advanced Topics* (2023), Ch. 21** | 2h | Heavier, more comprehensive. Use as reference if Bishop is too thin. |
| Re-read [[Normalizing Constant]] in this vault | 15 min | Refresher on the $Z_\theta$ vanishing trick. |

**Recommended path**: Bishop §16.1–16.3 + Doersch §2–3 (ELBO derivation only). If you finish early, Murphy Ch. 21 §21.1.

**Socratic check before moving on**: Can you (a) write down the ELBO from memory, (b) explain why we maximize the ELBO instead of $\log p_\theta(x)$ directly, (c) explain why reparameterization is needed for gradient-based training of latent-variable models? If yes to all three, move on. If not, re-read.

#### Block B (Saturday afternoon, ~3 hours): Score matching and Langevin dynamics

This is your warm-up for the score-based view of diffusion. You already have the punchline (score sidesteps $Z$) — now you need the machinery.

**Goals**

- [ ] **Score function** $s(x) := \nabla_x \log p(x)$ as a *gradient field* over data space. (You have this metaphor in [[Diffusion Models]] and [[Normalizing Constant]].)
- [ ] Score matching loss in concept: minimize $\mathbb{E}\|s_\theta(x) - \nabla_x \log p(x)\|^2$.
- [ ] **Denoising score matching** (Vincent 2011) — the only practical version. Add noise, learn the score of the noisy distribution.
- [ ] **Langevin dynamics** as the sampling mechanism: $x_{k+1} = x_k + \eta\,s_\theta(x_k) + \sqrt{2\eta}\,z_k$.
- [ ] The naive-score-+-naive-Langevin failure mode: scores are inaccurate in low-density regions, Langevin chains start in low-density regions, samples never reach the data manifold.
- [ ] **NCSN** (Song & Ermon 2019) — fix by perturbing data with multiple noise scales, train a single noise-conditional score model on all of them; sample with annealed Langevin.

**Readings**

| Reading | Time |
|---|---|
| **[[Generative Modeling by Estimating Gradients of the Data Distribution - Yang Song]]** §1–3 (Introduction → "Naive score-based generative modeling and its pitfalls" → "Score-based generative modeling with multiple noise perturbations") | 1.5h |
| **[[Diffusion Models]]** vault concept page §"The score interpretation (the unlock)" | 15 min |
| Skim Hyvärinen 2005, *Estimation of Non-Normalized Statistical Models by Score Matching* | 30 min (skim only — the original paper, dense but short) |
| Optional: Sander Dieleman's blog *"Diffusion models are autoencoders"* (sander.ai/2022/01/31/diffusion.html) | 30 min — a complementary framing |

**Socratic check**: Can you explain (a) why NCSN trains *one* network on *all* noise scales rather than $L$ separate networks, (b) why annealed Langevin starts at the largest noise scale and decreases, (c) what would go wrong if you skipped noise perturbation entirely? If yes, you have the score-based view.

### Day 2 — Sunday

#### Block C (Sunday morning, ~3 hours): The DDPM derivation

The Saturday work was the conceptual scaffolding. Sunday morning, you derive **denoising diffusion probabilistic models** (Ho et al. 2020) — the canonical modern formulation everyone implements.

**Goals**

- [ ] **Forward kernel** $q(x_t \mid x_{t-1})$ as a Gaussian Markov chain, plus the closed-form cumulative $q(x_t \mid x_0)$.
- [ ] **ELBO decomposition** into $L_T + \sum L_{t-1} + L_0$ — three pieces, each a closed-form KL between Gaussians.
- [ ] **ε-parameterization**: instead of predicting $\mu_\theta(x_t, t)$ directly, predict the *noise* $\epsilon_\theta(x_t, t)$. This reduces each $L_t$ to plain MSE.
- [ ] **The simplified loss** $L_{\text{simple}} = \mathbb{E}\|\epsilon - \epsilon_\theta(x_t, t)\|^2$ — Ho et al.'s empirical finding that dropping the variance weighting works *better*, not worse.
- [ ] **Sampling formula** — what you actually run at inference: start from $x_T \sim \mathcal{N}(0, I)$, iterate denoising for $T = 1000$ steps.
- [ ] The NCSN ↔ DDPM identity: $s_\theta(x_t, t) = -\epsilon_\theta(x_t, t)/\sqrt{1-\bar\alpha_t}$. Same network in two parameterizations.

**Readings**

| Reading | Time |
|---|---|
| **[[What are Diffusion Models - Lilian Weng]]** §"Forward diffusion process" through §"Connection with noise-conditioned score networks (NCSN)" | 2h |
| **[[Diffusion Models]]** vault concept page (re-read the Definition and Score interpretation sections) | 30 min |
| Optional but valuable: **Ho, Jain, Abbeel 2020** original DDPM paper (~16 pages, dense) | 1.5h — read once after the blog version |

**Socratic check**: (a) Why is the loss MSE on $\epsilon$ rather than MSE on $\mu$? (b) Why does the denoising network take $t$ as an input — what would go wrong with a separate network per timestep? (c) Where in the derivation does the assumption $\beta_t \ll 1$ enter, and what would happen if it failed? Three solid answers means you have DDPM.

#### Block D (Sunday afternoon, ~3 hours): The big picture and the modern landscape

By now you have DDPM and the score-based view. Sunday afternoon is **breadth**: see every major variation at least once, place each on the map, identify your "where do I go next" arrow.

**Goals — see and place, don't master**

- [ ] **DDPM ↔ score-based unification** (Song's "wave / matrix mechanics" framing).
- [ ] **SDE generalization** ($L \to \infty$): forward $d\mathbf{x} = f(x, t)dt + g(t)d\mathbf{w}$, reverse-time SDE has a closed form in the score, three SDE families (VE / VP / sub-VP).
- [ ] **Probability-flow ODE**: same marginals as the SDE but deterministic; enables exact likelihood via neural ODEs.
- [ ] **DDIM** (Song et al. 2020): deterministic sampling, $\eta$ knob between DDPM (stochastic) and DDIM (deterministic), allows huge sampling speedup (1000 steps → 10–50).
- [ ] **Classifier-free guidance** (Ho & Salimans 2022): the standard conditioning mechanism for text-to-image. $\tilde\epsilon = (1+w)\epsilon_\theta(x_t, t, c) - w\,\epsilon_\theta(x_t, t, \emptyset)$.
- [ ] **Latent diffusion** (LDM / Stable Diffusion): run diffusion on a VAE-compressed latent, not on pixels — massive efficiency win.
- [ ] **Architecture menu**: U-Net (default), DiT (transformer, scales better), ControlNet (adding dense conditioning to a frozen model).
- [ ] **Inverse problems via Bayes-on-scores** (Song's $\nabla \log p(x \mid y) = \nabla \log p(x) + \nabla \log p(y \mid x)$): inpainting, colorization, MRI, all from a single pre-trained unconditional score network.
- [ ] **Robotics application**: Diffusion Policy (Chi et al. 2023) — $x_0$ = action chunk, $c$ = recent observations.

**Readings**

| Reading | Time |
|---|---|
| **[[What are Diffusion Models - Lilian Weng]]** §"Parameterization of $\beta_t$" through end (cosine schedule → classifier-free guidance → DDIM → progressive distillation → consistency models → LDM → cascaded SR → unCLIP → Imagen → U-Net → ControlNet → DiT) | 2h — skim sections you don't care about |
| **[[Generative Modeling by Estimating Gradients of the Data Distribution - Yang Song]]** §"Score-based generative modeling with stochastic differential equations" through end | 1h — focus on the SDE-vs-ODE distinction and Bayes-on-scores for inverse problems |
| **Chi et al. 2023, *Diffusion Policy: Visuomotor Policy Learning via Action Diffusion*** (~12 pages) | 1h — skim §1–3 only; this is the application end-goal |

**Socratic check** (the closing one): (a) Why does Diffusion Policy use a small $T$ (~100) with DDIM sampling rather than $T = 1000$ DDPM? (b) What architectural choice does it inherit from image diffusion that *doesn't* transfer well to robotics, and what's the workaround? (c) Where would classifier-free guidance fit into a robot policy — and what would the "conditioning" $c$ be? If you can hand-wave plausible answers to all three, you have the map. You will get the *exact* answers from a future deep-read of Chi et al. — for now, plausible is fine.

## Auxiliary cluster: Normalizing flows (~1.5h, optional but recommended for the map)

You have two normalizing-flow tutorials in `raw/diffusion-model/`. These are not strictly required for diffusion, but they fill in **the other** likelihood-based generative-modeling family — and the connection becomes load-bearing in Sunday afternoon's **probability-flow ODE** (which IS a continuous normalizing flow).

**Quick goals**

- [ ] **Change-of-variables** for a transformation $y = f(x)$: $p_Y(y) = p_X(f^{-1}(y))\,|\det J_{f^{-1}}(y)|$.
- [ ] The whole *point* of normalizing flows: enforce invertibility + tractable Jacobian, in exchange for closed-form $p_\theta(x)$ with $Z = 1$ implicitly.
- [ ] Why architectures are restricted (RealNVP coupling layers, MAF/IAF autoregressive flows): the Jacobian determinant has to be cheap to compute.
- [ ] **MAF vs IAF tradeoff**: MAF trains fast / samples slow, IAF samples fast / trains slow. Parallel WaveNet uses both: MAF teacher + IAF student.

**Readings**

| Reading | Time |
|---|---|
| **[[Normalizing Flows Tutorial Part 1 - Eric Jang]]** vault source page (Distributions and Determinants — the change-of-variables story) | 30 min |
| **[[Normalizing Flows Tutorial Part 2 - Eric Jang]]** vault source page (MAF / IAF / Real-NVP) | 30 min |
| Optional: Kobyzev et al. 2020, *Normalizing Flows: An Introduction and Review of Current Methods* (survey paper, IEEE PAMI) | 1h |

**Why it's on the map**: When you read Song's blog Sunday afternoon and hit the **probability-flow ODE** section, the "this is a neural ODE / continuous normalizing flow" line will only land if you've seen the basic NF formalism. Three of the four hours-spent payoffs from normalizing flows are: (1) understanding probability-flow ODE, (2) recognizing the change-of-variables formula when it shows up in derivations, (3) being able to read **Flow Matching** (Lipman et al. 2022) and **Rectified Flow** (Liu et al. 2022) papers — the modern post-diffusion direction.

## Beyond the weekend: depth dives by interest

After the crash course, pick *one* of the directions below for a focused week's reading. Don't try to do all of them.

| If you want to | Read |
|---|---|
| **Train your first diffusion model end-to-end** | Karras et al. 2022, *Elucidating the Design Space of Diffusion-Based Generative Models* (the practitioner's guide, EDM); Hugging Face `diffusers` tutorials |
| **Master the math** | Yang Song's *PhD thesis* (2022, Stanford) — full canonical reference, ~200 pages but covers EVERYTHING; then Song et al. 2021 *SDE paper* |
| **Apply diffusion in robotics** | Chi et al. 2023 *Diffusion Policy* full + [[Compositional Diffusion Constraint Solvers]] in this vault (SetItUp) + Janner et al. 2022 *Diffuser* |
| **Modern post-diffusion direction** | Lipman et al. 2022 *Flow Matching*; Liu et al. 2022 *Rectified Flow*; Song et al. 2023 *Consistency Models* |
| **Conditional generation / multimodal** | Saharia et al. 2022 *Imagen*; Ramesh et al. 2022 *unCLIP* (DALL·E 2); Zhang et al. 2023 *ControlNet* |
| **Theory + connections** | De Bortoli et al. 2021 *Diffusion Schrödinger Bridge*; Albergo & Vanden-Eijnden 2023 *Stochastic Interpolants* |

## Quick reference: textbooks and tutorials

**Books** (in order of recommendation for *this* curriculum, not a general DL syllabus):

1. **Bishop & Bishop, *Deep Learning: Foundations and Concepts* (2024)** — Ch. 16 (VAEs), Ch. 17 (GANs), Ch. 20 (Diffusion). Most current, most readable, most relevant to this course.
2. **Murphy, *Probabilistic Machine Learning: Advanced Topics* (2023)** — Ch. 21 (VAE), Ch. 25 (Diffusion). Heavier, encyclopedic.
3. **Goodfellow, Bengio, Courville, *Deep Learning* (2016)** — Ch. 14 (autoencoders), Ch. 19 (variational inference). Older, lacks modern diffusion, but the foundational chapters age well.
4. **Wasserman, *All of Statistics* (2004)** — Ch. 9 §9.13 (KL divergence between Gaussians) if you want a probability refresher.

**Foundational papers** (in study order):

1. Hyvärinen 2005, *Estimation of Non-Normalized Statistical Models by Score Matching* — foundational score-matching paper.
2. Vincent 2011, *A Connection between Score Matching and Denoising Autoencoders* — denoising score matching, the practical version.
3. Sohl-Dickstein et al. 2015, *Deep Unsupervised Learning Using Nonequilibrium Thermodynamics* — first diffusion paper.
4. Song & Ermon 2019, *Generative Modeling by Estimating Gradients of the Data Distribution* — NCSN.
5. **Ho, Jain, Abbeel 2020, *Denoising Diffusion Probabilistic Models* — DDPM, the canonical modern formulation. Read this one in full.**
6. Song et al. 2020, *Denoising Diffusion Implicit Models* — DDIM, deterministic sampling.
7. Song et al. 2021, *Score-Based Generative Modeling through Stochastic Differential Equations* — SDE unification, ICLR 2021 Outstanding Paper.
8. Ho & Salimans 2022, *Classifier-Free Diffusion Guidance* — CFG, the dominant conditioning mechanism.
9. Rombach et al. 2022, *High-Resolution Image Synthesis with Latent Diffusion Models* — LDM / Stable Diffusion.
10. **Chi et al. 2023, *Diffusion Policy* — the robotics application end-goal.**

**Secondary surveys** (already ingested into this vault):

- [[What are Diffusion Models - Lilian Weng]] — DDPM-first canonical survey.
- [[Generative Modeling by Estimating Gradients of the Data Distribution - Yang Song]] — score-first canonical survey, explicit DDPM ↔ score unification.

**Course material**:

- **Pieter Abbeel's CS294-158 (UC Berkeley)** — Deep Unsupervised Learning, lectures on Vimeo, slides public. Best video course.
- **CVPR 2022 Tutorial: Denoising Diffusion-based Generative Modeling: Foundations and Applications** by Karsten Kreis, Ruiqi Gao, Arash Vahdat — ~3h video + slide deck, a perfect mid-point review (cvpr2022-tutorial-diffusion-models.github.io).
- **Sander Dieleman's blog** (sander.ai) — many short, deep posts on diffusion intuition.

## Pacing notes

- **If you start Saturday morning and feel behind by lunch**, skip Block B's Hyvärinen paper and the optional Dieleman blog. Block B's bare minimum is just the first three sections of Yang Song's blog.
- **If you finish Saturday early**, get a jump on Block C by reading the *first half* of [[What are Diffusion Models - Lilian Weng]] Saturday evening. Don't try to derive yet — just read it for flow.
- **If you fall behind by Sunday afternoon**, Block D is the most safely-skimmable. The Sunday-evening goal is "I have seen every named idea once," not "I can derive each one." DDIM, CFG, LDM, DiT, ControlNet — each is fine as a 5-minute "I know roughly what this is."
- **Don't open Pytorch.** No code this weekend. The temptation to "just run a notebook" will eat 4 hours and not advance the map.

## How this synthesis is structured (one-shot read)

If you only have an hour, read in this order:
1. This page's **Premise** section (top).
2. [[Normalizing Constant]] — the prerequisite you have, refresher.
3. [[Diffusion Models]] §"Definition" + §"The score interpretation (the unlock)" — the spine.
4. [[Generative Modeling by Estimating Gradients of the Data Distribution - Yang Song]] §1 + §"Connection to diffusion models and others" (the historical / unification sections) — the framing.
5. Come back to this curriculum for the full weekend when time allows.

## Related

- [[Diffusion Models]] — the spine of the curriculum; updated continuously.
- [[Normalizing Constant]] — Saturday-morning prerequisite, already covered.
- [[What are Diffusion Models - Lilian Weng]] — primary reading for Sunday morning.
- [[Generative Modeling by Estimating Gradients of the Data Distribution - Yang Song]] — primary reading for Saturday afternoon and Sunday afternoon.
- [[Normalizing Flows Tutorial Part 1 - Eric Jang]] — auxiliary normalizing-flows reading.
- [[Normalizing Flows Tutorial Part 2 - Eric Jang]] — auxiliary normalizing-flows reading.
- [[learning-tracker]] — coverage map; gets updated as you complete each block.
- (red link) [[Diffusion Policy]] — the next deep-read after the crash course.
