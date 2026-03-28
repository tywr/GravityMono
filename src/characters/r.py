from config import FontConfig
from shapes.rounded_half_loop import rounded_half_loop_tapered
from shapes.rect import rect
from shapes.intersection_filler import intersection_filler


def draw_r(pen, font_config: FontConfig, stroke: int):
    """Draw an 'r' with a top half tapered loop and a left stem."""
    outer_left = FontConfig.WIDTH / 2 - FontConfig.X_WIDTH / 2 - stroke / 2
    outer_right = FontConfig.WIDTH / 2 + FontConfig.X_WIDTH / 2 + stroke / 2

    max_xo = (outer_right - outer_left) / 2
    max_yo = FontConfig.X_HEIGHT / 2
    x_offset = min(FontConfig.X_OFFSET, max_xo)
    y_offset = min(FontConfig.Y_OFFSET, max_yo)
    bar_right = outer_left + stroke

    # Top half loop tapered on the left (where the stem is)
    rounded_half_loop_tapered(
        pen,
        x1=outer_left,
        y1=0,
        x2=outer_right,
        y2=FontConfig.X_HEIGHT,
        x_offset=x_offset,
        y_offset=y_offset,
        x_offset_taper=FontConfig.X_OFFSET_TAPER,
        y_offset_taper=FontConfig.Y_OFFSET_TAPER,
        stroke=stroke,
        ratio_taper=FontConfig.RATIO_TAPER,
        direction="left",
        half="top",
        stroke_left=stroke,
    )
    intersection_filler(
        pen=pen,
        stroke=stroke,
        outer_left=outer_left + stroke * FontConfig.RATIO_TAPER,
        outer_right=outer_right,
        height=FontConfig.X_HEIGHT,
        x_offset=x_offset,
        y_offset=y_offset,
        side="left",
        bar_position=bar_right,
        fill_height=FontConfig.INTERSECTION_FILL_HEIGHT,
        draw_bottom=False,
    )

    # Left vertical bar
    rect(pen, outer_left, 0, bar_right, FontConfig.X_HEIGHT)
