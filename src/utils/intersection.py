from scipy.optimize import brentq
import numpy as np


def bezier_intersect(p1, hp1, hp2, p2, a, axis):
    """axis=0 for x=a, axis=1 for y=a. Returns list of (t, other_coord)."""
    i, j = axis, 1 - axis

    A = -p1[i] + 3 * hp1[i] - 3 * hp2[i] + p2[i]
    B = 3 * p1[i] - 6 * hp1[i] + 3 * hp2[i]
    C = -3 * p1[i] + 3 * hp1[i]
    D = p1[i] - a

    results = []
    for t in np.roots([A, B, C, D]):
        if abs(t.imag) < 1e-6 and 0 <= t.real <= 1:
            t = t.real
            mt = 1 - t
            other = (
                mt**3 * p1[j]
                + 3 * mt**2 * t * hp1[j]
                + 3 * mt * t**2 * hp2[j]
                + t**3 * p2[j]
            )
            results.append((t, other))
    return results


def find_offset(x1, y1, x2, y2, hx, hy, stroke, tooth):
    """Find the offset so the outer superellipse crosses x=ix1 at y=y2-tooth (and y=y1+tooth).

    The outer superellipse in draw_superellipse_arch is inset by (stroke - offset)
    on the junction side. This function solves for the offset value that places
    the intersection of the outer curve with x = x1 + stroke exactly at
    y = y2 - tooth (top) and y = y1 + tooth (bottom), by symmetry.
    """
    ix1 = x1 + stroke
    target_y = y2 - tooth
    w = (x2 - x1) / 2
    h = (y2 - y1) / 2
    y_mid = (y1 + y2) / 2

    def _intersection_y(offset):
        ox1 = x1 + stroke - offset
        ox2 = x2
        omid_x = (ox1 + ox2) / 2
        ohx = hx * (w - offset) / w
        ohy = hy * (h - offset) / h

        # Top-left bezier of the outer superellipse (CCW winding)
        # Goes from (omid_x, y2) down to (ox1, y_mid)
        p0 = (omid_x, y2)
        cp1 = (omid_x - ohx, y2)
        cp2 = (ox1, y_mid + ohy)
        p3 = (ox1, y_mid)

        hits = bezier_intersect(p0, cp1, cp2, p3, ix1, axis=0)
        if not hits:
            return y_mid
        return max(hits, key=lambda h: h[1])[1]

    return brentq(lambda offset: _intersection_y(offset) - target_y, 0, stroke)


def find_offset_horizontal(x1, y1, x2, y2, hx, hy, stroke, tooth):
    """Find the offset for side='top'/'bottom' arches.

    The outer superellipse is inset by (stroke - offset) on the top.
    This function solves for the offset value that places the intersection
    of the outer curve with y = y2 - stroke exactly at x = x2 - tooth.
    By vertical symmetry the same offset applies to side='bottom'.
    """
    iy2 = y2 - stroke
    target_x = x2 - tooth
    w = (x2 - x1) / 2
    h = (y2 - y1) / 2

    def _intersection_x(offset):
        oy2 = y2 - (stroke - offset)
        omid_x = (x1 + x2) / 2
        omid_y = (y1 + oy2) / 2
        ohx = hx * (w - offset) / w
        ohy = hy * (h - offset) / h

        # Top-right bezier of the outer superellipse (CCW winding)
        # Goes from (x2, omid_y) up to (omid_x, oy2)
        p0 = (x2, omid_y)
        cp1 = (x2, omid_y + ohy)
        cp2 = (omid_x + ohx, oy2)
        p3 = (omid_x, oy2)

        hits = bezier_intersect(p0, cp1, cp2, p3, iy2, axis=1)
        if not hits:
            return omid_x
        return max(hits, key=lambda h: h[1])[1]

    return brentq(lambda offset: _intersection_x(offset) - target_x, 0, stroke)
