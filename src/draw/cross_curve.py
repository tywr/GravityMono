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
    hh = (y2 - y1) / 2

    sign = -1 if invert else 1

    # Compute perpendicular stroke at the midpoint based on the diagonal angle,
    # matching the parallelogramm stroke formula
    w = x2 - x1
    h = abs(y2 - y1)
    diag = sqrt(w**2 + h**2)
    s = sqrt((stroke_x * h / diag) ** 2 + (stroke_y * w / diag) ** 2)
    s2x = s / 2 * h / diag
    s2y = s / 2 * w / diag

    # Upper stroke edge spans hh + s2y, lower spans hh - s2y
    ahh = abs(hh)
    ohy = hy * (ahh + s2y) / ahh
    ihy = hy * (ahh - s2y) / ahh
    if invert:
        ihy, ohy = ohy, ihy

    pen.moveTo((x1, y1))
    pen.curveTo(
        (x1, y1 + sign * ohy),
        (x1, y1 + sign * ohy),
        (mid_x - sign * s2x, mid_y + sign * s2y),
    )
    pen.curveTo(
        (x2 - stroke_x, y2 - sign * ihy),
        (x2 - stroke_x, y2 - sign * ihy),
        (x2 - stroke_x, y2),
    )
    pen.lineTo((x2, y2))
    pen.curveTo(
        (x2, y2 - sign * ohy),
        (x2, y2 - sign * ohy),
        (mid_x + sign * s2x, mid_y - sign * s2y),
    )
    pen.curveTo(
        (x1 + stroke_x, y1 + sign * ihy),
        (x1 + stroke_x, y1 + sign * ihy),
        (x1 + stroke_x, y1),
    )
    pen.closePath()
