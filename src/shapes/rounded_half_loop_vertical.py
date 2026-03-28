def rounded_half_loop_vertical(
    pen, x1, y1, x2, y2, x_offset, y_offset, stroke, half="right",
):
    """Draw the left or right half of a rounded loop.

    Cuts the full loop vertically at the horizontal midpoint. The arch
    is two quarter-curves; the flat edge is the implicit closePath line.

    Args:
        x1, y1: bottom-left corner of the full bounding box.
        x2, y2: top-right corner of the full bounding box.
        x_offset: horizontal control point offset for the outer shape.
        y_offset: vertical control point offset for the outer shape.
        stroke: wall thickness.
        half: "left" or "right".
    """
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2

    # Inner dimensions
    ix1 = x1 + stroke
    ix2 = x2 - stroke
    iy1 = y1 + stroke
    iy2 = y2 - stroke
    imid_x = (ix1 + ix2) / 2
    imid_y = (iy1 + iy2) / 2

    # Scale inner offsets proportionally
    outer_half_w = (x2 - x1) / 2
    outer_half_h = (y2 - y1) / 2
    inner_half_w = (ix2 - ix1) / 2
    inner_half_h = (iy2 - iy1) / 2

    ixo = x_offset * inner_half_w / outer_half_w if outer_half_w > 0 else 0
    iyo = y_offset * inner_half_h / outer_half_h if outer_half_h > 0 else 0

    if half == "right":
        # Outer right half (CCW): bottom-mid -> right-mid -> top-mid -> close
        pen.moveTo((mid_x, y1))
        pen.curveTo(
            (mid_x + x_offset, y1),
            (x2, mid_y - y_offset),
            (x2, mid_y),
        )
        pen.curveTo(
            (x2, mid_y + y_offset),
            (mid_x + x_offset, y2),
            (mid_x, y2),
        )
        pen.closePath()

        # Inner right half (CW): top-mid -> right-mid -> bottom-mid -> close
        pen.moveTo((imid_x, iy2))
        pen.curveTo(
            (imid_x + ixo, iy2),
            (ix2, imid_y + iyo),
            (ix2, imid_y),
        )
        pen.curveTo(
            (ix2, imid_y - iyo),
            (imid_x + ixo, iy1),
            (imid_x, iy1),
        )
        pen.closePath()

    elif half == "left":
        # Outer left half (CCW): top-mid -> left-mid -> bottom-mid -> close
        pen.moveTo((mid_x, y2))
        pen.curveTo(
            (mid_x - x_offset, y2),
            (x1, mid_y + y_offset),
            (x1, mid_y),
        )
        pen.curveTo(
            (x1, mid_y - y_offset),
            (mid_x - x_offset, y1),
            (mid_x, y1),
        )
        pen.closePath()

        # Inner left half (CW): bottom-mid -> left-mid -> top-mid -> close
        pen.moveTo((imid_x, iy1))
        pen.curveTo(
            (imid_x - ixo, iy1),
            (ix1, imid_y - iyo),
            (ix1, imid_y),
        )
        pen.curveTo(
            (ix1, imid_y + iyo),
            (imid_x - ixo, iy2),
            (imid_x, iy2),
        )
        pen.closePath()


