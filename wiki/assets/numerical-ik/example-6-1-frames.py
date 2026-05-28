"""
MR Example 6.1, iteration 0 — same physical scene in two coordinate frames.

LEFT panel: space frame {s}. Shows the actual 2R arm at theta^0=(0,30 deg),
the body frame {b} attached to the EE (rotated 30 deg from {s}), the goal
pose, the ICR (screw axis) at space coords (0.683, 0.184), the arc, and the
v_b tangent direction drawn at the EE.

RIGHT panel: body frame {b} at theta^0. Same scene, re-expressed: body
origin at (0,0), x_b-y_b axes axis-aligned, goal origin at (-0.866, 1.500),
ICR at (-1.183, 0.317), v_b = (0.498, 1.858) is now a familiar coordinate
vector.

Both panels show the SAME physical ICR point — only its coordinate
description differs.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

theta1, theta2 = 0.0, np.radians(30)
theta1_d, theta2_d = np.radians(30), np.radians(90)

joint1 = np.array([0.0, 0.0])
joint2 = np.array([np.cos(theta1), np.sin(theta1)])
ee_space = joint2 + np.array([np.cos(theta1 + theta2), np.sin(theta1 + theta2)])

body_angle = theta1 + theta2
x_b_s = np.array([np.cos(body_angle), np.sin(body_angle)])
y_b_s = np.array([-np.sin(body_angle), np.cos(body_angle)])

goal_angle = theta1_d + theta2_d
goal_joint2 = np.array([np.cos(theta1_d), np.sin(theta1_d)])
goal_ee = goal_joint2 + np.array([np.cos(goal_angle), np.sin(goal_angle)])
x_g_s = np.array([np.cos(goal_angle), np.sin(goal_angle)])
y_g_s = np.array([-np.sin(goal_angle), np.cos(goal_angle)])

omega_zb = 1.571
v_xb, v_yb = 0.498, 1.858

icr_b = np.array([-v_yb / omega_zb, v_xb / omega_zb])
icr_s = ee_space + icr_b[0] * x_b_s + icr_b[1] * y_b_s
goal_b = np.array([-0.866, 1.500])

def arc_points(center, p_start, p_end, n=80):
    r = p_start - center
    radius = np.linalg.norm(r)
    t0 = np.arctan2(r[1], r[0])
    re = p_end - center
    t1 = np.arctan2(re[1], re[0])
    if t1 < t0:
        t1 += 2 * np.pi
    ts = np.linspace(t0, t1, n)
    return center[0] + radius * np.cos(ts), center[1] + radius * np.sin(ts)

arc_x_s, arc_y_s = arc_points(icr_s, ee_space, goal_ee)
arc_x_b, arc_y_b = arc_points(icr_b, np.array([0, 0]), goal_b)

r_s = ee_space - icr_s
v_b_in_space = omega_zb * np.array([-r_s[1], r_s[0]])

r_b = np.array([0, 0]) - icr_b
v_b_tangent_body = omega_zb * np.array([-r_b[1], r_b[0]])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# ====================================================================
# LEFT — SPACE FRAME
# ====================================================================
ax = ax1
ax.annotate("", xy=(0.45, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="black", lw=1.4))
ax.annotate("", xy=(0, 0.45), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="black", lw=1.4))
ax.text(0.47, -0.06, r"$\hat{x}_s$", fontsize=14, color="black")
ax.text(-0.10, 0.45, r"$\hat{y}_s$", fontsize=14, color="black")
ax.text(0.04, -0.18, "space frame $\\{s\\}$", fontsize=9, color="black")

ax.plot([joint1[0], joint2[0]], [joint1[1], joint2[1]],
        color="#1f77b4", lw=4, solid_capstyle="round")
ax.plot([joint2[0], ee_space[0]], [joint2[1], ee_space[1]],
        color="#1f77b4", lw=4, solid_capstyle="round")
ax.plot(*joint1, "s", color="black", markersize=10)
ax.plot(*joint2, "o", color="white", markeredgecolor="#1f77b4",
        markersize=9, mew=2)
ax.plot(*ee_space, "o", color="#1f77b4", markersize=10, zorder=5)

axis_len_b = 0.4
ax.annotate("", xy=ee_space + axis_len_b * x_b_s, xytext=ee_space,
            arrowprops=dict(arrowstyle="->", color="#1f77b4", lw=1.8))
ax.annotate("", xy=ee_space + axis_len_b * y_b_s, xytext=ee_space,
            arrowprops=dict(arrowstyle="->", color="#1f77b4", lw=1.8))
xb_label_pos = ee_space + (axis_len_b + 0.05) * x_b_s
yb_label_pos = ee_space + (axis_len_b + 0.05) * y_b_s
ax.text(*xb_label_pos, r"$\hat{x}_b$", fontsize=13, color="#1f77b4")
ax.text(yb_label_pos[0] - 0.18, yb_label_pos[1], r"$\hat{y}_b$",
        fontsize=13, color="#1f77b4")
ax.annotate("EE / body frame $\\{b\\}$\nspace coords:\n"
            f"$({ee_space[0]:.3f},\\,{ee_space[1]:.3f})$",
            ee_space, textcoords="offset points", xytext=(14, -45),
            fontsize=9.5, color="#1f77b4")

ax.plot([joint1[0], goal_joint2[0]], [joint1[1], goal_joint2[1]],
        color="#d62728", lw=3, alpha=0.32, solid_capstyle="round")
ax.plot([goal_joint2[0], goal_ee[0]], [goal_joint2[1], goal_ee[1]],
        color="#d62728", lw=3, alpha=0.32, solid_capstyle="round")
ax.plot(*goal_joint2, "o", color="white", markeredgecolor="#d62728",
        markersize=8, mew=2, alpha=0.6)
ax.plot(*goal_ee, "o", color="#d62728", markersize=10, zorder=5)
ax.annotate("", xy=goal_ee + axis_len_b * x_g_s, xytext=goal_ee,
            arrowprops=dict(arrowstyle="->", color="#d62728",
                            lw=1.5, alpha=0.7))
ax.annotate("", xy=goal_ee + axis_len_b * y_g_s, xytext=goal_ee,
            arrowprops=dict(arrowstyle="->", color="#d62728",
                            lw=1.5, alpha=0.7))
ax.annotate("goal pose $\\{goal\\}$\nspace coords:\n"
            f"$({goal_ee[0]:.3f},\\,{goal_ee[1]:.3f})$",
            goal_ee, textcoords="offset points", xytext=(-130, 4),
            fontsize=9.5, color="#d62728")

ax.plot(arc_x_s, arc_y_s, "--", color="#2ca02c", lw=1.8,
        label="arc (90° CCW)")
ax.plot([icr_s[0], ee_space[0]], [icr_s[1], ee_space[1]],
        color="#2ca02c", alpha=0.3, lw=1)
ax.plot([icr_s[0], goal_ee[0]], [icr_s[1], goal_ee[1]],
        color="#2ca02c", alpha=0.3, lw=1)

ax.plot(*icr_s, "x", color="#2ca02c", markersize=14, markeredgewidth=3)
ax.annotate(f"screw axis (ICR)\nspace coords:\n$({icr_s[0]:.3f},\\,{icr_s[1]:.3f})$",
            icr_s, textcoords="offset points", xytext=(15, -45),
            fontsize=9.5, color="#2ca02c")

scale = 0.4
arr = FancyArrowPatch(ee_space, ee_space + scale * v_b_in_space,
                      arrowstyle="-|>", color="#ff7f0e", lw=2.6,
                      mutation_scale=14)
ax.add_patch(arr)
ax.text(*(ee_space + scale * v_b_in_space + np.array([-0.65, 0.10])),
        f"$v_b$ direction at EE\n"
        f"in space coords:\n$({v_b_in_space[0]:.3f},\\,{v_b_in_space[1]:.3f})$",
        fontsize=9.5, color="#ff7f0e")

ax.set_xlim(-0.6, 2.6)
ax.set_ylim(-0.9, 2.4)
ax.set_aspect("equal")
ax.grid(True, alpha=0.3)
ax.axhline(0, color="black", lw=0.4)
ax.axvline(0, color="black", lw=0.4)
ax.set_xlabel(r"$x_s$ (m)", fontsize=11)
ax.set_ylabel(r"$y_s$ (m)", fontsize=11)
ax.set_title("LEFT — space frame {s}\n(the physical scene)", fontsize=12)
ax.legend(loc="upper right", fontsize=9)

# ====================================================================
# RIGHT — BODY FRAME at theta^0
# ====================================================================
ax = ax2
axis_len = 0.55
ax.annotate("", xy=(axis_len, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="#1f77b4", lw=1.6))
ax.annotate("", xy=(0, axis_len), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="#1f77b4", lw=1.6))
ax.text(axis_len + 0.04, -0.05, r"$\hat{x}_b$", fontsize=14, color="#1f77b4")
ax.text(-0.10, axis_len + 0.02, r"$\hat{y}_b$", fontsize=14, color="#1f77b4")

ax.plot([icr_b[0], 0], [icr_b[1], 0], color="#2ca02c", alpha=0.35, lw=1.0)
ax.plot([icr_b[0], goal_b[0]], [icr_b[1], goal_b[1]],
        color="#2ca02c", alpha=0.35, lw=1.0)

ax.plot(arc_x_b, arc_y_b, "--", color="#2ca02c", lw=1.8,
        label="arc (90° CCW)")
ax.plot([0, goal_b[0]], [0, goal_b[1]],
        ":", color="#888", lw=1.4, label="naive displacement (NOT $v_b$)")

scale = 0.5
arr = FancyArrowPatch((0, 0), scale * v_b_tangent_body,
                      arrowstyle="-|>", color="#ff7f0e", lw=2.6,
                      mutation_scale=16)
ax.add_patch(arr)
ax.text(scale * v_b_tangent_body[0] - 0.05,
        scale * v_b_tangent_body[1] + 0.13,
        r"$v_b = (0.498,\,1.858)$" + "\ntangent at body origin",
        fontsize=10, color="#ff7f0e")

ax.plot(0, 0, "o", color="#1f77b4", markersize=10, zorder=5)
ax.annotate("body origin (EE)\nbody coords:\n$(0,\\,0)$",
            (0, 0), textcoords="offset points", xytext=(10, -40),
            fontsize=9.5, color="#1f77b4")

ax.plot(*goal_b, "o", color="#d62728", markersize=10, zorder=5)
ax.annotate(f"goal origin\nbody coords:\n$({goal_b[0]:.3f},\\,{goal_b[1]:.3f})$",
            goal_b, textcoords="offset points", xytext=(-115, 4),
            fontsize=9.5, color="#d62728")

ax.plot(*icr_b, "x", color="#2ca02c", markersize=14, markeredgewidth=3, zorder=5)
ax.annotate(f"screw axis (ICR)\nbody coords:\n$({icr_b[0]:.3f},\\,{icr_b[1]:.3f})$",
            icr_b, textcoords="offset points", xytext=(-160, -45),
            fontsize=9.5, color="#2ca02c")

ax.axhline(0, color="black", lw=0.4)
ax.axvline(0, color="black", lw=0.4)
ax.set_xlim(-2.4, 1.5)
ax.set_ylim(-0.9, 2.4)
ax.set_aspect("equal")
ax.grid(True, alpha=0.3)
ax.set_xlabel(r"$x_b$ (m, body frame)", fontsize=11)
ax.set_ylabel(r"$y_b$ (m, body frame)", fontsize=11)
ax.set_title(r"RIGHT — body frame {b} at $\theta^0$" + "\n(same scene re-expressed)",
             fontsize=12)
ax.legend(loc="lower right", fontsize=9)

fig.suptitle(
    "Example 6.1 iteration 0 — same physical scene, two coordinate frames\n"
    "ICR is one physical point: space coords $(0.683,\\,0.184)$  ≡  body coords $(-1.183,\\,0.317)$",
    fontsize=12,
)

plt.tight_layout()
plt.savefig("example-6-1-frames.png", dpi=120, bbox_inches="tight")
