---
type: concept
domain: research
created: 2026-05-30
updated: 2026-05-30
aliases: ["partition function", "Z_theta", "normalization constant", "normalizing factor"]
tags: [probability, generative-models, energy-based-models, score-matching, foundations]
sources:
  - "[[Generative Modeling by Estimating Gradients of the Data Distribution - Yang Song]]"
---

# Normalizing Constant

## Explain like I'm 5

You cut a cake into 8 slices of different sizes. The slices have **raw weights** — say `[120, 80, 200, 150, 90, 60, 100, 200]` grams. Those weights tell you which slice is bigger than which, but they aren't *fractions of the cake* yet. To turn them into fractions (numbers that all add up to 1), you divide each one by the **total weight of the whole cake**:

$$
\text{fraction}_i \;=\; \frac{w_i}{w_1 + w_2 + \cdots + w_8} \;=\; \frac{w_i}{1000}.
$$

That $1000$ is the **normalizing constant**. It's the boring-but-essential glue that turns "relative sizes" into "actual probabilities." Every probability distribution on the planet has one.

## Bridges from

- **Cake-fraction math** *(extended)*. Statisticians do the same thing as the cake-cutter, just with continuous shapes. Anything that says "the bigger this is, the more likely the outcome" needs a normalizer at the end so the percentages add up to 100%.

  *Where the analogy breaks down*:
  - The cake has 8 discrete slices, so the "total weight" is a sum you can do by hand. In machine learning, $x$ usually lives in a continuous, high-dimensional space (every pixel of an image, every joint angle of a robot), so the "total weight" becomes an **integral** over an enormous domain. That integral is where the difficulty hides.
  - The cake exists in physical space, so the total weight is a finite number you can put on a scale. The "total weight" of a probability density defined by a neural network is a mathematical integral — well-defined in principle, but for a general neural-net energy function there is **no closed form** for it. Defined ≠ computable.

- **Grains of sand on Earth**. To answer "what fraction of all sand on Earth is in the Sahara?" you need (a) the Sahara count and (b) the *global* count. (a) is doable; (b) is intractable — you'd have to inventory every beach, every desert, every ocean floor. The denominator is the hard part, and that denominator is the normalizing constant.

## Definition

For any positive function $\tilde p(x)$ that we want to interpret as "unnormalized probability mass" (or unnormalized density), the **normalizing constant** is

$$
\boxed{\;Z \;=\; \int \tilde p(x)\,dx\;}
$$

(or a sum, $Z = \sum_x \tilde p(x)$, if $x$ is discrete). Dividing by $Z$ gives a proper probability density:

$$
p(x) \;=\; \frac{\tilde p(x)}{Z}, \qquad \int p(x)\,dx \;=\; 1.
$$

In Yang Song's setup, $\tilde p_\theta(x) = e^{-f_\theta(x)}$ where $f_\theta$ is a neural network (the **energy function**), so

$$
p_\theta(x) \;=\; \frac{e^{-f_\theta(x)}}{Z_\theta}, \qquad Z_\theta \;=\; \int e^{-f_\theta(x)}\,dx.
$$

The Boltzmann form $e^{-f}$ guarantees positivity for any real-valued $f$; dividing by $Z_\theta$ enforces "total mass = 1."

