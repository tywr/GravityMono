def draw_cross_curve(
    pen,
    stroke_x,
    stroke_y,
    x1,
    y1,
    x2,
    y2,
    hx,
    hy,
    invert=False,
):
    """Draw a center-symmetric S-curve stroke from (x1,y1) to (x2,y2).

    The curve starts at the bottom-left corner, crosses through the center
    of the bounding box, and ends at the top-right corner.

    At the corners the tangent is vertical; at the center it is horizontal.
    """
    from math import sqrt

    if invert:
        x1, y1, x2, y2 = x1, y2, x2, y1
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2

    sign = -1 if invert else 1
    inv = 1 if invert else 0

    # Compute perpendicular stroke at the midpoint based on the diagonal angle,
    # matching the parallelogramm stroke formula
    w = x2 - x1
    h = abs(y2 - y1)

    diag = sqrt(w**2 + h**2)
    s = sqrt((stroke_x * h / diag) ** 2 + (stroke_y * w / diag) ** 2)

    s2x = s / 2 * h / diag
    s2y = stroke_y / 2

    # Outer edges get increased handle, inner edges get decreased handle
    ohy = hy
    ihy = hy - 2 * s2y

    hx = hx - s2x

    if invert:
        ihy, ohy = ohy, ihy

    # Outer edge: (x1,y1) → upper mid → (x2,y2)
    pen.moveTo((x1 + inv * stroke_x, y1))
    pen.curveTo(
        (x1 + inv * stroke_x, y1 + sign * ohy),
        (mid_x - sign * s2x - hx, mid_y + s2y),
        (mid_x - sign * s2x, mid_y + s2y),
    )
    pen.curveTo(
        (mid_x - sign * s2x + hx, mid_y + s2y),
        (x2 - (1 - inv) * stroke_x, y2 - sign * ihy),
        (x2 - (1 - inv) * stroke_x, y2),
    )
    # Inner edge: (x2-stroke_x,y2) → lower mid → (x1+stroke_x,y1)
    pen.lineTo((x2 - inv * stroke_x, y2))
    pen.curveTo(
        (x2 - inv * stroke_x, y2 - sign * ohy),
        (mid_x + sign * s2x + hx, mid_y - s2y),
        (mid_x + sign * s2x, mid_y - s2y),
    )
    pen.curveTo(
        (mid_x + sign * s2x - hx, mid_y - s2y),
        (x1 + (1 - inv) * stroke_x, y1 + sign * ihy),
        (x1 + (1 - inv) * stroke_x, y1),
    )
    pen.closePath()
