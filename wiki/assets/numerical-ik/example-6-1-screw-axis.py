"""
Modern Robotics Example 6.1, iteration 0 — body-frame visualization
showing why v_xb > 0 even though the goal origin is in the -x_b direction.

Plots, in the body frame of the EE at theta^0 = (0 deg, 30 deg):
  - body origin (EE) at (0, 0)
  - goal origin at (-0.866, 1.500)
  - screw axis / ICR at (-1.183, 0.317)
  - arc trajectory: 90 deg CCW sweep around ICR from body origin to goal
  - v_b initial-tangent arrow at body origin
  - "naive" straight-line displacement vector to the goal, dashed (NOT v_b)

Numerical body twist from the textbook table (row i=0):
  V_b = (omega_zb, v_xb, v_yb) = (1.571, 0.498, 1.858)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

omega_zb = 1.571
v_xb = 0.498
v_yb = 1.858

body_origin = np.array([0.0, 0.0])
goal_origin = np.array([-0.866, 1.500])
icr = np.array([-v_yb / omega_zb, v_xb / omega_zb])

r_vec = body_origin - icr
radius = np.linalg.norm(r_vec)
theta_start = np.arctan2(r_vec[1], r_vec[0])
theta_end = np.arctan2(goal_origin[1] - icr[1], goal_origin[0] - icr[0])
if theta_end < theta_start:
    theta_end += 2 * np.pi
arc_t = np.linspace(theta_start, theta_end, 80)
arc_x = icr[0] + radius * np.cos(arc_t)
arc_y = icr[1] + radius * np.sin(arc_t)

tangent_dir = np.array([-r_vec[1], r_vec[0]])
v_b_vec = omega_zb * tangent_dir

fig, ax = plt.subplots(figsize=(7.5, 7.5))

axis_len = 0.55
ax.annotate("", xy=(axis_len, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="#555", lw=1.2))
ax.annotate("", xy=(0, axis_len), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="#555", lw=1.2))
ax.text(axis_len + 0.04, -0.04, r"$\hat{x}_b$", color="#555", fontsize=13)
ax.text(-0.10, axis_len + 0.02, r"$\hat{y}_b$", color="#555", fontsize=13)

ax.plot([icr[0], body_origin[0]], [icr[1], body_origin[1]],
        color="#2ca02c", alpha=0.35, lw=1.0)
ax.plot([icr[0], goal_origin[0]], [icr[1], goal_origin[1]],
        color="#2ca02c", alpha=0.35, lw=1.0)

ax.plot(arc_x, arc_y, "--", color="#2ca02c", lw=1.8,
        label="arc trajectory (90° CCW)")

ax.plot([body_origin[0], goal_origin[0]], [body_origin[1], goal_origin[1]],
        ":", color="#888", lw=1.4,
        label="naive displacement (NOT $v_b$)")

scale = 0.5
arrow = FancyArrowPatch(
    body_origin,
    body_origin + scale * v_b_vec,
    arrowstyle="-|>", color="#ff7f0e", lw=2.6, mutation_scale=16,
)
ax.add_patch(arrow)
ax.text(scale * v_b_vec[0] - 0.05, scale * v_b_vec[1] + 0.12,
        r"$v_b = (0.498,\,1.858)$" + "\ntangent at body origin",
        fontsize=11, color="#ff7f0e")

ax.plot(*body_origin, "o", color="#1f77b4", markersize=10, zorder=5)
ax.annotate("body origin (EE)\nat $\\theta^0$",
            body_origin, textcoords="offset points", xytext=(10, -32),
            fontsize=11, color="#1f77b4")

ax.plot(*goal_origin, "o", color="#d62728", markersize=10, zorder=5)
ax.annotate("goal origin\n$(-0.866,\\, 1.500)$",
            goal_origin, textcoords="offset points", xytext=(-115, 6),
            fontsize=11, color="#d62728")

ax.plot(*icr, "x", color="#2ca02c", markersize=14, markeredgewidth=3,
        zorder=5)
ax.annotate("screw axis (ICR)\n$(-1.183,\\, 0.317)$",
            icr, textcoords="offset points", xytext=(-150, -36),
            fontsize=11, color="#2ca02c")

ax.axhline(0, color="black", lw=0.4)
ax.axvline(0, color="black", lw=0.4)
ax.set_xlabel(r"$x_b$ (body frame, m)", fontsize=12)
ax.set_ylabel(r"$y_b$ (body frame, m)", fontsize=12)
ax.set_title(
    "Modern Robotics Example 6.1, iteration 0 (body frame)\n"
    r"Why $v_{xb} > 0$ even though the goal is in the $-\hat{x}_b$ direction",
    fontsize=12,
)
ax.set_xlim(-2.4, 1.4)
ax.set_ylim(-0.9, 2.3)
ax.set_aspect("equal")
ax.grid(True, alpha=0.3)
ax.legend(loc="lower right", fontsize=10, framealpha=0.95)

plt.tight_layout()
plt.savefig("example-6-1-screw-axis.png", dpi=120, bbox_inches="tight")
