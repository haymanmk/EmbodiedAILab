"""Visualize the score function s(x) = grad log p(x) for a 2D Gaussian
mixture. The score is what a denoising network implicitly learns: a vector
field that, at every point in space, points toward higher data density.

Side panel: a few sample trajectories from Langevin dynamics
x_{k+1} = x_k + eta * s(x_k) + sqrt(2*eta) * z, z ~ N(0, I)
starting from pure noise and walking 'uphill in log-density' under the
score field.
"""

import numpy as np
import matplotlib.pyplot as plt


def make_gmm(centers, sigma):
    centers = np.asarray(centers)

    def log_p(x):
        # x: (..., 2). Returns log-density up to a constant.
        diffs = x[..., None, :] - centers  # (..., K, 2)
        sq = -0.5 * (diffs ** 2).sum(axis=-1) / sigma ** 2  # (..., K)
        # log mean over components; constant offsets drop out for gradient.
        m = sq.max(axis=-1, keepdims=True)
        return (m.squeeze(-1) + np.log(np.exp(sq - m).mean(axis=-1)))

    def score(x):
        diffs = x[..., None, :] - centers  # (..., K, 2)
        sq = -0.5 * (diffs ** 2).sum(axis=-1) / sigma ** 2
        m = sq.max(axis=-1, keepdims=True)
        w = np.exp(sq - m.squeeze(-1)[..., None])  # responsibilities (unnormalized)
        w = w / w.sum(axis=-1, keepdims=True)
        # grad log p = sum_k w_k * (centers_k - x) / sigma^2
        grad = ((centers - x[..., None, :]) * w[..., None]).sum(axis=-2) / sigma ** 2
        return grad, log_p(x)

    return score, log_p


def main():
    rng = np.random.default_rng(1)

    centers = [(-1.5, -1.0), (1.5, -1.0), (0.0, 1.7)]
    sigma = 0.6
    score, log_p = make_gmm(centers, sigma)

    # Density contours.
    xs = np.linspace(-4, 4, 240)
    ys = np.linspace(-4, 4, 240)
    XX, YY = np.meshgrid(xs, ys)
    grid = np.stack([XX, YY], axis=-1)
    LP = log_p(grid)

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(11, 5))

    # Left: contours + score arrows.
    ax_left.contour(XX, YY, np.exp(LP), levels=10, cmap="Blues", alpha=0.8)

    qx = np.linspace(-4, 4, 18)
    qy = np.linspace(-4, 4, 18)
    QX, QY = np.meshgrid(qx, qy)
    qgrid = np.stack([QX, QY], axis=-1)
    S, _ = score(qgrid)
    # Normalize arrow length for legibility.
    mag = np.linalg.norm(S, axis=-1, keepdims=True) + 1e-9
    Sn = S / np.maximum(mag, 0.5)
    ax_left.quiver(QX, QY, Sn[..., 0], Sn[..., 1], color="#d62728", scale=22, width=0.0035, alpha=0.85)

    ax_left.set_title(r"Score field $\nabla \log p(x)$ (red) over density $p(x)$ (blue)", fontsize=10)
    ax_left.set_xlim(-4, 4)
    ax_left.set_ylim(-4, 4)
    ax_left.set_aspect("equal")
    ax_left.set_xticks([])
    ax_left.set_yticks([])

    # Right: Langevin sampling trajectories starting from pure noise.
    ax_right.contour(XX, YY, np.exp(LP), levels=10, cmap="Blues", alpha=0.5)

    n_traj = 5
    n_steps = 400
    eta = 0.02

    x = rng.standard_normal(size=(n_traj, 2)) * 2.5  # start far from modes
    traj = [x.copy()]
    for _ in range(n_steps):
        s, _ = score(x)
        x = x + eta * s + np.sqrt(2 * eta) * rng.standard_normal(size=x.shape) * 0.3
        traj.append(x.copy())
    traj = np.stack(traj, axis=0)  # (steps+1, n_traj, 2)

    colors = plt.cm.viridis(np.linspace(0, 0.9, n_traj))
    for i in range(n_traj):
        ax_right.plot(traj[:, i, 0], traj[:, i, 1], color=colors[i], lw=1.0, alpha=0.8)
        ax_right.scatter(traj[0, i, 0], traj[0, i, 1], color=colors[i], marker="o", s=40, edgecolor="black", zorder=3)
        ax_right.scatter(traj[-1, i, 0], traj[-1, i, 1], color=colors[i], marker="*", s=80, edgecolor="black", zorder=3)

    ax_right.set_title("Langevin sampling: ○ noisy start → ★ data mode\n(walking 'uphill' in log-density)", fontsize=10)
    ax_right.set_xlim(-4, 4)
    ax_right.set_ylim(-4, 4)
    ax_right.set_aspect("equal")
    ax_right.set_xticks([])
    ax_right.set_yticks([])

    plt.tight_layout()
    plt.savefig("score-field.png", dpi=120, bbox_inches="tight")


if __name__ == "__main__":
    main()
