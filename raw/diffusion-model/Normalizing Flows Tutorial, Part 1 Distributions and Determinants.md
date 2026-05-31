---
title: "Normalizing Flows Tutorial, Part 1: Distributions and Determinants"
source: "https://blog.evjang.com/2018/01/nf1.html"
author:
  - "[[Eric]]"
published: 2018-01-18
created: 2026-05-31
description: "I'm looking for help translate these posts into different languages! Please email me at <myfirstname><mylastname>2004<at>gmail.com if you ar..."
tags:
  - "clippings"
---
*I'm looking for help translate these posts into different languages! Please email me at <myfirstname><mylastname>2004<at>gmail.com if you are interested.*  
Xiaoyi Yin (尹肖贻) has kindly translated this post into Chinese ([中文](https://www.jianshu.com/p/66393cebe8ba)).  
Jaeseong You has kindly translated this post into Korean ([한국어](https://jaeseongyou.wordpress.com/2020/05/04/%ec%a0%95%ea%b7%9c%ed%99%94-%ed%94%8c%eb%a1%9c%ec%9a%b0-%ed%8a%9c%ed%86%a0%eb%a6%ac%ec%96%bc-%ed%8c%8c%ed%8a%b81-%eb%b6%84%ed%8f%ac%ec%99%80-%ed%96%89%eb%a0%ac%ec%8b%9d/))

Kieran Didi has kindly translated this post into German ([Deutsch](https://kdidi.netlify.app/blog/ml/2022-08-30-flowmodels1/))  
  
If you are a machine learning practitioner working on generative modeling, Bayesian deep learning, or deep reinforcement learning, **normalizing flows** are a handy technique to have in your algorithmic toolkit.

Normalizing flows transform simple densities (like Gaussians) into rich complex distributions that can be used for generative models, RL, and variational inference

. TensorFlow has [a nice set of functions](https://arxiv.org/pdf/1711.10604.pdf) that make it easy to build flows and train them to suit real-world data.  

This tutorial comes in two parts:  
- [Part 1: Distributions and Determinants](http://blog.evjang.com/2018/01/nf1.html). In this post, I explain how invertible transformations of densities can be used to implement more complex densities, and how these transformations can be chained together to form a “normalizing flow”.
- [Part 2: Modern Normalizing Flows](http://blog.evjang.com/2018/01/nf2.html): In a follow-up post, I survey recent techniques developed by researchers to learn normalizing flows, and explain how a slew of modern generative modeling techniques -- autoregressive models, MAF, IAF, NICE, Real-NVP, Parallel-Wavenet -- are all related to each other.
This series is written for an audience with a rudimentary understanding of linear algebra, probability, neural networks, and TensorFlow. Knowledge of recent advances in Deep Learning, generative models will be helpful in understanding the motivations and context underlying these techniques, but they are not necessary.

## Background

Statistical Machine Learning algorithms try to learn the structure of data by fitting a parametric distribution $p(x; \theta)$ to it. Given a dataset, if we can represent it with a distribution, we can:

1. Generate new data “for free” by sampling from the learned distribution *in silico*; no need to run the true generative process for the data. This is a useful tool if the data is expensive to generate, i.e. a real-world experiment that takes a long time to run \[1\]. Sampling is also used to construct estimators of high-dimensional integrals over spaces.
2. Evaluate the likelihood of data observed at test time (this can be used for rejection sampling or to score how good our model is).
3. Find the conditional relationship between variables. For example, learning the distribution $p(x_2 | x_1)$ allows us to build discriminative classification or regression models.
4. Score our algorithm by using complexity measures like entropy, mutual information, and moments of the distribution.

We’ve gotten pretty good at sampling (1), as evidenced by recent work on generative models for [images](http://research.nvidia.com/publication/2017-10_Progressive-Growing-of) and [audio](https://google.github.io/tacotron/publications/tacotron2/index.html). These kinds of generative models are already being deployed in real [commercial applications](https://qz.com/1090267/artificial-intelligence-can-now-show-you-how-those-pants-will-fit/) and [Google products](https://deepmind.com/blog/wavenet-launches-google-assistant/).

However, the research community currently directs less attention towards unconditional & conditional likelihood estimation (2, 3) and model scoring (4). For instance, we don’t know how to compute the [support](https://en.wikipedia.org/wiki/Support_\(mathematics\)) of a GAN decoder (how much of the output space has been assigned nonzero probability by the model), we don’t know how to compute the density of an image with respect to a [DRAW distribution](https://arxiv.org/abs/1502.04623) or even a [VAE](https://arxiv.org/abs/1606.05908), and we don’t know how to analytically compute various metrics (KL, earth-mover distance) on arbitrary distributions, even if we know their analytic densities.

Generating likely samples isn’t enough: we also care about answering “

how likely is the data?

” \[2\], having flexible conditional densities (e.g. for sampling/evaluating divergences of multi-modal policies in RL), and being able to choose rich families of priors and posteriors in variational inference.

Consider for a moment, your friendly neighborhood [Normal Distribution](https://en.wikipedia.org/wiki/Normal_distribution). It’s the [Chicken Soup](https://en.wikipedia.org/wiki/Comfort_food) of distributions: we can draw samples from it easily, we know its analytic density and KL divergence to other Normal distributions, the [central limit theorem](https://en.wikipedia.org/wiki/Central_limit_theorem) gives us confidence that we can apply it to pretty much any data, and we can even backprop through its samples via the reparameterization trick. The Normal Distribution’s ease-of-use makes it a very popular choice for many generative modeling and reinforcement learning algorithms.

Unfortunately, the Normal distribution just doesn’t cut it in many real-world problems we care about. In Reinforcement Learning -- especially continuous control tasks such as robotics -- policies are often modeled as [multivariate Gaussians with diagonal covariance matrices](https://www.tensorflow.org/api_docs/python/tf/contrib/distributions/MultivariateNormalDiag).

By construction, uni-modal Gaussians cannot do well on tasks that require sampling from a multi-modal distribution. A classic example of where uni-modal policies fail is an agent trying to get to its house across a lake. It can get home by circumventing the lake clockwise (left) or counterclockwise (right), but a Gaussian policy is not able to represent two modes. Instead, it chooses actions from a Gaussian whose mean is a linear combination of the two modes, resulting in the agent going straight into the icy water. Sad!

The above example illustrates how the Normal distribution can be overly simplistic. In addition to bad symmetry assumptions, Gaussians have most of their density concentrated at [the edges](http://www.inference.vc/high-dimensional-gaussian-distributions-are-soap-bubble/) in high dimensions and are [not robust to rare events](https://arxiv.org/pdf/1103.5672.pdf). Can we find a better distribution with the following properties?

1. Complex enough to model rich, multi-modal data distributions like images and value functions in RL environments?
2. … while retaining the easy comforts of a Normal distribution: sampling, density evaluation, and with re-parameterizable samples?

The answer is yes! Here are a few ways to do it:  
- Use a mixture model to represent a multi-modal policy, where a categorical represents the “option” and the mixture represents the sub-policy. This provides samples that are easy to sample and evaluate, but samples are not trivially re-parameterizable, which makes them hard to use for VAEs and posterior inference. However, using a [Gumbel-Softmax](https://arxiv.org/abs/1611.01144) / [Concrete](https://arxiv.org/abs/1611.00712) relaxation of the categorical “option” would provide a multi-modal, re-parameterizable distribution.
- [Autoregressive factorizations of policy / value distributions](https://arxiv.org/abs/1705.05035). In particular, the Categorical distribution can model any discrete distribution.
- In RL, one can avoid this altogether by symmetry-breaking the value distribution via [recurrent policies](https://arxiv.org/pdf/1707.02920.pdf), noise, or [distributional RL](https://arxiv.org/abs/1707.06887). This helps by collapsing the complex value distributions into simpler conditional distributions at each timestep.
- Learning with [energy-based models](http://yann.lecun.com/exdb/publis/pdf/lecun-06.pdf), a.k.a [undirected graphical models](https://courses.cs.washington.edu/courses/cse590st/04sp/slides/mn.pdf) with potential functions that eschew an normalized probabilistic interpretation. Here’s a [recent example](https://arxiv.org/abs/1702.08165) of this applied to RL.
- Normalizing Flows: learn invertible, volume-tracking transformations of distributions that we can manipulate easily.

Let's explore the last approach - Normalizing Flows.  
  

## Change of Variables, Change of Volume

Let's build up some intuition by examining linear transformations of 1D random variables. Let $X$ be the distribution . Let random variable . is a simple affine (scale & shift) transformation of the underlying “source distribution” . What this means is that a sample from can be converted into a sample from by simply applying the function to it.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiRGNBOlzdMg6krBIj1cSqgXB9rintNXu6kIY71cPQVuiSllaYHdOoLqFqp73CQhHOAAfaX83HQ2quM6ivXgfjJBA-fErZeLil01qo4W3JgUbjYVUi3Hb7T41NCSs83hHMgNTVW1HnbU34/s400/flow1.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiRGNBOlzdMg6krBIj1cSqgXB9rintNXu6kIY71cPQVuiSllaYHdOoLqFqp73CQhHOAAfaX83HQ2quM6ivXgfjJBA-fErZeLil01qo4W3JgUbjYVUi3Hb7T41NCSs83hHMgNTVW1HnbU34/s1600/flow1.png)

  
  
The green square represents the shaded probability mass on $\mathbb{R}$ for both and - the height represents the density function at that value. Observe that because probability mass must integrate to 1 for any distribution, the act of scaling the domain by 2 everywhere means we must divide the probability density by 2 everywhere, so that the total area of the green square and blue rectangle are the same (=1).  
  
If we zoom in on a particular x and an infinitesimally nearby point , then applying f to them takes us to the pair .  
  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjmtdEA7hNY650VkJ04jLlQyNiYl-qGX_I-vIIxxAv_bRfkqtR0rTMe52BQO9gVm_gkUzqYj2yaFKv4w5qdXGK5QDACCjKvF6auYbMuB30xj5VQXCcHwvRzP4XO6Q_AFC2qt_KccIKZ1J0/s400/flow2.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjmtdEA7hNY650VkJ04jLlQyNiYl-qGX_I-vIIxxAv_bRfkqtR0rTMe52BQO9gVm_gkUzqYj2yaFKv4w5qdXGK5QDACCjKvF6auYbMuB30xj5VQXCcHwvRzP4XO6Q_AFC2qt_KccIKZ1J0/s1600/flow2.png)

  
  
On the left, we have a locally increasing function () and on the right, a locally decreasing function (). In order to preserve total probability, the change of along interval must be equivalent to the change of along interval :

$$
p(x) dx = p(y) dy
$$
  
  
In order to conserve probability, we only care about the amount of change in y and not its direction (it doesn’t matter if is increasing or decreasing at x, we assume the amount of change in y is the same regardless). Therefore, . Note that in log-space, this is equivalent to . Computing log-densities is more well-scaled for numerical stability reasons.  
  
Now let’s consider the multivariate case, with 2 variables. Again, zooming into an infinitesimally small region of our domain, our initial “segment” of the base distribution is now a square with width dx.  
  
Note that a transformation that merely shifts a rectangular patch does not change the area. We are only interested in the rate of change per unit area of x, so the displacement can be thought of as a unit of measure, which is arbitrary. To make the following analysis simple and unit-less, let’s investigate a unit square on the origin, i.e. 4 points .  
  
Multiplying this by the matrix will take points on this square into a parallelogram, as shown on the figure to the right (below). is sent to , is sent to , sent to , sent to .  
  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgFADSt_SMaOb2CWwtb_n1o_w7GtSoyzzkY6K1rjcZBE_qJNC2oaRGEhLDcwlQ64qUYhTF8dkd6-w0n3OvAIOj5EUjZqYtrOcpk1ufhp4ZJUjeqbwfh5ddwWAJ9seKUJ1kSQAtq7-J0nXQ/s400/flow3.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgFADSt_SMaOb2CWwtb_n1o_w7GtSoyzzkY6K1rjcZBE_qJNC2oaRGEhLDcwlQ64qUYhTF8dkd6-w0n3OvAIOj5EUjZqYtrOcpk1ufhp4ZJUjeqbwfh5ddwWAJ9seKUJ1kSQAtq7-J0nXQ/s1600/flow3.png)

  
  
Thus, a unit square in the domain of corresponds to a deformed parallelogram in the domain of , so the per-unit rate of change in area is the area of the parallelogram, i.e. .

The area of a parallelogram, $ad - bc$, is nothing more than the absolute value of the determinant of the linear transformation!  
  
In 3 dimensions, the “change in area of parallelogram” becomes a “change in volume of parallelpiped”, and even higher dimensions, this becomes “change in volume of a n-parallelotope”. But the concept remains the same - determinants are nothing more than the amount (and direction) of volume distortion of a linear transformation, generalized to any number of dimensions.  
  
What if the transformation f is nonlinear? Instead of a single parallelogram that tracks the distortion of any point in space, you can picture many infinitesimally small parallelograms corresponding to the amount of volume distortion for each point in the domain. Mathematically, this locally-linear change in volume is , where J(f^-1(x)) is the Jacobian of the function inverse - a higher-dimensional generalization of the quantity dx/dy from before.  

$$
p(y) = p(f^{-1}(y)) \cdot |\text{det} J(f^{-1}(y))|
$$

When I learned about determinants in middle & high school I was very confused at the seemingly arbitrary definition of determinants. We were only taught how to compute a determinant, instead of what a determinant meant: the local, linearized rate of volume change of a transformation.  

## Transformed Distributions in TensorFlow

TensorFlow has an elegant API for transforming distributions. A TransformedDistribution is specified by a base distribution object that we will transform, and a Bijector object that implements 1) a forward transformation $y = f(x)$, where 2) its inverse transformation , and 3) the inverse log determinant of the Jacobian . For the rest of this post, I will abbreviate this quantity as ILDJ.

Under this abstraction, forward sampling is trivial:  
  

> bijector.forward(base\_dist.sample())

  
To evaluate log-density of the transformed distribution:  
  

> distribution.log\_prob(bijector.inverse(x)) + bijector.inverse\_log\_det\_jacobian(x)

Furthermore, if bijector.forward is a differentiable function, then Y = bijector.forward(x) is a re-parameterizable distribution with respect to samples x = base\_distribution.sample(). This means that normalizing flows can be used as a drop-in replacement for variational posteriors in a VAE (as an alternative to a Gaussian).  
  
Some commonly used TensorFlow distributions are actually implemented using these TransformedDistributions.  
  

| **Source Distribution** | **Bijector.forward** | **Transformed Distribution** |
| --- | --- | --- |
| Normal | exp(x) | LogNormal |
| Exp(rate=1) | \-log(x) | Gumbel(0,1) |
| Gumbel(0,1) | Softmax(x) | Gumbel-Softmax / Concrete |

  
Under standard convention, TransformedDistributions are named as $\text{Bijector}^{-1}\text{BaseDistribution}$ so an ExpBijector applied to a Normal distribution becomes LogNormal. There are some exceptions to this naming scheme - the [Gumbel-Softmax](http://blog.evjang.com/2016/11/tutorial-categorical-variational.html) distribution is implemented as the RelaxedOneHotCategorical distribution, which applies a SoftmaxCentered bijector to a Gumbel distribution.  
  

## Normalizing Flows and Learning Flexible Bijectors

  
Why stop at 1 bijector? We can chain any number of bijectors together, much like we chain layers together in a neural network \[3\]. This is construct is known as a “normalizing flow”. Additionally, if a bijector has tunable parameters with respect to bijector.log\_prob, then the bijector can actually be learned to transform our base distribution to suit arbitrary densities. Each bijector functions as a learnable “layer”, and you can use an optimizer to learn the parameters of the transformation to suit our data distribution we are trying to model. One algorithm to do this is maximum likelihood estimation, which modifies our model parameters so that our training data points have maximum log-probability under our transformed distribution. We compute and optimize over log probabilities rather than probabilities for [numerical stability reasons](https://stats.stackexchange.com/questions/174481/why-to-optimize-max-log-probability-instead-of-probability).  
  
This slide from Shakir Mohamed and Danilo Rezende’s UAW [talk](https://www.youtube.com/watch?v=JrO5fSskISY) [(slides)](http://www.shakirm.com/slides/DeepGenModelsTutorial.pdf) that illustrates this concept:  
  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiLQZ_wPP5YX98x9ZDiX5dUCA6PTeYvU0wtq2ujITnNQ10wOqcs8SO_WQl9WygoiMbSPhd6diXgw-RkOqCfC8LwI0OjGI_9tsmKZR36iNJ-NF4MLNnomfDzdcHBI_hEVpeFYInz7Blw_G0/s400/shakir_danilo_slide.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiLQZ_wPP5YX98x9ZDiX5dUCA6PTeYvU0wtq2ujITnNQ10wOqcs8SO_WQl9WygoiMbSPhd6diXgw-RkOqCfC8LwI0OjGI_9tsmKZR36iNJ-NF4MLNnomfDzdcHBI_hEVpeFYInz7Blw_G0/s1600/shakir_danilo_slide.png)

  
  
However, computing the determinant of an arbitrary Jacobian matrix has runtime complexity , which is very expensive to put in a neural network. There is also the trouble of inverting an arbitrary function approximator. Much of the current research on Normalizing Flows focuses on how to design expressive Bijectors that exploit GPU parallelism during forward and inverse computations, all while maintaining computationally efficient ILDJs.  
  

## Code Example

Let’s build a basic normalizing flow in TensorFlow in about 100 lines of code. This code example will make use of:  
  
- TF [Distributions](https://www.tensorflow.org/probability/api_docs/python/tfp/distributions/Distribution) - general API for manipulating distributions in TF. For this tutorial you’ll need TensorFlow r1.5 or later.
- TF [Bijector](https://www.tensorflow.org/probability/api_docs/python/tfp/bijectors) - general API for creating operators on distributions
- Numpy, Matplotlib.

```
import numpy as np

import matplotlib.pyplot as plt

import tensorflow as tf

tfd = tf.contrib.distributions

tfb = tfd.bijectors
```

  
We are trying to model the distribution . We can generate samples from the target distribution using the following code snippet (we generate them in TensorFlow to avoid having to copy samples from the CPU to the GPU on each minibatch):  
  

```
batch_size=512

x2_dist = tfd.Normal(loc=0., scale=4.)

x2_samples = x2_dist.sample(batch_size)

x1 = tfd.Normal(loc=.25 * tf.square(x2_samples),

                scale=tf.ones(batch_size, dtype=tf.float32))

x1_samples = x1.sample()

x_samples = tf.stack([x1_samples, x2_samples], axis=1)
```

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjB40OKK52JQQVteS9mUqaJHORvNh2EayqZmlObSRSyGHF7JODhnjA8nONaKpeAu64NvcG54qlGgNKkLpqTFqfkSszG5mD0X0sv-gcUx9V4hV7TW6gXwco7UWmKS-MydgqOHY8sRm66-3s/s400/ar_toy.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjB40OKK52JQQVteS9mUqaJHORvNh2EayqZmlObSRSyGHF7JODhnjA8nONaKpeAu64NvcG54qlGgNKkLpqTFqfkSszG5mD0X0sv-gcUx9V4hV7TW6gXwco7UWmKS-MydgqOHY8sRm66-3s/s1600/ar_toy.png)

  
  
For our base distribution, we’ll use an Isotropic Gaussian.  
  

```
base_dist = tfd.MultivariateNormalDiag(loc=tf.zeros([2], tf.float32))
```

  
Next, we construct the bijector and create a TransformedDistribution from it. Let’s build a flow that resembles a standard fully-connected network, i.e. alternating matrix multiplication with nonlinearities.  
  
The Jacobian of an affine function is trivial to compute, but worst case [determinants are](https://en.wikipedia.org/wiki/Computational_complexity_of_mathematical_operations) , which is unacceptably slow to compute. Instead, TensorFlow provides a structured affine transformation whose determinant can be computed more efficiently. This Affine transform is parameterized as a lower triangular matrix plus a low rank update:  

To compute $\text{det}(M + V \cdot D \cdot V^T)$ cheaply, we use the [matrix determinant lemma](https://en.wikipedia.org/wiki/Matrix_determinant_lemma).  
  
Next, we need an invertible nonlinearity in order to express non-linear functions (otherwise the chain of affine bijectors remains affine). Sigmoid / tanh may seem like good choices, but they are incredibly unstable to invert - small changes in the output near -1 or 1 correspond to massive changes in input. In my experiments I could not chain 2 saturating nonlinearities together without gradients exploding. Meanwhile, ReLU is stable, but not invertible for .  
  
I chose to implement PReLU (parameterized ReLU), which is the same as Leaky ReLU but with a learnable slope in the negative regime. The simplicity of PReLU and its straightforward Jacobian makes for a nice exercise in implementing your own custom Bijectors: notice that the ILDJ is 0 when (no volume change) and otherwise (compensating for the contraction in volume from multiplying x by ).  
  

```
# quite easy to interpret - multiplying by alpha causes a contraction in volume.

class LeakyReLU(tfb.Bijector):

    def __init__(self, alpha=0.5, validate_args=False, name="leaky_relu"):

        super(LeakyReLU, self).__init__(

            event_ndims=1, validate_args=validate_args, name=name)

        self.alpha = alpha

    def _forward(self, x):

        return tf.where(tf.greater_equal(x, 0), x, self.alpha * x)

    def _inverse(self, y):

        return tf.where(tf.greater_equal(y, 0), y, 1. / self.alpha * y)

    def _inverse_log_det_jacobian(self, y):

        event_dims = self._event_dims_tensor(y)

        I = tf.ones_like(y)

        J_inv = tf.where(tf.greater_equal(y, 0), I, 1.0 / self.alpha * I)

        # abs is actually redundant here, since this det Jacobian is > 0

        log_abs_det_J_inv = tf.log(tf.abs(J_inv))

        return tf.reduce_sum(log_abs_det_J_inv, axis=event_dims)
```

PReLU is an element-wise transformation, so the Jacobian is diagonal. The determinant of a diagonal matrix is just the product of the diagonal entries, so we compute the ILDJ by simply summing the diagonal entries of the log-Jacobian \[4\]. We build the “MLP Bijector” by using tfb.Chain(), then apply it to our base distribution to create the transformed distribution:  
  

```
d, r = 2, 2

DTYPE = tf.float32

bijectors = []

num_layers = 6

for i in range(num_layers):

    with tf.variable_scope('bijector_%d' % i):

        V = tf.get_variable('V', [d, r], dtype=DTYPE)  # factor loading

        shift = tf.get_variable('shift', [d], dtype=DTYPE)  # affine shift

        L = tf.get_variable('L', [d * (d + 1) / 2],

                            dtype=DTYPE)  # lower triangular

        bijectors.append(tfb.Affine(

            scale_tril=tfd.fill_triangular(L),

            scale_perturb_factor=V,

            shift=shift,

        ))

        alpha = tf.abs(tf.get_variable('alpha', [], dtype=DTYPE)) + .01

        bijectors.append(LeakyReLU(alpha=alpha))

# Last layer is affine. Note that tfb.Chain takes a list of bijectors in the *reverse* order

# that they are applied.

mlp_bijector = tfb.Chain(

    list(reversed(bijectors[:-1])), name='2d_mlp_bijector')

dist = tfd.TransformedDistribution(

    distribution=base_dist,

    bijector=mlp_bijector

)
```

  
Finally, we’ll train the model using Maximum Likelihood estimation: maximize the expected log probability of samples from the real data distribution, under our choice of model.  
  

```
loss = -tf.reduce_mean(dist.log_prob(x_samples))

train_op = tf.train.AdamOptimizer(1e-3).minimize(loss)

sess = tf.InteractiveSession()

sess.run(tf.global_variables_initializer())

NUM_STEPS = int(1e5)

global_step = []

np_losses = []

for i in range(NUM_STEPS):

    _, np_loss = sess.run([train_op, loss])

    if i % 1000 == 0:

        global_step.append(i)

        np_losses.append(np_loss)

    if i % int(1e4) == 0:

        print(i, np_loss)
```

We can visualize the (slow) deformation of space by coloring samples from base distribution according to their starting quadrant,  
  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgVkmMielPwHseIB1YQwAX1zYckZbAuAUDBAvzXFRP-_5RdtG3Q8TD_3dbqiEFT_EszycGSfwWE708dAyLff9H282m6fGBhOFRGq0bT6ETxNQ_Me6EHhRCTpcZPC3Sm1A1BqZugCaatfpU/s640/toy2d_flow.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgVkmMielPwHseIB1YQwAX1zYckZbAuAUDBAvzXFRP-_5RdtG3Q8TD_3dbqiEFT_EszycGSfwWE708dAyLff9H282m6fGBhOFRGq0bT6ETxNQ_Me6EHhRCTpcZPC3Sm1A1BqZugCaatfpU/s1600/toy2d_flow.png)

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgcGmSzVCukLLE9x1TRUiJbFABl70Vis-p86xH1SliM3Jfs_2pkrQHkcI3Yz8M6mP9iizehP3k8xK92z9uKbZeVz3HqBORsLqtjbTm7Z-G3H_JaGOs99lyDFE1PVlDvRl7noFRBdbWGsf8/s400/toy2d_out.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgcGmSzVCukLLE9x1TRUiJbFABl70Vis-p86xH1SliM3Jfs_2pkrQHkcI3Yz8M6mP9iizehP3k8xK92z9uKbZeVz3HqBORsLqtjbTm7Z-G3H_JaGOs99lyDFE1PVlDvRl7noFRBdbWGsf8/s1600/toy2d_out.png)

  
  
And that’s it! TensorFlow distributions makes normalizing flows to implement, and automatically accumulate all the Jacobians determinants in a way that is clean and highly readable. Full source code for this post can be found on [Github](https://github.com/ericjang/normalizing-flows-tutorial/blob/master/nf_part1_intro.ipynb).  
  
You might notice that the deformation is rather slow, and it takes a lot of layers to learn a rather simple transformation \[5\]. In the [next post](http://blog.evjang.com/2018/01/nf2.html), I will cover more modern techniques for learning normalizing flows.  
  

## Acknowledgements

  
I am very grateful to [Dustin Tran](http://dustintran.com/) for clarifying my understanding of normalizing flows, [Luke Metz](https://lukemetz.github.io/), Katherine Lee, and [Samy Bengio](http://bengio.abracadoudou.com/) for proofreading this post, and to [Ben Poole](https://cs.stanford.edu/~poole/), Rif A. Saurous, Ian Langmore for helping me to debug my code. You rock!  
  

## Footnotes

  
\[1\] The notion that we can augment our dataset with \*new\* information from a finite set of data is a rather disturbing one, and it remains to be shown whether probabilistic machine learning can truly replace true generative processes (e.g. simulation of fluid dynamics), or whether at the end of the day it is only good for amortizing computation and any generalization we get on the training / test distribution is a lucky accident.  
\[2\] See [A note on the evaluation of generative models](https://arxiv.org/abs/1511.01844) for a thought-provoking discussion about how high log-likelihood is neither sufficient nor necessary to generate “plausible” images. Still, it’s better than nothing and in practice a useful diagnostic tool.  
\[3\]There’s a connection between Normalizing Flows and GANs via encoder-decoder GAN architectures that learn the inverse of the generator (ALI / BiGAN). Since there is a separate encoder trying to recover such that , the generator can be thought of as a flow for the simple uniform distribution. However, we don’t know how to compute the amount of volume expansion/contraction w.r.t. X, so we cannot recover density from GANs. However, it’s probably not entirely unreasonable to model the log-det-jacobian numerically or enforce some kind of linear-time Jacobian by construction.  
\[4\] The lemma “Determinant of diagonal matrices is the product of the diagonal entries” is quite intuitive from a geometric point of view: each dimension’s length distortion is independent of the other dimensions, so the total volume change is just the product of changes in each direction, as if we were computing the volume of a high-dimensional rectangular prism.  
\[5\] This MLP is rather limited in capacity because each affine transformation is only a 2x2 matrix, and the PReLU “warps” the underlying distribution very slowly (so several PreLUs are needed to bend the data into the right shape). For low dimensional distributions, this MLP is a very poor choice of a normalizing flow, and is meant for educational purposes.