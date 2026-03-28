import math

import pathops

from config import FontConfig


def _thick_bar(x1, y1, x2, y2, stroke):
    """Create a pathops.Path for a thick diagonal bar."""
    dx = x2 - x1
    dy = y2 - y1
    length = math.sqrt(dx * dx + dy * dy)
    hx = stroke / 2 * (-dy / length)
    hy = stroke / 2 * (dx / length)

    # Extend beyond endpoints for clean clipping
    extend = stroke
    ex = extend * dx / length
    ey = extend * dy / length

    path = pathops.Path()
    p = path.getPen()
    p.moveTo((x1 - ex + hx, y1 - ey + hy))
    p.lineTo((x2 + ex + hx, y2 + ey + hy))
    p.lineTo((x2 + ex - hx, y2 + ey - hy))
    p.lineTo((x1 - ex - hx, y1 - ey - hy))
    p.closePath()
    return path


def draw_v(pen, font_config: FontConfig, stroke: int):
    """Draw a lowercase 'v' — two diagonal bars meeting at bottom center, cut flush."""
    outer_left = FontConfig.WIDTH / 2 - FontConfig.X_WIDTH / 2 - stroke / 2
    outer_right = FontConfig.WIDTH / 2 + FontConfig.X_WIDTH / 2 + stroke / 2
    center_x = FontConfig.WIDTH / 2
    top = FontConfig.X_HEIGHT
    bottom = 0

    # Left bar: top-left to bottom-center
    bar1 = _thick_bar(outer_left, top, center_x, bottom, stroke)

    # Right bar: bottom-center to top-right
    bar2 = _thick_bar(center_x, bottom, outer_right, top, stroke)

    bars = pathops.op(bar1, bar2, pathops.PathOp.UNION, fix_winding=True)

    # Clip flush at y=0 and y=x-height
    clip = pathops.Path()
    cp = clip.getPen()
    cp.moveTo((-50, bottom))
    cp.lineTo((-50, top))
    cp.lineTo((FontConfig.WIDTH + 50, top))
    cp.lineTo((FontConfig.WIDTH + 50, bottom))
    cp.closePath()

    result = pathops.op(bars, clip, pathops.PathOp.INTERSECTION, fix_winding=True)

    result.draw(pen)
