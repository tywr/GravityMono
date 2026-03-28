import math

import pathops

from config import FontConfig
from characters.v import _thick_bar


def draw_w(pen, font_config: FontConfig, stroke: int):
    """Draw a lowercase 'w' — two V shapes side by side, cut flush."""
    outer_left = FontConfig.WIDTH / 2 - FontConfig.X_WIDTH / 2 - stroke / 2
    outer_right = FontConfig.WIDTH / 2 + FontConfig.X_WIDTH / 2 + stroke / 2
    center_x = FontConfig.WIDTH / 2
    top = FontConfig.X_HEIGHT
    bottom = 0

    # Two valleys at 1/4 and 3/4 of the letter width
    valley_left = (outer_left + center_x) / 2
    valley_right = (center_x + outer_right) / 2
    # Center peak at mid-height
    peak_y = top * FontConfig.M_CUT_RATIO

    # Four diagonal bars
    bar1 = _thick_bar(outer_left, top, valley_left, bottom, stroke)
    bar2 = _thick_bar(valley_left, bottom, center_x, peak_y, stroke)
    bar3 = _thick_bar(center_x, peak_y, valley_right, bottom, stroke)
    bar4 = _thick_bar(valley_right, bottom, outer_right, top, stroke)

    result = pathops.op(bar1, bar2, pathops.PathOp.UNION, fix_winding=True)
    result = pathops.op(result, bar3, pathops.PathOp.UNION, fix_winding=True)
    result = pathops.op(result, bar4, pathops.PathOp.UNION, fix_winding=True)

    # Clip flush at y=0 and y=x-height
    clip = pathops.Path()
    cp = clip.getPen()
    cp.moveTo((-50, bottom))
    cp.lineTo((-50, top))
    cp.lineTo((FontConfig.WIDTH + 50, top))
    cp.lineTo((FontConfig.WIDTH + 50, bottom))
    cp.closePath()

    result = pathops.op(result, clip, pathops.PathOp.INTERSECTION, fix_winding=True)

    result.draw(pen)
