"""Plot the sigmoid (logistic) function for the concept page.

Run from this directory:
    cd wiki/assets/sigmoid && python sigmoid.py

Produces sigmoid.png in this directory.
"""

import numpy as np
import matplotlib.pyplot as plt


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def main():
    x = np.linspace(-8.0, 8.0, 400)
    y = sigmoid(x)
    dy = y * (1.0 - y)

    fig, ax = plt.subplots(figsize=(7.0, 4.2))

    # sigmoid curve
    ax.plot(x, y, color="#1f77b4", lw=2.2, label=r"$\sigma(x) = 1/(1+e^{-x})$")

    # derivative for shape reference
    ax.plot(x, dy, color="#ff7f0e", lw=1.4, ls="--",
            label=r"$\sigma'(x) = \sigma(x)(1-\sigma(x))$")

    # asymptotes
    ax.axhline(0.0, color="#888", lw=0.7, ls=":")
    ax.axhline(1.0, color="#888", lw=0.7, ls=":")
    ax.axhline(0.5, color="#aaaaaa", lw=0.6, ls=":")
    ax.axvline(0.0, color="#aaaaaa", lw=0.6, ls=":")

    # mark sigma(0) = 0.5
    ax.plot([0.0], [0.5], marker="o", color="#d62728", ms=6, zorder=5)
    ax.annotate(r"$\sigma(0) = \frac{1}{2}$",
                xy=(0.0, 0.5), xytext=(1.0, 0.35),
                arrowprops=dict(arrowstyle="-", color="#666", lw=0.8),
                fontsize=11, color="#444")

    # saturation labels
    ax.text(-7.6, 0.04, r"$\sigma(x) \to 0$  (saturated low)",
            fontsize=10, color="#444")
    ax.text(3.8, 0.96, r"$\sigma(x) \to 1$  (saturated high)",
            fontsize=10, color="#444")

    ax.set_xlim(-8.0, 8.0)
    ax.set_ylim(-0.05, 1.15)
    ax.set_xlabel("x")
    ax.set_ylabel("σ(x)")
    ax.set_title("The sigmoid (logistic) function")
    ax.legend(loc="lower right", frameon=False, fontsize=10)
    ax.grid(True, alpha=0.25)

    fig.tight_layout()
    fig.savefig("sigmoid.png", dpi=120)
    print("wrote sigmoid.png")


if __name__ == "__main__":
    main()
