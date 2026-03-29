from shapes.rounded_half_loop import rounded_half_loop_tapered
from shapes.rounded_half_loop import rounded_half_loop
from shapes.rect import rect
from shapes.intersection_filler import intersection_filler

from config import FontConfig


def draw_m(pen, font_config: FontConfig, stroke: int):
    """Draw an 'm' using two narrow arches side by side.

    Left arch: tapered o, bottom cut, with a full left stem.
    Right arch: non-tapered o, bottom cut, with a short right descender.
    The two arches share a middle stem via pathops union.
    """
    outer_left = FontConfig.WIDTH / 2 - FontConfig.X_WIDTH_LARGE / 2 - stroke / 2
    outer_right = FontConfig.WIDTH / 2 + FontConfig.X_WIDTH_LARGE / 2 + stroke / 2

    max_xo = (outer_right - outer_left) / 8
    max_yo = FontConfig.X_HEIGHT / 2
    x_offset = min(FontConfig.X_OFFSET, max_xo)
    y_offset = min(FontConfig.Y_OFFSET, max_yo)
    bar_right = outer_left + stroke

    rounded_half_loop_tapered(
        pen,
        x1=outer_left,
        y1=0,
        x2=FontConfig.WIDTH / 2 + stroke / 2,
        y2=FontConfig.X_HEIGHT,
        x_offset=x_offset,
        y_offset=y_offset,
        x_offset_taper=45,
        y_offset_taper=y_offset,
        stroke=stroke,
        ratio_taper=FontConfig.RATIO_TAPER,
        direction="left",
        half="top",
    )
    intersection_filler(
        pen=pen,
        stroke=stroke,
        outer_left=outer_left + stroke * FontConfig.RATIO_TAPER,
        outer_right=FontConfig.WIDTH / 2 + 1.2 * stroke,
        height=FontConfig.X_HEIGHT,
        x_offset=x_offset,
        y_offset=y_offset,
        side="left",
        bar_position=bar_right,
        fill_height=FontConfig.INTERSECTION_FILL_HEIGHT,
        draw_bottom=False,
    )
    rounded_half_loop(
        pen,
        x1=FontConfig.WIDTH / 2 - stroke / 2,
        y1=0,
        x2=outer_right,
        y2=FontConfig.X_HEIGHT,
        x_offset=x_offset,
        y_offset=y_offset,
        stroke=stroke,
        half="top",
    )
    rect(
        pen,
        outer_left,
        0,
        bar_right,
        FontConfig.X_HEIGHT,
    )
    rect(
        pen,
        outer_right - stroke,
        0,
        outer_right,
        FontConfig.X_HEIGHT / 2,
    )
    rect(
        pen,
        FontConfig.WIDTH / 2 - stroke / 2,
        FontConfig.X_HEIGHT * FontConfig.M_CUT_RATIO,
        FontConfig.WIDTH / 2 + stroke / 2,
        FontConfig.X_HEIGHT / 2,
    )
