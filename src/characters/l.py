from config import FontConfig


def draw_l(pen, font_config: FontConfig, stroke: int):
    """Draw a lowercase 'l' — vertical stem with horizontal top and bottom bars."""
    center_x = FontConfig.WIDTH / 2
    outer_left = center_x - FontConfig.X_WIDTH / 2 - stroke / 2
    outer_right = center_x + FontConfig.X_WIDTH / 2 + stroke / 2
    stem_left = center_x - stroke / 2
    stem_right = center_x + stroke / 2

    # Bottom horizontal bar
    pen.moveTo((outer_left, 0))
    pen.lineTo((outer_left, stroke))
    pen.lineTo((outer_right, stroke))
    pen.lineTo((outer_right, 0))
    pen.closePath()

    # Vertical stem
    pen.moveTo((stem_left, 0))
    pen.lineTo((stem_left, FontConfig.ASCENT))
    pen.lineTo((stem_right, FontConfig.ASCENT))
    pen.lineTo((stem_right, 0))
    pen.closePath()

    # Top horizontal bar
    pen.moveTo((outer_left, FontConfig.ASCENT - stroke))
    pen.lineTo((outer_left, FontConfig.ASCENT))
    pen.lineTo((stem_right, FontConfig.ASCENT))
    pen.lineTo((stem_right, FontConfig.ASCENT - stroke))
    pen.closePath()