## What "raw shape" vs. "normalized density" looks like

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 340" font-family="sans-serif" font-size="13">
  <defs>
    <marker id="arrow-nc" markerWidth="10" markerHeight="8" refX="8" refY="4" orient="auto">
      <polygon points="0 0, 10 4, 0 8" fill="black"/>
    </marker>
  </defs>

  <!-- Left panel: unnormalized -->
  <g>
    <text x="160" y="22" text-anchor="middle" font-weight="bold" font-size="14">Unnormalized shape</text>
    <text x="160" y="42" text-anchor="middle" fill="#555">y = e^(−f(x))</text>
    <line x1="30" y1="280" x2="290" y2="280" stroke="black" stroke-width="1.2"/>
    <line x1="30" y1="280" x2="30" y2="70" stroke="black" stroke-width="1.2"/>
    <path d="M 30 280 C 90 280, 100 90, 160 90 C 220 90, 230 280, 290 280 Z"
          fill="#5B8DEF" fill-opacity="0.45" stroke="#1f4ea1" stroke-width="2"/>
    <text x="160" y="200" text-anchor="middle" font-size="14" fill="#1f4ea1" font-weight="bold">area = Z_θ</text>
    <text x="160" y="220" text-anchor="middle" font-size="11" fill="#1f4ea1">(some positive number — usually big)</text>
    <text x="160" y="305" text-anchor="middle" fill="#555">x</text>
  </g>

  <!-- divide-by-Z arrow -->
  <g transform="translate(330, 175)">
    <line x1="0" y1="0" x2="60" y2="0" stroke="black" stroke-width="2" marker-end="url(#arrow-nc)"/>
    <text x="30" y="-10" text-anchor="middle" font-size="14" font-weight="bold">÷ Z_θ</text>
  </g>

  <!-- Right panel: normalized -->
  <g transform="translate(400, 0)">
    <text x="160" y="22" text-anchor="middle" font-weight="bold" font-size="14">Probability density</text>
    <text x="160" y="42" text-anchor="middle" fill="#555">p(x) = e^(−f(x)) / Z_θ</text>
    <line x1="30" y1="280" x2="290" y2="280" stroke="black" stroke-width="1.2"/>
    <line x1="30" y1="280" x2="30" y2="70" stroke="black" stroke-width="1.2"/>
    <path d="M 30 280 C 90 280, 100 215, 160 215 C 220 215, 230 280, 290 280 Z"
          fill="#38a169" fill-opacity="0.45" stroke="#22543d" stroke-width="2"/>
    <text x="160" y="262" text-anchor="middle" font-size="14" fill="#22543d" font-weight="bold">area = 1</text>
    <text x="160" y="305" text-anchor="middle" fill="#555">x</text>
  </g>

  <text x="360" y="328" text-anchor="middle" font-size="12" fill="#555" font-style="italic">
    Same shape, different scaling. Dividing by Z_θ squashes the curve so its total area equals 1.
  </text>
</svg>

The shape of $p_\theta(x)$ — *which $x$ values are more or less likely relative to each other* — is fully determined by $f_\theta(x)$. The normalizing constant just rescales the height of the entire curve so the area becomes 1. It carries no information about which $x$ is more likely; it's pure bookkeeping.

That observation is what Yang exploits, as we'll see in a moment.

## What "tractable" means

**Tractable** = *computable in practice, in a reasonable amount of time*.

- For the cake, $Z = 1000$ is tractable: 8 slices, add them up, done in 2 seconds.
- For $Z_\theta = \int e^{-f_\theta(x)}\,dx$ when $x$ is a 256×256 RGB image, you're integrating over $\mathbb{R}^{196608}$. For a general neural net $f_\theta$, there is **no closed form**, and naive numerical integration is exponentially expensive in the dimension (the **curse of dimensionality**). You can write the integral down on paper; you cannot evaluate it.

That gap — "mathematically well-defined" vs. "actually computable" — is what "intractable" means. A model whose density requires evaluating an intractable $Z_\theta$ to score even one data point is, practically, untrainable by maximum likelihood.

## Why this is the load-bearing problem in generative modeling

Maximum-likelihood training maximizes $\log p_\theta(x_i)$ on observed data $\{x_i\}$, which expands to

$$
\log p_\theta(x_i) \;=\; \underbrace{-f_\theta(x_i)}_{\text{easy — one forward pass}} \;-\; \underbrace{\log Z_\theta}_{\text{a } d\text{-dim integral}}.
$$

The first term is one neural-net forward pass. The second is an integral over all of $\mathbb{R}^d$. So **every** likelihood-based model family is, fundamentally, a strategy for getting around $\log Z_\theta$:

