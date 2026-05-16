"""Visualize the first-order Taylor argument behind grad-perpendicular-
to-tangent.

Two side-by-side panels at the same point on the level set h(x,y) = 1:

  Left:  step in tangent direction → stays on the contour (h unchanged
         to first order). Shows h(x+ε v) ≈ h(x) when ∇h·v = 0.
  Right: step in gradient direction → leaves the contour. Shows
         h(x+ε∇h) ≈ h(x) + ε ‖∇h‖².

Annotations report the actual h values at the step endpoints so the
reader can compare "essentially 1" vs. "noticeably larger than 1."

Run:
    cd wiki/assets/constraint-gradient && python3 tangent_decomposition.py
"""

import numpy as np
import matplotlib.pyplot as plt


def h(x, y):
    return 0.5 * x ** 2 + 1.5 * y ** 2 + 0.4 * x * y


def grad_h(x, y):
    return np.array([x + 0.4 * y, 3.0 * y + 0.4 * x])


def draw_panel(ax, mode, title):
    """mode: 'tangent' or 'normal'."""
    # Background contours (faint, so the eye picks up the level set)
    xs = np.linspace(0.6, 2.2, 200)
    ys = np.linspace(-1.0, 0.8, 200)
    X, Y = np.meshgrid(xs, ys)
    Z = h(X, Y)
    ax.contour(X, Y, Z, levels=[0.4, 0.7, 1.0, 1.3, 1.6],
               colors="#bbb", linewidths=0.7)
    ax.contour(X, Y, Z, levels=[1.0], colors="#d62728", linewidths=2.0)

    # Pick the point on h = 1 in the right half-plane near y = 0
    rs = np.linspace(0.01, 3.0, 5000)
    th = -0.1
    xs_r = rs * np.cos(th)
    ys_r = rs * np.sin(th)
    h_r = h(xs_r, ys_r)
    i = np.argmin(np.abs(h_r - 1.0))
    px, py = xs_r[i], ys_r[i]

    # Unit gradient and unit tangent at p
    g = grad_h(px, py)
    gmag = np.linalg.norm(g)
    u = g / gmag                # unit normal
    t = np.array([-u[1], u[0]]) # unit tangent (90° rotation)

    # Step length — visible but small enough that 1st-order story holds
    # cleanly: tangent step drift is O(ε²) curvature, normal step is O(ε).
    eps = 0.18

    # Origin point
    ax.plot([px], [py], "o", color="#222", ms=6, zorder=6)
    ax.annotate(
        f"  x  (h = {h(px, py):.3f})",
        xy=(px, py), color="#222", fontsize=10, va="center",
    )

    # Draw both reference arrows lightly in both panels
    al_n = 0.55
    al_t = 0.55
    ax.annotate(
        "",
        xy=(px + al_n * u[0], py + al_n * u[1]), xytext=(px, py),
        arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.3, alpha=0.5),
    )
    ax.annotate(
        "",
        xy=(px + al_t * t[0], py + al_t * t[1]), xytext=(px, py),
        arrowprops=dict(arrowstyle="->", color="#1f77b4", lw=1.3, alpha=0.5),
    )
    ax.text(px + al_n * u[0] + 0.04, py + al_n * u[1] + 0.05,
            r"$\nabla h$", color="#d62728", fontsize=11)
    ax.text(px + al_t * t[0] - 0.32, py + al_t * t[1] - 0.05,
            r"tangent $v$", color="#1f77b4", fontsize=11)

    # The actual step
    if mode == "tangent":
        dx, dy = eps * t
        step_color = "#1f77b4"
        endpoint_label = (
            r"$x + \epsilon v$"
            + f"\n(h = {h(px + dx, py + dy):.3f})"
        )
    else:
        # Step along ∇h, same Euclidean length ε for fair comparison
        dx, dy = eps * u
        step_color = "#d62728"
        endpoint_label = (
            r"$x + \epsilon\, \hat{\nabla h}$"
            + f"\n(h = {h(px + dx, py + dy):.3f})"
        )

    ax.annotate(
        "",
        xy=(px + dx, py + dy), xytext=(px, py),
        arrowprops=dict(arrowstyle="->", color=step_color, lw=2.6),
    )
    ax.plot([px + dx], [py + dy], "o", color=step_color, ms=7, zorder=6)
    ax.annotate(
        endpoint_label,
        xy=(px + dx, py + dy),
        xytext=(px + dx + 0.06, py + dy - 0.06 if mode == "tangent"
                else py + dy + 0.04),
        color=step_color, fontsize=10,
    )

    # Layout
    ax.set_xlim(0.6, 2.2)
    ax.set_ylim(-1.0, 0.8)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title(title, fontsize=11)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, alpha=0.15)


def main():
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6))

    draw_panel(
        axes[0], "tangent",
        r"Tangent step: $\nabla h \cdot v = 0$ ⟹ $h$ unchanged "
        r"to first order",
    )
    draw_panel(
        axes[1], "normal",
        r"Normal step: $\nabla h \cdot v \ne 0$ ⟹ $h$ changes "
        r"linearly in $\epsilon$",
    )

    fig.suptitle(
        r"Why $\nabla h \perp$ tangent: the first-order Taylor argument, "
        r"step length $\epsilon = 0.18$",
        fontsize=12, y=1.02,
    )
    fig.tight_layout()
    fig.savefig("tangent_decomposition.png", dpi=120,
                bbox_inches="tight")
    print("wrote tangent_decomposition.png")


if __name__ == "__main__":
    main()
