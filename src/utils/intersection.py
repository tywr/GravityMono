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


def _superellipse_beziers(x1, y1, x2, y2, hx, hy):
    """Return the 4 cubic Bézier segments of a superellipse (CCW winding)."""
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    return [
        # right -> top
        ((x2, mid_y), (x2, mid_y + hy), (mid_x + hx, y2), (mid_x, y2)),
        # top -> left
        ((mid_x, y2), (mid_x - hx, y2), (x1, mid_y + hy), (x1, mid_y)),
        # left -> bottom
        ((x1, mid_y), (x1, mid_y - hy), (mid_x - hx, y1), (mid_x, y1)),
        # bottom -> right
        ((mid_x, y1), (mid_x + hx, y1), (x2, mid_y - hy), (x2, mid_y)),
    ]


def _eval_bezier(p0, p1, p2, p3, t):
    """Evaluate a cubic Bézier at parameter t."""
    mt = 1 - t
    x = mt**3 * p0[0] + 3 * mt**2 * t * p1[0] + 3 * mt * t**2 * p2[0] + t**3 * p3[0]
    y = mt**3 * p0[1] + 3 * mt**2 * t * p1[1] + 3 * mt * t**2 * p2[1] + t**3 * p3[1]
    return (x, y)


def _bezier_bbox(p0, p1, p2, p3):
    """Conservative bounding box of a cubic Bézier (using control-point hull)."""
    xs = [p0[0], p1[0], p2[0], p3[0]]
    ys = [p0[1], p1[1], p2[1], p3[1]]
    return (min(xs), min(ys), max(xs), max(ys))


def _bboxes_overlap(a, b, tol=1e-6):
    return not (
        a[2] < b[0] - tol or b[2] < a[0] - tol or a[3] < b[1] - tol or b[3] < a[1] - tol
    )


def _split_bezier(p0, p1, p2, p3, t=0.5):
    """Split a cubic Bézier at parameter t into two sub-curves."""
    q0 = (p0[0] + t * (p1[0] - p0[0]), p0[1] + t * (p1[1] - p0[1]))
    q1 = (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))
    q2 = (p2[0] + t * (p3[0] - p2[0]), p2[1] + t * (p3[1] - p2[1]))
    r0 = (q0[0] + t * (q1[0] - q0[0]), q0[1] + t * (q1[1] - q0[1]))
    r1 = (q1[0] + t * (q2[0] - q1[0]), q1[1] + t * (q2[1] - q1[1]))
    s = (r0[0] + t * (r1[0] - r0[0]), r0[1] + t * (r1[1] - r0[1]))
    return (p0, q0, r0, s), (s, r1, q2, p3)


def _bezier_bezier_intersect(seg_a, seg_b, tol=0.5, depth=0, max_depth=50):
    """Find intersections between two cubic Bézier segments via recursive subdivision."""
    bbox_a = _bezier_bbox(*seg_a)
    bbox_b = _bezier_bbox(*seg_b)
    if not _bboxes_overlap(bbox_a, bbox_b):
        return []

    # Check if both curves are small enough to count as a single point
    size_a = max(bbox_a[2] - bbox_a[0], bbox_a[3] - bbox_a[1])
    size_b = max(bbox_b[2] - bbox_b[0], bbox_b[3] - bbox_b[1])
    if size_a < tol and size_b < tol:
        # Return midpoint of the overlap region
        px = (bbox_a[0] + bbox_a[2] + bbox_b[0] + bbox_b[2]) / 4
        py = (bbox_a[1] + bbox_a[3] + bbox_b[1] + bbox_b[3]) / 4
        return [(px, py)]

    if depth >= max_depth:
        px = (bbox_a[0] + bbox_a[2] + bbox_b[0] + bbox_b[2]) / 4
        py = (bbox_a[1] + bbox_a[3] + bbox_b[1] + bbox_b[3]) / 4
        return [(px, py)]

    # Subdivide the larger curve
    a1, a2 = _split_bezier(*seg_a)
    b1, b2 = _split_bezier(*seg_b)

    results = []
    for sa in (a1, a2):
        for sb in (b1, b2):
            results.extend(_bezier_bezier_intersect(sa, sb, tol, depth + 1, max_depth))
    return _dedupe_points(results, tol=tol)


def _dedupe_points(points, tol=1.0):
    """Remove duplicate intersection points within tolerance."""
    unique = []
    for p in points:
        if not any(abs(p[0] - u[0]) < tol and abs(p[1] - u[1]) < tol for u in unique):
            unique.append((float(p[0]), float(p[1])))
    return unique


def intersection_superellipses(d1, d2, tol=0.5):
    """Find intersection points between two superellipses.

    Args:
        d1: Superellipse instance for the first superellipse.
        d2: Superellipse instance for the second superellipse.
        tol: tolerance for intersection detection (in font units).

    Returns:
        List of (x, y) tuples where the two superellipses intersect.
    """
    beziers_a = _superellipse_beziers(d1.x1, d1.y1, d1.x2, d1.y2, d1.hx, d1.hy)
    beziers_b = _superellipse_beziers(d2.x1, d2.y1, d2.x2, d2.y2, d2.hx, d2.hy)

    raw_points = []
    for seg_a in beziers_a:
        for seg_b in beziers_b:
            raw_points.extend(_bezier_bezier_intersect(seg_a, seg_b, tol))

    return _dedupe_points(raw_points, tol=tol * 2)


def intersection_superellipse_y(d1, y, tol=0.5):
    """Find intersection points between a superellipse and the horizontal line y=Y.

    Args:
        d1: Superellipse instance.
        y: the y-coordinate of the horizontal line.

    Returns:
        List of (x, y) tuples where the superellipse crosses y=Y.
    """
    beziers = _superellipse_beziers(d1.x1, d1.y1, d1.x2, d1.y2, d1.hx, d1.hy)
    points = []
    for seg in beziers:
        for _t, x in bezier_intersect(seg[0], seg[1], seg[2], seg[3], y, axis=1):
            points.append((x, y))
    return _dedupe_points(points, tol=tol)


def intersection_superellipse_x(d1, x, tol=0.5):
    """Find intersection points between a superellipse and the vertical line x=X.

    Args:
        d1: Superellipse instance.
        x: the x-coordinate of the vertical line.

    Returns:
        List of (x, y) tuples where the superellipse crosses x=X.
    """
    beziers = _superellipse_beziers(d1.x1, d1.y1, d1.x2, d1.y2, d1.hx, d1.hy)
    points = []
    for seg in beziers:
        for _t, y in bezier_intersect(seg[0], seg[1], seg[2], seg[3], x, axis=0):
            points.append((x, y))
    return _dedupe_points(points, tol=tol)