| Family | Strategy | Cost paid |
|---|---|---|
| **Autoregressive** (PixelRNN, GPT) | Factor $p(x) = \prod_i p(x_i \mid x_{<i})$; each 1D conditional has a tiny tractable normalizer (softmax / 1D Gaussian). The product of normalized things is normalized. | Sequential generation (slow at inference); architecture is constrained to be causal. |
| **Normalizing flows** (RealNVP, Glow) | Define $x = g_\theta(z)$ for $z \sim \mathcal{N}(0, I)$ with $g_\theta$ invertible and easy-Jacobian. Change-of-variables formula gives $p_\theta(x)$ in closed form — $Z$ is implicitly 1. | Severely restricted architecture (must be invertible and Jacobian-tractable). |
| **VAEs** | Don't compute $p_\theta(x)$ at all — optimize the **ELBO**, a tractable lower bound on $\log p_\theta(x)$ that uses a learned encoder. | Bound is not tight; samples are blurry compared to GANs / diffusion. |
| **Energy-based models** (EBMs) | Embrace the intractable $Z$; train with **score matching** or **contrastive divergence** to dodge it. | Sampling requires MCMC; training is finicky. |
| **GANs** | Side-step the entire density-modeling question; learn a sampler $G_\theta : z \mapsto x$ adversarially. | No density (only samples); training is unstable. |
| **Diffusion / score-based** | Either learn a noise-prediction MSE loss (DDPM-style) that *implicitly* matches the score, or directly learn the score $s_\theta(x) \approx \nabla_x \log p(x)$ (NCSN/SDE-style). Both bypass $Z$ entirely. | Slow sampling (many denoising steps). |

The whole table is "tractability strategies." If $Z_\theta$ were free to compute, generative modeling would be a much smaller field — everyone would just do max-likelihood on whatever architecture they wanted.

## The score-based escape (the unlock)

Take the gradient of $\log p_\theta(x)$ with respect to $x$:

$$
\nabla_x \log p_\theta(x) \;=\; \nabla_x\bigl(-f_\theta(x) - \log Z_\theta\bigr) \;=\; -\nabla_x f_\theta(x) \;-\; \underbrace{\nabla_x \log Z_\theta}_{= \,0}.
$$

$Z_\theta = \int e^{-f_\theta(x)}\,dx$ is an integral over $x$ — once you integrate $x$ out, the result is a number that depends on $\theta$ but **not on $x$**. So as a function of $x$, $\log Z_\theta$ is constant, and its gradient is zero. **The normalizing constant vanishes from the score.**

This is the entire reason score-based modeling exists. Yang puts it directly:

> *"Note that the score-based model $s_\theta(x)$ is independent of the normalizing constant $Z_\theta$! This significantly expands the family of models that we can tractably use, since we don't need any special architectures to make the normalizing constant tractable."*

You can choose **any** neural architecture for $f_\theta$ (or equivalently for the score network $s_\theta$ directly) — no causal masks, no invertibility, no pre-baked Gaussians — without ever worrying about whether $\int e^{-f_\theta(x)}\,dx$ is computable. Everything downstream in his blog (score matching, Langevin dynamics, NCSN, SDE generalization, probability-flow ODE, Bayes-on-scores for inverse problems) is built on top of this one observation.

## Where else you'll meet $Z$

The normalizing constant is everywhere in probability — once you see it, you start spotting it:

- **Bayesian inference.** Bayes' rule says $p(\theta \mid \text{data}) = p(\theta)\,p(\text{data} \mid \theta) / p(\text{data})$. The denominator $p(\text{data}) = \int p(\theta)\,p(\text{data} \mid \theta)\,d\theta$ is a normalizing constant — sometimes called the **marginal likelihood** or **evidence** — and it's the reason variational inference and MCMC exist (both are ways to avoid computing it).
- **Softmax classification.** The softmax $p(y = k \mid x) = e^{z_k} / \sum_j e^{z_j}$ has $Z = \sum_j e^{z_j}$ as its normalizer. Tractable because $j$ ranges over a small number of classes — it's the small-discrete case of Yang's $Z_\theta$.
- **Statistical physics: the partition function.** $Z = \sum_s e^{-E(s)/kT}$ over all microstates $s$ of a physical system. The Boltzmann distribution $p(s) = e^{-E(s)/kT}/Z$ over thermal microstates is *exactly* an energy-based model in disguise. Energy-based generative models inherit the name "partition function" from physics.
- **Conditional random fields (CRFs).** Normalize over all valid label sequences. Tractable only for chain-structured CRFs (where dynamic programming evaluates $Z$ in linear time); intractable for general graphs.
- **Markov random fields, Boltzmann machines, Ising models.** All defined by $p(x) = e^{-E(x)}/Z$; the intractability of $Z$ is the central computational hurdle.

If you encounter a *partition function* in a paper, that's the same object as a normalizing constant; the term is borrowed from statistical physics.

## Common confusions

