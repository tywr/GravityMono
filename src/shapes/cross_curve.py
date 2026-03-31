def draw_cross_curve(
    pen,
    stroke,
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
    The stroke is drawn inside the bounding box.

    At the corners the tangent is vertical; at the center it is horizontal.
    """
    if invert:
        x1, y1, x2, y2 = x1, y2, x2, y1
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    hh = (y2 - y1) / 2

    sign = -1 if invert else 1
    ohy = hy * (hh + stroke / 2) / hh
    ihy = hy * (hh - stroke / 2) / hh
    if invert:
        ihy, ohy = ohy, ihy

    s2 = stroke / 2

    pen.moveTo((x1, y1))
    pen.curveTo((x1, y1 + sign * ohy), (x1, y1 + sign * ohy), (mid_x, mid_y + sign * s2))
    pen.curveTo((x2 - stroke, y2 - sign * ihy), (x2 - stroke, y2 - sign * ihy), (x2 - stroke, y2))
    pen.lineTo((x2, y2))
    pen.curveTo((x2, y2 - sign * ohy), (x2, y2 - sign * ohy), (mid_x, mid_y - sign * s2))
    pen.curveTo((x1 + stroke, y1 + sign * ihy), (x1 + stroke, y1 + sign * ihy), (x1 + stroke, y1))
    pen.closePath()
