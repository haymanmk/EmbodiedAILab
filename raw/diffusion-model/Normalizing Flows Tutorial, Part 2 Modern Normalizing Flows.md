---
title: "Normalizing Flows Tutorial, Part 2: Modern Normalizing Flows"
source: "https://blog.evjang.com/2018/01/nf2.html"
author:
  - "[[Eric]]"
published: 2018-01-18
created: 2026-05-31
description: "This tutorial will show you how to use normalizing flows like MAF, IAF, and Real-NVP to deform an isotropic 2D Gaussian into a complex cl..."
tags:
  - "clippings"
---
![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhK4TAyELdV76Ywo0sV2A7NdKQ7bkeQxLwTDd-jZ_0nann9QnC4jyVZbjlix72IKfiAORZd1GKeydxLPCSVdkxLkVpngO-dt8GZ1I34SZZUd9ekew8gA0Zef5HDXym2-2j_AluXuhgEMtk/s400/siggraph_flow.png) This tutorial will show you how to use normalizing flows like MAF, IAF, and Real-NVP to deform an isotropic 2D Gaussian into a complex cloud of points spelling the words "SIGGRAPH" in space. Like stretching taffy. *I'm looking for help translate these posts into different languages! Please email me at <myfirstname><mylastname>2004<at>gmail.com if you are interested.*