- **"Tractable" doesn't mean "small" or "simple."** It means "computable with reasonable resources." A normalizing constant can be a huge number (and usually is) and still be tractable, as long as you can compute it. Conversely, $Z$ for a discrete distribution over 100 binary variables is "just a sum," but it has $2^{100}$ terms — intractable.
- **The shape and the normalizer carry different information.** $f_\theta(x)$ determines *which $x$ is more likely than which*; $Z_\theta$ determines only the *absolute scale* of the probabilities. For ranking ("is $x_1$ more likely than $x_2$?") you only need the unnormalized $\tilde p$. For probabilities ("what is $P(x_1)$?") you need $Z$.
- **The gradient trick doesn't work for $\log p$ itself, only for $\nabla_x \log p$.** $\log Z_\theta$ is constant in $x$ (so it vanishes from $\nabla_x \log p$) but it is *not* constant in $\theta$ — so $\nabla_\theta \log p$ does not vanish. Max-likelihood training, which differentiates with respect to $\theta$, still has to grapple with $Z_\theta$. Score-based training escapes by replacing the max-likelihood objective entirely with a score-matching objective.
- **"Tractable normalizing constant" can mean two different things.** (1) The integral has a closed-form expression (e.g., the Gaussian's $Z = (2\pi\sigma^2)^{d/2}$). (2) The integral can be computed numerically in reasonable time (e.g., the discrete sum of a softmax over 50,000 vocabulary tokens). Both count as tractable. Neither applies to a general high-dimensional neural-network energy.

## Origins / sources

- **Statistical physics**: the **partition function** $Z = \sum_s e^{-E(s)/kT}$ was the original normalizing constant — see Gibbs (1902), *Elementary Principles in Statistical Mechanics*. The term and the notation $Z$ both come from physics.
- **Bayesian inference**: the **marginal likelihood / evidence** $p(\text{data}) = \int p(\theta)\,p(\text{data} \mid \theta)\,d\theta$ as a normalizing constant traces to Bayes (1763) and Laplace; computing it is the central problem of approximate Bayesian inference.
- **Energy-based models in ML**: LeCun et al., *A Tutorial on Energy-Based Learning* (2006); Hinton, *Training Products of Experts by Minimizing Contrastive Divergence* (2002) — the modern framing where neural nets parameterize $f_\theta$ and $Z_\theta$ is intractable.
- **Why score-based modeling lets you ignore $Z$**: Hyvärinen (2005), *Estimation of Non-Normalized Statistical Models by Score Matching* — the foundational paper showing you can train a model that defines a density up to a normalizing constant without ever computing that constant. Yang Song's blog ([[Generative Modeling by Estimating Gradients of the Data Distribution - Yang Song]]) is the modern presentation.

## Related concepts

- [[Diffusion Models]] — built to dodge $Z_\theta$. The whole reason ε-prediction / score-matching is preferred over direct density modeling.
- [[Generative Modeling by Estimating Gradients of the Data Distribution - Yang Song]] — the source that motivated this page; the score-based "vanish $Z_\theta$" trick is its opening move.
- [[What are Diffusion Models - Lilian Weng]] — Weng's DDPM derivation reaches an MSE loss that, via the score identity, is *also* avoiding $Z_\theta$ — but the connection is hidden behind the variational bound and only becomes obvious when you see the score-based view.
- [[Constraint Gradients and Tangent Spaces]] — same "gradient of a scalar function" mental object. The constraint gradient $\nabla h(x)$ and the score $\nabla \log p(x)$ are both gradient fields over $\mathbb{R}^d$, just pointing toward different targets (constraint surface vs. data manifold).
- [[Sigmoid Function]] — the 2-class softmax, where the normalizer $Z = e^{z_0} + e^{z_1}$ is so small that you never think of it as a normalizing constant — but it is one.
- (red link) [[Energy-Based Models]] — the model family where $Z_\theta$ is the central computational hurdle.
- (red link) [[Score Matching]] — Hyvärinen's training method that side-steps $Z$ by matching the score instead of the density.
- (red link) [[Partition Function]] — the statistical-physics name for the same object.
- (red link) [[Softmax]] — the small-discrete tractable case.

## Mentions

- [[Diffusion Models]] — cites this page in the score-vs-density discussion.
- [[Generative Modeling by Estimating Gradients of the Data Distribution - Yang Song]] — the source whose opening section motivated this concept page.
