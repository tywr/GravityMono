def draw_cross_curve(
    pen,
    stroke,
    x1, y1,
    x2, y2,
    hx, hy,
):
    """Draw a center-symmetric S-curve stroke from (x1,y1) to (x2,y2).

    The curve starts at the bottom-left corner, crosses through the center
    of the bounding box, and ends at the top-right corner.
    The stroke is drawn inside the bounding box.

    At the corners the tangent is vertical; at the center it is horizontal.
    """
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    hw = (x2 - x1) / 2
    hh = (y2 - y1) / 2
    ihx = hx * (hw - stroke) / hw if hw > 0 else 0
    ihy = hy * (hh - stroke) / hh if hh > 0 else 0

    # Bottom-right crescent: from (x1,y1) to center
    pen.moveTo((x1, y1))
    pen.curveTo((x1, y1 + hy), (mid_x - hx, mid_y), (mid_x, mid_y))
    pen.lineTo((mid_x, mid_y + stroke))
    pen.curveTo((mid_x - ihx, mid_y + stroke), (x1 + stroke, y1 + ihy), (x1 + stroke, y1))
    pen.closePath()

    # Top-left crescent: 180° rotation of the bottom-right crescent
    pen.moveTo((x2, y2))
    pen.curveTo((x2, y2 - hy), (mid_x + hx, mid_y), (mid_x, mid_y))
    pen.lineTo((mid_x, mid_y - stroke))
    pen.curveTo((mid_x + ihx, mid_y - stroke), (x2 - stroke, y2 - ihy), (x2 - stroke, y2))
    pen.closePath()
