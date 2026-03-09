"""
Generate heatmap and radar charts for the Joy in Software Creation paper.
Uses the CORRECTED sensitivity matrix (Phase 1.1 reconciliation).

Usage:  python generate_figures.py
Output: images/heatmap.png, images/radar.png
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import FancyBboxPatch
from math import pi

# ── Corrected sensitivity matrix ──────────────────────────────────────────

archetypes = [
    "Mastery-Seeker", "Solver", "Architect", "Builder",
    "Creator", "Synthesizer", "Helper", "Stabilizer",
    "Explorer", "Strategist", "Harmonizer", "Autonomist",
]

dimensions = ["Growth", "Resolution", "Coherence", "Creation", "Contribution", "Autonomy"]

# Rows = archetypes, Cols = dimensions  (G, R, C, Cr, Co, A)
data = np.array([
    [1.0, 0.6, 0.3, 0.0, 0.0, 0.0],  # Mastery-Seeker
    [0.6, 1.0, 0.6, 0.0, 0.0, 0.0],  # Solver
    [0.3, 0.6, 1.0, 0.0, 0.3, 0.3],  # Architect
    [0.6, 0.6, 0.3, 1.0, 0.0, 0.0],  # Builder
    [0.3, 0.0, 0.0, 1.0, 0.0, 0.6],  # Creator
    [0.3, 0.6, 1.0, 0.6, 0.6, 0.0],  # Synthesizer
    [0.3, 0.6, 0.0, 0.0, 1.0, 0.3],  # Helper
    [0.0, 1.0, 0.6, 0.0, 0.6, 0.0],  # Stabilizer
    [0.6, 0.0, 0.0, 0.6, 0.3, 1.0],  # Explorer
    [0.6, 0.3, 0.6, 0.0, 1.0, 0.3],  # Strategist
    [0.3, 0.6, 0.6, 0.0, 1.0, 0.3],  # Harmonizer
    [0.0, 0.3, 0.0, 0.3, 0.3, 1.0],  # Autonomist
])


# ── HEATMAP ───────────────────────────────────────────────────────────────

def generate_heatmap(data, archetypes, dimensions, outpath="images/heatmap.png"):
    fig, ax = plt.subplots(figsize=(10, 8))

    # Green sequential colormap matching original
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "green_joy",
        ["#e8f5e9", "#a5d6a7", "#66bb6a", "#2e7d32", "#1b5e20"],
        N=256,
    )

    im = ax.imshow(data, cmap=cmap, aspect="auto", vmin=0.0, vmax=1.0)

    # Axes
    ax.set_xticks(range(len(dimensions)))
    ax.set_xticklabels(dimensions, fontsize=11)
    ax.set_yticks(range(len(archetypes)))
    ax.set_yticklabels(archetypes, fontsize=11)
    ax.xaxis.set_ticks_position("bottom")

    # Annotate cells
    for i in range(len(archetypes)):
        for j in range(len(dimensions)):
            val = data[i, j]
            color = "white" if val >= 0.7 else "black"
            ax.text(j, i, f"{val:.1f}", ha="center", va="center",
                    fontsize=11, fontweight="bold", color=color)

    # Colorbar
    cbar = fig.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
    cbar.ax.tick_params(labelsize=10)

    ax.set_title("Motivational Sensitivity Heatmap", fontsize=14, pad=12)
    ax.set_ylabel("Archetype", fontsize=12)

    plt.tight_layout()
    fig.savefig(outpath, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  ✓ Heatmap saved to {outpath}")


# ── RADAR CHARTS ──────────────────────────────────────────────────────────

# Colors matching the original style (one per archetype)
RADAR_COLORS = [
    "#4472C4",  # Mastery-Seeker – blue
    "#5B7F95",  # Solver – slate
    "#C4A535",  # Architect – gold
    "#C0392B",  # Builder – red
    "#8E6EA0",  # Creator – mauve
    "#2E74B5",  # Synthesizer – royal blue
    "#7CB342",  # Helper – green
    "#E8A838",  # Stabilizer – orange
    "#C0392B",  # Explorer – dark red
    "#2E7D32",  # Strategist – forest green
    "#A0722D",  # Harmonizer – brown
    "#5D3A6E",  # Autonomist – dark purple
]


def generate_radar_charts(data, archetypes, dimensions, outpath="images/radar.png"):
    N = len(dimensions)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]  # close the polygon

    fig, axes = plt.subplots(4, 3, figsize=(14, 18),
                             subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("white")

    for idx, ax in enumerate(axes.flat):
        if idx >= len(archetypes):
            ax.set_visible(False)
            continue

        values = data[idx].tolist()
        values += values[:1]  # close
        color = RADAR_COLORS[idx]

        # Plot
        ax.set_theta_offset(pi / 2)   # Growth at top
        ax.set_theta_direction(-1)     # clockwise
        ax.plot(angles, values, "o-", linewidth=1.8, color=color, markersize=4)
        ax.fill(angles, values, alpha=0.15, color=color)

        # Fixed radial range
        ax.set_ylim(0, 1.0)
        ax.set_yticks([0.0, 0.25, 0.50, 0.75, 1.00])
        ax.set_yticklabels(["0.00", "0.25", "0.50", "0.75", "1.00"],
                           fontsize=7, color="grey")

        # Dimension labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(dimensions, fontsize=8)

        # Title with colored dot
        ax.set_title(f"● {archetypes[idx]}", fontsize=10, pad=14,
                     color=color, fontweight="bold")

        # Grid style
        ax.grid(color="lightgrey", linewidth=0.5)
        ax.spines["polar"].set_color("lightgrey")

    plt.tight_layout(pad=2.0)
    fig.savefig(outpath, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  ✓ Radar charts saved to {outpath}")


# ── MAIN ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Generating figures from corrected sensitivity matrix...")
    generate_heatmap(data, archetypes, dimensions)
    generate_radar_charts(data, archetypes, dimensions)
    print("Done.")
