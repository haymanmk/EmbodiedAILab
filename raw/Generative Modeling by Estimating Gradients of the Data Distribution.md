---
title: "Generative Modeling by Estimating Gradients of the Data Distribution"
source: "https://yang-song.net/blog/2021/score/"
author:
  - "[[Yang Song]]"
published:
created: 2026-05-30
description: "This blog post focuses on a promising new direction for generative modeling. We can learn score functions (gradients of log probability density functions) on a large number of noise-perturbed data distributions, then generate samples with Langevin-type sampling. The resulting generative models, often called <em>score-based generative models</em>, has several important advantages over existing model families: GAN-level sample quality without adversarial training, flexible model architectures, exact log-likelihood computation, and inverse problem solving without re-training models. In this blog post, we will show you in more detail the intuition, basic concepts, and potential applications of score-based generative models."
tags:
  - "clippings"
---
This blog post focuses on a promising new direction for generative modeling. We can learn score functions (gradients of log probability density functions) on a large number of noise-perturbed data distributions, then generate samples with Langevin-type sampling. The resulting generative models, often called *score-based generative models*, has several important advantages over existing model families: GAN-level sample quality without adversarial training, flexible model architectures, exact log-likelihood computation, and inverse problem solving without re-training models. In this blog post, we will show you in more detail the intuition, basic concepts, and potential applications of score-based generative models.

## Introduction

Existing generative modeling techniques can largely be grouped into two categories based on how they represent probability distributions.

1. **likelihood-based models**, which directly learn the distribution’s probability density (or mass) function via (approximate) maximum likelihood. Typical likelihood-based models include autoregressive models
	- **The neural autoregressive distribution estimator**  
		H. Larochelle, I. Murray.  
		International Conference on Artificial Intelligence and Statistics, pp. 29--37. 2011.
	- **Made: Masked autoencoder for distribution estimation**  
		M. Germain, K. Gregor, I. Murray, H. Larochelle.  
		International Conference on Machine Learning, pp. 881--889. 2015.
	- **Pixel recurrent neural networks**  
		A. Van Oord, N. Kalchbrenner, K. Kavukcuoglu.  
		International Conference on Machine Learning, pp. 1747--1756. 2016.
	\[1, 2, 3\]
	, normalizing flow models
	- **NICE: Non-linear independent components estimation**  
		L. Dinh, D. Krueger, Y. Bengio.  
		arXiv preprint arXiv:1410.8516. 2014.
	- **Density estimation using Real NVP**  
		L. Dinh, J. Sohl-Dickstein, S. Bengio.  
		International Conference on Learning Representations. 2017.
	\[4, 5\]
	, energy-based models (EBMs)
	- **A tutorial on energy-based learning**  
		Y. LeCun, S. Chopra, R. Hadsell, M. Ranzato, F. Huang.  
		Predicting structured data, Vol 1(0). 2006.
	- **How to Train Your Energy-Based Models**  
		Y. Song, D.P. Kingma.  
		arXiv preprint arXiv:2101.03288. 2021.
	\[6, 7\]
	, and variational auto-encoders (VAEs)
	- **Auto-encoding variational bayes**  
		D.P. Kingma, M. Welling.  
		International Conference on Learning Representations. 2014.
	- **Stochastic backpropagation and approximate inference in deep generative models**  
		D.J. Rezende, S. Mohamed, D. Wierstra.  
		International conference on machine learning, pp. 1278--1286. 2014.
	\[8, 9\]
	.
2. **implicit generative models**
	- **Learning in implicit generative models**  
		S. Mohamed, B. Lakshminarayanan.  
		arXiv preprint arXiv:1610.03483. 2016.
	\[10\]
	, where the probability distribution is implicitly represented by a model of its sampling process. The most prominent example is generative adversarial networks (GANs)
	- **Generative adversarial nets**  
		I. Goodfellow, J. Pouget-Abadie, M. Mirza, B. Xu, D. Warde-Farley, S. Ozair, A. Courville, Y. Bengio.  
		Advances in neural information processing systems, pp. 2672--2680. 2014.
	\[11\]
	, where new samples from the data distribution are synthesized by transforming a random Gaussian vector with a neural network.