*Xiaoyi Yin (尹肖贻) has kindly translated this post into Chinese ([中文](https://www.jianshu.com/p/db72c38233f3)).*

*Jaeseong You has kindly translated this post into Korean ([한국어](https://jaeseongyou.wordpress.com/2020/05/04/%ec%a0%95%ea%b7%9c%ed%99%94-%ed%94%8c%eb%a1%9c%ec%9a%b0-%ed%8a%9c%ed%86%a0%eb%a6%ac%ec%96%bc-%ed%8c%8c%ed%8a%b8-2/))*

*Kieran Didi has kindly translated this post into German ([Deutsch](https://kdidi.netlify.app/blog/ml/2022-08-31-flowmodels2/))  
*  
In my [previous blog post](http://blog.evjang.com/2018/01/nf1.html), I described how simple distributions like Gaussians can be “deformed” to fit complex data distributions using normalizing flows. We implemented a simple flow by chaining 2D Affine Bijectors with PreLU nonlinearities to build a small invertible neural net.  

However, this MLP flow is pretty weak: there are only 2 units per hidden layer. Furthermore, the non-linearity is monotonic and piecewise linear, so all it does is slightly warp the data manifold around the origin. This flow completely fails to implement more complex transformations like separating an isotropic Gaussian into two modes when trying to learn the “Two Moons” dataset below:  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhonGRgUtku70rhm5Ar7t3kC5iILL9Pp6f7bnvP2ZucK45rYDZH5EmphvroD3Rh-AW3i1y8-hb_L8TfC2-0kcLQdgw4TsfuK0r2I1NlFlHFlIvXrTHWWRo2MV9TkoOcLCc-v9NfubDUIpg/s400/two_moons.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhonGRgUtku70rhm5Ar7t3kC5iILL9Pp6f7bnvP2ZucK45rYDZH5EmphvroD3Rh-AW3i1y8-hb_L8TfC2-0kcLQdgw4TsfuK0r2I1NlFlHFlIvXrTHWWRo2MV9TkoOcLCc-v9NfubDUIpg/s1600/two_moons.png)

  
  
Fortunately, there are several more powerful normalizing flows that have been introduced in recent Machine Learning literature. We will explore several of these techniques in this tutorial.  
  

## Autoregressive Models are Normalizing Flows

Autoregressive density estimation techniques like [WaveNet](https://arxiv.org/abs/1609.03499) and [PixelRNN](https://arxiv.org/abs/1601.06759) model learn complex joint densities $p(x_{1:D})$ by decomposing the joint density into a product of one-dimensional conditional densities, where each depends on only the previous values:  

The conditional densities usually have learnable parameters. For example, a common choice is an autoregressive density $p(x_{1:D})$ whose conditional density is a univariate Gaussian, whose mean and standard deviations are computed by neural networks that depend on the previous .  

$$
\mu_i = f_{\mu_i}(x_{1:i-1})
$$
 
$$
\alpha_i = f_{\alpha_i}(x_{1:i-1})
$$

Learning data with autoregressive density estimation makes the rather bold inductive bias that the ordering of variables are such that your earlier variables don’t depend on later variables. Intuitively, this shouldn’t be true at all for natural data (the top row of pixels in an image does have a causal, conditional dependency on the bottom of the image). However it’s still possible to [generate plausible images](https://github.com/openai/pixel-cnn) in this manner (to the surprise of many researchers!).

To sample from this distribution, we compute $D$ “noise variates” from the standard Normal, , then apply the following recursion to get .

$$
x_i = u_i\exp{\alpha_i} + \mu_i
$$
  
  
The procedure of autoregressive sampling is a deterministic transformation of the underlying noise variates (sampled from ) into a new distribution, so autoregressive samples can actually be interpreted as a TransformedDistribution of the standard Normal!  
  
Armed with this insight, we can stack multiple autoregressive transformations into a normalizing flow. The advantage of doing this is that we can change the ordering of variables for each bijector in the flow, so that if one autoregressive factorization cannot model a distribution well (due to a poor choice of variable ordering), a subsequent layer might be able to do it.  
  
The [Masked Autoregressive Flow](https://arxiv.org/abs/1705.07057) (MAF) bijector implements such a conditional-Gaussian autoregressive model. Here is a schematic of the forward pass for a single entry in a sample of the transformed distribution, :  
  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEisLRqu1UNoAeHav90MquuzKcrk2BFEuDQaQmsmI_1mH89sdqWkzxwYubBwkh4zt1yNPvSM8f0zJ-QWprKldmJqd-OJm1Xglw1wWjLM_W9W2HS4RZXb6cTssyyISgpBFjz8WxyYp_UUKeI/s400/autoregressive.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEisLRqu1UNoAeHav90MquuzKcrk2BFEuDQaQmsmI_1mH89sdqWkzxwYubBwkh4zt1yNPvSM8f0zJ-QWprKldmJqd-OJm1Xglw1wWjLM_W9W2HS4RZXb6cTssyyISgpBFjz8WxyYp_UUKeI/s1600/autoregressive.png)

  
  
The gray unit is the unit we are trying to compute, and the blue units are the values it depends on. and are scalars that are computed by passing through neural networks (magenta, orange circles). Even though the transformation is a mere scale-and-shift, the scale and shift can have complex dependencies on previous variables. For the first unit , and are usually set to learnable scalar variables that don’t depend on any or .  
  
More importantly, the transformation is designed this way so that computing the inverse does not require us to invert or . Because the transformation is parameterized as a scale-and-shift, we can recover the original noise variates by reversing the shift and scale: . The forward and inverse pass of the bijector only depend on the forward evaluation of and , allowing us to use non-invertible functions like ReLU and non-square matrix multiplication in the neural networks and .  
  
The inverse pass of the MAF model is used to evaluate density:  
  
distribution.log\_prob(bijector.inverse(x)) + bijector.inverse\_log\_det\_jacobian(x))  
  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEipnUHk0BJg9Ryi_ahBlWnBCFyGIgEZp3XHI5PBs3XB3Euuk69PF8Vp8vhz6fsGYovsAEGQ7WrITXyeuu60ASoKL8Dh1JbvWuPCEDOXOOV5VonsNJtqlMh2_jcoPiWUkDMKfr5ajMX7RkU/s400/autoregressive_inv.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEipnUHk0BJg9Ryi_ahBlWnBCFyGIgEZp3XHI5PBs3XB3Euuk69PF8Vp8vhz6fsGYovsAEGQ7WrITXyeuu60ASoKL8Dh1JbvWuPCEDOXOOV5VonsNJtqlMh2_jcoPiWUkDMKfr5ajMX7RkU/s1600/autoregressive_inv.png)

## Runtime Complexity and MADE

  
Autoregressive models and MAF can be trained “quickly” because all conditional likelihoods can be evaluated simultaneously in a single pass of D threads, leveraging the batch parallelism of modern GPUs. We are operating under the assumption that parallelism, such as [SIMD vectorization](https://en.wikipedia.org/wiki/SIMD) on CPUs/GPUs, has zero runtime overhead.  
  
On the other hand, sampling autoregressive models is slow because you must wait for all previous to be computed before computing new . The runtime complexity of generating a single sample is D sequential passes of a single thread, which fails to exploit processor parallelism.  
  
Another issue: in the parallelizable inverse pass, should we use separate neural nets (with differently-sized inputs) for computing each and ? That's inefficient, especially if we consider that learned representations between these D networks should be shared (as long as the autoregressive dependency is not violated). In the [Masked Autoencoder for Distribution Estimation](https://www.google.com/search?q=Masked+Autoencoder+for+Distribution+Estimation&oq=Masked+Autoencoder+for+Distribution+Estimation&aqs=chrome..69i57.205j0j9&sourceid=chrome&ie=UTF-8) (MADE) paper, the authors propose a very nice solution: use a single neural net to output all values of and simultaneously, but mask the weights so that the autoregressive property is preserved.  
  
This trick makes it possible to recover all values of from all values of with a single pass through a single neural network (D inputs, D outputs). This is far more efficient than processing D neural networks simultaneously (D(D+1)/2 inputs, D outputs).  
  
To summarize, MAF uses the MADE architecture as an efficiency trick for computing nonlinear parameters of shift-and-scale autoregressive transformations, and casts these efficient autoregressive models into the normalizing flows framework.  
  

## Inverse Autoregressive Flow (IAF)

  
In Inverse Autoregressive Flow, the nonlinear shift/scale statistics are computed using the previous noise variates , instead of the data samples:  
  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjZrAlEH1OMcZgfGExa641icuSEzc1YjGOwW2xOakJ3tBM-9h-v_gsanj5TxD-D7GApbDfmCxn6U8vlkn1I-bbS6VIiTbZXQk8c5x98ooQ2Voo-pizKl0pZNrl1uA1nsjeKSPfO8HSBmE4/s400/iaf.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjZrAlEH1OMcZgfGExa641icuSEzc1YjGOwW2xOakJ3tBM-9h-v_gsanj5TxD-D7GApbDfmCxn6U8vlkn1I-bbS6VIiTbZXQk8c5x98ooQ2Voo-pizKl0pZNrl1uA1nsjeKSPfO8HSBmE4/s1600/iaf.png)

  
  
The forward (sampling) pass of IAF is fast: all the can be computed in a single pass of threads working in parallel. IAF also uses MADE networks to implement this parallelism efficiently.  
  
However, if we are given a new data point and asked to evaluate the density, we need to recover and this process is slow: first we recover , then sequentially. On the other hand, it’s trivial to track the (log) probability of samples generated by IAF, since we already know all of the values to begin with without having to invert from .  
  
The astute reader will notice that if you re-label the bottom row as x\_1,.. x\_D, and the top row as u\_1, … u\_D, this is exactly equivalent to the Inverse Pass of the MAF bijector! Likewise, the inverse of IAF is nothing more than the forward pass of MAF (with and swapped). Therefore in TensorFlow Distributions, MAF and IAF are actually implemented using the exact same Bijector class, and there is a convenient “Invert” feature for inverting Bijectors to swap their inverse and forward passes.  
  
iaf\_bijector = tfb.Invert(maf\_bijector)  
  
IAF and MAF make opposite computational tradeoffs - MAF trains quickly but samples slowly, while IAF trains slowly but samples quickly. For training neural networks, we usually demand way more throughput with density evaluation than sampling, so MAF is usually a more appropriate choice when learning distributions.  
  

## Parallel Wavenet

  
An obvious follow-up question is whether these two approaches can be combined to get the best of both worlds, i.e. fast training *and* sampling.  
  
The answer is yes! The much-publicized [Parallel Wavenet](https://arxiv.org/abs/1711.10433) by DeepMind does exactly this: an autoregressive model (MAF) is used to train a generative model efficiently, then an IAF model is trained to maximize the likelihood of its own samples under this teacher. Recall that with IAF, it is costly to compute density of external data points (such as those from the training set), but it can cheaply compute density of its *own* samples by caching the noise variates , thereby circumventing the need to call the inverse pass. Thus, we can train the “student” IAF model by minimizing the divergence between the student and teacher distributions.  
  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhFheaRm9OF_4hGkoR6N95K4ya8E12CrLFVQTH08z2NFei3m_cscV1RC6BRUmrh_oyBWAmvRngE62i7MShPtIsxpnZ4KW5anBNs1DjG2Krm2vRwn5JFpTV0ZHxNhh2rOYmCku_oF9Oyy_c/s400/pdd.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhFheaRm9OF_4hGkoR6N95K4ya8E12CrLFVQTH08z2NFei3m_cscV1RC6BRUmrh_oyBWAmvRngE62i7MShPtIsxpnZ4KW5anBNs1DjG2Krm2vRwn5JFpTV0ZHxNhh2rOYmCku_oF9Oyy_c/s1600/pdd.png)

  
  
This is an incredibly impactful application of normalizing flows research - the end result is a real-time audio synthesis model that is 20 times faster to sample, and is already deployed in real-world products like the Google Assistant.  
  

## NICE and Real-NVP

  
Finally, we consider is Real-NVP, which can be thought of as a special case of the IAF bijector.  
  
In a NVP “coupling layer”, we fix an integer . Like IAF, is a shift-and-scale that depends on previous values. The difference is that we also force to only depend on these values, so a single network pass can be used to produce and .  
  
As for they are “pass-through” units that are set equivalently to . Therefore, Real-NVP is also a special case of the MAF bijector (since ).  
  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgvblXuavZGdK5ClAXwOigFd_Hs9nCadI80uYRRh7jyLvo1EuhlGhtSPuAGaqJq9F5bcB2_3WiZWIug07vNU_zr50QhgyNSqdsIW8c8x7deWJJuSI1iRTz0P7Krqr9RGtyWWHyr5dWaKWE/s400/real_nvp.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgvblXuavZGdK5ClAXwOigFd_Hs9nCadI80uYRRh7jyLvo1EuhlGhtSPuAGaqJq9F5bcB2_3WiZWIug07vNU_zr50QhgyNSqdsIW8c8x7deWJJuSI1iRTz0P7Krqr9RGtyWWHyr5dWaKWE/s1600/real_nvp.png)

  
  
Because the shift-and-scale statistics for the whole layer can be computed from either or in a single pass, NVP can perform forward and inverse computations in a single parallel pass (sampling and estimation are both fast). MADE is also not needed.  
  
However, empirical studies suggest that Real-NVP tends to underperform MAF and IAF and my experience has been that NVP tends to fit my toy 2D datasets (e.g. SIGGRAPH dataset) more poorly when using the same number of layers. Real-NVP and IAF are nearly equivalent in the 2D case, except the first unit of IAF is still transformed via a scale-and-shift that does not depend on , while Real-NVP leaves the first unit unmodified.  
  
Real-NVP was a follow-up work to the NICE bijector, which is a shift-only variant that assumes . Because NICE does not scale the distribution, the ILDJ is actually constant!  
  

## Batch Normalization Bijector

The Real-NVP paper proposes several novel contributions, one of which is a Batch Normalization bijector used to stabilize training. Conventionally, Batch Norm is applied to training neural networks where the forward statistics are mean-centered and scaled to diagonal unit covariance, and the batchnorm statistics (running mean, running variance) are accumulated via an exponential moving average. At test time, the accumulated statistics are used to normalize data.  
  
In normalizing flows, batch norm is used in bijector.inverse during training, and the accumulated statistics are used to de-normalize data at “test time” (bijector.forward). Concretely, BatchNorm Bijectors are typically implemented as follows:  
  
Inverse pass:  
1. Compute the current mean and standard deviation of the data distribution .
2. Update running mean and standard deviation
3. Batch normalize the data using current mean/std
Forward pass:  
1. Use running mean and standard deviation to un-normalize the data distribution.
  
Thanks to TF Bijectors, this can be implemented with only a few lines of code:  
  

```
class BatchNorm(tfb.Bijector):

    def __init__(self, eps=1e-5, decay=0.95, validate_args=False, name="batch_norm"):

        super(BatchNorm, self).__init__(

            event_ndims=1, validate_args=validate_args, name=name)

        self._vars_created = False

        self.eps = eps

        self.decay = decay

    def _create_vars(self, x):

        n = x.get_shape().as_list()[1]

        with tf.variable_scope(self.name):

            self.beta = tf.get_variable('beta', [1, n], dtype=DTYPE)

            self.gamma = tf.get_variable('gamma', [1, n], dtype=DTYPE)

            self.train_m = tf.get_variable(

                'mean', [1, n], dtype=DTYPE, trainable=False)

            self.train_v = tf.get_variable(

                'var', [1, n], dtype=DTYPE, initializer=tf.ones_initializer, trainable=False)

        self._vars_created = True

    def _forward(self, u):

        if not self._vars_created:

            self._create_vars(u)

        return (u - self.beta) * tf.exp(-self.gamma) * tf.sqrt(self.train_v + self.eps) + self.train_m

    def _inverse(self, x):

        # Eq 22. Called during training of a normalizing flow.

        if not self._vars_created:

            self._create_vars(x)

        # statistics of current minibatch

        m, v = tf.nn.moments(x, axes=[0], keep_dims=True)

        # update train statistics via exponential moving average

        update_train_m = tf.assign_sub(

            self.train_m, self.decay * (self.train_m - m))

        update_train_v = tf.assign_sub(

            self.train_v, self.decay * (self.train_v - v))

        # normalize using current minibatch statistics, followed by BN scale and shift

        with tf.control_dependencies([update_train_m, update_train_v]):

            return (x - m) * 1. / tf.sqrt(v + self.eps) * tf.exp(self.gamma) + self.beta

    def _inverse_log_det_jacobian(self, x):

        # at training time, the log_det_jacobian is computed from statistics of the

        # current minibatch.

        if not self._vars_created:

            self._create_vars(x)

        _, v = tf.nn.moments(x, axes=[0], keep_dims=True)

        abs_log_det_J_inv = tf.reduce_sum(

            self.gamma - .5 * tf.log(v + self.eps))

        return abs_log_det_J_inv
```

  
  
The ILDJ can be derived easily by simply taking the log derivative of inverse function (consider the univariate case).  
  

## Code Example

  
Thanks to the efforts of Josh Dillon and the Google Bayesflow team, there is already a flexible implementation of [MaskedAutoregressiveFlow](https://www.tensorflow.org/versions/master/api_docs/python/tf/contrib/distributions/bijectors/MaskedAutoregressiveFlow) Bijector that uses MADE networks to implement efficient recovery of for training.  
  
I’ve created a complex 2D distribution, which is a point cloud in the shape of the letters “SIGGRAPH” using this [blender script](https://gist.github.com/ericjang/dd56bbde3f9dc971c8ed6f78017c40f0). We construct our dataset, bijector, and transformed distribution in a very similar fashion to the first tutorial, so I won’t repeat the code snippets here - you can find the Jupyter notebook [here](https://github.com/ericjang/normalizing-flows-tutorial/blob/master/nf_part2_modern.ipynb). This notebook can train a normalizing flow using MAF, IAF, Real-NVP with/without BatchNorm, for both the "Two Moons" and "SIGGRAPH" datasets.  
  
One detail that’s easy to miss / introduce bugs on is that this doesn’t work at all unless you permute the ordering of variable at each flow. Otherwise, none of the layers’ autoregressive factorization will be learn structure of . Fortunately, TensorFlow has a Permute bijector specially made for doing this.  
  

```
for i in range(num_bijectors):

    bijectors.append(tfb.MaskedAutoregressiveFlow(

      shift_and_log_scale_fn=tfb.masked_autoregressive_default_template(

      hidden_layers=[512, 512])))

    bijectors.append(tfb.Permute(permutation=[1, 0]))

flow_bijector = tfb.Chain(list(reversed(bijectors[:-1])))
```

  
  
Here’s the learned flow, along with the final result. It reminds me a lot of a [taffy pulling machine](https://imgur.com/gallery/3oW9IgP).  
  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgTygqhkciBzhqoT1NRh7HUOaRWw1eq_xLrR9b-pML7HyxxHjuENP3nwaPJKbh1YwAmC6Ul7GHXjU7Za0qjiHEb3psNKSBQMhlZ9Wi7NyaC7z6k4G7X_psKlA3K_qURxN92Wmi8UGKcw1s/s400/siggraph_trained.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgTygqhkciBzhqoT1NRh7HUOaRWw1eq_xLrR9b-pML7HyxxHjuENP3nwaPJKbh1YwAmC6Ul7GHXjU7Za0qjiHEb3psNKSBQMhlZ9Wi7NyaC7z6k4G7X_psKlA3K_qURxN92Wmi8UGKcw1s/s1600/siggraph_trained.png)

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi0o_uJX8eVBRgV8AsnvZyuqPPQYOoPLe_1PEmEeA2S2Buc_eyxP2_jvOBMCVcH0l7pzGwyj85SlzxatKzpcJWVCDEhyphenhyphenLVAy5NjoHiwKBWEWu5n3YrNxpt2yBcmRRgPWFNoGFQ2c-8ryno/s400/siggraph_out.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi0o_uJX8eVBRgV8AsnvZyuqPPQYOoPLe_1PEmEeA2S2Buc_eyxP2_jvOBMCVcH0l7pzGwyj85SlzxatKzpcJWVCDEhyphenhyphenLVAy5NjoHiwKBWEWu5n3YrNxpt2yBcmRRgPWFNoGFQ2c-8ryno/s1600/siggraph_out.png)

## Discussion

  
TensorFlow distributions makes normalizing flows easy to implement, and automatically accumulate all the Jacobians determinants in a chain for us in a way that is clean and highly readable. When deciding which Normalizing Flow to use, consider the design tradeoff between a fast forward pass and a fast inverse pass, as well as between an expressive flow and a speedy ILJD.  
In Part 1 of the tutorial, I motivated Normalizing Flows by saying that we need availability of more powerful distributions that can be used in reinforcement learning and generative modeling. In the big picture of things, it’s not clear whether having volume-tracking normalizing flows is actually the best tool for AI applications like robotics, structured prediction, when techniques like variational inference and implicit density models already work extremely well in practice. Even still, normalizing flows are a neat family of methods to have in your back pocket and they have demonstrable real-world applications, such as in real-time generative audio models deployed on Google Assistant.

Although explicit-density models like normalizing flows are amenable to training via maximum likelihood, this is not the only way they can be used and are complementary to VAEs and GANs. It’s possible to use normalizing flow as a drop-in replacement for anywhere you would use a Gaussian, such as VAE priors and latent codes in GANs. For example, [this](http://proceedings.mlr.press/v48/ranganath16.pdf) paper use normalizing flows as flexible variational priors, and the [TensorFlow distributions](https://arxiv.org/pdf/1711.10604.pdf) paper presents a VAE that uses a normalizing flow as a prior along with a PixelCNN decoder. Parallel Wavenet trains an IAF "student" model via KL divergence.

One of the most intriguing properties of normalizing flows is that they implement reversible computation (i.e. have a defined inverse of an expressive function). This means that if we want to perform a backprop pass, we can re-compute the forward activation values without having to store them in memory during the forward pass (potentially expensive for large graphs). In a setting where credit assignment may take place over very long time scales, we can use reversible computation to “recover” past decision states while keeping memory usage bounded. In fact, this idea was utilized in the [RevNets](https://arxiv.org/abs/1707.04585) paper, and was actually inspired by the invertibility of the NICE bijector. I’m reminded of the main character from the film [Memento](https://en.wikipedia.org/wiki/Memento_\(film\)) who is unable to store memories, so he uses invertible compute to remember things.  
  
Thank you for reading.  
  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgLy_rISOSPCLrLzoxfvIlcUcFhi4PqIZ0rqSdpj5c2WJfaEWn7TCbbxzgrY5h2PeVwblrcRgAsvOc7cy3VL-kpKPRI7VuPk7YW8SIAkNsI7OJIwSNLkKylFf687DymCoFm8NgUB5OjAg4/s1600/salt_bae_mod.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgLy_rISOSPCLrLzoxfvIlcUcFhi4PqIZ0rqSdpj5c2WJfaEWn7TCbbxzgrY5h2PeVwblrcRgAsvOc7cy3VL-kpKPRI7VuPk7YW8SIAkNsI7OJIwSNLkKylFf687DymCoFm8NgUB5OjAg4/s1600/salt_bae_mod.png)

[Code on Github](https://github.com/ericjang/normalizing-flows-tutorial)

## Acknowledgements

  
I’m grateful to Dustin Tran, Luke Metz, Jonathan Shen, Katherine Lee, and Samy Bengio for proofreading this post.  
  

## References and Further Reading

- The content and outline of this blog post was heavily influenced by the [Masked Autoregressive Flow for Density Estimation](https://arxiv.org/abs/1705.07057) paper, which is very well-written and is more or less my primary source for understanding this topic. Give it a read!
- Some earlier work on NFs: [https://math.nyu.edu/faculty/tabak/publications/Tabak-Turner.pdf](https://math.nyu.edu/faculty/tabak/publications/Tabak-Turner.pdf) and [https://arxiv.org/pdf/1302.5125.pdf](https://arxiv.org/pdf/1302.5125.pdf) and [https://arxiv.org/abs/1505.05770](https://arxiv.org/abs/1505.05770)
- [Talk by Laurent Dinh](https://www.periscope.tv/w/1ypKdAVmbEpGW) & discussion by Twitter Cortex researchers. Some neat ideas and discussion here.
- Tutorial on [Normalizing Flows using PyMC](http://docs.pymc.io/notebooks/normalizing_flows_overview.html).
- There’s a body of work that I don’t fully understand yet, bridging Normalizing Flows to [Langevin Flow](https://arxiv.org/abs/1410.6460) and [Hamiltonian Flow](https://arxiv.org/abs/1410.6460). As the number of Bijectors in a normalizing flow goes to infinity, one arrives at a [Continuous-Time Flow](https://arxiv.org/abs/1709.01179), which apparently can express even richer transformations.