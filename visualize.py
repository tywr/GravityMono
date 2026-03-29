#!/usr/bin/env python3
"""Visualize a single glyph. Usage: python visualize_one.py <letter>"""

import sys
import importlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path
from fontTools.pens.recordingPen import RecordingPen

sys.path.insert(0, "src")
from config import FontConfig as fc

STROKE = 60


def recording_to_mpl_path(recording):
    """Convert RecordingPen operations to a matplotlib Path."""
    verts = []
    codes = []
    for op, args in recording.value:
        if op == "moveTo":
            verts.append(args[0])
            codes.append(Path.MOVETO)
        elif op == "lineTo":
            verts.append(args[0])
            codes.append(Path.LINETO)
        elif op == "curveTo":
            for pt in args:
                verts.append(pt)
            codes.extend([Path.CURVE4, Path.CURVE4, Path.CURVE4])
        elif op == "closePath":
            verts.append(verts[-len(verts) + codes.index(Path.MOVETO)])
            codes.append(Path.CLOSEPOLY)
    return Path(verts, codes)


def visualize(family, glyph):
    mod = importlib.import_module(f"glyphs.{family}.{glyph}")
    draw_fn = getattr(mod, f"draw_{glyph}")

    rec = RecordingPen()
    draw_fn(rec, stroke=STROKE)

    fig, ax = plt.subplots(1, 1, figsize=(6, 8))

    path = recording_to_mpl_path(rec)
    patch = mpatches.PathPatch(path, facecolor="#222222", edgecolor="none")
    ax.add_patch(patch)

    # draw guides
    for y, label, color in [
        (0, "baseline", "#e74c3c"),
        (fc.x_height, "x-height", "#3498db"),
        (fc.cap, "cap", "#2ecc71"),
        (fc.descent, "descent", "#e67e22"),
        (fc.ascent, "ascent", "#9b59b6"),
    ]:
        ax.axhline(y, color=color, linewidth=0.5, linestyle="--", alpha=0.6)
        ax.text(fc.width + 10, y, label, fontsize=7, color=color, va="center")

    # advance width
    ax.axvline(0, color="#aaa", linewidth=0.5, linestyle=":")
    ax.axvline(fc.width, color="#aaa", linewidth=0.5, linestyle=":")

    ax.set_xlim(-50, fc.width + 80)
    ax.set_ylim(fc.descent - 50, fc.ascent + 50)
    ax.set_aspect("equal")
    ax.set_title(f"'{glyph}'", fontsize=16)
    ax.grid(True, alpha=0.15)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
    visualize(sys.argv[1], sys.argv[2])
