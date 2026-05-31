---
title: "What are Diffusion Models?"
source: "https://lilianweng.github.io/posts/2021-07-11-diffusion-models/"
author:
  - "[[Lilian Weng]]"
published: 2021-07-11
created: 2026-05-30
description: "[Updated on 2021-09-19: Highly recommend this blog post on score-based generative modeling by Yang Song (author of several key papers in the references)].[Updated on 2022-08-27: Added classifier-free guidance, GLIDE, unCLIP and Imagen.[Updated on 2022-08-31: Added latent diffusion model.[Updated on 2024-04-13: Added progressive distillation, consistency models, and the Model Architecture section."
tags:
  - "clippings"
---
\[Updated on 2021-09-19: Highly recommend this blog post on [score-based generative modeling](https://yang-song.github.io/blog/2021/score/) by Yang Song (author of several key papers in the references)\].  
\[Updated on 2022-08-27: Added [classifier-free guidance](#classifier-free-guidance), [GLIDE](#glide), [unCLIP](#unclip) and [Imagen](#imagen).  
\[Updated on 2022-08-31: Added [latent diffusion model](#ldm).  
\[Updated on 2024-04-13: Added [progressive distillation](#prog-distll), [consistency models](#consistency), and the [Model Architecture section](#model-architecture).

So far, I’ve written about three types of generative models, [GAN](https://lilianweng.github.io/posts/2017-08-20-gan/), [VAE](https://lilianweng.github.io/posts/2018-08-12-vae/), and [Flow-based](https://lilianweng.github.io/posts/2018-10-13-flow-models/) models. They have shown great success in generating high-quality samples, but each has some limitations of its own. GAN models are known for potentially unstable training and less diversity in generation due to their adversarial training nature. VAE relies on a surrogate loss. Flow models have to use specialized architectures to construct reversible transform.

Diffusion models are inspired by non-equilibrium thermodynamics. They define a Markov chain of diffusion steps to slowly add random noise to data and then learn to reverse the diffusion process to construct desired data samples from the noise. Unlike VAE or flow models, diffusion models are learned with a fixed procedure and the latent variable has high dimensionality (same as the original data).

![](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/generative-overview.png)

Overview of different types of generative models.

Several diffusion-based generative models have been proposed with similar ideas underneath, including *diffusion probabilistic models* ([Sohl-Dickstein et al., 2015](https://arxiv.org/abs/1503.03585)), *noise-conditioned score network* (**NCSN**; [Yang & Ermon, 2019](https://arxiv.org/abs/1907.05600)), and *denoising diffusion probabilistic models* (**DDPM**; [Ho et al. 2020](https://arxiv.org/abs/2006.11239)).

## Forward diffusion process

Given a data point sampled from a real data distribution $\mathbf{x}_{0} sim q \left(\right. \mathbf{x} \left.\right)$, let us define a *forward diffusion process* in which we add small amount of Gaussian noise to the sample in $T$ steps, producing a sequence of noisy samples $\mathbf{x}_{1} , \ldots , \mathbf{x}_{T}$. The step sizes are controlled by a variance schedule $\left{\right. \beta_{t} \in \left(\right. 0 , 1 \left.\right) \left.\right}_{t = 1}^{T}$.

$$
q \left( \mathbf{x}_{t} \mid  \mathbf{x}_{t - 1} \right) = \mathcal{N} \left( \mathbf{x}_{t} ; \sqrt{1 - \beta_{t}} \mathbf{x}_{t - 1} , \beta_{t} \mathbf{I} \right) q \left( \mathbf{x}_{1 : T} \mid  \mathbf{x}_{0} \right) = \prod_{t = 1}^{T} q \left( \mathbf{x}_{t} \mid  \mathbf{x}_{t - 1} \right)
$$

The data sample $\mathbf{x}_{0}$ gradually loses its distinguishable features as the step $t$ becomes larger. Eventually when $T \rightarrow \infty$, $\mathbf{x}_{T}$ is equivalent to an isotropic Gaussian distribution.

![](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/DDPM.png)

The Markov chain of forward (reverse) diffusion process of generating a sample by slowly adding (removing) noise. (Image source: Ho et al. 2020 with a few additional annotations)

A nice property of the above process is that we can sample $\mathbf{x}_{t}$ at any arbitrary time step $t$ in a closed form using [reparameterization trick](https://lilianweng.github.io/posts/2018-08-12-vae/#reparameterization-trick). Let $\alpha_{t} = 1 - \beta_{t}$ and $\bar{\alpha}_{t} = \prod_{i = 1}^{t} \alpha_{i}$:

$$
\begin{aligned}
\mathbf{x}_{t} & = \sqrt{\alpha_{t}} \mathbf{x}_{t - 1} + \sqrt{1 - \alpha_{t}} \mathbf{\mathit{\epsilon}}_{t - 1} & \quad\text{where } \mathbf{\mathit{\epsilon}}_{t - 1} , \mathbf{\mathit{\epsilon}}_{t - 2} , \hdots \sim \mathcal{N} \left( 0 , \mathbf{I} \right) \\ = \sqrt{\alpha_{t} \alpha_{t - 1}} \mathbf{x}_{t - 2} + \sqrt{1 - \alpha_{t} \alpha_{t - 1}} \bar{\mathbf{\mathit{\epsilon}}}_{t - 2} & \quad\text{where } \bar{\mathbf{\mathit{\epsilon}}}_{t - 2} \text{merges two Gaussians }(*). \\ = \ldots \\ = \sqrt{\bar{\alpha}_{t}} \mathbf{x}_{0} + \sqrt{1 - \bar{\alpha}_{t}} \mathbf{\mathit{\epsilon}} \\ q \left( \mathbf{x}_{t} \mid  \mathbf{x}_{0} \right) & = \mathcal{N} \left( \mathbf{x}_{t} ; \sqrt{\bar{\alpha}_{t}} \mathbf{x}_{0} , \left( 1 - \bar{\alpha}_{t} \right) \mathbf{I} \right)
\end{aligned}
$$

(\*) Recall that when we merge two Gaussians with different variance, $\mathcal{N} \left(\right. 0 , \sigma_{1}^{2} \mathbf{I} \left.\right)$ and $\mathcal{N} \left(\right. 0 , \sigma_{2}^{2} \mathbf{I} \left.\right)$, the new distribution is $\mathcal{N} \left(\right. 0 , \left(\right. \sigma_{1}^{2} + \sigma_{2}^{2} \left.\right) \mathbf{I} \left.\right)$. Here the merged standard deviation is $\sqrt{\left(\right. 1 - \alpha_{t} \left.\right) + \alpha_{t} \left(\right. 1 - \alpha_{t - 1} \left.\right)} = \sqrt{1 - \alpha_{t} \alpha_{t - 1}}$.

Usually, we can afford a larger update step when the sample gets noisier, so $\beta_{1} < \beta_{2} < \hdots < \beta_{T}$ and therefore $\bar{\alpha}_{1} > \hdots > \bar{\alpha}_{T}$.

### Connection with stochastic gradient Langevin dynamics

Langevin dynamics is a concept from physics, developed for statistically modeling molecular systems. Combined with stochastic gradient descent, *stochastic gradient Langevin dynamics* ([Welling & Teh 2011](https://www.stats.ox.ac.uk/~teh/research/compstats/WelTeh2011a.pdf)) can produce samples from a probability density $p \left(\right. \mathbf{x} \left.\right)$ using only the gradients $\nabla_{\mathbf{x}} log ⁡ p \left(\right. \mathbf{x} \left.\right)$ in a Markov chain of updates:

$$
\mathbf{x}_{t} = \mathbf{x}_{t - 1} + \frac{\delta}{2} \nabla_{\mathbf{x}} \log  p \left( \mathbf{x}_{t - 1} \right) + \sqrt{\delta} \mathbf{\mathit{\epsilon}}_{t} , \text{where } \mathbf{\mathit{\epsilon}}_{t} \sim \mathcal{N} \left( 0 , \mathbf{I} \right)
$$

where $\delta$ is the step size. When $T \rightarrow \infty , \epsilon \rightarrow 0$, $\mathbf{x}_{T}$ equals to the true probability density $p \left(\right. \mathbf{x} \left.\right)$.

Compared to standard SGD, stochastic gradient Langevin dynamics injects Gaussian noise into the parameter updates to avoid collapses into local minima.

## Reverse diffusion process

If we can reverse the above process and sample from $q \left(\right. \mathbf{x}_{t - 1} \left|\right. \mathbf{x}_{t} \left.\right)$, we will be able to recreate the true sample from a Gaussian noise input, $\mathbf{x}_{T} sim \mathcal{N} \left(\right. 0 , \mathbf{I} \left.\right)$. Note that if $\beta_{t}$ is small enough, $q \left(\right. \mathbf{x}_{t - 1} \left|\right. \mathbf{x}_{t} \left.\right)$ will also be Gaussian. Unfortunately, we cannot easily estimate $q \left(\right. \mathbf{x}_{t - 1} \left|\right. \mathbf{x}_{t} \left.\right)$ because it needs to use the entire dataset and therefore we need to learn a model $p_{\theta}$ to approximate these conditional probabilities in order to run the *reverse diffusion process*.

$$
p_{\theta} \left( \mathbf{x}_{0 : T} \right) = p \left( \mathbf{x}_{T} \right) \prod_{t = 1}^{T} p_{\theta} \left( \mathbf{x}_{t - 1} \mid  \mathbf{x}_{t} \right) p_{\theta} \left( \mathbf{x}_{t - 1} \mid  \mathbf{x}_{t} \right) = \mathcal{N} \left( \mathbf{x}_{t - 1} ; \mathbf{\mathit{\mu}}_{\theta} \left( \mathbf{x}_{t} , t \right) , \mathbf{\Sigma}_{\theta} \left( \mathbf{x}_{t} , t \right) \right)
$$
![](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/diffusion-example.png)

An example of training a diffusion model for modeling a 2D swiss roll data. (Image source: Sohl-Dickstein et al., 2015 )

It is noteworthy that the reverse conditional probability is tractable when conditioned on $\mathbf{x}_{0}$:

$$
q \left( \mathbf{x}_{t - 1} \mid  \mathbf{x}_{t} , \mathbf{x}_{0} \right) = \mathcal{N} \left( \mathbf{x}_{t - 1} ; \overset{\sim}{\mathbf{\mathit{\mu}}} \left( \mathbf{x}_{t} , \mathbf{x}_{0} \right) , \overset{\sim}{\beta}_{t} \mathbf{I} \right)
$$

Using Bayes’ rule, we have:

$$
\begin{aligned}
q \left( \mathbf{x}_{t - 1} \mid  \mathbf{x}_{t} , \mathbf{x}_{0} \right) & = q \left( \mathbf{x}_{t} \mid  \mathbf{x}_{t - 1} , \mathbf{x}_{0} \right) \frac{q \left( \mathbf{x}_{t - 1} \mid  \mathbf{x}_{0} \right)}{q \left( \mathbf{x}_{t} \mid  \mathbf{x}_{0} \right)} \\ \propto \exp  \left( - \frac{1}{2} \left( \frac{\left( \mathbf{x}_{t} - \sqrt{\alpha_{t}} \mathbf{x}_{t - 1} \right)^{2}}{\beta_{t}} + \frac{\left( \mathbf{x}_{t - 1} - \sqrt{\bar{\alpha}_{t - 1}} \mathbf{x}_{0} \right)^{2}}{1 - \bar{\alpha}_{t - 1}} - \frac{\left( \mathbf{x}_{t} - \sqrt{\bar{\alpha}_{t}} \mathbf{x}_{0} \right)^{2}}{1 - \bar{\alpha}_{t}} \right) \right) \\ = \exp  \left( - \frac{1}{2} \left( \frac{\mathbf{x}_{t}^{2} - 2 \sqrt{\alpha_{t}} \mathbf{x}_{t} \mathbf{x}_{t - 1} + \alpha_{t} \mathbf{x}_{t - 1}^{2}}{\beta_{t}} + \frac{\mathbf{x}_{t - 1}^{2} - 2 \sqrt{\bar{\alpha}_{t - 1}} \mathbf{x}_{0} \mathbf{x}_{t - 1} + \bar{\alpha}_{t - 1} \mathbf{x}_{0}^{2}}{1 - \bar{\alpha}_{t - 1}} - \frac{\left( \mathbf{x}_{t} - \sqrt{\bar{\alpha}_{t}} \mathbf{x}_{0} \right)^{2}}{1 - \bar{\alpha}_{t}} \right) \right) \\ = \exp  \left( - \frac{1}{2} \left( \left( \frac{\alpha_{t}}{\beta_{t}} + \frac{1}{1 - \bar{\alpha}_{t - 1}} \right) \mathbf{x}_{t - 1}^{2} - \left( \frac{2 \sqrt{\alpha_{t}}}{\beta_{t}} \mathbf{x}_{t} + \frac{2 \sqrt{\bar{\alpha}_{t - 1}}}{1 - \bar{\alpha}_{t - 1}} \mathbf{x}_{0} \right) \mathbf{x}_{t - 1} + C \left( \mathbf{x}_{t} , \mathbf{x}_{0} \right) \right) \right)
\end{aligned}
$$

where $C \left(\right. \mathbf{x}_{t} , \mathbf{x}_{0} \left.\right)$ is some function not involving $\mathbf{x}_{t - 1}$ and details are omitted. Following the standard Gaussian density function, the mean and variance can be parameterized as follows (recall that $\alpha_{t} = 1 - \beta_{t}$ and $\bar{\alpha}_{t} = \prod_{i = 1}^{t} \alpha_{i}$):

$$
\begin{aligned}
\overset{\sim}{\beta}_{t} & = 1 / \left( \frac{\alpha_{t}}{\beta_{t}} + \frac{1}{1 - \bar{\alpha}_{t - 1}} \right) = 1 / \left( \frac{\alpha_{t} - \bar{\alpha}_{t} + \beta_{t}}{\beta_{t} \left( 1 - \bar{\alpha}_{t - 1} \right)} \right) = \frac{1 - \bar{\alpha}_{t - 1}}{1 - \bar{\alpha}_{t}} \cdot \beta_{t} \\ \overset{\sim}{\mathbf{\mathit{\mu}}}_{t} \left( \mathbf{x}_{t} , \mathbf{x}_{0} \right) & = \left( \frac{\sqrt{\alpha_{t}}}{\beta_{t}} \mathbf{x}_{t} + \frac{\sqrt{\bar{\alpha}_{t - 1}}}{1 - \bar{\alpha}_{t - 1}} \mathbf{x}_{0} \right) / \left( \frac{\alpha_{t}}{\beta_{t}} + \frac{1}{1 - \bar{\alpha}_{t - 1}} \right) \\ = \left( \frac{\sqrt{\alpha_{t}}}{\beta_{t}} \mathbf{x}_{t} + \frac{\sqrt{\bar{\alpha}_{t - 1}}}{1 - \bar{\alpha}_{t - 1}} \mathbf{x}_{0} \right) \frac{1 - \bar{\alpha}_{t - 1}}{1 - \bar{\alpha}_{t}} \cdot \beta_{t} \\ = \frac{\sqrt{\alpha_{t}} \left( 1 - \bar{\alpha}_{t - 1} \right)}{1 - \bar{\alpha}_{t}} \mathbf{x}_{t} + \frac{\sqrt{\bar{\alpha}_{t - 1}} \beta_{t}}{1 - \bar{\alpha}_{t}} \mathbf{x}_{0}
\end{aligned}
$$

Thanks to the [nice property](#nice), we can represent $\mathbf{x}_{0} = \frac{1}{\sqrt{\bar{\alpha}_{t}}} \left(\right. \mathbf{x}_{t} - \sqrt{1 - \bar{\alpha}_{t}} \mathbf{\mathit{\epsilon}}_{t} \left.\right)$ and plug it into the above equation and obtain:

$$
\begin{aligned}
\overset{\sim}{\mathbf{\mathit{\mu}}}_{t} & = \frac{\sqrt{\alpha_{t}} \left( 1 - \bar{\alpha}_{t - 1} \right)}{1 - \bar{\alpha}_{t}} \mathbf{x}_{t} + \frac{\sqrt{\bar{\alpha}_{t - 1}} \beta_{t}}{1 - \bar{\alpha}_{t}} \frac{1}{\sqrt{\bar{\alpha}_{t}}} \left( \mathbf{x}_{t} - \sqrt{1 - \bar{\alpha}_{t}} \mathbf{\mathit{\epsilon}}_{t} \right) \\ = \frac{1}{\sqrt{\alpha_{t}}} \left( \mathbf{x}_{t} - \frac{1 - \alpha_{t}}{\sqrt{1 - \bar{\alpha}_{t}}} \mathbf{\mathit{\epsilon}}_{t} \right)
\end{aligned}
$$

As demonstrated in Fig. 2., such a setup is very similar to [VAE](https://lilianweng.github.io/posts/2018-08-12-vae/) and thus we can use the variational lower bound to optimize the negative log-likelihood.

$$
\begin{aligned}
- \log  p_{\theta} \left( \mathbf{x}_{0} \right) & \leq - \log  p_{\theta} \left( \mathbf{x}_{0} \right) + D_{\text{KL}} \left( q \left( \mathbf{x}_{1 : T} \mid  \mathbf{x}_{0} \right) \parallel p_{\theta} \left( \mathbf{x}_{1 : T} \mid  \mathbf{x}_{0} \right) \right) & \quad\text{ KL is non}-\text{negative} \\ = - \log  p_{\theta} \left( \mathbf{x}_{0} \right) + \mathbb{E}_{\mathbf{x}_{1 : T} \sim q \left( \mathbf{x}_{1 : T} \mid  \mathbf{x}_{0} \right)} \left[ \log  \frac{q \left( \mathbf{x}_{1 : T} \mid  \mathbf{x}_{0} \right)}{p_{\theta} \left( \mathbf{x}_{0 : T} \right) / p_{\theta} \left( \mathbf{x}_{0} \right)} \left]\right. \\ = - \log  p_{\theta} \left( \mathbf{x}_{0} \right) + \mathbb{E}_{q} \left[ \log  \frac{q \left( \mathbf{x}_{1 : T} \mid  \mathbf{x}_{0} \right)}{p_{\theta} \left( \mathbf{x}_{0 : T} \right)} + \log  p_{\theta} \left( \mathbf{x}_{0} \right) \left]\right. \\ = \mathbb{E}_{q} \left[ \log  \frac{q \left( \mathbf{x}_{1 : T} \mid  \mathbf{x}_{0} \right)}{p_{\theta} \left( \mathbf{x}_{0 : T} \right)} \left]\right. \\ \text{Let } L_{\text{VLB}} & = \mathbb{E}_{q \left( \mathbf{x}_{0 : T} \right)} \left[ \log  \frac{q \left( \mathbf{x}_{1 : T} \mid  \mathbf{x}_{0} \right)}{p_{\theta} \left( \mathbf{x}_{0 : T} \right)} \left]\right. \geq - \mathbb{E}_{q \left( \mathbf{x}_{0} \right)} \log  p_{\theta} \left( \mathbf{x}_{0} \right)
\end{aligned}
$$

It is also straightforward to get the same result using Jensen’s inequality. Say we want to minimize the cross entropy as the learning objective,

$$
\begin{aligned}
L_{\text{CE}} & = - \mathbb{E}_{q \left( \mathbf{x}_{0} \right)} \log  p_{\theta} \left( \mathbf{x}_{0} \right) \\ = - \mathbb{E}_{q \left( \mathbf{x}_{0} \right)} \log  \left( \int p_{\theta} \left( \mathbf{x}_{0 : T} \right) d \mathbf{x}_{1 : T} \right) \\ = - \mathbb{E}_{q \left( \mathbf{x}_{0} \right)} \log  \left( \int q \left( \mathbf{x}_{1 : T} \mid  \mathbf{x}_{0} \right) \frac{p_{\theta} \left( \mathbf{x}_{0 : T} \right)}{q \left( \mathbf{x}_{1 : T} \mid  \mathbf{x}_{0} \right)} d \mathbf{x}_{1 : T} \right) \\ = - \mathbb{E}_{q \left( \mathbf{x}_{0} \right)} \log  \left( \mathbb{E}_{q \left( \mathbf{x}_{1 : T} \mid  \mathbf{x}_{0} \right)} \frac{p_{\theta} \left( \mathbf{x}_{0 : T} \right)}{q \left( \mathbf{x}_{1 : T} \mid  \mathbf{x}_{0} \right)} \right) \\ \leq - \mathbb{E}_{q \left( \mathbf{x}_{0 : T} \right)} \log  \frac{p_{\theta} \left( \mathbf{x}_{0 : T} \right)}{q \left( \mathbf{x}_{1 : T} \mid  \mathbf{x}_{0} \right)} \\ = \mathbb{E}_{q \left( \mathbf{x}_{0 : T} \right)} \left[ \log  \frac{q \left( \mathbf{x}_{1 : T} \mid  \mathbf{x}_{0} \right)}{p_{\theta} \left( \mathbf{x}_{0 : T} \right)} \left]\right. = L_{\text{VLB}}
\end{aligned}
$$

To convert each term in the equation to be analytically computable, the objective can be further rewritten to be a combination of several KL-divergence and entropy terms (See the detailed step-by-step process in Appendix B in [Sohl-Dickstein et al., 2015](https://arxiv.org/abs/1503.03585)):

$$
\begin{aligned}
L_{\text{VLB}} & = \mathbb{E}_{q \left( \mathbf{x}_{0 : T} \right)} \left[ \log  \frac{q \left( \mathbf{x}_{1 : T} \mid  \mathbf{x}_{0} \right)}{p_{\theta} \left( \mathbf{x}_{0 : T} \right)} \left]\right. \\ = \mathbb{E}_{q} \left[ \log  \frac{\prod_{t = 1}^{T} q \left( \mathbf{x}_{t} \mid  \mathbf{x}_{t - 1} \right)}{p_{\theta} \left( \mathbf{x}_{T} \right) \prod_{t = 1}^{T} p_{\theta} \left( \mathbf{x}_{t - 1} \mid  \mathbf{x}_{t} \right)} \left]\right. \\ = \mathbb{E}_{q} \left[ - \log  p_{\theta} \left( \mathbf{x}_{T} \right) + \sum_{t = 1}^{T} \log  \frac{q \left( \mathbf{x}_{t} \mid  \mathbf{x}_{t - 1} \right)}{p_{\theta} \left( \mathbf{x}_{t - 1} \mid  \mathbf{x}_{t} \right)} \left]\right. \\ = \mathbb{E}_{q} \left[ - \log  p_{\theta} \left( \mathbf{x}_{T} \right) + \sum_{t = 2}^{T} \log  \frac{q \left( \mathbf{x}_{t} \mid  \mathbf{x}_{t - 1} \right)}{p_{\theta} \left( \mathbf{x}_{t - 1} \mid  \mathbf{x}_{t} \right)} + \log  \frac{q \left( \mathbf{x}_{1} \mid  \mathbf{x}_{0} \right)}{p_{\theta} \left( \mathbf{x}_{0} \mid  \mathbf{x}_{1} \right)} \left]\right. \\ = \mathbb{E}_{q} \left[ - \log  p_{\theta} \left( \mathbf{x}_{T} \right) + \sum_{t = 2}^{T} \log  \left( \frac{q \left( \mathbf{x}_{t - 1} \mid  \mathbf{x}_{t} , \mathbf{x}_{0} \right)}{p_{\theta} \left( \mathbf{x}_{t - 1} \mid  \mathbf{x}_{t} \right)} \cdot \frac{q \left( \mathbf{x}_{t} \mid  \mathbf{x}_{0} \right)}{q \left( \mathbf{x}_{t - 1} \mid  \mathbf{x}_{0} \right)} \right) + \log  \frac{q \left( \mathbf{x}_{1} \mid  \mathbf{x}_{0} \right)}{p_{\theta} \left( \mathbf{x}_{0} \mid  \mathbf{x}_{1} \right)} \left]\right. \\ = \mathbb{E}_{q} \left[ - \log  p_{\theta} \left( \mathbf{x}_{T} \right) + \sum_{t = 2}^{T} \log  \frac{q \left( \mathbf{x}_{t - 1} \mid  \mathbf{x}_{t} , \mathbf{x}_{0} \right)}{p_{\theta} \left( \mathbf{x}_{t - 1} \mid  \mathbf{x}_{t} \right)} + \sum_{t = 2}^{T} \log  \frac{q \left( \mathbf{x}_{t} \mid  \mathbf{x}_{0} \right)}{q \left( \mathbf{x}_{t - 1} \mid  \mathbf{x}_{0} \right)} + \log  \frac{q \left( \mathbf{x}_{1} \mid  \mathbf{x}_{0} \right)}{p_{\theta} \left( \mathbf{x}_{0} \mid  \mathbf{x}_{1} \right)} \left]\right. \\ = \mathbb{E}_{q} \left[ - \log  p_{\theta} \left( \mathbf{x}_{T} \right) + \sum_{t = 2}^{T} \log  \frac{q \left( \mathbf{x}_{t - 1} \mid  \mathbf{x}_{t} , \mathbf{x}_{0} \right)}{p_{\theta} \left( \mathbf{x}_{t - 1} \mid  \mathbf{x}_{t} \right)} + \log  \frac{q \left( \mathbf{x}_{T} \mid  \mathbf{x}_{0} \right)}{q \left( \mathbf{x}_{1} \mid  \mathbf{x}_{0} \right)} + \log  \frac{q \left( \mathbf{x}_{1} \mid  \mathbf{x}_{0} \right)}{p_{\theta} \left( \mathbf{x}_{0} \mid  \mathbf{x}_{1} \right)} \left]\right. \\ = \mathbb{E}_{q} \left[ \log  \frac{q \left( \mathbf{x}_{T} \mid  \mathbf{x}_{0} \right)}{p_{\theta} \left( \mathbf{x}_{T} \right)} + \sum_{t = 2}^{T} \log  \frac{q \left( \mathbf{x}_{t - 1} \mid  \mathbf{x}_{t} , \mathbf{x}_{0} \right)}{p_{\theta} \left( \mathbf{x}_{t - 1} \mid  \mathbf{x}_{t} \right)} - \log  p_{\theta} \left( \mathbf{x}_{0} \mid  \mathbf{x}_{1} \right) \left]\right. \\ = \mathbb{E}_{q} \left[ \underset{L_{T}}{\underbrace{D_{\text{KL}} \left( q \left( \mathbf{x}_{T} \mid  \mathbf{x}_{0} \right) \parallel p_{\theta} \left( \mathbf{x}_{T} \right) \right)}} + \sum_{t = 2}^{T} \underset{L_{t - 1}}{\underbrace{D_{\text{KL}} \left( q \left( \mathbf{x}_{t - 1} \mid  \mathbf{x}_{t} , \mathbf{x}_{0} \right) \parallel p_{\theta} \left( \mathbf{x}_{t - 1} \mid  \mathbf{x}_{t} \right) \right)}} \underset{L_{0}}{\underbrace{- \log  p_{\theta} \left( \mathbf{x}_{0} \mid  \mathbf{x}_{1} \right)}} \left]\right.
\end{aligned}
$$

Let’s label each component in the variational lower bound loss separately:

$$
\begin{aligned}
L_{\text{VLB}} & = L_{T} + L_{T - 1} + \hdots + L_{0} \\ \text{where } L_{T} & = D_{\text{KL}} \left( q \left( \mathbf{x}_{T} \mid  \mathbf{x}_{0} \right) \parallel p_{\theta} \left( \mathbf{x}_{T} \right) \right) \\ L_{t} & = D_{\text{KL}} \left( q \left( \mathbf{x}_{t} \mid  \mathbf{x}_{t + 1} , \mathbf{x}_{0} \right) \parallel p_{\theta} \left( \mathbf{x}_{t} \mid  \mathbf{x}_{t + 1} \right) \right) \text{for } 1 \leq t \leq T - 1 \\ L_{0} & = - \log  p_{\theta} \left( \mathbf{x}_{0} \mid  \mathbf{x}_{1} \right)
\end{aligned}
$$

Every KL term in $L_{\text{VLB}}$ (except for $L_{0}$) compares two Gaussian distributions and therefore they can be computed in [closed form](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence#Multivariate_normal_distributions). $L_{T}$ is constant and can be ignored during training because $q$ has no learnable parameters and $\mathbf{x}_{T}$ is a Gaussian noise. [Ho et al. 2020](https://arxiv.org/abs/2006.11239) models $L_{0}$ using a separate discrete decoder derived from $\mathcal{N} \left(\right. \mathbf{x}_{0} ; \mathbf{\mathit{\mu}}_{\theta} \left(\right. \mathbf{x}_{1} , 1 \left.\right) , \mathbf{\Sigma}_{\theta} \left(\right. \mathbf{x}_{1} , 1 \left.\right) \left.\right)$.

## Parameterization of Lt for Training Loss

Recall that we need to learn a neural network to approximate the conditioned probability distributions in the reverse diffusion process, $p_{\theta} \left(\right. \mathbf{x}_{t - 1} \left|\right. \mathbf{x}_{t} \left.\right) = \mathcal{N} \left(\right. \mathbf{x}_{t - 1} ; \mathbf{\mathit{\mu}}_{\theta} \left(\right. \mathbf{x}_{t} , t \left.\right) , \mathbf{\Sigma}_{\theta} \left(\right. \mathbf{x}_{t} , t \left.\right) \left.\right)$. We would like to train $\mathbf{\mathit{\mu}}_{\theta}$ to predict $\overset{\sim}{\mathbf{\mathit{\mu}}}_{t} = \frac{1}{\sqrt{\alpha_{t}}} \left(\right. \mathbf{x}_{t} - \frac{1 - \alpha_{t}}{\sqrt{1 - \bar{\alpha}_{t}}} \mathbf{\mathit{\epsilon}}_{t} \left.\right)$. Because $\mathbf{x}_{t}$ is available as input at training time, we can reparameterize the Gaussian noise term instead to make it predict $\mathbf{\mathit{\epsilon}}_{t}$ from the input $\mathbf{x}_{t}$ at time step $t$:

$$
\begin{aligned}
\mathbf{\mathit{\mu}}_{\theta} \left( \mathbf{x}_{t} , t \right) & = \frac{1}{\sqrt{\alpha_{t}}} \left( \mathbf{x}_{t} - \frac{1 - \alpha_{t}}{\sqrt{1 - \bar{\alpha}_{t}}} \mathbf{\mathit{\epsilon}}_{\theta} \left( \mathbf{x}_{t} , t \right) \right) \\ \text{Thus } \mathbf{x}_{t - 1} & = \mathcal{N} \left( \mathbf{x}_{t - 1} ; \frac{1}{\sqrt{\alpha_{t}}} \left( \mathbf{x}_{t} - \frac{1 - \alpha_{t}}{\sqrt{1 - \bar{\alpha}_{t}}} \mathbf{\mathit{\epsilon}}_{\theta} \left( \mathbf{x}_{t} , t \right) \right) , \mathbf{\Sigma}_{\theta} \left( \mathbf{x}_{t} , t \right) \right)
\end{aligned}
$$

The loss term $L_{t}$ is parameterized to minimize the difference from $\overset{\sim}{\mathbf{\mathit{\mu}}}$:

$$
\begin{aligned}
L_{t} & = \mathbb{E}_{\mathbf{x}_{0} , \mathbf{\mathit{\epsilon}}} \left[ \frac{1}{2 \parallel \mathbf{\Sigma}_{\theta} \left( \mathbf{x}_{t} , t \right) \parallel_{2}^{2}} \parallel \overset{\sim}{\mathbf{\mathit{\mu}}}_{t} \left( \mathbf{x}_{t} , \mathbf{x}_{0} \right) - \mathbf{\mathit{\mu}}_{\theta} \left( \mathbf{x}_{t} , t \right) \parallel^{2} \left]\right. \\ = \mathbb{E}_{\mathbf{x}_{0} , \mathbf{\mathit{\epsilon}}} \left[ \frac{1}{2 \parallel \mathbf{\Sigma}_{\theta} \parallel_{2}^{2}} \parallel \frac{1}{\sqrt{\alpha_{t}}} \left( \mathbf{x}_{t} - \frac{1 - \alpha_{t}}{\sqrt{1 - \bar{\alpha}_{t}}} \mathbf{\mathit{\epsilon}}_{t} \right) - \frac{1}{\sqrt{\alpha_{t}}} \left( \mathbf{x}_{t} - \frac{1 - \alpha_{t}}{\sqrt{1 - \bar{\alpha}_{t}}} \mathbf{\mathit{\epsilon}}_{\theta} \left( \mathbf{x}_{t} , t \right) \right) \parallel^{2} \left]\right. \\ = \mathbb{E}_{\mathbf{x}_{0} , \mathbf{\mathit{\epsilon}}} \left[ \frac{\left( 1 - \alpha_{t} \right)^{2}}{2 \alpha_{t} \left( 1 - \bar{\alpha}_{t} \right) \parallel \mathbf{\Sigma}_{\theta} \parallel_{2}^{2}} \parallel \mathbf{\mathit{\epsilon}}_{t} - \mathbf{\mathit{\epsilon}}_{\theta} \left( \mathbf{x}_{t} , t \right) \parallel^{2} \left]\right. \\ = \mathbb{E}_{\mathbf{x}_{0} , \mathbf{\mathit{\epsilon}}} \left[ \frac{\left( 1 - \alpha_{t} \right)^{2}}{2 \alpha_{t} \left( 1 - \bar{\alpha}_{t} \right) \parallel \mathbf{\Sigma}_{\theta} \parallel_{2}^{2}} \parallel \mathbf{\mathit{\epsilon}}_{t} - \mathbf{\mathit{\epsilon}}_{\theta} \left( \sqrt{\bar{\alpha}_{t}} \mathbf{x}_{0} + \sqrt{1 - \bar{\alpha}_{t}} \mathbf{\mathit{\epsilon}}_{t} , t \right) \parallel^{2} \left]\right.
\end{aligned}
$$

### Simplification

Empirically, [Ho et al. (2020)](https://arxiv.org/abs/2006.11239) found that training the diffusion model works better with a simplified objective that ignores the weighting term:

$$
\begin{aligned}
L_{t}^{\text{simple}} & = \mathbb{E}_{t \sim \left[ 1 , T \left]\right. , \mathbf{x}_{0} , \mathbf{\mathit{\epsilon}}_{t}} \left[ \parallel \mathbf{\mathit{\epsilon}}_{t} - \mathbf{\mathit{\epsilon}}_{\theta} \left( \mathbf{x}_{t} , t \right) \parallel^{2} \left]\right. \\ = \mathbb{E}_{t \sim \left[ 1 , T \left]\right. , \mathbf{x}_{0} , \mathbf{\mathit{\epsilon}}_{t}} \left[ \parallel \mathbf{\mathit{\epsilon}}_{t} - \mathbf{\mathit{\epsilon}}_{\theta} \left( \sqrt{\bar{\alpha}_{t}} \mathbf{x}_{0} + \sqrt{1 - \bar{\alpha}_{t}} \mathbf{\mathit{\epsilon}}_{t} , t \right) \parallel^{2} \left]\right.
\end{aligned}
$$

The final simple objective is:

$$
L_{\text{simple}} = L_{t}^{\text{simple}} + C
$$

where $C$ is a constant not depending on $\theta$.

![](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/DDPM-algo.png)

The training and sampling algorithms in DDPM (Image source: Ho et al. 2020 )

### Connection with noise-conditioned score networks (NCSN)

[Song & Ermon (2019)](https://arxiv.org/abs/1907.05600) proposed a score-based generative modeling method where samples are produced via [Langevin dynamics](#connection-with-stochastic-gradient-langevin-dynamics) using gradients of the data distribution estimated with score matching. The score of each sample $\mathbf{x}$ ’s density probability is defined as its gradient $\nabla_{\mathbf{x}} log ⁡ q \left(\right. \mathbf{x} \left.\right)$. A score network $\mathbf{s}_{\theta} : \mathbb{R}^{D} \rightarrow \mathbb{R}^{D}$ is trained to estimate it, $\mathbf{s}_{\theta} \left(\right. \mathbf{x} \left.\right) \approx \nabla_{\mathbf{x}} log ⁡ q \left(\right. \mathbf{x} \left.\right)$.

To make it scalable with high-dimensional data in the deep learning setting, they proposed to use either *denoising score matching* ([Vincent, 2011](http://www.iro.umontreal.ca/~vincentp/Publications/smdae_techreport.pdf)) or *sliced score matching* (use random projections; [Song et al., 2019](https://arxiv.org/abs/1905.07088)). Denosing score matching adds a pre-specified small noise to the data $q \left(\right. \overset{\sim}{\mathbf{x}} \left|\right. \mathbf{x} \left.\right)$ and estimates $q \left(\right. \overset{\sim}{\mathbf{x}} \left.\right)$ with score matching.

Recall that Langevin dynamics can sample data points from a probability density distribution using only the score $\nabla_{\mathbf{x}} log ⁡ q \left(\right. \mathbf{x} \left.\right)$ in an iterative process.

However, according to the manifold hypothesis, most of the data is expected to concentrate in a low dimensional manifold, even though the observed data might look only arbitrarily high-dimensional. It brings a negative effect on score estimation since the data points cannot cover the whole space. In regions where data density is low, the score estimation is less reliable. After adding a small Gaussian noise to make the perturbed data distribution cover the full space $\mathbb{R}^{D}$, the training of the score estimator network becomes more stable. [Song & Ermon (2019)](https://arxiv.org/abs/1907.05600) improved it by perturbing the data with the noise of *different levels* and train a noise-conditioned score network to *jointly* estimate the scores of all the perturbed data at different noise levels.

The schedule of increasing noise levels resembles the forward diffusion process. If we use the diffusion process annotation, the score approximates $\mathbf{s}_{\theta} \left(\right. \mathbf{x}_{t} , t \left.\right) \approx \nabla_{\mathbf{x}_{t}} log ⁡ q \left(\right. \mathbf{x}_{t} \left.\right)$. Given a Gaussian distribution $\mathbf{x} sim \mathcal{N} \left(\right. \mu , \sigma^{2} \mathbf{I} \left.\right)$, we can write the derivative of the logarithm of its density function as $\nabla_{\mathbf{x}} log ⁡ p \left(\right. \mathbf{x} \left.\right) = \nabla_{\mathbf{x}} \left(\right. - \frac{1}{2 \sigma^{2}} \left(\right. \mathbf{x} - \mathbf{\mathit{\mu}} \left.\right)^{2} \left.\right) = - \frac{\mathbf{x} - \mathbf{\mathit{\mu}}}{\sigma^{2}} = - \frac{\mathbf{\mathit{\epsilon}}}{\sigma}$ where $\mathbf{\mathit{\epsilon}} sim \mathcal{N} \left(\right. 0 , \mathbf{I} \left.\right)$. [Recall](#nice) that $q \left(\right. \mathbf{x}_{t} \left|\right. \mathbf{x}_{0} \left.\right) sim \mathcal{N} \left(\right. \sqrt{\bar{\alpha}_{t}} \mathbf{x}_{0} , \left(\right. 1 - \bar{\alpha}_{t} \left.\right) \mathbf{I} \left.\right)$ and therefore,

$$
\mathbf{s}_{\theta} \left( \mathbf{x}_{t} , t \right) \approx \nabla_{\mathbf{x}_{t}} \log  q \left( \mathbf{x}_{t} \right) = \mathbb{E}_{q \left( \mathbf{x}_{0} \right)} \left[ \nabla_{\mathbf{x}_{t}} \log  q \left( \mathbf{x}_{t} \mid  \mathbf{x}_{0} \right) \left]\right. = \mathbb{E}_{q \left( \mathbf{x}_{0} \right)} \left[ - \frac{\mathbf{\mathit{\epsilon}}_{\theta} \left( \mathbf{x}_{t} , t \right)}{\sqrt{1 - \bar{\alpha}_{t}}} \left]\right. = - \frac{\mathbf{\mathit{\epsilon}}_{\theta} \left( \mathbf{x}_{t} , t \right)}{\sqrt{1 - \bar{\alpha}_{t}}}
$$

## Parameterization of βt

The forward variances are set to be a sequence of linearly increasing constants in [Ho et al. (2020)](https://arxiv.org/abs/2006.11239), from $\beta_{1} = 10^{- 4}$ to $\beta_{T} = 0.02$. They are relatively small compared to the normalized image pixel values between $\left[\right. - 1 , 1 \left]\right.$. Diffusion models in their experiments showed high-quality samples but still could not achieve competitive model log-likelihood as other generative models.

[Nichol & Dhariwal (2021)](https://arxiv.org/abs/2102.09672) proposed several improvement techniques to help diffusion models to obtain lower NLL. One of the improvements is to use a cosine-based variance schedule. The choice of the scheduling function can be arbitrary, as long as it provides a near-linear drop in the middle of the training process and subtle changes around $t = 0$ and $t = T$.

$$
\beta_{t} = \text{clip} \left( 1 - \frac{\bar{\alpha}_{t}}{\bar{\alpha}_{t - 1}} , 0.999 \right) \bar{\alpha}_{t} = \frac{f \left( t \right)}{f \left( 0 \right)} \text{where } f \left( t \right) = \cos  \left( \frac{t / T + s}{1 + s} \cdot \frac{\pi}{2} \right)^{2}
$$

where the small offset $s$ is to prevent $\beta_{t}$ from being too small when close to $t = 0$.

![](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/diffusion-beta.png)

Comparison of linear and cosine-based scheduling of β \_ t during training. (Image source: Nichol & Dhariwal, 2021 )

## Parameterization of reverse process variance Σθ

[Ho et al. (2020)](https://arxiv.org/abs/2006.11239) chose to fix $\beta_{t}$ as constants instead of making them learnable and set $\mathbf{\Sigma}_{\theta} \left(\right. \mathbf{x}_{t} , t \left.\right) = \sigma_{t}^{2} \mathbf{I}$, where $\sigma_{t}$ is not learned but set to $\beta_{t}$ or $\overset{\sim}{\beta}_{t} = \frac{1 - \bar{\alpha}_{t - 1}}{1 - \bar{\alpha}_{t}} \cdot \beta_{t}$. Because they found that learning a diagonal variance $\mathbf{\Sigma}_{\theta}$ leads to unstable training and poorer sample quality.

[Nichol & Dhariwal (2021)](https://arxiv.org/abs/2102.09672) proposed to learn $\mathbf{\Sigma}_{\theta} \left(\right. \mathbf{x}_{t} , t \left.\right)$ as an interpolation between $\beta_{t}$ and $\overset{\sim}{\beta}_{t}$ by model predicting a mixing vector $\mathbf{v}$:

$$
\mathbf{\Sigma}_{\theta} \left( \mathbf{x}_{t} , t \right) = \exp  \left( \mathbf{v} \log  \beta_{t} + \left( 1 - \mathbf{v} \right) \log  \overset{\sim}{\beta}_{t} \right)
$$

However, the simple objective $L_{\text{simple}}$ does not depend on $\mathbf{\Sigma}_{\theta}$. To add the dependency, they constructed a hybrid objective $L_{\text{hybrid}} = L_{\text{simple}} + \lambda L_{\text{VLB}}$ where $\lambda = 0.001$ is small and stop gradient on $\mathbf{\mathit{\mu}}_{\theta}$ in the $L_{\text{VLB}}$ term such that $L_{\text{VLB}}$ only guides the learning of $\mathbf{\Sigma}_{\theta}$. Empirically they observed that $L_{\text{VLB}}$ is pretty challenging to optimize likely due to noisy gradients, so they proposed to use a time-averaging smoothed version of $L_{\text{VLB}}$ with importance sampling.

![](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/improved-DDPM-nll.png)

Comparison of negative log-likelihood of improved DDPM with other likelihood-based generative models. NLL is reported in the unit of bits/dim. (Image source: Nichol & Dhariwal, 2021 )

## Conditioned Generation

While training generative models on images with conditioning information such as ImageNet dataset, it is common to generate samples conditioned on class labels or a piece of descriptive text.

## Classifier Guided Diffusion

To explicit incorporate class information into the diffusion process, [Dhariwal & Nichol (2021)](https://arxiv.org/abs/2105.05233) trained a classifier $f_{\phi} \left(\right. y \left|\right. \mathbf{x}_{t} , t \left.\right)$ on noisy image $\mathbf{x}_{t}$ and use gradients $\nabla_{\mathbf{x}} log ⁡ f_{\phi} \left(\right. y \left|\right. \mathbf{x}_{t} \left.\right)$ to guide the diffusion sampling process toward the conditioning information $y$ (e.g. a target class label) by altering the noise prediction. [Recall](#score) that $\nabla_{\mathbf{x}_{t}} log ⁡ q \left(\right. \mathbf{x}_{t} \left.\right) = - \frac{1}{\sqrt{1 - \bar{\alpha}_{t}}} \mathbf{\mathit{\epsilon}}_{\theta} \left(\right. \mathbf{x}_{t} , t \left.\right)$ and we can write the score function for the joint distribution $q \left(\right. \mathbf{x}_{t} , y \left.\right)$ as following,

$$
\begin{aligned}
\nabla_{\mathbf{x}_{t}} \log  q \left( \mathbf{x}_{t} , y \right) & = \nabla_{\mathbf{x}_{t}} \log  q \left( \mathbf{x}_{t} \right) + \nabla_{\mathbf{x}_{t}} \log  q \left( y \mid  \mathbf{x}_{t} \right) \\ \approx - \frac{1}{\sqrt{1 - \bar{\alpha}_{t}}} \mathbf{\mathit{\epsilon}}_{\theta} \left( \mathbf{x}_{t} , t \right) + \nabla_{\mathbf{x}_{t}} \log  f_{\phi} \left( y \mid  \mathbf{x}_{t} \right) \\ = - \frac{1}{\sqrt{1 - \bar{\alpha}_{t}}} \left( \mathbf{\mathit{\epsilon}}_{\theta} \left( \mathbf{x}_{t} , t \right) - \sqrt{1 - \bar{\alpha}_{t}} \nabla_{\mathbf{x}_{t}} \log  f_{\phi} \left( y \mid  \mathbf{x}_{t} \right) \right)
\end{aligned}
$$

Thus, a new classifier-guided predictor $\bar{\mathbf{\mathit{\epsilon}}}_{\theta}$ would take the form as following,

$$
\bar{\mathbf{\mathit{\epsilon}}}_{\theta} \left( \mathbf{x}_{t} , t \right) = \mathbf{\mathit{\epsilon}}_{\theta} \left( x_{t} , t \right) - \sqrt{1 - \bar{\alpha}_{t}} \nabla_{\mathbf{x}_{t}} \log  f_{\phi} \left( y \mid  \mathbf{x}_{t} \right)
$$

To control the strength of the classifier guidance, we can add a weight $w$ to the delta part,

$$
\bar{\mathbf{\mathit{\epsilon}}}_{\theta} \left( \mathbf{x}_{t} , t \right) = \mathbf{\mathit{\epsilon}}_{\theta} \left( x_{t} , t \right) - \sqrt{1 - \bar{\alpha}_{t}} w \nabla_{\mathbf{x}_{t}} \log  f_{\phi} \left( y \mid  \mathbf{x}_{t} \right)
$$

The resulting *ablated diffusion model* (**ADM**) and the one with additional classifier guidance (**ADM-G**) are able to achieve better results than SOTA generative models (e.g. BigGAN).

![](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/conditioned-DDPM.png)

The algorithms use guidance from a classifier to run conditioned generation with DDPM and DDIM. (Image source: Dhariwal & Nichol, 2021 \])

Additionally with some modifications on the U-Net architecture, [Dhariwal & Nichol (2021)](https://arxiv.org/abs/2105.05233) showed performance better than GAN with diffusion models. The architecture modifications include larger model depth/width, more attention heads, multi-resolution attention, BigGAN residual blocks for up/downsampling, residual connection rescale by $1 / \sqrt{2}$ and adaptive group normalization (AdaGN).

## Classifier-Free Guidance

Without an independent classifier $f_{\phi}$, it is still possible to run conditional diffusion steps by incorporating the scores from a conditional and an unconditional diffusion model ([Ho & Salimans, 2021](https://openreview.net/forum?id=qw8AKxfYbI)). Let unconditional denoising diffusion model $p_{\theta} \left(\right. \mathbf{x} \left.\right)$ parameterized through a score estimator $\mathbf{\mathit{\epsilon}}_{\theta} \left(\right. \mathbf{x}_{t} , t \left.\right)$ and the conditional model $p_{\theta} \left(\right. \mathbf{x} \left|\right. y \left.\right)$ parameterized through $\mathbf{\mathit{\epsilon}}_{\theta} \left(\right. \mathbf{x}_{t} , t , y \left.\right)$. These two models can be learned via a single neural network. Precisely, a conditional diffusion model $p_{\theta} \left(\right. \mathbf{x} \left|\right. y \left.\right)$ is trained on paired data $\left(\right. \mathbf{x} , y \left.\right)$, where the conditioning information $y$ gets discarded periodically at random such that the model knows how to generate images unconditionally as well, i.e. $\mathbf{\mathit{\epsilon}}_{\theta} \left(\right. \mathbf{x}_{t} , t \left.\right) = \mathbf{\mathit{\epsilon}}_{\theta} \left(\right. \mathbf{x}_{t} , t , y = \emptyset \left.\right)$.

The gradient of an implicit classifier can be represented with conditional and unconditional score estimators. Once plugged into the classifier-guided modified score, the score contains no dependency on a separate classifier.

$$
\begin{aligned}
\nabla_{\mathbf{x}_{t}} \log  p \left( y \mid  \mathbf{x}_{t} \right) & = \nabla_{\mathbf{x}_{t}} \log  p \left( \mathbf{x}_{t} \mid  y \right) - \nabla_{\mathbf{x}_{t}} \log  p \left( \mathbf{x}_{t} \right) \\ = - \frac{1}{\sqrt{1 - \bar{\alpha}_{t}}} \left( \mathbf{\mathit{\epsilon}}_{\theta} \left( \mathbf{x}_{t} , t , y \right) - \mathbf{\mathit{\epsilon}}_{\theta} \left( \mathbf{x}_{t} , t \right) \right) \\ \bar{\mathbf{\mathit{\epsilon}}}_{\theta} \left( \mathbf{x}_{t} , t , y \right) & = \mathbf{\mathit{\epsilon}}_{\theta} \left( \mathbf{x}_{t} , t , y \right) - \sqrt{1 - \bar{\alpha}_{t}} w \nabla_{\mathbf{x}_{t}} \log  p \left( y \mid  \mathbf{x}_{t} \right) \\ = \mathbf{\mathit{\epsilon}}_{\theta} \left( \mathbf{x}_{t} , t , y \right) + w \left( \mathbf{\mathit{\epsilon}}_{\theta} \left( \mathbf{x}_{t} , t , y \right) - \mathbf{\mathit{\epsilon}}_{\theta} \left( \mathbf{x}_{t} , t \right) \right) \\ = \left( w + 1 \right) \mathbf{\mathit{\epsilon}}_{\theta} \left( \mathbf{x}_{t} , t , y \right) - w \mathbf{\mathit{\epsilon}}_{\theta} \left( \mathbf{x}_{t} , t \right)
\end{aligned}
$$

Their experiments showed that classifier-free guidance can achieve a good balance between FID (distinguish between synthetic and generated images) and IS (quality and diversity).

The guided diffusion model, GLIDE ([Nichol, Dhariwal & Ramesh, et al. 2022](https://arxiv.org/abs/2112.10741)), explored both guiding strategies, CLIP guidance and classifier-free guidance, and found that the latter is more preferred. They hypothesized that it is because CLIP guidance exploits the model with adversarial examples towards the CLIP model, rather than optimize the better matched images generation.

## Speed up Diffusion Models

It is very slow to generate a sample from DDPM by following the Markov chain of the reverse diffusion process, as $T$ can be up to one or a few thousand steps. One data point from [Song et al. (2020)](https://arxiv.org/abs/2010.02502): “For example, it takes around 20 hours to sample 50k images of size 32 × 32 from a DDPM, but less than a minute to do so from a GAN on an Nvidia 2080 Ti GPU.”

## Fewer Sampling Steps & Distillation

One simple way is to run a strided sampling schedule ([Nichol & Dhariwal, 2021](https://arxiv.org/abs/2102.09672)) by taking the sampling update every $\lceil T / S \rceil$ steps to reduce the process from $T$ to $S$ steps. The new sampling schedule for generation is $\left{\right. \tau_{1} , \ldots , \tau_{S} \left.\right}$ where $\tau_{1} < \tau_{2} < \hdots < \tau_{S} \in \left[\right. 1 , T \left]\right.$ and $S < T$.

For another approach, let’s rewrite $q_{\sigma} \left(\right. \mathbf{x}_{t - 1} \left|\right. \mathbf{x}_{t} , \mathbf{x}_{0} \left.\right)$ to be parameterized by a desired standard deviation $\sigma_{t}$ according to the [nice property](#nice):

$$
\begin{aligned}
\mathbf{x}_{t - 1} & = \sqrt{\bar{\alpha}_{t - 1}} \mathbf{x}_{0} + \sqrt{1 - \bar{\alpha}_{t - 1}} \mathbf{\mathit{\epsilon}}_{t - 1} \\ = \sqrt{\bar{\alpha}_{t - 1}} \mathbf{x}_{0} + \sqrt{1 - \bar{\alpha}_{t - 1} - \sigma_{t}^{2}} \mathbf{\mathit{\epsilon}}_{t} + \sigma_{t} \mathbf{\mathit{\epsilon}} \\ = \sqrt{\bar{\alpha}_{t - 1}} \left( \frac{\mathbf{x}_{t} - \sqrt{1 - \bar{\alpha}_{t}} \epsilon_{\theta}^{\left( t \right)} \left( \mathbf{x}_{t} \right)}{\sqrt{\bar{\alpha}_{t}}} \right) + \sqrt{1 - \bar{\alpha}_{t - 1} - \sigma_{t}^{2}} \epsilon_{\theta}^{\left( t \right)} \left( \mathbf{x}_{t} \right) + \sigma_{t} \mathbf{\mathit{\epsilon}} \\ q_{\sigma} \left( \mathbf{x}_{t - 1} \mid  \mathbf{x}_{t} , \mathbf{x}_{0} \right) & = \mathcal{N} \left( \mathbf{x}_{t - 1} ; \sqrt{\bar{\alpha}_{t - 1}} \left( \frac{\mathbf{x}_{t} - \sqrt{1 - \bar{\alpha}_{t}} \epsilon_{\theta}^{\left( t \right)} \left( \mathbf{x}_{t} \right)}{\sqrt{\bar{\alpha}_{t}}} \right) + \sqrt{1 - \bar{\alpha}_{t - 1} - \sigma_{t}^{2}} \epsilon_{\theta}^{\left( t \right)} \left( \mathbf{x}_{t} \right) , \sigma_{t}^{2} \mathbf{I} \right)
\end{aligned}
$$

where the model $\epsilon_{\theta}^{\left(\right. t \left.\right)} \left(\right. . \left.\right)$ predicts the $\epsilon_{t}$ from $\mathbf{x}_{t}$.

Recall that in $q \left(\right. \mathbf{x}_{t - 1} \left|\right. \mathbf{x}_{t} , \mathbf{x}_{0} \left.\right) = \mathcal{N} \left(\right. \mathbf{x}_{t - 1} ; \overset{\sim}{\mathbf{\mathit{\mu}}} \left(\right. \mathbf{x}_{t} , \mathbf{x}_{0} \left.\right) , \overset{\sim}{\beta}_{t} \mathbf{I} \left.\right)$, therefore we have:

$$
\overset{\sim}{\beta}_{t} = \sigma_{t}^{2} = \frac{1 - \bar{\alpha}_{t - 1}}{1 - \bar{\alpha}_{t}} \cdot \beta_{t}
$$

Let $\sigma_{t}^{2} = \eta \cdot \overset{\sim}{\beta}_{t}$ such that we can adjust $\eta \in \mathbb{R}^{+}$ as a hyperparameter to control the sampling stochasticity. The special case of $\eta = 0$ makes the sampling process *deterministic*. Such a model is named the *denoising diffusion implicit model* (**DDIM**; [Song et al., 2020](https://arxiv.org/abs/2010.02502)). DDIM has the same marginal noise distribution but deterministically maps noise back to the original data samples.

During generation, we don’t have to follow the whole chain $t = 1 , \ldots , T$, but rather a subset of steps. Let’s denote $s < t$ as two steps in this accelerated trajectory. The DDIM update step is:

$$
q_{\sigma , s < t} \left( \mathbf{x}_{s} \mid  \mathbf{x}_{t} , \mathbf{x}_{0} \right) = \mathcal{N} \left( \mathbf{x}_{s} ; \sqrt{\bar{\alpha}_{s}} \left( \frac{\mathbf{x}_{t} - \sqrt{1 - \bar{\alpha}_{t}} \epsilon_{\theta}^{\left( t \right)} \left( \mathbf{x}_{t} \right)}{\sqrt{\bar{\alpha}_{t}}} \right) + \sqrt{1 - \bar{\alpha}_{s} - \sigma_{t}^{2}} \epsilon_{\theta}^{\left( t \right)} \left( \mathbf{x}_{t} \right) , \sigma_{t}^{2} \mathbf{I} \right)
$$

While all the models are trained with $T = 1000$ diffusion steps in the experiments, they observed that DDIM ($\eta = 0$) can produce the best quality samples when $S$ is small, while DDPM ($\eta = 1$) performs much worse on small $S$. DDPM does perform better when we can afford to run the full reverse Markov diffusion steps ($S = T = 1000$). With DDIM, it is possible to train the diffusion model up to any arbitrary number of forward steps but only sample from a subset of steps in the generative process.

![](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/DDIM-results.png)

FID scores on CIFAR10 and CelebA datasets by diffusion models of different settings, including DDIM ( η = 0 ) and DDPM σ ^ ). (Image source: Song et al., 2020 )

Compared to DDPM, DDIM is able to:

1. Generate higher-quality samples using a much fewer number of steps.
2. Have “consistency” property since the generative process is deterministic, meaning that multiple samples conditioned on the same latent variable should have similar high-level features.
3. Because of the consistency, DDIM can do semantically meaningful interpolation in the latent variable.
![](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/progressive-distillation.png)

Progressive distillation can reduce the diffusion sampling steps by half in each iteration. (Image source: Salimans & Ho, 2022 )

**Progressive Distillation** ([Salimans & Ho, 2022](https://arxiv.org/abs/2202.00512)) is a method for distilling trained deterministic samplers into new models of halved sampling steps. The student model is initialized from the teacher model and denoises towards a target where one student DDIM step matches 2 teacher steps, instead of using the original sample $\mathbf{x}_{0}$ as the denoise target. In every progressive distillation iteration, we can half the sampling steps.

![](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/progressive-distillation-algo.png)

Comparison of Algorithm 1 (diffusion model training) and Algorithm 2 (progressive distillation) side-by-side, where the relative changes in progressive distillation are highlighted in green. (Image source: Salimans & Ho, 2022 )

**Consistency Models** ([Song et al. 2023](https://arxiv.org/abs/2303.01469)) learns to map any intermediate noisy data points $\mathbf{x}_{t} , t > 0$ on the diffusion sampling trajectory back to its origin $\mathbf{x}_{0}$ directly. It is named as *consistency* model because of its *self-consistency* property as any data points on the same trajectory is mapped to the same origin.

![](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/consistency-models.png)

Consistency models learn to map any data point on the trajectory back to its origin. (Image source: Song et al., 2023 )

Given a trajectory $\left{\right. \mathbf{x}_{t} \left|\right. t \in \left[\right. \epsilon , T \left]\right. \left.\right}$, the *consistency function* $f$ is defined as $f : \left(\right. \mathbf{x}_{t} , t \left.\right) \rightarrowtail \mathbf{x}_{\epsilon}$ and the equation $f \left(\right. \mathbf{x}_{t} , t \left.\right) = f \left(\right. \mathbf{x}_{t^{'}} , t^{'} \left.\right) = \mathbf{x}_{\epsilon}$ holds true for all $t , t^{'} \in \left[\right. \epsilon , T \left]\right.$. When $t = \epsilon$, $f$ is an identify function. The model can be parameterized as follows, where $c_{\text{skip}} \left(\right. t \left.\right)$ and $c_{\text{out}} \left(\right. t \left.\right)$ functions are designed in a way that $c_{\text{skip}} \left(\right. \epsilon \left.\right) = 1 , c_{\text{out}} \left(\right. \epsilon \left.\right) = 0$:

$$
f_{\theta} \left( \mathbf{x} , t \right) = c_{\text{skip}} \left( t \right) \mathbf{x} + c_{\text{out}} \left( t \right) F_{\theta} \left( \mathbf{x} , t \right)
$$

It is possible for the consistency model to generate samples in a single step, while still maintaining the flexibility of trading computation for better quality following a multi-step sampling process.

The paper introduced two ways to train consistency models:

1. **Consistency Distillation (CD)**: Distill a diffusion model into a consistency model by minimizing the difference between model outputs for pairs generated out of the same trajectory. This enables a much cheaper sampling evaluation. The consistency distillation loss is:
	$$
\begin{aligned}
\mathcal{L}_{\text{CD}}^{N} \left( \theta , \theta^{-} ; \phi \right) & = \mathbb{E} \left[ \lambda \left( t_{n} \right) d \left( f_{\theta} \left( \mathbf{x}_{t_{n + 1}} , t_{n + 1} \right) , f_{\theta^{-}} \left( \hat{\mathbf{x}}_{t_{n}}^{\phi} , t_{n} \right) \left]\right. \\ \hat{\mathbf{x}}_{t_{n}}^{\phi} & = \mathbf{x}_{t_{n + 1}} - \left( t_{n} - t_{n + 1} \right) \Phi \left( \mathbf{x}_{t_{n + 1}} , t_{n + 1} ; \phi \right)
\end{aligned}
$$
	where
	- $\Phi \left(\right. . ; \phi \left.\right)$ is the update function of a one-step [ODE](https://en.wikipedia.org/wiki/Ordinary_differential_equation) solver;
		- $n sim \mathcal{U} \left[\right. 1 , N - 1 \left]\right.$, has an uniform distribution over $1 , \ldots , N - 1$;
		- The network parameters $\theta^{-}$ is EMA version of $\theta$ which greatly stabilizes the training (just like in [DQN](https://lilianweng.github.io/posts/2018-02-19-rl-overview/#deep-q-network) or [momentum](https://lilianweng.github.io/posts/2021-05-31-contrastive/#moco--moco-v2) contrastive learning);
		- $d \left(\right. . , . \left.\right)$ is a positive distance metric function that satisfies $\forall \mathbf{x} , \mathbf{y} : d \left(\right. \mathbf{x} , \mathbf{y} \left.\right) \geq 0$ and $d \left(\right. \mathbf{x} , \mathbf{y} \left.\right) = 0$ if and only if $\mathbf{x} = \mathbf{y}$ such as $ℓ_{2}$, $ℓ_{1}$ or [LPIPS](https://arxiv.org/abs/1801.03924) (learned perceptual image patch similarity) distance;
		- $\lambda \left(\right. . \left.\right) \in \mathbb{R}^{+}$ is a positive weighting function and the paper sets $\lambda \left(\right. t_{n} \left.\right) = 1$.
2. **Consistency Training (CT)**: The other option is to train a consistency model independently. Note that in CD, a pre-trained score model $s_{\phi} \left(\right. \mathbf{x} , t \left.\right)$ is used to approximate the ground truth score $\nabla log ⁡ p_{t} \left(\right. \mathbf{x} \left.\right)$ but in CT we need a way to estimate this score function and it turns out an unbiased estimator of $\nabla log ⁡ p_{t} \left(\right. \mathbf{x} \left.\right)$ exists as $- \frac{\mathbf{x}_{t} - \mathbf{x}}{t^{2}}$. The CT loss is defined as follows:
$$
\mathcal{L}_{\text{CT}}^{N} \left( \theta , \theta^{-} ; \phi \right) = \mathbb{E} \left[ \lambda \left( t_{n} \right) d \left( f_{\theta} \left( \mathbf{x} + t_{n + 1} \mathbf{z} , t_{n + 1} \right) , f_{\theta^{-}} \left( \mathbf{x} + t_{n} \mathbf{z} , t_{n} \right) \left]\right. \text{where } \mathbf{z} \in \mathcal{N} \left( 0 , \mathbf{I} \right)
$$

According to the experiments in the paper, they found,

- Heun ODE solver works better than Euler’s first-order solver, since higher order ODE solvers have smaller estimation errors with the same $N$.
- Among different options of the distance metric function $d \left(\right. . \left.\right)$, the LPIPS metric works better than $ℓ_{1}$ and $ℓ_{2}$ distance.
- Smaller $N$ leads to faster convergence but worse samples, whereas larger $N$ leads to slower convergence but better samples upon convergence.
![](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/consistency-models-exp.png)

Comparison of consistency models' performance under different configurations. The best configuration for CD is LPIPS distance metric, Heun ODE solver, and N = 18. (Image source: Song et al., 2023 )

## Latent Variable Space

*Latent diffusion model* (**LDM**; [Rombach & Blattmann, et al. 2022](https://arxiv.org/abs/2112.10752)) runs the diffusion process in the latent space instead of pixel space, making training cost lower and inference speed faster. It is motivated by the observation that most bits of an image contribute to perceptual details and the semantic and conceptual composition still remains after aggressive compression. LDM loosely decomposes the perceptual compression and semantic compression with generative modeling learning by first trimming off pixel-level redundancy with autoencoder and then manipulating / generating semantic concepts with diffusion process on learned latent.

![](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/image-distortion-rate.png)

The plot for tradeoff between compression rate and distortion, illustrating two-stage compressions - perceptual and semantic compression. (Image source: Rombach & Blattmann, et al. 2022 )

The perceptual compression process relies on an autoencoder model. An encoder $\mathcal{E}$ is used to compress the input image $\mathbf{x} \in \mathbb{R}^{H \times W \times 3}$ to a smaller 2D latent vector $\mathbf{z} = \mathcal{E} \left(\right. \mathbf{x} \left.\right) \in \mathbb{R}^{h \times w \times c}$, where the downsampling rate $f = H / h = W / w = 2^{m} , m \in \mathbb{N}$. Then an decoder $\mathcal{D}$ reconstructs the images from the latent vector, $\overset{\sim}{\mathbf{x}} = \mathcal{D} \left(\right. \mathbf{z} \left.\right)$. The paper explored two types of regularization in autoencoder training to avoid arbitrarily high-variance in the latent spaces.

- *KL-reg*: A small KL penalty towards a standard normal distribution over the learned latent, similar to [VAE](https://lilianweng.github.io/posts/2018-08-12-vae/).
- *VQ-reg*: Uses a vector quantization layer within the decoder, like [VQVAE](https://lilianweng.github.io/posts/2018-08-12-vae/#vq-vae-and-vq-vae-2) but the quantization layer is absorbed by the decoder.

The diffusion and denoising processes happen on the latent vector $\mathbf{z}$. The denoising model is a time-conditioned U-Net, augmented with the cross-attention mechanism to handle flexible conditioning information for image generation (e.g. class labels, semantic maps, blurred variants of an image). The design is equivalent to fuse representation of different modality into the model with a cross-attention mechanism. Each type of conditioning information is paired with a domain-specific encoder $\tau_{\theta}$ to project the conditioning input $y$ to an intermediate representation that can be mapped into cross-attention component, $\tau_{\theta} \left(\right. y \left.\right) \in \mathbb{R}^{M \times d_{\tau}}$:

$$
\text{Attention} \left( \mathbf{Q} , \mathbf{K} , \mathbf{V} \right) = \text{softmax} \left( \frac{\mathbf{Q} \mathbf{K}^{\top}}{\sqrt{d}} \right) \cdot \mathbf{V} \\ \text{where } \mathbf{Q} = \mathbf{W}_{Q}^{\left( i \right)} \cdot \varphi_{i} \left( \mathbf{z}_{i} \right) , \mathbf{K} = \mathbf{W}_{K}^{\left( i \right)} \cdot \tau_{\theta} \left( y \right) , \mathbf{V} = \mathbf{W}_{V}^{\left( i \right)} \cdot \tau_{\theta} \left( y \right) \\ \text{and } \mathbf{W}_{Q}^{\left( i \right)} \in \mathbb{R}^{d \times d_{\epsilon}^{i}} , \mathbf{W}_{K}^{\left( i \right)} , \mathbf{W}_{V}^{\left( i \right)} \in \mathbb{R}^{d \times d_{\tau}} , \varphi_{i} \left( \mathbf{z}_{i} \right) \in \mathbb{R}^{N \times d_{\epsilon}^{i}} , \tau_{\theta} \left( y \right) \in \mathbb{R}^{M \times d_{\tau}}
$$
![](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/latent-diffusion-arch.png)

The architecture of the latent diffusion model (LDM). (Image source: Rombach & Blattmann, et al. 2022 )

## Scale up Generation Resolution and Quality

To generate high-quality images at high resolution, [Ho et al. (2021)](https://arxiv.org/abs/2106.15282) proposed to use a pipeline of multiple diffusion models at increasing resolutions. *Noise conditioning augmentation* between pipeline models is crucial to the final image quality, which is to apply strong data augmentation to the conditioning input $\mathbf{z}$ of each super-resolution model $p_{\theta} \left(\right. \mathbf{x} \left|\right. \mathbf{z} \left.\right)$. The conditioning noise helps reduce compounding error in the pipeline setup. *U-net* is a common choice of model architecture in diffusion modeling for high-resolution image generation.

![](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/cascaded-diffusion.png)

A cascaded pipeline of multiple diffusion models at increasing resolutions. (Image source: Ho et al. 2021 \])

They found the most effective noise is to apply Gaussian noise at low resolution and Gaussian blur at high resolution. In addition, they also explored two forms of conditioning augmentation that require small modification to the training process. Note that conditioning noise is only applied to training but not at inference.

- Truncated conditioning augmentation stops the diffusion process early at step $t > 0$ for low resolution.
- Non-truncated conditioning augmentation runs the full low resolution reverse process until step 0 but then corrupt it by $\mathbf{z}_{t} sim q \left(\right. \mathbf{x}_{t} \left|\right. \mathbf{x}_{0} \left.\right)$ and then feeds the corrupted $\mathbf{z}_{t}$ s into the super-resolution model.

The two-stage diffusion model **unCLIP** ([Ramesh et al. 2022](https://arxiv.org/abs/2204.06125)) heavily utilizes the CLIP text encoder to produce text-guided images at high quality. Given a pretrained CLIP model $\mathbf{c}$ and paired training data for the diffusion model, $\left(\right. \mathbf{x} , y \left.\right)$, where $x$ is an image and $y$ is the corresponding caption, we can compute the CLIP text and image embedding, $\mathbf{c}^{t} \left(\right. y \left.\right)$ and $\mathbf{c}^{i} \left(\right. \mathbf{x} \left.\right)$, respectively. The unCLIP learns two models in parallel:

- A prior model $P \left(\right. \mathbf{c}^{i} \left|\right. y \left.\right)$: outputs CLIP image embedding $\mathbf{c}^{i}$ given the text $y$.
- A decoder $P \left(\right. \mathbf{x} \left|\right. \mathbf{c}^{i} , \left[\right. y \left]\right. \left.\right)$: generates the image $\mathbf{x}$ given CLIP image embedding $\mathbf{c}^{i}$ and optionally the original text $y$.

These two models enable conditional generation, because

$$
\underset{\mathbf{c}^{i} \text{is deterministic given } \mathbf{x}}{\underbrace{P \left( \mathbf{x} \mid  y \right) = P \left( \mathbf{x} , \mathbf{c}^{i} \mid  y \right)}} = P \left( \mathbf{x} \mid  \mathbf{c}^{i} , y \right) P \left( \mathbf{c}^{i} \mid  y \right)
$$
![](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/unCLIP.png)

The architecture of unCLIP. (Image source: Ramesh et al. 2022 \])

unCLIP follows a two-stage image generation process:

1. Given a text $y$, a CLIP model is first used to generate a text embedding $\mathbf{c}^{t} \left(\right. y \left.\right)$. Using CLIP latent space enables zero-shot image manipulation via text.
2. A diffusion or autoregressive prior $P \left(\right. \mathbf{c}^{i} \left|\right. y \left.\right)$ processes this CLIP text embedding to construct an image prior and then a diffusion decoder $P \left(\right. \mathbf{x} \left|\right. \mathbf{c}^{i} , \left[\right. y \left]\right. \left.\right)$ generates an image, conditioned on the prior. This decoder can also generate image variations conditioned on an image input, preserving its style and semantics.

Instead of CLIP model, **Imagen** ([Saharia et al. 2022](https://arxiv.org/abs/2205.11487)) uses a pre-trained large LM (i.e. a frozen T5-XXL text encoder) to encode text for image generation. There is a general trend that larger model size can lead to better image quality and text-image alignment. They found that T5-XXL and CLIP text encoder achieve similar performance on MS-COCO, but human evaluation prefers T5-XXL on DrawBench (a collection of prompts covering 11 categories).

When applying classifier-free guidance, increasing $w$ may lead to better image-text alignment but worse image fidelity. They found that it is due to train-test mismatch, that is to say, because training data $\mathbf{x}$ stays within the range $\left[\right. - 1 , 1 \left]\right.$, the test data should be so too. Two thresholding strategies are introduced:

- Static thresholding: clip $\mathbf{x}$ prediction to $\left[\right. - 1 , 1 \left]\right.$
- Dynamic thresholding: at each sampling step, compute $s$ as a certain percentile absolute pixel value; if $s > 1$, clip the prediction to $\left[\right. - s , s \left]\right.$ and divide by $s$.

Imagen modifies several designs in U-net to make it *efficient U-Net*.

- Shift model parameters from high resolution blocks to low resolution by adding more residual locks for the lower resolutions;
- Scale the skip connections by $1 / \sqrt{2}$
- Reverse the order of downsampling (move it before convolutions) and upsampling operations (move it after convolution) in order to improve the speed of forward pass.

They found that noise conditioning augmentation, dynamic thresholding and efficient U-Net are critical for image quality, but scaling text encoder size is more important than U-Net size.

## Model Architecture

There are two common backbone architecture choices for diffusion models: U-Net and Transformer.

**U-Net** ([Ronneberger, et al. 2015](https://arxiv.org/abs/1505.04597)) consists of a downsampling stack and an upsampling stack.

- *Downsampling*: Each step consists of the repeated application of two 3x3 convolutions (unpadded convolutions), each followed by a ReLU and a 2x2 max pooling with stride 2. At each downsampling step, the number of feature channels is doubled.
- *Upsampling*: Each step consists of an upsampling of the feature map followed by a 2x2 convolution and each halves the number of feature channels.
- *Shortcuts*: Shortcut connections result in a concatenation with the corresponding layers of the downsampling stack and provide the essential high-resolution features to the upsampling process.
![](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/U-net.png)

The U-net architecture. Each blue square is a feature map with the number of channels labeled on top and the height x width dimension labeled on the left bottom side. The gray arrows mark the shortcut connections. (Image source: Ronneberger, 2015 )

To enable image generation conditioned on additional images for composition info like Canny edges, Hough lines, user scribbles, human post skeletons, segmentation maps, depths and normals, **ControlNet** ([Zhang et al. 2023](https://arxiv.org/abs/2302.05543) introduces architectural changes via adding a “sandwiched” zero convolution layers of a trainable copy of the original model weights into each encoder layer of the U-Net. Precisely, given a neural network block $\mathcal{F}_{\theta} \left(\right. . \left.\right)$, ControlNet does the following:

1. First, freeze the original parameters $\theta$ of the original block
2. Clone it to be a copy with trainable parameters $\theta_{c}$ and an additional conditioning vector $\mathbf{c}$.
3. Use two zero convolution layers, denoted as $\mathcal{Z}_{\theta_{z 1}} \left(\right. . ; . \left.\right)$ and $\mathcal{Z}_{\theta_{z 2}} \left(\right. . ; . \left.\right)$, which is 1x1 convo layers with both weights and biases initialized to be zeros, to connect these two blocks. Zero convolutions protect this back-bone by eliminating random noise as gradients in the initial training steps.
4. The final output is: $\mathbf{y}_{c} = \mathcal{F}_{\theta} \left(\right. \mathbf{x} \left.\right) + \mathcal{Z}_{\theta_{z 2}} \left(\right. \mathcal{F}_{\theta_{c}} \left(\right. \mathbf{x} + \mathcal{Z}_{\theta_{z 1}} \left(\right. \mathbf{c} \left.\right) \left.\right) \left.\right)$
![](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/ControlNet.png)

The ControlNet architecture. (Image source: Zhang et al. 2023 )

**Diffusion Transformer** (**DiT**; [Peebles & Xie, 2023](https://arxiv.org/abs/2212.09748)) for diffusion modeling operates on latent patches, using the same design space of [LDM](#ldm) (Latent Diffusion Model)\]. DiT has the following setup:

1. Take the latent representation of an input $\mathbf{z}$ as input to DiT.
2. “Patchify” the noise latent of size $I \times I \times C$ into patches of size $p$ and convert it into a sequence of patches of size $\left(\right. I / p \left.\right)^{2}$.
3. Then this sequence of tokens go through Transformer blocks. They are exploring three different designs for how to do generation conditioned on contextual information like timestep $t$ or class label $c$. Among three designs, *adaLN (Adaptive layer norm)-Zero* works out the best, better than in-context conditioning and cross-attention block. The scale and shift parameters, $\gamma$ and $\beta$, are regressed from the sum of the embedding vectors of $t$ and $c$. The dimension-wise scaling parameters $\alpha$ is also regressed and applied immediately prior to any residual connections within the DiT block.
4. The transformer decoder outputs noise predictions and an output diagonal covariance prediction.
![](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/DiT.png)

The Diffusion Transformer (DiT) architecture. (Image source: Peebles & Xie, 2023 )

Transformer architecture can be easily scaled up and it is well known for that. This is one of the biggest benefits of DiT as its performance scales up with more compute and larger DiT models are more compute efficient according to the experiments.

## Quick Summary

- **Pros**: Tractability and flexibility are two conflicting objectives in generative modeling. Tractable models can be analytically evaluated and cheaply fit data (e.g. via a Gaussian or Laplace), but they cannot easily describe the structure in rich datasets. Flexible models can fit arbitrary structures in data, but evaluating, training, or sampling from these models is usually expensive. Diffusion models are both analytically tractable and flexible
- **Cons**: Diffusion models rely on a long Markov chain of diffusion steps to generate samples, so it can be quite expensive in terms of time and compute. New methods have been proposed to make the process much faster, but the sampling is still slower than GAN.

## Citation

Cited as:

> Weng, Lilian. (Jul 2021). What are diffusion models? Lil’Log. https://lilianweng.github.io/posts/2021-07-11-diffusion-models/.

Or

```coffeescript
@article{weng2021diffusion,
  title   = "What are diffusion models?",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io",
  year    = "2021",
  month   = "Jul",
  url     = "https://lilianweng.github.io/posts/2021-07-11-diffusion-models/"
}
```

## References

\[1\] Jascha Sohl-Dickstein et al. [“Deep Unsupervised Learning using Nonequilibrium Thermodynamics.”](https://arxiv.org/abs/1503.03585) ICML 2015.

\[2\] Max Welling & Yee Whye Teh. [“Bayesian learning via stochastic gradient langevin dynamics.”](https://www.stats.ox.ac.uk/~teh/research/compstats/WelTeh2011a.pdf) ICML 2011.

\[3\] Yang Song & Stefano Ermon. [“Generative modeling by estimating gradients of the data distribution.”](https://arxiv.org/abs/1907.05600) NeurIPS 2019.

\[4\] Yang Song & Stefano Ermon. [“Improved techniques for training score-based generative models.”](https://arxiv.org/abs/2006.09011) NeuriPS 2020.

\[5\] Jonathan Ho et al. [“Denoising diffusion probabilistic models.”](https://arxiv.org/abs/2006.11239) arxiv Preprint arxiv:2006.11239 (2020). \[[code](https://github.com/hojonathanho/diffusion)\]

\[6\] Jiaming Song et al. [“Denoising diffusion implicit models.”](https://arxiv.org/abs/2010.02502) arxiv Preprint arxiv:2010.02502 (2020). \[[code](https://github.com/ermongroup/ddim)\]

\[7\] Alex Nichol & Prafulla Dhariwal. [“Improved denoising diffusion probabilistic models”](https://arxiv.org/abs/2102.09672) arxiv Preprint arxiv:2102.09672 (2021). \[[code](https://github.com/openai/improved-diffusion)\]

\[8\] Prafula Dhariwal & Alex Nichol. [“Diffusion Models Beat GANs on Image Synthesis.”](https://arxiv.org/abs/2105.05233) arxiv Preprint arxiv:2105.05233 (2021). \[[code](https://github.com/openai/guided-diffusion)\]

\[9\] Jonathan Ho & Tim Salimans. [“Classifier-Free Diffusion Guidance.”](https://arxiv.org/abs/2207.12598) NeurIPS 2021 Workshop on Deep Generative Models and Downstream Applications.

\[10\] Yang Song, et al. [“Score-Based Generative Modeling through Stochastic Differential Equations.”](https://openreview.net/forum?id=PxTIG12RRHS) ICLR 2021.

\[11\] Alex Nichol, Prafulla Dhariwal & Aditya Ramesh, et al. [“GLIDE: Towards Photorealistic Image Generation and Editing with Text-Guided Diffusion Models.”](https://arxiv.org/abs/2112.10741) ICML 2022.

\[12\] Jonathan Ho, et al. [“Cascaded diffusion models for high fidelity image generation.”](https://arxiv.org/abs/2106.15282) J. Mach. Learn. Res. 23 (2022): 47-1.

\[13\] Aditya Ramesh et al. [“Hierarchical Text-Conditional Image Generation with CLIP Latents.”](https://arxiv.org/abs/2204.06125) arxiv Preprint arxiv:2204.06125 (2022).

\[14\] Chitwan Saharia & William Chan, et al. [“Photorealistic Text-to-Image Diffusion Models with Deep Language Understanding.”](https://arxiv.org/abs/2205.11487) arxiv Preprint arxiv:2205.11487 (2022).

\[15\] Rombach & Blattmann, et al. [“High-Resolution Image Synthesis with Latent Diffusion Models.”](https://arxiv.org/abs/2112.10752) CVPR 2022.[code](https://github.com/CompVis/latent-diffusion)

\[16\] Song et al. [“Consistency Models”](https://arxiv.org/abs/2303.01469) arxiv Preprint arxiv:2303.01469 (2023)

\[17\] Salimans & Ho. [“Progressive Distillation for Fast Sampling of Diffusion Models”](https://arxiv.org/abs/2202.00512) ICLR 2022.

\[18\] Ronneberger, et al. [“U-Net: Convolutional Networks for Biomedical Image Segmentation”](https://arxiv.org/abs/1505.04597) MICCAI 2015.

\[19\] Peebles & Xie. [“Scalable diffusion models with transformers.”](https://arxiv.org/abs/2212.09748) ICCV 2023.

\[20\] Zhang et al. [“Adding Conditional Control to Text-to-Image Diffusion Models.”](https://arxiv.org/abs/2302.05543) arxiv Preprint arxiv:2302.05543 (2023).