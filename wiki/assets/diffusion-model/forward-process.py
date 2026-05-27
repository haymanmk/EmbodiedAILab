"""Forward diffusion process on a 2D 'two-moons' dataset.

Visualizes x_t = sqrt(alpha_bar_t) * x_0 + sqrt(1 - alpha_bar_t) * eps,
with eps ~ N(0, I). Reads left->right as the forward (noising) process and
right->left as the reverse (denoising) process the network must learn.
"""

import numpy as np
import matplotlib.pyplot as plt


def two_moons(n, rng, noise=0.04):
    n_a = n // 2
    n_b = n - n_a
    t_a = np.pi * rng.random(n_a)
    a = np.stack([np.cos(t_a), np.sin(t_a)], axis=1)
    t_b = np.pi * rng.random(n_b)
    b = np.stack([1.0 - np.cos(t_b), 0.5 - np.sin(t_b)], axis=1)
    x = np.concatenate([a, b], axis=0)
    x = x + noise * rng.standard_normal(size=x.shape)
    return x


def main():
    rng = np.random.default_rng(0)

    x0 = two_moons(2000, rng)
    x0 = (x0 - x0.mean(axis=0)) / x0.std(axis=0)

    # Linear schedule on alpha_bar, from ~1 (clean) down to ~0 (pure noise).
    snapshots = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]  # fraction of T
    alpha_bars = [1.0 - s for s in snapshots]

    fig, axes = plt.subplots(1, len(snapshots), figsize=(15, 2.8), sharex=True, sharey=True)
    for ax, frac, abar in zip(axes, snapshots, alpha_bars):
        eps = rng.standard_normal(size=x0.shape)
        xt = np.sqrt(abar) * x0 + np.sqrt(1.0 - abar) * eps
        ax.scatter(xt[:, 0], xt[:, 1], s=3, alpha=0.5, color="#1f77b4", linewidths=0)
        ax.set_title(f"t = {int(frac * 1000)}\n" + r"$\bar\alpha_t$ = " + f"{abar:.2f}", fontsize=10)
        ax.set_xlim(-4.5, 4.5)
        ax.set_ylim(-4.5, 4.5)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])

    axes[0].set_ylabel("data plane", fontsize=9)
    fig.suptitle(
        "Forward diffusion: data → noise   (read right→left for the reverse process the network learns)",
        fontsize=11,
        y=1.02,
    )
    plt.tight_layout()
    plt.savefig("forward-process.png", dpi=120, bbox_inches="tight")


if __name__ == "__main__":
    main()