![](https://yang-song.net/assets/img/score/likelihood_based_models.png)

Bayesian networks, Markov random fields (MRF), autoregressive models, and normalizing flow models are all examples of likelihood-based models. All these models represent the probability density or mass function of a distribution.

![](https://yang-song.net/assets/img/score/implicit_models.png)

GAN is an example of implicit models. It implicitly represents a distribution over all objects that can be produced by the generator network.

Likelihood-based models and implicit generative models, however, both have significant limitations. Likelihood-based models either require strong restrictions on the model architecture to ensure a tractable normalizing constant for likelihood computation, or must rely on surrogate objectives to approximate maximum likelihood training. Implicit generative models, on the other hand, often require adversarial training, which is notoriously unstable

- **Improved techniques for training gans**  
	T. Salimans, I. Goodfellow, W. Zaremba, V. Cheung, A. Radford, X. Chen.  
	Advances in Neural Information Processing Systems, pp. 2226--2234. 2016.

\[12\]

and can lead to mode collapse

- **Unrolled Generative Adversarial Networks**   [\[link\]](https://openreview.net/forum?id=BydrOIcle)  
	L. Metz, B. Poole, D. Pfau, J. Sohl-Dickstein.  
	5th International Conference on Learning Representations, ICLR 2017, Toulon, France, April 24-26, 2017, Conference Track Proceedings. OpenReview.net. 2017.

\[13\]

.

In this blog post, I will introduce another way to represent probability distributions that may circumvent several of these limitations. The key idea is to model *the gradient of the log probability density function*, a quantity often known as the (Stein) **score function**

- **A Kernel Test of Goodness of Fit**   [\[HTML\]](https://proceedings.mlr.press/v48/chwialkowski16.html)  
	K. Chwialkowski, H. Strathmann, A. Gretton.  
	Proceedings of The 33rd International Conference on Machine Learning, Vol 48, pp. 2606--2615. PMLR. 2016.
- **A kernelized Stein discrepancy for goodness-of-fit tests**  
	Q. Liu, J. Lee, M. Jordan.  
	International conference on machine learning, pp. 276--284. 2016.

\[14, 15\]

. Such **score-based models** are not required to have a tractable normalizing constant, and can be directly learned by **score matching**

- **Estimation of non-normalized statistical models by score matching**  
	A. Hyvarinen.  
	Journal of Machine Learning Research, Vol 6(Apr), pp. 695--709. 2005.
- **A connection between score matching and denoising autoencoders**  
	P. Vincent.  
	Neural computation, Vol 23(7), pp. 1661--1674. MIT Press. 2011.

\[16, 17\]

.

![](https://yang-song.net/assets/img/score/score_contour.jpg)

Score function (the vector field) and density function (contours) of a mixture of two Gaussians.

Score-based models have achieved state-of-the-art performance on many downstream tasks and applications. These tasks include, among others, image generation

- **Generative Modeling by Estimating Gradients of the Data Distribution**   [\[PDF\]](http://arxiv.org/pdf/1907.05600.pdf)  
	Y. Song, S. Ermon.  
	Advances in Neural Information Processing Systems, pp. 11895--11907. 2019.
- **Improved Techniques for Training Score-Based Generative Models**   [\[PDF\]](http://arxiv.org/pdf/2006.09011.pdf)  
	Y. Song, S. Ermon.  
	Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual. 2020.
- **Denoising diffusion probabilistic models**  
	J. Ho, A. Jain, P. Abbeel.  
	arXiv preprint arXiv:2006.11239. 2020.
- **Score-Based Generative Modeling through Stochastic Differential Equations**   [\[link\]](https://openreview.net/forum?id=PxTIG12RRHS)  
	Y. Song, J. Sohl-Dickstein, D.P. Kingma, A. Kumar, S. Ermon, B. Poole.  
	International Conference on Learning Representations. 2021.
- **Diffusion models beat gans on image synthesis**  
	P. Dhariwal, A. Nichol.  
	arXiv preprint arXiv:2105.05233. 2021.
- **Cascaded Diffusion Models for High Fidelity Image Generation**  
	J. Ho, C. Saharia, W. Chan, D.J. Fleet, M. Norouzi, T. Salimans.  
	2021.

\[18, 19, 20, 21, 22, 23\]

(Yes, better than GANs!), audio synthesis

- **WaveGrad: Estimating Gradients for Waveform Generation**   [\[link\]](https://openreview.net/forum?id=NsMLjcFaO8O)  
	N. Chen, Y. Zhang, H. Zen, R.J. Weiss, M. Norouzi, W. Chan.  
	International Conference on Learning Representations. 2021.
- **DiffWave: A Versatile Diffusion Model for Audio Synthesis**   [\[link\]](https://openreview.net/forum?id=a-xFK8Ymz5J)  
	Z. Kong, W. Ping, J. Huang, K. Zhao, B. Catanzaro.  
	International Conference on Learning Representations. 2021.
- **Grad-tts: A diffusion probabilistic model for text-to-speech**  
	V. Popov, I. Vovk, V. Gogoryan, T. Sadekova, M. Kudinov.  
	arXiv preprint arXiv:2105.06337. 2021.

\[24, 25, 26\]

, shape generation

- **Learning Gradient Fields for Shape Generation**  
	R. Cai, G. Yang, H. Averbuch-Elor, Z. Hao, S. Belongie, N. Snavely, B. Hariharan.  
	Proceedings of the European Conference on Computer Vision (ECCV). 2020.

\[27\]

, and music generation

- **Symbolic Music Generation with Diffusion Models**  
	G. Mittal, J. Engel, C. Hawthorne, I. Simon.  
	arXiv preprint arXiv:2103.16091. 2021.

\[28\]

. Moreover, score-based models have connections to [normalizing flow models](https://blog.evjang.com/2018/01/nf1.html), therefore allowing exact likelihood computation and representation learning. Additionally, modeling and estimating scores facilitates [inverse problem](https://en.wikipedia.org/wiki/Inverse_problem#:~:text=An%20inverse%20problem%20in%20science,measurements%20of%20its%20gravity%20field) solving, with applications such as image inpainting

- **Generative Modeling by Estimating Gradients of the Data Distribution**   [\[PDF\]](http://arxiv.org/pdf/1907.05600.pdf)  
	Y. Song, S. Ermon.  
	Advances in Neural Information Processing Systems, pp. 11895--11907. 2019.
- **Score-Based Generative Modeling through Stochastic Differential Equations**   [\[link\]](https://openreview.net/forum?id=PxTIG12RRHS)  
	Y. Song, J. Sohl-Dickstein, D.P. Kingma, A. Kumar, S. Ermon, B. Poole.  
	International Conference on Learning Representations. 2021.

\[18, 21\]

, image colorization

- **Score-Based Generative Modeling through Stochastic Differential Equations**   [\[link\]](https://openreview.net/forum?id=PxTIG12RRHS)  
	Y. Song, J. Sohl-Dickstein, D.P. Kingma, A. Kumar, S. Ermon, B. Poole.  
	International Conference on Learning Representations. 2021.

\[21\]

, [compressive sensing](https://en.wikipedia.org/wiki/Compressed_sensing), and medical image reconstruction (e.g., CT, MRI)

- **Robust Compressed Sensing MRI with Deep Generative Priors**  
	A. Jalal, M. Arvinte, G. Daras, E. Price, A.G. Dimakis, J.I. Tamir.  
	Advances in neural information processing systems. 2021.

\[29\]

.

![](https://yang-song.net/assets/img/score/ffhq_samples.jpg)

1024 x 1024 samples generated from score-based models

- **Score-Based Generative Modeling through Stochastic Differential Equations**   [\[link\]](https://openreview.net/forum?id=PxTIG12RRHS)  
	Y. Song, J. Sohl-Dickstein, D.P. Kingma, A. Kumar, S. Ermon, B. Poole.  
	International Conference on Learning Representations. 2021.

\[21\]

This post aims to show you the motivation and intuition of score-based generative modeling, as well as its basic concepts, properties and applications.

## The score function, score-based models, and score matching

Suppose we are given a dataset $\left{\right. \mathbf{x}_{1} , \mathbf{x}_{2} , \hdots , \mathbf{x}_{N} \left.\right}$, where each point is drawn independently from an underlying data distribution $p \left(\right. \mathbf{x} \left.\right)$. Given this dataset, the goal of generative modeling is to fit a model to the data distribution such that we can synthesize new data points at will by sampling from the distribution.

In order to build such a generative model, we first need a way to represent a probability distribution. One such way, as in likelihood-based models, is to directly model the [probability density function](https://en.wikipedia.org/wiki/Probability_density_function) (p.d.f.) or [probability mass function](https://en.wikipedia.org/wiki/Probability_mass_function) (p.m.f.). Let $f_{\theta} \left(\right. \mathbf{x} \left.\right) \in \mathbb{R}$ be a real-valued function parameterized by a learnable parameter $\theta$. We can define a p.d.f.

[^1]

via 
$$
(\text{1}) p_{\theta} \left(\right. \mathbf{x} \left.\right) = \frac{e^{- f_{\theta} \left(\right. \mathbf{x} \left.\right)}}{Z_{\theta}} ,
$$
 where $Z_{\theta} > 0$ is a normalizing constant dependent on $\theta$, such that $\int p_{\theta} \left(\right. \mathbf{x} \left.\right) \text{d} \mathbf{x} = 1$. Here the function $f_{\theta} \left(\right. \mathbf{x} \left.\right)$ is often called an unnormalized probabilistic model, or energy-based model

- **How to Train Your Energy-Based Models**  
	Y. Song, D.P. Kingma.  
	arXiv preprint arXiv:2101.03288. 2021.

\[7\]

.

We can train $p_{\theta} \left(\right. \mathbf{x} \left.\right)$ by maximizing the log-likelihood of the data 
$$
(\text{2}) \underset{\theta}{max} \sum_{i = 1}^{N} log ⁡ p_{\theta} \left(\right. \mathbf{x}_{i} \left.\right) .
$$
 However, equation $(\text{2})$ requires $p_{\theta} \left(\right. \mathbf{x} \left.\right)$ to be a normalized probability density function. This is undesirable because in order to compute $p_{\theta} \left(\right. \mathbf{x} \left.\right)$, we must evaluate the normalizing constant $Z_{\theta}$ —a typically intractable quantity for any general $f_{\theta} \left(\right. \mathbf{x} \left.\right)$. Thus to make maximum likelihood training feasible, likelihood-based models must either restrict their model architectures (e.g., causal convolutions in autoregressive models, invertible networks in normalizing flow models) to make $Z_{\theta}$ tractable, or approximate the normalizing constant (e.g., variational inference in VAEs, or MCMC sampling used in contrastive divergence

- **Training products of experts by minimizing contrastive divergence**  
	G.E. Hinton.  
	Neural computation, Vol 14(8), pp. 1771--1800. MIT Press. 2002.

\[30\]

) which may be computationally expensive.

By modeling the score function instead of the density function, we can sidestep the difficulty of intractable normalizing constants. The **score function** of a distribution $p \left(\right. \mathbf{x} \left.\right)$ is defined as 
$$
\nabla_{\mathbf{x}} log ⁡ p \left(\right. \mathbf{x} \left.\right) ,
$$
 and a model for the score function is called a **score-based model**

- **Generative Modeling by Estimating Gradients of the Data Distribution**   [\[PDF\]](http://arxiv.org/pdf/1907.05600.pdf)  
	Y. Song, S. Ermon.  
	Advances in Neural Information Processing Systems, pp. 11895--11907. 2019.

\[18\]

, which we denote as $\mathbf{s}_{\theta} \left(\right. \mathbf{x} \left.\right)$. The score-based model is learned such that $\mathbf{s}_{\theta} \left(\right. \mathbf{x} \left.\right) \approx \nabla_{\mathbf{x}} log ⁡ p \left(\right. \mathbf{x} \left.\right)$, and can be parameterized without worrying about the normalizing constant. For example, we can easily parameterize a score-based model with the energy-based model defined in equation $(\text{1})$, via

$$
(\text{3}) \mathbf{s}_{\theta} \left(\right. \mathbf{x} \left.\right) = \nabla_{\mathbf{x}} log ⁡ p_{\theta} \left(\right. \mathbf{x} \left.\right) = - \nabla_{\mathbf{x}} f_{\theta} \left(\right. \mathbf{x} \left.\right) - \underset{= 0}{\underbrace{\nabla_{\mathbf{x}} log ⁡ Z_{\theta}}} = - \nabla_{\mathbf{x}} f_{\theta} \left(\right. \mathbf{x} \left.\right) .
$$

Note that the score-based model $\mathbf{s}_{\theta} \left(\right. \mathbf{x} \left.\right)$ is independent of the normalizing constant $Z_{\theta}$! This significantly expands the family of models that we can tractably use, since we don’t need any special architectures to make the normalizing constant tractable.

![](https://yang-song.net/assets/img/score/ebm.gif)

Parameterizing probability density functions. No matter how you change the model family and parameters, it has to be normalized (area under the curve must integrate to one).

![](https://yang-song.net/assets/img/score/score.gif)

Parameterizing score functions. No need to worry about normalization.

Similar to likelihood-based models, we can train score-based models by minimizing the **Fisher divergence**

[^2]

between the model and the data distributions, defined as $(\text{5}) \mathbb{E}_{p \left(\right. \mathbf{x} \left.\right)} \left[\right. \parallel \nabla_{\mathbf{x}} log ⁡ p \left(\right. \mathbf{x} \left.\right) - \mathbf{s}_{\theta} \left(\right. \mathbf{x} \left.\right) \parallel_{2}^{2} \left]\right.$

Intuitively, the Fisher divergence compares the squared $ℓ_{2}$ distance between the ground-truth data score and the score-based model. Directly computing this divergence, however, is infeasible because it requires access to the unknown data score $\nabla_{\mathbf{x}} log ⁡ p \left(\right. \mathbf{x} \left.\right)$. Fortunately, there exists a family of methods called **score matching**

[^3]

- **Estimation of non-normalized statistical models by score matching**  
	A. Hyvarinen.  
	Journal of Machine Learning Research, Vol 6(Apr), pp. 695--709. 2005.
- **A connection between score matching and denoising autoencoders**  
	P. Vincent.  
	Neural computation, Vol 23(7), pp. 1661--1674. MIT Press. 2011.
- **Sliced score matching: A scalable approach to density and score estimation**   [\[PDF\]](http://arxiv.org/pdf/1905.07088.pdf)  
	Y. Song, S. Garg, J. Shi, S. Ermon.  
	Uncertainty in Artificial Intelligence, pp. 574--584. 2020.

\[16, 17, 31\]

that minimize the Fisher divergence without knowledge of the ground-truth data score. Score matching objectives can directly be estimated on a dataset and optimized with stochastic gradient descent, analogous to the log-likelihood objective for training likelihood-based models (with known normalizing constants). We can train the score-based model by minimizing a score matching objective, **without requiring adversarial optimization**.

Additionally, using the score matching objective gives us a considerable amount of modeling flexibility. The Fisher divergence itself does not require $\mathbf{s}_{\theta} \left(\right. \mathbf{x} \left.\right)$ to be an actual score function of any normalized distribution—it simply compares the $ℓ_{2}$ distance between the ground-truth data score and the score-based model, with no additional assumptions on the form of $\mathbf{s}_{\theta} \left(\right. \mathbf{x} \left.\right)$. In fact, the only requirement on the score-based model is that it should be a vector-valued function with the same input and output dimensionality, which is easy to satisfy in practice.

As a brief summary, we can represent a distribution by modeling its score function, which can be estimated by training a score-based model of free-form architectures with score matching.

## Langevin dynamics

Once we have trained a score-based model $\mathbf{s}_{\theta} \left(\right. \mathbf{x} \left.\right) \approx \nabla_{\mathbf{x}} log ⁡ p \left(\right. \mathbf{x} \left.\right)$, we can use an iterative procedure called [**Langevin dynamics**](https://en.wikipedia.org/wiki/Metropolis-adjusted_Langevin_algorithm)

- **Correlation functions and computer simulations**  
	G. Parisi.  
	Nuclear Physics B, Vol 180(3), pp. 378--384. Elsevier. 1981.
- **Representations of knowledge in complex systems**  
	U. Grenander, M.I. Miller.  
	Journal of the Royal Statistical Society: Series B (Methodological), Vol 56(4), pp. 549--581. Wiley Online Library. 1994.

\[32, 33\]

to draw samples from it.

Langevin dynamics provides an MCMC procedure to sample from a distribution $p \left(\right. \mathbf{x} \left.\right)$ using only its score function $\nabla_{\mathbf{x}} log ⁡ p \left(\right. \mathbf{x} \left.\right)$. Specifically, it initializes the chain from an arbitrary prior distribution $\mathbf{x}_{0} sim \pi \left(\right. \mathbf{x} \left.\right)$, and then iterates the following

$$
(\text{6}) \mathbf{x}_{i + 1} \leftarrow \mathbf{x}_{i} + \epsilon \nabla_{\mathbf{x}} log ⁡ p \left(\right. \mathbf{x} \left.\right) + \sqrt{2 \epsilon} \mathbf{z}_{i} , i = 0 , 1 , \hdots , K ,
$$

where $\mathbf{z}_{i} sim \mathcal{N} \left(\right. 0 , I \left.\right)$. When $\epsilon \rightarrow 0$ and $K \rightarrow \infty$, $\mathbf{x}_{K}$ obtained from the procedure in $(\text{6})$ converges to a sample from $p \left(\right. \mathbf{x} \left.\right)$ under some regularity conditions. In practice, the error is negligible when $\epsilon$ is sufficiently small and $K$ is sufficiently large.

![](https://yang-song.net/assets/img/score/langevin.gif)

Using Langevin dynamics to sample from a mixture of two Gaussians.

Note that Langevin dynamics accesses $p \left(\right. \mathbf{x} \left.\right)$ only through $\nabla_{\mathbf{x}} log ⁡ p \left(\right. \mathbf{x} \left.\right)$. Since $\mathbf{s}_{\theta} \left(\right. \mathbf{x} \left.\right) \approx \nabla_{\mathbf{x}} log ⁡ p \left(\right. \mathbf{x} \left.\right)$, we can produce samples from our score-based model $\mathbf{s}_{\theta} \left(\right. \mathbf{x} \left.\right)$ by plugging it into equation $(\text{6})$.

## Naive score-based generative modeling and its pitfalls

So far, we’ve discussed how to train a score-based model with score matching, and then produce samples via Langevin dynamics. However, this naive approach has had limited success in practice—we’ll talk about some pitfalls of score matching that received little attention in prior works

- **Generative Modeling by Estimating Gradients of the Data Distribution**   [\[PDF\]](http://arxiv.org/pdf/1907.05600.pdf)  
	Y. Song, S. Ermon.  
	Advances in Neural Information Processing Systems, pp. 11895--11907. 2019.

\[18\]

.

![](https://yang-song.net/assets/img/score/smld.jpg)

Score-based generative modeling with score matching + Langevin dynamics.

The key challenge is the fact that the estimated score functions are inaccurate in low density regions, where few data points are available for computing the score matching objective. This is expected as score matching minimizes the Fisher divergence

$$
\mathbb{E}_{p \left(\right. \mathbf{x} \left.\right)} \left[\right. \parallel \nabla_{\mathbf{x}} log ⁡ p \left(\right. \mathbf{x} \left.\right) - \mathbf{s}_{\theta} \left(\right. \mathbf{x} \left.\right) \parallel_{2}^{2} \left]\right. = \int p \left(\right. \mathbf{x} \left.\right) \parallel \nabla_{\mathbf{x}} log ⁡ p \left(\right. \mathbf{x} \left.\right) - \mathbf{s}_{\theta} \left(\right. \mathbf{x} \left.\right) \parallel_{2}^{2} d \mathbf{x} .
$$

Since the $ℓ_{2}$ differences between the true data score function and score-based model are weighted by $p \left(\right. \mathbf{x} \left.\right)$, they are largely ignored in low density regions where $p \left(\right. \mathbf{x} \left.\right)$ is small. This behavior can lead to subpar results, as illustrated by the figure below:

![](https://yang-song.net/assets/img/score/pitfalls.jpg)

Estimated scores are only accurate in high density regions.

When sampling with Langevin dynamics, our initial sample is highly likely in low density regions when data reside in a high dimensional space. Therefore, having an inaccurate score-based model will derail Langevin dynamics from the very beginning of the procedure, preventing it from generating high quality samples that are representative of the data.

## Score-based generative modeling with multiple noise perturbations

How can we bypass the difficulty of accurate score estimation in regions of low data density? Our solution is to **perturb** data points with noise and train score-based models on the noisy data points instead. When the noise magnitude is sufficiently large, it can populate low data density regions to improve the accuracy of estimated scores. For example, here is what happens when we perturb a mixture of two Gaussians perturbed by additional Gaussian noise.

![](https://yang-song.net/assets/img/score/single_noise.jpg)

Estimated scores are accurate everywhere for the noise-perturbed data distribution due to reduced low data density regions.

Yet another question remains: how do we choose an appropriate noise scale for the perturbation process? Larger noise can obviously cover more low density regions for better score estimation, but it over-corrupts the data and alters it significantly from the original distribution. Smaller noise, on the other hand, causes less corruption of the original data distribution, but does not cover the low density regions as well as we would like.

To achieve the best of both worlds, we use multiple scales of noise perturbations simultaneously

- **Generative Modeling by Estimating Gradients of the Data Distribution**   [\[PDF\]](http://arxiv.org/pdf/1907.05600.pdf)  
	Y. Song, S. Ermon.  
	Advances in Neural Information Processing Systems, pp. 11895--11907. 2019.
- **Improved Techniques for Training Score-Based Generative Models**   [\[PDF\]](http://arxiv.org/pdf/2006.09011.pdf)  
	Y. Song, S. Ermon.  
	Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual. 2020.

\[18, 19\]

. Suppose we always perturb the data with isotropic Gaussian noise, and let there be a total of $L$ increasing standard deviations $\sigma_{1} < \sigma_{2} < \hdots < \sigma_{L}$. We first perturb the data distribution $p \left(\right. \mathbf{x} \left.\right)$ with each of the Gaussian noise $\mathcal{N} \left(\right. 0 , \sigma_{i}^{2} I \left.\right) , i = 1 , 2 , \hdots , L$ to obtain a noise-perturbed distribution

$$
p_{\sigma_{i}} \left(\right. \mathbf{x} \left.\right) = \int p \left(\right. \mathbf{y} \left.\right) \mathcal{N} \left(\right. \mathbf{x} ; \mathbf{y} , \sigma_{i}^{2} I \left.\right) d \mathbf{y} .
$$

Note that we can easily draw samples from $p_{\sigma_{i}} \left(\right. \mathbf{x} \left.\right)$ by sampling $\mathbf{x} sim p \left(\right. \mathbf{x} \left.\right)$ and computing $\mathbf{x} + \sigma_{i} \mathbf{z}$, with $\mathbf{z} sim \mathcal{N} \left(\right. 0 , I \left.\right)$.

Next, we estimate the score function of each noise-perturbed distribution, $\nabla_{\mathbf{x}} log ⁡ p_{\sigma_{i}} \left(\right. \mathbf{x} \left.\right)$, by training a **Noise Conditional Score-Based Model** $\mathbf{s}_{\theta} \left(\right. \mathbf{x} , i \left.\right)$ (also called a Noise Conditional Score Network, or NCSN

- **Generative Modeling by Estimating Gradients of the Data Distribution**   [\[PDF\]](http://arxiv.org/pdf/1907.05600.pdf)  
	Y. Song, S. Ermon.  
	Advances in Neural Information Processing Systems, pp. 11895--11907. 2019.
- **Improved Techniques for Training Score-Based Generative Models**   [\[PDF\]](http://arxiv.org/pdf/2006.09011.pdf)  
	Y. Song, S. Ermon.  
	Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual. 2020.
- **Score-Based Generative Modeling through Stochastic Differential Equations**   [\[link\]](https://openreview.net/forum?id=PxTIG12RRHS)  
	Y. Song, J. Sohl-Dickstein, D.P. Kingma, A. Kumar, S. Ermon, B. Poole.  
	International Conference on Learning Representations. 2021.

\[18, 19, 21\]

, when parameterized with a neural network) with score matching, such that $\mathbf{s}_{\theta} \left(\right. \mathbf{x} , i \left.\right) \approx \nabla_{\mathbf{x}} log ⁡ p_{\sigma_{i}} \left(\right. \mathbf{x} \left.\right)$ for all $i = 1 , 2 , \hdots , L$.

![](https://yang-song.net/assets/img/score/multi_scale.jpg)

We apply multiple scales of Gaussian noise to perturb the data distribution (**first row**), and jointly estimate the score functions for all of them (**second row**).

![](https://yang-song.net/assets/img/score/duoduo.jpg)

Perturbing an image with multiple scales of Gaussian noise.

The training objective for $\mathbf{s}_{\theta} \left(\right. \mathbf{x} , i \left.\right)$ is a weighted sum of Fisher divergences for all noise scales. In particular, we use the objective below:

$$
(\text{7}) \sum_{i = 1}^{L} \lambda \left(\right. i \left.\right) \mathbb{E}_{p_{\sigma_{i}} \left(\right. \mathbf{x} \left.\right)} \left[\right. \parallel \nabla_{\mathbf{x}} log ⁡ p_{\sigma_{i}} \left(\right. \mathbf{x} \left.\right) - \mathbf{s}_{\theta} \left(\right. \mathbf{x} , i \left.\right) \parallel_{2}^{2} \left]\right. ,
$$

where $\lambda \left(\right. i \left.\right) \in \mathbb{R}_{> 0}$ is a positive weighting function, often chosen to be $\lambda \left(\right. i \left.\right) = \sigma_{i}^{2}$. The objective $(\text{7})$ can be optimized with score matching, exactly as in optimizing the naive (unconditional) score-based model $\mathbf{s}_{\theta} \left(\right. \mathbf{x} \left.\right)$.

After training our noise-conditional score-based model $\mathbf{s}_{\theta} \left(\right. \mathbf{x} , i \left.\right)$, we can produce samples from it by running Langevin dynamics for $i = L , L - 1 , \hdots , 1$ in sequence. This method is called **annealed Langevin dynamics** (defined by Algorithm 1 in

- **Generative Modeling by Estimating Gradients of the Data Distribution**   [\[PDF\]](http://arxiv.org/pdf/1907.05600.pdf)  
	Y. Song, S. Ermon.  
	Advances in Neural Information Processing Systems, pp. 11895--11907. 2019.

\[18\]

, and improved by

- **Improved Techniques for Training Score-Based Generative Models**   [\[PDF\]](http://arxiv.org/pdf/2006.09011.pdf)  
	Y. Song, S. Ermon.  
	Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual. 2020.
- **Adversarial score matching and improved sampling for image generation**   [\[link\]](https://openreview.net/forum?id=eLfqMl3z3lq)  
	A. Jolicoeur-Martineau, R. Piche-Taillefer, I. Mitliagkas, R.T.d. Combes.  
	International Conference on Learning Representations. 2021.

\[19, 34\]

), since the noise scale $\sigma_{i}$ decreases (anneals) gradually over time.

![](https://yang-song.net/assets/img/score/ald.gif)

Annealed Langevin dynamics combine a sequence of Langevin chains with gradually decreasing noise scales.

![](https://yang-song.net/assets/img/score/celeba_large.gif) ![](https://yang-song.net/assets/img/score/cifar10_large.gif)

Annealed Langevin dynamics for the Noise Conditional Score Network (NCSN) model (from ref.

- **Generative Modeling by Estimating Gradients of the Data Distribution**   [\[PDF\]](http://arxiv.org/pdf/1907.05600.pdf)  
	Y. Song, S. Ermon.  
	Advances in Neural Information Processing Systems, pp. 11895--11907. 2019.

\[18\]

) trained on CelebA (**left**) and CIFAR-10 (**right**). We can start from unstructured noise, modify images according to the scores, and generate nice samples. The method achieved state-of-the-art Inception score on CIFAR-10 at its time.

Here are some practical recommendations for tuning score-based generative models with multiple noise scales:

- Choose $\sigma_{1} < \sigma_{2} < \hdots < \sigma_{L}$ as a [geometric progression](https://en.wikipedia.org/wiki/Geometric_progression#:~:text=In%20mathematics%2C%20a%20geometric%20progression,number%20called%20the%20common%20ratio.), with $\sigma_{1}$ being sufficiently small and $\sigma_{L}$ comparable to the maximum pairwise distance between all training data points
	- **Improved Techniques for Training Score-Based Generative Models**   [\[PDF\]](http://arxiv.org/pdf/2006.09011.pdf)  
		Y. Song, S. Ermon.  
		Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual. 2020.
	\[19\]
	. $L$ is typically on the order of hundreds or thousands.
- Parameterize the score-based model $\mathbf{s}_{\theta} \left(\right. \mathbf{x} , i \left.\right)$ with U-Net skip connections
	- **Generative Modeling by Estimating Gradients of the Data Distribution**   [\[PDF\]](http://arxiv.org/pdf/1907.05600.pdf)  
		Y. Song, S. Ermon.  
		Advances in Neural Information Processing Systems, pp. 11895--11907. 2019.
	- **Denoising diffusion probabilistic models**  
		J. Ho, A. Jain, P. Abbeel.  
		arXiv preprint arXiv:2006.11239. 2020.
	\[18, 20\]
	.
- Apply exponential moving average on the weights of the score-based model when used at test time
	- **Improved Techniques for Training Score-Based Generative Models**   [\[PDF\]](http://arxiv.org/pdf/2006.09011.pdf)  
		Y. Song, S. Ermon.  
		Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual. 2020.
	- **Denoising diffusion probabilistic models**  
		J. Ho, A. Jain, P. Abbeel.  
		arXiv preprint arXiv:2006.11239. 2020.
	\[19, 20\]
	.

With such best practices, we are able to generate high quality image samples with comparable quality to GANs on various datasets, such as below:

![](https://yang-song.net/assets/img/score/ncsnv2.jpg)

Samples from the NCSNv2

- **Improved Techniques for Training Score-Based Generative Models**   [\[PDF\]](http://arxiv.org/pdf/2006.09011.pdf)  
	Y. Song, S. Ermon.  
	Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual. 2020.

\[19\]

model. From left to right: FFHQ 256x256, LSUN bedroom 128x128, LSUN tower 128x128, LSUN church\_outdoor 96x96, and CelebA 64x64.

## Score-based generative modeling with stochastic differential equations (SDEs)

As we already discussed, adding multiple noise scales is critical to the success of score-based generative models. By generalizing the number of noise scales to infinity

- **Score-Based Generative Modeling through Stochastic Differential Equations**   [\[link\]](https://openreview.net/forum?id=PxTIG12RRHS)  
	Y. Song, J. Sohl-Dickstein, D.P. Kingma, A. Kumar, S. Ermon, B. Poole.  
	International Conference on Learning Representations. 2021.

\[21\]

, we obtain not only **higher quality samples**, but also, among others, **exact log-likelihood computation**, and **controllable generation for inverse problem solving**.

In addition to this introduction, we have tutorials written in [Google Colab](https://colab.research.google.com/) to provide a step-by-step guide for training a toy model on MNIST. We also have more advanced code repositories that provide full-fledged implementations for large scale applications.

| Link | Description |
| --- | --- |
|  | Tutorial of score-based generative modeling with SDEs in JAX + FLAX |
|  | Load our pretrained checkpoints and play with sampling, likelihood computation, and controllable synthesis (JAX + FLAX) |
|  | Tutorial of score-based generative modeling with SDEs in PyTorch |
|  | Load our pretrained checkpoints and play with sampling, likelihood computation, and controllable synthesis (PyTorch) |
| [Code in JAX](https://github.com/yang-song/score_sde) | Score SDE codebase in JAX + FLAX |
| [Code in PyTorch](https://github.com/yang-song/score_sde_pytorch) | Score SDE codebase in PyTorch |

### Perturbing data with an SDE

When the number of noise scales approaches infinity, we essentially perturb the data distribution with continuously growing levels of noise. In this case, the noise perturbation procedure is a continuous-time [stochastic process](https://en.wikipedia.org/wiki/Stochastic_process#:~:text=A%20stochastic%20process%20is%20defined,measurable%20with%20respect%20to%20some), as demonstrated below

![](https://yang-song.net/assets/img/score/perturb_vp.gif)

Perturbing data to noise with a continuous-time stochastic process.

How can we represent a stochastic process in a concise way? Many stochastic processes ([diffusion processes](https://en.wikipedia.org/wiki/Diffusion_process) in particular) are solutions of stochastic differential equations (SDEs). In general, an SDE possesses the following form:

$$
(\text{8}) d \mathbf{x} = \mathbf{f} \left(\right. \mathbf{x} , t \left.\right) d t + g \left(\right. t \left.\right) d \mathbf{w} ,
$$

where $\mathbf{f} \left(\right. \cdot , t \left.\right) : \mathbb{R}^{d} \rightarrow \mathbb{R}^{d}$ is a vector-valued function called the drift coefficient, $g \left(\right. t \left.\right) \in \mathbb{R}$ is a real-valued function called the diffusion coefficient, $\mathbf{w}$ denotes a standard [Brownian motion](https://en.wikipedia.org/wiki/Brownian_motion), and $d \mathbf{w}$ can be viewed as infinitesimal white noise. The solution of a stochastic differential equation is a continuous collection of random variables $\left{\right. \mathbf{x} \left(\right. t \left.\right) \left.\right}_{t \in \left[\right. 0 , T \left]\right.}$. These random variables trace stochastic trajectories as the time index $t$ grows from the start time $0$ to the end time $T$. Let $p_{t} \left(\right. \mathbf{x} \left.\right)$ denote the (marginal) probability density function of $\mathbf{x} \left(\right. t \left.\right)$. Here $t \in \left[\right. 0 , T \left]\right.$ is analogous to $i = 1 , 2 , \hdots , L$ when we had a finite number of noise scales, and $p_{t} \left(\right. \mathbf{x} \left.\right)$ is analogous to $p_{\sigma_{i}} \left(\right. \mathbf{x} \left.\right)$. Clearly, $p_{0} \left(\right. \mathbf{x} \left.\right) = p \left(\right. \mathbf{x} \left.\right)$ is the data distribution since no perturbation is applied to data at $t = 0$. After perturbing $p \left(\right. \mathbf{x} \left.\right)$ with the stochastic process for a sufficiently long time $T$, $p_{T} \left(\right. \mathbf{x} \left.\right)$ becomes close to a tractable noise distribution $\pi \left(\right. \mathbf{x} \left.\right)$, called a **prior distribution**. We note that $p_{T} \left(\right. \mathbf{x} \left.\right)$ is analogous to $p_{\sigma_{L}} \left(\right. \mathbf{x} \left.\right)$ in the case of finite noise scales, which corresponds to applying the largest noise perturbation $\sigma_{L}$ to the data.

The SDE in $(\text{8})$ is **hand designed**, similarly to how we hand-designed $\sigma_{1} < \sigma_{2} < \hdots < \sigma_{L}$ in the case of finite noise scales. There are numerous ways to add noise perturbations, and the choice of SDEs is not unique. For example, the following SDE

$$
(\text{9}) d \mathbf{x} = e^{t} d \mathbf{w}
$$

perturbs data with a Gaussian noise of mean zero and exponentially growing variance, which is analogous to perturbing data with $\mathcal{N} \left(\right. 0 , \sigma_{1}^{2} I \left.\right) , \mathcal{N} \left(\right. 0 , \sigma_{2}^{2} I \left.\right) , \hdots , \mathcal{N} \left(\right. 0 , \sigma_{L}^{2} I \left.\right)$ when $\sigma_{1} < \sigma_{2} < \hdots < \sigma_{L}$ is a [geometric progression](https://en.wikipedia.org/wiki/Geometric_progression#:~:text=In%20mathematics%2C%20a%20geometric%20progression,number%20called%20the%20common%20ratio.). Therefore, the SDE should be viewed as part of the model, much like $\left{\right. \sigma_{1} , \sigma_{2} , \hdots , \sigma_{L} \left.\right}$. In

- **Score-Based Generative Modeling through Stochastic Differential Equations**   [\[link\]](https://openreview.net/forum?id=PxTIG12RRHS)  
	Y. Song, J. Sohl-Dickstein, D.P. Kingma, A. Kumar, S. Ermon, B. Poole.  
	International Conference on Learning Representations. 2021.

\[21\]

, we provide three SDEs that generally work well for images: the Variance Exploding SDE (VE SDE), the Variance Preserving SDE (VP SDE), and the sub-VP SDE.

### Reversing the SDE for sample generation

Recall that with a finite number of noise scales, we can generate samples by reversing the perturbation process with **annealed Langevin dynamics**, i.e., sequentially sampling from each noise-perturbed distribution using Langevin dynamics. For infinite noise scales, we can analogously reverse the perturbation process for sample generation by using the reverse SDE.

![](https://yang-song.net/assets/img/score/denoise_vp.gif)

Generate data from noise by reversing the perturbation procedure.

Importantly, any SDE has a corresponding reverse SDE

- **Reverse-time diffusion equation models**  
	B.D. Anderson.  
	Stochastic Processes and their Applications, Vol 12(3), pp. 313--326. Elsevier. 1982.

\[35\]

, whose closed form is given by

$$
(\text{10}) d \mathbf{x} = \left[\right. \mathbf{f} \left(\right. \mathbf{x} , t \left.\right) - g^{2} \left(\right. t \left.\right) \nabla_{\mathbf{x}} log ⁡ p_{t} \left(\right. \mathbf{x} \left.\right) \left]\right. d t + g \left(\right. t \left.\right) d \mathbf{w} .
$$

Here $d t$ represents a negative infinitesimal time step, since the SDE $(\text{10})$ needs to be solved backwards in time (from $t = T$ to $t = 0$). In order to compute the reverse SDE, we need to estimate $\nabla_{\mathbf{x}} log ⁡ p_{t} \left(\right. \mathbf{x} \left.\right)$, which is exactly the **score function** of $p_{t} \left(\right. \mathbf{x} \left.\right)$.

![](https://yang-song.net/assets/img/score/sde_schematic.jpg)

Solving a reverse SDE yields a score-based generative model. Transforming data to a simple noise distribution can be accomplished with an SDE. It can be reversed to generate samples from noise if we know the score of the distribution at each intermediate time step.

### Estimating the reverse SDE with score-based models and score matching

Solving the reverse SDE requires us to know the terminal distribution $p_{T} \left(\right. \mathbf{x} \left.\right)$, and the score function $\nabla_{\mathbf{x}} log ⁡ p_{t} \left(\right. \mathbf{x} \left.\right)$. By design, the former is close to the prior distribution $\pi \left(\right. \mathbf{x} \left.\right)$ which is fully tractable. In order to estimate $\nabla_{\mathbf{x}} log ⁡ p_{t} \left(\right. \mathbf{x} \left.\right)$, we train a **Time-Dependent Score-Based Model** $\mathbf{s}_{\theta} \left(\right. \mathbf{x} , t \left.\right)$, such that $\mathbf{s}_{\theta} \left(\right. \mathbf{x} , t \left.\right) \approx \nabla_{\mathbf{x}} log ⁡ p_{t} \left(\right. \mathbf{x} \left.\right)$. This is analogous to the noise-conditional score-based model $\mathbf{s}_{\theta} \left(\right. \mathbf{x} , i \left.\right)$ used for finite noise scales, trained such that $\mathbf{s}_{\theta} \left(\right. \mathbf{x} , i \left.\right) \approx \nabla_{\mathbf{x}} log ⁡ p_{\sigma_{i}} \left(\right. \mathbf{x} \left.\right)$.

Our training objective for $\mathbf{s}_{\theta} \left(\right. \mathbf{x} , t \left.\right)$ is a continuous weighted combination of Fisher divergences, given by

$$
(\text{11}) \mathbb{E}_{t \in \mathcal{U} \left(\right. 0 , T \left.\right)} \mathbb{E}_{p_{t} \left(\right. \mathbf{x} \left.\right)} \left[\right. \lambda \left(\right. t \left.\right) \parallel \nabla_{\mathbf{x}} log ⁡ p_{t} \left(\right. \mathbf{x} \left.\right) - \mathbf{s}_{\theta} \left(\right. \mathbf{x} , t \left.\right) \parallel_{2}^{2} \left]\right. ,
$$

where $\mathcal{U} \left(\right. 0 , T \left.\right)$ denotes a uniform distribution over the time interval $\left[\right. 0 , T \left]\right.$, and $\lambda : \mathbb{R} \rightarrow \mathbb{R}_{> 0}$ is a positive weighting function. Typically we use $\lambda \left(\right. t \left.\right) \propto 1 / \mathbb{E} \left[\right. \parallel \nabla_{\mathbf{x} \left(\right. t \left.\right)} log ⁡ p \left(\right. \mathbf{x} \left(\right. t \left.\right) \mid \mathbf{x} \left(\right. 0 \left.\right) \left.\right) \parallel_{2}^{2} \left]\right.$ to balance the magnitude of different score matching losses across time.

As before, our weighted combination of Fisher divergences can be efficiently optimized with score matching methods, such as denoising score matching

- **A connection between score matching and denoising autoencoders**  
	P. Vincent.  
	Neural computation, Vol 23(7), pp. 1661--1674. MIT Press. 2011.

\[17\]

and sliced score matching

- **Sliced score matching: A scalable approach to density and score estimation**   [\[PDF\]](http://arxiv.org/pdf/1905.07088.pdf)  
	Y. Song, S. Garg, J. Shi, S. Ermon.  
	Uncertainty in Artificial Intelligence, pp. 574--584. 2020.

\[31\]

. Once our score-based model $\mathbf{s}_{\theta} \left(\right. \mathbf{x} , t \left.\right)$ is trained to optimality, we can plug it into the expression of the reverse SDE in $(\text{10})$ to obtain an estimated reverse SDE.

$$
(\text{12}) d \mathbf{x} = \left[\right. \mathbf{f} \left(\right. \mathbf{x} , t \left.\right) - g^{2} \left(\right. t \left.\right) \mathbf{s}_{\theta} \left(\right. \mathbf{x} , t \left.\right) \left]\right. d t + g \left(\right. t \left.\right) d \mathbf{w} .
$$

We can start with $\mathbf{x} \left(\right. T \left.\right) sim \pi$, and solve the above reverse SDE to obtain a sample $\mathbf{x} \left(\right. 0 \left.\right)$. Let us denote the distribution of $\mathbf{x} \left(\right. 0 \left.\right)$ obtained in such way as $p_{\theta}$. When the score-based model $\mathbf{s}_{\theta} \left(\right. \mathbf{x} , t \left.\right)$ is well-trained, we have $p_{\theta} \approx p_{0}$, in which case $\mathbf{x} \left(\right. 0 \left.\right)$ is an approximate sample from the data distribution $p_{0}$.

When $\lambda \left(\right. t \left.\right) = g^{2} \left(\right. t \left.\right)$, we have an important connection between our weighted combination of Fisher divergences and the KL divergence from $p_{0}$ to $p_{\theta}$ under some regularity conditions

- **Maximum Likelihood Training of Score-Based Diffusion Models**  
	Y. Song, C. Durkan, I. Murray, S. Ermon.  
	Advances in Neural Information Processing Systems (NeurIPS). 2021.

\[36\]

:

$$
KL ⁡ \left(\right. p_{0} \left(\right. \mathbf{x} \left.\right) \parallel p_{\theta} \left(\right. \mathbf{x} \left.\right) \left.\right) \leq \frac{T}{2} \mathbb{E}_{t \in \mathcal{U} \left(\right. 0 , T \left.\right)} \mathbb{E}_{p_{t} \left(\right. \mathbf{x} \left.\right)} \left[\right. \lambda \left(\right. t \left.\right) \parallel \nabla_{\mathbf{x}} log ⁡ p_{t} \left(\right. \mathbf{x} \left.\right) - \mathbf{s}_{\theta} \left(\right. \mathbf{x} , t \left.\right) \parallel_{2}^{2} \left]\right. \\ (\text{13}) + KL ⁡ \left(\right. p_{T} \parallel \pi \left.\right) .
$$

Due to this special connection to the KL divergence and the equivalence between minimizing KL divergences and maximizing likelihood for model training, we call $\lambda \left(\right. t \left.\right) = g \left(\right. t \left.\right)^{2}$ the **likelihood weighting function**. Using this likelihood weighting function, we can train score-based generative models to achieve very high likelihoods, comparable or even superior to state-of-the-art autoregressive models

- **Maximum Likelihood Training of Score-Based Diffusion Models**  
	Y. Song, C. Durkan, I. Murray, S. Ermon.  
	Advances in Neural Information Processing Systems (NeurIPS). 2021.

\[36\]

.

### How to solve the reverse SDE

By solving the estimated reverse SDE with numerical SDE solvers, we can simulate the reverse stochastic process for sample generation. Perhaps the simplest numerical SDE solver is the [Euler-Maruyama method](https://en.wikipedia.org/wiki/Euler%E2%80%93Maruyama_method). When applied to our estimated reverse SDE, it discretizes the SDE using finite time steps and small Gaussian noise. Specifically, it chooses a small negative time step $\Delta t \approx 0$, initializes $t \leftarrow T$, and iterates the following procedure until $t \approx 0$:

$$
\Delta \mathbf{x} & \leftarrow \left[\right. \mathbf{f} \left(\right. \mathbf{x} , t \left.\right) - g^{2} \left(\right. t \left.\right) \mathbf{s}_{\theta} \left(\right. \mathbf{x} , t \left.\right) \left]\right. \Delta t + g \left(\right. t \left.\right) \sqrt{\left|\right. \Delta t \left|\right.} \mathbf{z}_{t} \\ \mathbf{x} & \leftarrow \mathbf{x} + \Delta \mathbf{x} \\ t & \leftarrow t + \Delta t ,
$$

Here $\mathbf{z}_{t} sim \mathcal{N} \left(\right. 0 , I \left.\right)$. The Euler-Maruyama method is qualitatively similar to Langevin dynamics—both update $\mathbf{x}$ by following score functions perturbed with Gaussian noise.

Aside from the Euler-Maruyama method, other numerical SDE solvers can be directly employed to solve the reverse SDE for sample generation, including, for example, [Milstein method](https://en.wikipedia.org/wiki/Milstein_method), and [stochastic Runge-Kutta methods](https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_method_\(SDE\)). In

- **Score-Based Generative Modeling through Stochastic Differential Equations**   [\[link\]](https://openreview.net/forum?id=PxTIG12RRHS)  
	Y. Song, J. Sohl-Dickstein, D.P. Kingma, A. Kumar, S. Ermon, B. Poole.  
	International Conference on Learning Representations. 2021.

\[21\]

, we provided a reverse diffusion solver similar to Euler-Maruyama, but more tailored for solving reverse-time SDEs. More recently, authors in

- **Gotta Go Fast When Generating Data with Score-Based Models**  
	A. Jolicoeur-Martineau, K. Li, R. Piche-Taillefer, T. Kachman, I. Mitliagkas.  
	arXiv preprint arXiv:2105.14080. 2021.

\[37\]

introduced adaptive step-size SDE solvers that can generate samples faster with better quality.

In addition, there are two special properties of our reverse SDE that allow for even more flexible sampling methods:

- We have an estimate of $\nabla_{\mathbf{x}} log ⁡ p_{t} \left(\right. \mathbf{x} \left.\right)$ via our time-dependent score-based model $\mathbf{s}_{\theta} \left(\right. \mathbf{x} , t \left.\right)$.
- We only care about sampling from each marginal distribution $p_{t} \left(\right. \mathbf{x} \left.\right)$. Samples obtained at different time steps can have arbitrary correlations and do not have to form a particular trajectory sampled from the reverse SDE.

As a consequence of these two properties, we can apply MCMC approaches to fine-tune the trajectories obtained from numerical SDE solvers. Specifically, we propose **Predictor-Corrector samplers**. The **predictor** can be any numerical SDE solver that predicts $\mathbf{x} \left(\right. t + \Delta t \left.\right) sim p_{t + \Delta t} \left(\right. \mathbf{x} \left.\right)$ from an existing sample $\mathbf{x} \left(\right. t \left.\right) sim p_{t} \left(\right. \mathbf{x} \left.\right)$. The **corrector** can be any MCMC procedure that solely relies on the score function, such as Langevin dynamics and Hamiltonian Monte Carlo.

At each step of the Predictor-Corrector sampler, we first use the predictor to choose a proper step size $\Delta t < 0$, and then predict $\mathbf{x} \left(\right. t + \Delta t \left.\right)$ based on the current sample $\mathbf{x} \left(\right. t \left.\right)$. Next, we run several corrector steps to improve the sample $\mathbf{x} \left(\right. t + \Delta t \left.\right)$ according to our score-based model $\mathbf{s}_{\theta} \left(\right. \mathbf{x} , t + \Delta t \left.\right)$, so that $\mathbf{x} \left(\right. t + \Delta t \left.\right)$ becomes a higher-quality sample from $p_{t + \Delta t} \left(\right. \mathbf{x} \left.\right)$.

With Predictor-Corrector methods and better architectures of score-based models, we can achieve **state-of-the-art** sample quality on CIFAR-10 (measured in FID

- **GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium**  
	M. Heusel, H. Ramsauer, T. Unterthiner, B. Nessler, S. Hochreiter.  
	Advances in Neural Information Processing Systems 30: Annual Conference on Neural Information Processing Systems 2017, December 4-9, 2017, Long Beach, CA, {USA}, pp. 6626--6637. 2017.

\[38\]

and Inception scores

- **Improved techniques for training gans**  
	T. Salimans, I. Goodfellow, W. Zaremba, V. Cheung, A. Radford, X. Chen.  
	Advances in Neural Information Processing Systems, pp. 2226--2234. 2016.

\[12\]

), outperforming the best GAN model to date (StyleGAN2 + ADA

- **Training Generative Adversarial Networks with Limited Data**  
	T. Karras, M. Aittala, J. Hellsten, S. Laine, J. Lehtinen, T. Aila.  
	Proc. NeurIPS. 2020.

\[39\]

).

| Method | FID $\downarrow$ | Inception score $\uparrow$ |
| --- | --- | --- |
| StyleGAN2 + ADA  - **Training Generative Adversarial Networks with Limited Data**   	T. Karras, M. Aittala, J. Hellsten, S. Laine, J. Lehtinen, T. Aila.   	Proc. NeurIPS. 2020.  \[39\] | 2.92 | 9.83 |
| Ours  - **Score-Based Generative Modeling through Stochastic Differential Equations**   [\[link\]](https://openreview.net/forum?id=PxTIG12RRHS)   	Y. Song, J. Sohl-Dickstein, D.P. Kingma, A. Kumar, S. Ermon, B. Poole.   	International Conference on Learning Representations. 2021.  \[21\] | **2.20** | **9.89** |

The sampling methods are also scalable for extremely high dimensional data. For example, it can successfully generate high fidelity images of resolution $1024 \times 1024$.

![](https://yang-song.net/assets/img/score/ffhq_1024.jpeg)

1024 x 1024 samples from a score-based model trained on the FFHQ dataset.

Some additional (uncurated) samples for other datasets (taken from this [GitHub repo](https://github.com/yang-song/score_sde)):

![](https://yang-song.net/assets/img/score/bedroom.jpeg)

256 x 256 samples on LSUN bedroom.

![](https://yang-song.net/assets/img/score/celebahq_256.jpg)

256 x 256 samples on CelebA-HQ.

### Probability flow ODE

Despite capable of generating high-quality samples, samplers based on Langevin MCMC and SDE solvers do not provide a way to compute the exact log-likelihood of score-based generative models. Below, we introduce a sampler based on ordinary differential equations (ODEs) that allow for exact likelihood computation.

In

- **Score-Based Generative Modeling through Stochastic Differential Equations**   [\[link\]](https://openreview.net/forum?id=PxTIG12RRHS)  
	Y. Song, J. Sohl-Dickstein, D.P. Kingma, A. Kumar, S. Ermon, B. Poole.  
	International Conference on Learning Representations. 2021.

\[21\]

, we show t is possible to convert any SDE into an ordinary differential equation (ODE) without changing its marginal distributions $\left{\right. p_{t} \left(\right. \mathbf{x} \left.\right) \left.\right}_{t \in \left[\right. 0 , T \left]\right.}$. Thus by solving this ODE, we can sample from the same distributions as the reverse SDE. The corresponding ODE of an SDE is named **probability flow ODE**

- **Score-Based Generative Modeling through Stochastic Differential Equations**   [\[link\]](https://openreview.net/forum?id=PxTIG12RRHS)  
	Y. Song, J. Sohl-Dickstein, D.P. Kingma, A. Kumar, S. Ermon, B. Poole.  
	International Conference on Learning Representations. 2021.

\[21\]

, given by

$$
(\text{14}) d \mathbf{x} = \left[\right. \mathbf{f} \left(\right. \mathbf{x} , t \left.\right) - \frac{1}{2} g^{2} \left(\right. t \left.\right) \nabla_{\mathbf{x}} log ⁡ p_{t} \left(\right. \mathbf{x} \left.\right) \left]\right. d t .
$$

The following figure depicts trajectories of both SDEs and probability flow ODEs. Although ODE trajectories are noticeably smoother than SDE trajectories, they convert the same data distribution to the same prior distribution and vice versa, sharing the same set of marginal distributions $\left{\right. p_{t} \left(\right. \mathbf{x} \left.\right) \left.\right}_{t \in \left[\right. 0 , T \left]\right.}$. In other words, trajectories obtained by solving the probability flow ODE have the same marginal distributions as the SDE trajectories.

![](https://yang-song.net/assets/img/score/teaser.jpg)

We can map data to a noise distribution (the prior) with an SDE, and reverse this SDE for generative modeling. We can also reverse the associated probability flow ODE, which yields a deterministic process that samples from the same distribution as the SDE. Both the reverse-time SDE and probability flow ODE can be obtained by estimating score functions.

This probability flow ODE formulation has several unique advantages.

When $\nabla_{\mathbf{x}} log ⁡ p_{t} \left(\right. \mathbf{x} \left.\right)$ is replaced by its approximation $\mathbf{s}_{\theta} \left(\right. \mathbf{x} , t \left.\right)$, the probability flow ODE becomes a special case of a neural ODE

- **Neural Ordinary Differential Equations**  
	T.Q. Chen, Y. Rubanova, J. Bettencourt, D. Duvenaud.  
	Advances in Neural Information Processing Systems 31: Annual Conference on Neural Information Processing Systems 2018, NeurIPS 2018, December 3-8, 2018, Montr{\\'{e}}al, Canada, pp. 6572--6583. 2018.

\[40\]

. In particular, it is an example of continuous normalizing flows

- **Scalable Reversible Generative Models with Free-form Continuous Dynamics**   [\[link\]](https://openreview.net/forum?id=rJxgknCcK7)  
	W. Grathwohl, R.T.Q. Chen, J. Bettencourt, D. Duvenaud.  
	International Conference on Learning Representations. 2019.

\[41\]

, since the probability flow ODE converts a data distribution $p_{0} \left(\right. \mathbf{x} \left.\right)$ to a prior noise distribution $p_{T} \left(\right. \mathbf{x} \left.\right)$ (since it shares the same marginal distributions as the SDE) and is fully invertible.

As such, the probability flow ODE inherits all properties of neural ODEs or continuous normalizing flows, including exact log-likelihood computation. Specifically, we can leverage the instantaneous change-of-variable formula (Theorem 1 in

- **Neural Ordinary Differential Equations**  
	T.Q. Chen, Y. Rubanova, J. Bettencourt, D. Duvenaud.  
	Advances in Neural Information Processing Systems 31: Annual Conference on Neural Information Processing Systems 2018, NeurIPS 2018, December 3-8, 2018, Montr{\\'{e}}al, Canada, pp. 6572--6583. 2018.

\[40\]

, Equation (4) in

- **Scalable Reversible Generative Models with Free-form Continuous Dynamics**   [\[link\]](https://openreview.net/forum?id=rJxgknCcK7)  
	W. Grathwohl, R.T.Q. Chen, J. Bettencourt, D. Duvenaud.  
	International Conference on Learning Representations. 2019.

\[41\]

) to compute the unknown data density $p_{0}$ from the known prior density $p_{T}$ with numerical ODE solvers.

In fact, our model achieves the **state-of-the-art** log-likelihoods on uniformly dequantized

[^4]

CIFAR-10 images

- **Score-Based Generative Modeling through Stochastic Differential Equations**   [\[link\]](https://openreview.net/forum?id=PxTIG12RRHS)  
	Y. Song, J. Sohl-Dickstein, D.P. Kingma, A. Kumar, S. Ermon, B. Poole.  
	International Conference on Learning Representations. 2021.

\[21\]

, **even without maximum likelihood training**.

| Method | Negative log-likelihood (bits/dim) $\downarrow$ |
| --- | --- |
| RealNVP | 3.49 |
| iResNet | 3.45 |
| Glow | 3.35 |
| FFJORD | 3.40 |
| Flow++ | 3.29 |
| Ours | **2.99** |

When training score-based models with the **likelihood weighting** we discussed before, and using **variational dequantization** to obtain likelihoods on discrete images, we can achieve comparable or even superior likelihood to the state-of-the-art autoregressive models (all without any data augmentation)

- **Maximum Likelihood Training of Score-Based Diffusion Models**  
	Y. Song, C. Durkan, I. Murray, S. Ermon.  
	Advances in Neural Information Processing Systems (NeurIPS). 2021.

\[36\]

.

| Method | Negative log-likelihood (bits/dim) $\downarrow$ on CIFAR-10 | Negative log-likelihood (bits/dim) $\downarrow$ on ImageNet 32x32 |
| --- | --- | --- |
| Sparse Transformer | **2.80** | \- |
| Image Transformer | 2.90 | 3.77 |
| Ours | 2.83 | **3.76** |

### Controllable generation for inverse problem solving

Score-based generative models are particularly suitable for solving inverse problems. At its core, inverse problems are same as Bayesian inference problems. Let $\mathbf{x}$ and $\mathbf{y}$ be two random variables, and suppose we know the forward process of generating $\mathbf{y}$ from $\mathbf{x}$, represented by the transition probability distribution $p \left(\right. \mathbf{y} \mid \mathbf{x} \left.\right)$. The inverse problem is to compute $p \left(\right. \mathbf{x} \mid \mathbf{y} \left.\right)$. From Bayes’ rule, we have $p \left(\right. \mathbf{x} \mid \mathbf{y} \left.\right) = p \left(\right. \mathbf{x} \left.\right) p \left(\right. \mathbf{y} \mid \mathbf{x} \left.\right) / \int p \left(\right. \mathbf{x} \left.\right) p \left(\right. \mathbf{y} \mid \mathbf{x} \left.\right) d \mathbf{x}$. This expression can be greatly simplified by taking gradients with respect to $\mathbf{x}$ on both sides, leading to the following Bayes’ rule for score functions:

$$
(\text{15}) \nabla_{\mathbf{x}} log ⁡ p \left(\right. \mathbf{x} \mid \mathbf{y} \left.\right) = \nabla_{\mathbf{x}} log ⁡ p \left(\right. \mathbf{x} \left.\right) + \nabla_{\mathbf{x}} log ⁡ p \left(\right. \mathbf{y} \mid \mathbf{x} \left.\right) .
$$

Through score matching, we can train a model to estimate the score function of the unconditional data distribution, i.e., $\mathbf{s}_{\theta} \left(\right. \mathbf{x} \left.\right) \approx \nabla_{\mathbf{x}} log ⁡ p \left(\right. \mathbf{x} \left.\right)$. This will allow us to easily compute the posterior score function $\nabla_{\mathbf{x}} log ⁡ p \left(\right. \mathbf{x} \mid \mathbf{y} \left.\right)$ from the known forward process $p \left(\right. \mathbf{y} \mid \mathbf{x} \left.\right)$ via equation $(\text{15})$, and sample from it with Langevin-type sampling

- **Score-Based Generative Modeling through Stochastic Differential Equations**   [\[link\]](https://openreview.net/forum?id=PxTIG12RRHS)  
	Y. Song, J. Sohl-Dickstein, D.P. Kingma, A. Kumar, S. Ermon, B. Poole.  
	International Conference on Learning Representations. 2021.

\[21\]

.

A recent work from UT Austin

- **Robust Compressed Sensing MRI with Deep Generative Priors**  
	A. Jalal, M. Arvinte, G. Daras, E. Price, A.G. Dimakis, J.I. Tamir.  
	Advances in neural information processing systems. 2021.

\[29\]

has demonstrated that score-based generative models can be applied to solving inverse problems in medical imaging, such as accelerating magnetic resonance imaging (MRI). Concurrently in

- **Solving Inverse Problems in Medical Imaging with Score-Based Generative Models**   [\[PDF\]](http://arxiv.org/pdf/2111.08005.pdf)  
	Y. Song, L. Shen, L. Xing, S. Ermon.  
	International Conference on Learning Representations. 2022.

\[42\]

, we demonstrated superior performance of score-based generative models not only on accelerated MRI, but also sparse-view computed tomography (CT). We were able to achieve comparable or even better performance than supervised or unrolled deep learning approaches, while being more robust to different measurement processes at test time.

Below we show some examples on solving inverse problems for computer vision.

![](https://yang-song.net/assets/img/score/class_cond.png)

Class-conditional generation with an unconditional time-dependent score-based model, and a pre-trained noise-conditional image classifier on CIFAR-10.

![](https://yang-song.net/assets/img/score/inpainting.png)

Image inpainting with a time-dependent score-based model trained on LSUN bedroom. The leftmost column is ground-truth. The second column shows masked images (y in our framework). The rest columns show different inpainted images, generated by solving the conditional reverse-time SDE.

![](https://yang-song.net/assets/img/score/colorization.png)

Image colorization with a time-dependent score-based model trained on LSUN church\_outdoor and bedroom. The leftmost column is ground-truth. The second column shows gray-scale images (y in our framework). The rest columns show different colorizedimages, generated by solving the conditional reverse-time SDE.

![](https://yang-song.net/assets/img/score/lincoln.png)

We can even colorize gray-scale portrays of famous people in history (Abraham Lincoln) with a time-dependent score-based model trained on FFHQ. The image resolution is 1024 x 1024.

## Connection to diffusion models and others

I started working on score-based generative modeling since 2019, when I was trying hard to make score matching scalable for training deep energy-based models on high-dimensional datasets. My first attempt at this led to the method sliced score matching

- **Sliced score matching: A scalable approach to density and score estimation**   [\[PDF\]](http://arxiv.org/pdf/1905.07088.pdf)  
	Y. Song, S. Garg, J. Shi, S. Ermon.  
	Uncertainty in Artificial Intelligence, pp. 574--584. 2020.

\[31\]

. Despite the scalability of sliced score matching for training energy-based models, I found to my surprise that Langevin sampling from those models fails to produce reasonable samples even on the MNIST dataset. I started investigating this issue and discovered three crucial improvements that can lead to extremely good samples: (1) perturbing data with multiple scales of noise, and training score-based models for each noise scale; (2) using a U-Net architecture (we used RefineNet since it is a modern version of U-Nets) for the score-based model; (3) applying Langevin MCMC to each noise scale and chaining them together. With those methods, I was able to obtain the state-of-the-art Inception Score on CIFAR-10 in

- **Generative Modeling by Estimating Gradients of the Data Distribution**   [\[PDF\]](http://arxiv.org/pdf/1907.05600.pdf)  
	Y. Song, S. Ermon.  
	Advances in Neural Information Processing Systems, pp. 11895--11907. 2019.

\[18\]

(even better than the best GANs!), and generate high-fidelity image samples of resolution up to

$256\times 256$

in

- **Improved Techniques for Training Score-Based Generative Models**   [\[PDF\]](http://arxiv.org/pdf/2006.09011.pdf)  
	Y. Song, S. Ermon.  
	Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual. 2020.

\[19\]

.

The idea of perturbing data with multiple scales of noise is by no means unique to score-based generative models though. It has been previously used in, for example, [simulated annealing](https://en.wikipedia.org/wiki/Simulated_annealing), annealed importance sampling

- **Annealed importance sampling**  
	R.M. Neal.  
	Statistics and computing, Vol 11(2), pp. 125--139. Springer. 2001.

\[43\]

, diffusion probabilistic models

- **Deep unsupervised learning using nonequilibrium thermodynamics**  
	J. Sohl-Dickstein, E. Weiss, N. Maheswaranathan, S. Ganguli.  
	International Conference on Machine Learning, pp. 2256--2265. 2015.

\[44\]

, infusion training

- **Learning to generate samples from noise through infusion training**  
	F. Bordes, S. Honari, P. Vincent.  
	arXiv preprint arXiv:1703.06975. 2017.

\[45\]

, and variational walkback

- **Variational walkback: Learning a transition operator as a stochastic recurrent net**  
	A. Goyal, N.R. Ke, S. Ganguli, Y. Bengio.  
	arXiv preprint arXiv:1711.02282. 2017.

\[46\]

for generative stochastic networks

- **GSNs: generative stochastic networks**  
	G. Alain, Y. Bengio, L. Yao, J. Yosinski, E. Thibodeau-Laufer, S. Zhang, P. Vincent.  
	Information and Inference: A Journal of the IMA, Vol 5(2), pp. 210--249. Oxford University Press. 2016.

\[47\]

. Out of all these works, diffusion probabilistic modeling is perhaps the closest to score-based generative modeling. Diffusion probabilistic models are hierachical latent variable models first proposed by [Jascha](http://www.sohldickstein.com/) and his colleagues

- **Deep unsupervised learning using nonequilibrium thermodynamics**  
	J. Sohl-Dickstein, E. Weiss, N. Maheswaranathan, S. Ganguli.  
	International Conference on Machine Learning, pp. 2256--2265. 2015.

\[44\]

in 2015, which generate samples by learning a variational decoder to reverse a discrete diffusion process that perturbs data to noise. Without awareness of this work, score-based generative modeling was proposed and motivated independently from a very different perspective. Despite both perturbing data with multiple scales of noise, the connection between score-based generative modeling and diffusion probabilistic modeling seemed superficial at that time, since the former is trained by score matching and sampled by Langevin dynamics, while the latter is trained by the evidence lower bound (ELBO) and sampled with a learned decoder.

In 2020, [Jonathan Ho](http://www.jonathanho.me/) and colleagues

- **Denoising diffusion probabilistic models**  
	J. Ho, A. Jain, P. Abbeel.  
	arXiv preprint arXiv:2006.11239. 2020.

\[20\]

significantly improved the empirical performance of diffusion probabilistic models and first unveiled a deeper connection to score-based generative modeling. They showed that the ELBO used for training diffusion probabilistic models is essentially equivalent to the weighted combination of score matching objectives used in score-based generative modeling. Moreover, by parameterizing the decoder as a sequence of score-based models with a U-Net architecture, they demonstrated for the first time that diffusion probabilistic models can also generate high quality image samples comparable or superior to GANs.

Inspired by their work, we further investigated the relationship between diffusion models and score-based generative models in an ICLR 2021 paper

- **Score-Based Generative Modeling through Stochastic Differential Equations**   [\[link\]](https://openreview.net/forum?id=PxTIG12RRHS)  
	Y. Song, J. Sohl-Dickstein, D.P. Kingma, A. Kumar, S. Ermon, B. Poole.  
	International Conference on Learning Representations. 2021.

\[21\]

. We found that the sampling method of diffusion probabilistic models can be integrated with annealed Langevin dynamics of score-based models to create a unified and more powerful sampler (the Predictor-Corrector sampler). By generalizing the number of noise scales to infinity, we further proved that score-based generative models and diffusion probabilistic models can both be viewed as discretizations to stochastic differential equations determined by score functions. This work bridges both score-based generative modeling and diffusion probabilistic modeling into a unified framework.

Collectively, these latest developments seem to indicate that both score-based generative modeling with multiple noise perturbations and diffusion probabilistic models are different perspectives of the same model family, much like how [wave mechanics](https://en.wikipedia.org/wiki/Wave_mechanics) and [matrix mechanics](https://en.wikipedia.org/wiki/Matrix_mechanics) are equivalent formulations of quantum mechanics in the history of physics

[^5]

. The perspective of score matching and score-based models allows one to calculate log-likelihoods exactly, solve inverse problems naturally, and is directly connected to energy-based models, Schrödinger bridges and optimal transport

- **Diffusion Schrödinger Bridge with Applications to Score-Based Generative Modeling**  
	V. De Bortoli, J. Thornton, J. Heng, A. Doucet.  
	Advances in Neural Information Processing Systems (NeurIPS). 2021.

\[48\]

. The perspective of diffusion models is naturally connected to VAEs, lossy compression, and can be directly incorporated with variational probabilistic inference. This blog post focuses on the first perspective, but I highly recommend interested readers to learn about the alternative perspective of diffusion models as well (see [a great blog by Lilian Weng](https://lilianweng.github.io/lil-log/2021/07/11/diffusion-models.html)).

Many recent works on score-based generative models or diffusion probabilistic models have been deeply influenced by knowledge from both sides of research (see a [website](https://scorebasedgenerativemodeling.github.io/) curated by researchers at the University of Oxford). Despite this deep connection between score-based generative models and diffusion models, it is hard to come up with an umbrella term for the model family that they both belong to. Some colleagues in DeepMind propose to call them “Generative Diffusion Processes”. It remains to be seen if this will be adopted by the community in the future.

## Concluding remarks

This blog post gives a detailed introduction to score-based generative models. We demonstrate that this new paradigm of generative modeling is able to produce high quality samples, compute exact log-likelihoods, and perform controllable generation for inverse problem solving. It is a compilation of several papers we published in the past few years. Please visit them if you are interested in more details:

- [Yang Song\*, Sahaj Garg\*, Jiaxin Shi, and Stefano Ermon. *Sliced Score Matching: A Scalable Approach to Density and Score Estimation*. UAI 2019 (Oral)](https://arxiv.org/abs/1905.07088)
- [Yang Song, and Stefano Ermon. *Generative Modeling by Estimating Gradients of the Data Distribution*. NeurIPS 2019 (Oral)](https://arxiv.org/abs/1907.05600)
- [Yang Song, and Stefano Ermon. *Improved Techniques for Training Score-Based Generative Models*. NeurIPS 2020](https://arxiv.org/abs/2006.09011)
- [Yang Song, Jascha Sohl-Dickstein, Diederik P. Kingma, Abhishek Kumar, Stefano Ermon, and Ben Poole. *Score-Based Generative Modeling through Stochastic Differential Equations*. ICLR 2021 (Outstanding Paper Award)](https://arxiv.org/abs/2011.13456)
- [Yang Song\*, Conor Durkan\*, Iain Murray, and Stefano Ermon. *Maximum Likelihood Training of Score-Based Diffusion Models*. NeurIPS 2021 (Spotlight)](https://arxiv.org/abs/2101.09258)
- [Yang Song\*, Liyue Shen\*, Lei Xing, and Stefano Ermon. *Solving Inverse Problems in Medical Imaging with Score-Based Generative Models*. ICLR 2022](https://arxiv.org/abs/2111.08005)

For a list of works that have been influenced by score-based generative modeling, researchers at the University of Oxford have built a very useful (but necessarily incomplete) website: [https://scorebasedgenerativemodeling.github.io/](https://scorebasedgenerativemodeling.github.io/).

There are two major challenges of score-based generative models. First, the sampling speed is slow since it involves a large number of Langevin-type iterations. Second, it is inconvenient to work with discrete data distributions since scores are only defined on continuous distributions.

The first challenge can be partially solved by using numerical ODE solvers for the probability flow ODE with lower precision (a similar method, denoising diffusion implicit modeling, has been proposed in

- **Denoising Diffusion Implicit Models**   [\[link\]](https://openreview.net/forum?id=St1giarCHLP)  
	J. Song, C. Meng, S. Ermon.  
	International Conference on Learning Representations. 2021.

\[49\]

). It is also possible to learn a direct mapping from the latent space of probability flow ODEs to the image space, as shown in

- **Knowledge Distillation in Iterative Generative Models for Improved Sampling Speed**  
	E. Luhman, T. Luhman.  
	arXiv e-prints, pp. arXiv--2101. 2021.

\[50\]

. However, all such methods to date result in worse sample quality.

The second challenge can be addressed by learning an autoencoder on discrete data and performing score-based generative modeling on its continuous latent space

- **Symbolic Music Generation with Diffusion Models**  
	G. Mittal, J. Engel, C. Hawthorne, I. Simon.  
	arXiv preprint arXiv:2103.16091. 2021.
- **Score-based Generative Modeling in Latent Space**  
	A. Vahdat, K. Kreis, J. Kautz.  
	Advances in Neural Information Processing Systems (NeurIPS). 2021.

\[28, 51\]

. Jascha’s original work on diffusion models

- **Deep unsupervised learning using nonequilibrium thermodynamics**  
	J. Sohl-Dickstein, E. Weiss, N. Maheswaranathan, S. Ganguli.  
	International Conference on Machine Learning, pp. 2256--2265. 2015.

\[44\]

also provides a discrete diffusion process for discrete data distributions, but its potential for large scale applications remains yet to be proven.

It is my conviction that these challenges will soon be solved with the joint efforts of the research community, and score-based generative models/ diffusion-based models will become one of the most useful tools for data generation, density estimation, inverse problem solving, and many other downstream tasks in machine learning.

### Footnotes

1. Hereafter we only consider probability density functions. Probability mass functions are similar.
2. Fisher divergence is typically between two distributions p and q, defined as 
	$$
	(\text{4}) \mathbb{E}_{p \left(\right. \mathbf{x} \left.\right)} \left[\right. \parallel \nabla_{\mathbf{x}} log ⁡ p \left(\right. \mathbf{x} \left.\right) - \nabla_{\mathbf{x}} log ⁡ q \left(\right. \mathbf{x} \left.\right) \parallel_{2}^{2} \left]\right. .
	$$
	 Here we slightly abuse the term as the name of a closely related expression for score-based models.
3. Commonly used score matching methods include denoising score matching
	- **A connection between score matching and denoising autoencoders**  
		P. Vincent.  
		Neural computation, Vol 23(7), pp. 1661--1674. MIT Press. 2011.
	\[17\]
	and sliced score matching
	- **Sliced score matching: A scalable approach to density and score estimation**   [\[PDF\]](http://arxiv.org/pdf/1905.07088.pdf)  
		Y. Song, S. Garg, J. Shi, S. Ermon.  
		Uncertainty in Artificial Intelligence, pp. 574--584. 2020.
	\[31\]
	. Here is an introduction to [score matching and sliced score matching](https://yang-song.net/blog/2019/ssm/).
4. It is typical for normalizing flow models to convert discrete images to continuous ones by adding small uniform noise to them.
5. Goes without saying that the significance of score-based generative models/diffusion probabilistic models is in no way comparable to quantum mechanics.

### References

[^1]: The neural autoregressive distribution estimator  
Larochelle, H. and Murray, I., 2011. International Conference on Artificial Intelligence and Statistics, pp. 29--37.

[^2]: Made: Masked autoencoder for distribution estimation  
Germain, M., Gregor, K., Murray, I. and Larochelle, H., 2015. International Conference on Machine Learning, pp. 881--889.

[^3]: Pixel recurrent neural networks  
Van Oord, A., Kalchbrenner, N. and Kavukcuoglu, K., 2016. International Conference on Machine Learning, pp. 1747--1756.

[^4]: NICE: Non-linear independent components estimation  
Dinh, L., Krueger, D. and Bengio, Y., 2014. arXiv preprint arXiv:1410.8516.

[^5]: Density estimation using Real NVP  
Dinh, L., Sohl-Dickstein, J. and Bengio, S., 2017. International Conference on Learning Representations.

[^6]: A tutorial on energy-based learning  
LeCun, Y., Chopra, S., Hadsell, R., Ranzato, M. and Huang, F., 2006. Predicting structured data, Vol 1(0).

[^7]: How to Train Your Energy-Based Models  
Song, Y. and Kingma, D.P., 2021. arXiv preprint arXiv:2101.03288.

[^8]: Auto-encoding variational bayes  
Kingma, D.P. and Welling, M., 2014. International Conference on Learning Representations.

[^9]: Stochastic backpropagation and approximate inference in deep generative models  
Rezende, D.J., Mohamed, S. and Wierstra, D., 2014. International conference on machine learning, pp. 1278--1286.

[^10]: Learning in implicit generative models  
Mohamed, S. and Lakshminarayanan, B., 2016. arXiv preprint arXiv:1610.03483.

[^11]: Generative adversarial nets  
Goodfellow, I., Pouget-Abadie, J., Mirza, M., Xu, B., Warde-Farley, D., Ozair, S., Courville, A. and Bengio, Y., 2014. Advances in neural information processing systems, pp. 2672--2680.

[^12]: Improved techniques for training gans  
Salimans, T., Goodfellow, I., Zaremba, W., Cheung, V., Radford, A. and Chen, X., 2016. Advances in Neural Information Processing Systems, pp. 2226--2234.

[^13]: Unrolled Generative Adversarial Networks   [\[link\]](https://openreview.net/forum?id=BydrOIcle)  
Metz, L., Poole, B., Pfau, D. and Sohl-Dickstein, J., 2017. 5th International Conference on Learning Representations, ICLR 2017, Toulon, France, April 24-26, 2017, Conference Track Proceedings. OpenReview.net.

[^14]: A Kernel Test of Goodness of Fit   [\[HTML\]](https://proceedings.mlr.press/v48/chwialkowski16.html)  
Chwialkowski, K., Strathmann, H. and Gretton, A., 2016. Proceedings of The 33rd International Conference on Machine Learning, Vol 48, pp. 2606--2615. PMLR.

[^15]: A kernelized Stein discrepancy for goodness-of-fit tests  
Liu, Q., Lee, J. and Jordan, M., 2016. International conference on machine learning, pp. 276--284.

[^16]: Estimation of non-normalized statistical models by score matching  
Hyvarinen, A., 2005. Journal of Machine Learning Research, Vol 6(Apr), pp. 695--709.

[^17]: A connection between score matching and denoising autoencoders  
Vincent, P., 2011. Neural computation, Vol 23(7), pp. 1661--1674. MIT Press.

[^18]: Generative Modeling by Estimating Gradients of the Data Distribution   [\[PDF\]](http://arxiv.org/pdf/1907.05600.pdf)  
Song, Y. and Ermon, S., 2019. Advances in Neural Information Processing Systems, pp. 11895--11907.

[^19]: Improved Techniques for Training Score-Based Generative Models   [\[PDF\]](http://arxiv.org/pdf/2006.09011.pdf)  
Song, Y. and Ermon, S., 2020. Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual.

[^20]: Denoising diffusion probabilistic models  
Ho, J., Jain, A. and Abbeel, P., 2020. arXiv preprint arXiv:2006.11239.

[^21]: Score-Based Generative Modeling through Stochastic Differential Equations   [\[link\]](https://openreview.net/forum?id=PxTIG12RRHS)  
Song, Y., Sohl-Dickstein, J., Kingma, D.P., Kumar, A., Ermon, S. and Poole, B., 2021. International Conference on Learning Representations.

[^22]: Diffusion models beat gans on image synthesis  
Dhariwal, P. and Nichol, A., 2021. arXiv preprint arXiv:2105.05233.

[^23]: Cascaded Diffusion Models for High Fidelity Image Generation  
Ho, J., Saharia, C., Chan, W., Fleet, D.J., Norouzi, M. and Salimans, T., 2021.

[^24]: WaveGrad: Estimating Gradients for Waveform Generation   [\[link\]](https://openreview.net/forum?id=NsMLjcFaO8O)  
Chen, N., Zhang, Y., Zen, H., Weiss, R.J., Norouzi, M. and Chan, W., 2021. International Conference on Learning Representations.

[^25]: DiffWave: A Versatile Diffusion Model for Audio Synthesis   [\[link\]](https://openreview.net/forum?id=a-xFK8Ymz5J)  
Kong, Z., Ping, W., Huang, J., Zhao, K. and Catanzaro, B., 2021. International Conference on Learning Representations.

[^26]: Grad-tts: A diffusion probabilistic model for text-to-speech  
Popov, V., Vovk, I., Gogoryan, V., Sadekova, T. and Kudinov, M., 2021. arXiv preprint arXiv:2105.06337.

[^27]: Learning Gradient Fields for Shape Generation  
Cai, R., Yang, G., Averbuch-Elor, H., Hao, Z., Belongie, S., Snavely, N. and Hariharan, B., 2020. Proceedings of the European Conference on Computer Vision (ECCV).

[^28]: Symbolic Music Generation with Diffusion Models  
Mittal, G., Engel, J., Hawthorne, C. and Simon, I., 2021. arXiv preprint arXiv:2103.16091.

[^29]: Robust Compressed Sensing MRI with Deep Generative Priors  
Jalal, A., Arvinte, M., Daras, G., Price, E., Dimakis, A.G. and Tamir, J.I., 2021. Advances in neural information processing systems.

[^30]: Training products of experts by minimizing contrastive divergence  
Hinton, G.E., 2002. Neural computation, Vol 14(8), pp. 1771--1800. MIT Press.

[^31]: Sliced score matching: A scalable approach to density and score estimation   [\[PDF\]](http://arxiv.org/pdf/1905.07088.pdf)  
Song, Y., Garg, S., Shi, J. and Ermon, S., 2020. Uncertainty in Artificial Intelligence, pp. 574--584.

[^32]: Correlation functions and computer simulations  
Parisi, G., 1981. Nuclear Physics B, Vol 180(3), pp. 378--384. Elsevier.

[^33]: Representations of knowledge in complex systems  
Grenander, U. and Miller, M.I., 1994. Journal of the Royal Statistical Society: Series B (Methodological), Vol 56(4), pp. 549--581. Wiley Online Library.

[^34]: Adversarial score matching and improved sampling for image generation   [\[link\]](https://openreview.net/forum?id=eLfqMl3z3lq)  
Jolicoeur-Martineau, A., Piche-Taillefer, R., Mitliagkas, I. and Combes, R.T.d., 2021. International Conference on Learning Representations.

[^35]: Reverse-time diffusion equation models  
Anderson, B.D., 1982. Stochastic Processes and their Applications, Vol 12(3), pp. 313--326. Elsevier.

[^36]: Maximum Likelihood Training of Score-Based Diffusion Models  
Song, Y., Durkan, C., Murray, I. and Ermon, S., 2021. Advances in Neural Information Processing Systems (NeurIPS).

[^37]: Gotta Go Fast When Generating Data with Score-Based Models  
Jolicoeur-Martineau, A., Li, K., Piche-Taillefer, R., Kachman, T. and Mitliagkas, I., 2021. arXiv preprint arXiv:2105.14080.

[^38]: GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium  
Heusel, M., Ramsauer, H., Unterthiner, T., Nessler, B. and Hochreiter, S., 2017. Advances in Neural Information Processing Systems 30: Annual Conference on Neural Information Processing Systems 2017, December 4-9, 2017, Long Beach, CA, {USA}, pp. 6626--6637.

[^39]: Training Generative Adversarial Networks with Limited Data  
Karras, T., Aittala, M., Hellsten, J., Laine, S., Lehtinen, J. and Aila, T., 2020. Proc. NeurIPS.

[^40]: Neural Ordinary Differential Equations  
Chen, T.Q., Rubanova, Y., Bettencourt, J. and Duvenaud, D., 2018. Advances in Neural Information Processing Systems 31: Annual Conference on Neural Information Processing Systems 2018, NeurIPS 2018, December 3-8, 2018, Montr{\\'{e}}al, Canada, pp. 6572--6583.

[^41]: Scalable Reversible Generative Models with Free-form Continuous Dynamics   [\[link\]](https://openreview.net/forum?id=rJxgknCcK7)  
Grathwohl, W., Chen, R.T.Q., Bettencourt, J. and Duvenaud, D., 2019. International Conference on Learning Representations.

[^42]: Solving Inverse Problems in Medical Imaging with Score-Based Generative Models   [\[PDF\]](http://arxiv.org/pdf/2111.08005.pdf)  
Song, Y., Shen, L., Xing, L. and Ermon, S., 2022. International Conference on Learning Representations.

[^43]: Annealed importance sampling  
Neal, R.M., 2001. Statistics and computing, Vol 11(2), pp. 125--139. Springer.

[^44]: Deep unsupervised learning using nonequilibrium thermodynamics  
Sohl-Dickstein, J., Weiss, E., Maheswaranathan, N. and Ganguli, S., 2015. International Conference on Machine Learning, pp. 2256--2265.

[^45]: Learning to generate samples from noise through infusion training  
Bordes, F., Honari, S. and Vincent, P., 2017. arXiv preprint arXiv:1703.06975.

[^46]: Variational walkback: Learning a transition operator as a stochastic recurrent net  
Goyal, A., Ke, N.R., Ganguli, S. and Bengio, Y., 2017. arXiv preprint arXiv:1711.02282.

[^47]: GSNs: generative stochastic networks  
Alain, G., Bengio, Y., Yao, L., Yosinski, J., Thibodeau-Laufer, E., Zhang, S. and Vincent, P., 2016. Information and Inference: A Journal of the IMA, Vol 5(2), pp. 210--249. Oxford University Press.

[^48]: Diffusion Schrödinger Bridge with Applications to Score-Based Generative Modeling  
De Bortoli, V., Thornton, J., Heng, J. and Doucet, A., 2021. Advances in Neural Information Processing Systems (NeurIPS).

[^49]: Denoising Diffusion Implicit Models   [\[link\]](https://openreview.net/forum?id=St1giarCHLP)  
Song, J., Meng, C. and Ermon, S., 2021. International Conference on Learning Representations.

[^50]: Knowledge Distillation in Iterative Generative Models for Improved Sampling Speed  
Luhman, E. and Luhman, T., 2021. arXiv e-prints, pp. arXiv--2101.

[^51]: Score-based Generative Modeling in Latent Space  
Vahdat, A., Kreis, K. and Kautz, J., 2021. Advances in Neural Information Processing Systems (NeurIPS).