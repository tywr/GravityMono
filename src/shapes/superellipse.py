def draw_superellipse(
    pen,
    x1, y1,
    x2, y2,
    hx, hy,
    clockwise=False,
):
    """
    Draw a superellipse whose anchors sit at the midpoint of each bounding side.
    Shape is controlled purely by hx/hy handle tension:
        hx=hy=0          → diamond
        hx=hy small      → Eurostile squared look
        hx ~ half-width  → rectangle (handles reach the corners)

    Args:
        x1, y1: bottom-left corner of the bounding box.
        x2, y2: top-right corner of the bounding box.
        hx: horizontal handle offset from the side midpoint anchor.
        hy: vertical handle offset from the side midpoint anchor.
        clockwise: winding direction (True for inner contour / counter).
    """
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2

    if not clockwise:
        # CCW: bottom → right → top → left
        pen.moveTo((mid_x, y1))
        pen.curveTo(            # bottom-right
            (mid_x + hx, y1),
            (x2, mid_y - hy),
            (x2, mid_y),
        )
        pen.curveTo(            # top-right
            (x2, mid_y + hy),
            (mid_x + hx, y2),
            (mid_x, y2),
        )
        pen.curveTo(            # top-left
            (mid_x - hx, y2),
            (x1, mid_y + hy),
            (x1, mid_y),
        )
        pen.curveTo(            # bottom-left
            (x1, mid_y - hy),
            (mid_x - hx, y1),
            (mid_x, y1),
        )
    else:
        # CW: bottom → left → top → right
        pen.moveTo((mid_x, y1))
        pen.curveTo(            # bottom-left
            (mid_x - hx, y1),
            (x1, mid_y - hy),
            (x1, mid_y),
        )
        pen.curveTo(            # top-left
            (x1, mid_y + hy),
            (mid_x - hx, y2),
            (mid_x, y2),
        )
        pen.curveTo(            # top-right
            (mid_x + hx, y2),
            (x2, mid_y + hy),
            (x2, mid_y),
        )
        pen.curveTo(            # bottom-right
            (x2, mid_y - hy),
            (mid_x + hx, y1),
            (mid_x, y1),
        )

    pen.closePath()
