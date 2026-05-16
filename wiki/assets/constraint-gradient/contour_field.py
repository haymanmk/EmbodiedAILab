"""Visualize the hiker analogy: contour lines of h(x,y) plus gradient
arrows. Gradient arrows must visibly be perpendicular to the contour
they sit on.

Run:
    cd wiki/assets/constraint-gradient && python3 contour_field.py
"""

import numpy as np
import matplotlib.pyplot as plt


def h(x, y):
    # Tilted elliptical bowl — non-trivial enough that gradients change
    # direction across the plane.
    return 0.5 * x ** 2 + 1.5 * y ** 2 + 0.4 * x * y


def grad_h(x, y):
    # ∇h = ( ∂h/∂x , ∂h/∂y )
    dhdx = x + 0.4 * y
    dhdy = 3.0 * y + 0.4 * x
    return dhdx, dhdy


def main():
    # Background field
    xs = np.linspace(-3.0, 3.0, 400)
    ys = np.linspace(-2.5, 2.5, 400)
    X, Y = np.meshgrid(xs, ys)
    Z = h(X, Y)

    fig, ax = plt.subplots(figsize=(7.5, 5.5))

    # Faint filled bands for "altitude"
    ax.contourf(X, Y, Z, levels=12, cmap="Blues", alpha=0.35)

    # Contour lines (the level sets) — emphasize one as the constraint
    levels = [0.25, 1.0, 2.0, 3.5, 5.5]
    cs = ax.contour(X, Y, Z, levels=levels, colors="#444", linewidths=1.0)
    ax.clabel(cs, fmt={lv: f"h = {lv}" for lv in levels}, fontsize=9,
              inline=True, inline_spacing=4)

    # Highlight one contour as "the constraint h(x,y) = 1"
    cs_hi = ax.contour(X, Y, Z, levels=[1.0], colors="#d62728",
                       linewidths=2.4)

    # Sample points ON the highlighted contour h = 1
    sample_pts = []
    target = 1.0
    for theta in np.linspace(0, 2 * np.pi, 9, endpoint=False):
        # Search radially for the contour
        rs = np.linspace(0.01, 2.5, 600)
        xs_r = rs * np.cos(theta)
        ys_r = rs * np.sin(theta)
        h_r = h(xs_r, ys_r)
        # Find where h crosses target
        idx = np.argmin(np.abs(h_r - target))
        if abs(h_r[idx] - target) < 0.05:
            sample_pts.append((xs_r[idx], ys_r[idx]))

    # Plot gradient arrows at each sample point — scaled to a sensible
    # visual length so the perpendicularity reads clearly
    arrow_len = 0.55  # in axis units
    for px, py in sample_pts:
        gx, gy = grad_h(px, py)
        gmag = np.hypot(gx, gy)
        ux, uy = gx / gmag, gy / gmag  # unit gradient direction
        ax.annotate(
            "",
            xy=(px + arrow_len * ux, py + arrow_len * uy),
            xytext=(px, py),
            arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.8),
        )
        ax.plot([px], [py], "o", color="#222", ms=4, zorder=5)

    # Legend hint: single sample tangent at one point
    px, py = sample_pts[0]
    gx, gy = grad_h(px, py)
    gmag = np.hypot(gx, gy)
    ux, uy = gx / gmag, gy / gmag
    tx, ty = -uy, ux  # 90° rotation = tangent
    tan_len = 0.5
    ax.annotate(
        "",
        xy=(px + tan_len * tx, py + tan_len * ty),
        xytext=(px - tan_len * tx, py - tan_len * ty),
        arrowprops=dict(arrowstyle="-", color="#1f77b4", lw=2.0),
    )
    # Small right-angle indicator
    s = 0.12
    corner = np.array([px + s * ux + s * tx,
                       py + s * uy + s * ty])
    p1 = np.array([px + s * ux, py + s * uy])
    p2 = np.array([px + s * tx, py + s * ty])
    ax.plot([p1[0], corner[0], p2[0]], [p1[1], corner[1], p2[1]],
            color="#666", lw=0.9)

    # Annotations
    ax.annotate(r"$\nabla h$", xy=(px + arrow_len * ux + 0.05,
                                   py + arrow_len * uy + 0.05),
                color="#d62728", fontsize=12, fontweight="bold")
    ax.annotate("tangent", xy=(px - tan_len * tx - 0.65,
                               py - tan_len * ty - 0.15),
                color="#1f77b4", fontsize=11, fontweight="bold")
    ax.annotate("constraint\n" + r"$h(x,y) = 1$",
                xy=(2.0, -1.3), color="#d62728", fontsize=11,
                ha="center")

    ax.set_xlim(-3.0, 3.0)
    ax.set_ylim(-2.5, 2.5)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(
        r"Gradient $\nabla h$ is perpendicular to the level set "
        r"$h(x,y) = c$ at every regular point"
    )
    ax.grid(True, alpha=0.15)

    fig.tight_layout()
    fig.savefig("contour_field.png", dpi=120)
    print("wrote contour_field.png")


if __name__ == "__main__":
    main()