def rounded_half_loop_vertical_tapered(
    pen, x1, y1, x2, y2,
    x_offset, y_offset,
    x_offset_taper, y_offset_taper,
    stroke, ratio_taper,
    direction="right",
    half="right",
):
    """Draw the left or right half of a tapered rounded loop.

    One side uses (x_offset, y_offset), the tapered side uses
    (x_offset_taper, y_offset_taper) with the outer edge inset by the
    taper amount — matching rounded_loop_tapered behaviour.

    Args:
        x1, y1: bottom-left corner of the full bounding box.
        x2, y2: top-right corner of the full bounding box.
        x_offset: horizontal control point offset for the normal side.
        y_offset: vertical control point offset for the normal side.
        x_offset_taper: horizontal control point offset for the tapered side.
        y_offset_taper: vertical control point offset for the tapered side.
        stroke: wall thickness.
        ratio_taper: thickness ratio on the tapered side (e.g. 0.3 = 30%).
        direction: "left" or "right" — which side gets tapered offsets.
        half: "left" or "right" — which half to draw.
    """
    taper_inset = (1 - ratio_taper) * stroke

    if direction == "right":
        xo_left, yo_left = x_offset, y_offset
        xo_right, yo_right = x_offset_taper, y_offset_taper
        outer_x1 = x1
        outer_x2 = x2 - taper_inset
    else:
        xo_left, yo_left = x_offset_taper, y_offset_taper
        xo_right, yo_right = x_offset, y_offset
        outer_x1 = x1 + taper_inset
        outer_x2 = x2

    mid_y = (y1 + y2) / 2

    # Inner contour uses the original x1/x2 inset by full stroke,
    # so the tapered side has a thinner wall (ratio_taper * stroke).
    ix1 = x1 + stroke
    ix2 = x2 - stroke
    iy1 = y1 + stroke
    iy2 = y2 - stroke
    imid_x = (ix1 + ix2) / 2
    imid_y = (iy1 + iy2) / 2

    outer_half_w = (x2 - x1) / 2
    outer_half_h = (y2 - y1) / 2
    inner_half_w = (ix2 - ix1) / 2
    inner_half_h = (iy2 - iy1) / 2

    ratio_w = inner_half_w / outer_half_w if outer_half_w > 0 else 0
    ratio_h = inner_half_h / outer_half_h if outer_half_h > 0 else 0

    ixo = x_offset * ratio_w
    iyo = y_offset * ratio_h

    if half == "right":
        outer_mid_x = (outer_x1 + outer_x2) / 2

        # Outer right half (CCW): bottom-mid -> right-mid -> top-mid -> close
        pen.moveTo((outer_mid_x, y1))
        pen.curveTo(
            (outer_mid_x + xo_right, y1),
            (outer_x2, mid_y - yo_right),
            (outer_x2, mid_y),
        )
        pen.curveTo(
            (outer_x2, mid_y + yo_right),
            (outer_mid_x + xo_right, y2),
            (outer_mid_x, y2),
        )
        pen.closePath()

        # Inner right half (CW): top-mid -> right-mid -> bottom-mid -> close
        pen.moveTo((imid_x, iy2))
        pen.curveTo(
            (imid_x + ixo, iy2),
            (ix2, imid_y + iyo),
            (ix2, imid_y),
        )
        pen.curveTo(
            (ix2, imid_y - iyo),
            (imid_x + ixo, iy1),
            (imid_x, iy1),
        )
        pen.closePath()

    elif half == "left":
        outer_mid_x = (outer_x1 + outer_x2) / 2

        # Outer left half (CCW): top-mid -> left-mid -> bottom-mid -> close
        pen.moveTo((outer_mid_x, y2))
        pen.curveTo(
            (outer_mid_x - xo_left, y2),
            (outer_x1, mid_y + yo_left),
            (outer_x1, mid_y),
        )
        pen.curveTo(
            (outer_x1, mid_y - yo_left),
            (outer_mid_x - xo_left, y1),
            (outer_mid_x, y1),
        )
        pen.closePath()

        # Inner left half (CW): bottom-mid -> left-mid -> top-mid -> close
        pen.moveTo((imid_x, iy1))
        pen.curveTo(
            (imid_x - ixo, iy1),
            (ix1, imid_y - iyo),
            (ix1, imid_y),
        )
        pen.curveTo(
            (ix1, imid_y + iyo),
            (imid_x - ixo, iy2),
            (imid_x, iy2),
        )
        pen.closePath()

    return {
        "x1": outer_x1,
        "y1": y1,
        "x2": outer_x2,
        "y2": y2,
        "x_offset_left": xo_left,
        "y_offset_left": yo_left,
        "x_offset_right": xo_right,
        "y_offset_right": yo_right,
    }
