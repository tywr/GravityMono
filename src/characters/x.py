import math

import pathops

from config import FontConfig


def draw_x(pen, font_config: FontConfig, stroke: int):
    """Draw a lowercase 'x' — two diagonal bars, cut flush at y=0 and y=x-height."""
    outer_left = FontConfig.WIDTH / 2 - FontConfig.X_WIDTH / 2 - stroke / 2
    outer_right = FontConfig.WIDTH / 2 + FontConfig.X_WIDTH / 2 + stroke / 2
    top = FontConfig.X_HEIGHT
    bottom = 0

    # Direction vector for the "/" bar
    dx = outer_right - outer_left
    dy = top - bottom
    length = math.sqrt(dx * dx + dy * dy)

    # Perpendicular offset for stroke width
    hx = stroke / 2 * (-dy / length)
    hy = stroke / 2 * (dx / length)

    # Extend bars beyond top/bottom so clipping produces flush ends
    extend = stroke
    ex = extend * dx / length
    ey = extend * dy / length

    # Bar 1: bottom-left to top-right ("/")
    x1, y1 = outer_left - ex, bottom - ey
    x2, y2 = outer_right + ex, top + ey
    bar1 = pathops.Path()
    b1 = bar1.getPen()
    b1.moveTo((x1 + hx, y1 + hy))
    b1.lineTo((x2 + hx, y2 + hy))
    b1.lineTo((x2 - hx, y2 - hy))
    b1.lineTo((x1 - hx, y1 - hy))
    b1.closePath()

    # Bar 2: bottom-right to top-left ("\")
    x3, y3 = outer_right + ex, bottom - ey
    x4, y4 = outer_left - ex, top + ey
    bar2 = pathops.Path()
    b2 = bar2.getPen()
    b2.moveTo((x3 - hx, y3 + hy))
    b2.lineTo((x4 - hx, y4 + hy))
    b2.lineTo((x4 + hx, y4 - hy))
    b2.lineTo((x3 + hx, y3 - hy))
    b2.closePath()

    bars = pathops.op(bar1, bar2, pathops.PathOp.UNION, fix_winding=True)

    # Clip to bounding box: flush at y=0 and y=x-height
    clip = pathops.Path()
    cp = clip.getPen()
    cp.moveTo((-50, bottom))
    cp.lineTo((-50, top))
    cp.lineTo((FontConfig.WIDTH + 50, top))
    cp.lineTo((FontConfig.WIDTH + 50, bottom))
    cp.closePath()

    result = pathops.op(bars, clip, pathops.PathOp.INTERSECTION, fix_winding=True)

    result.draw(pen)
