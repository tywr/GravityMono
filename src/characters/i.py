from config import FontConfig
from shapes.rect import rect


def draw_i(pen, font_config: FontConfig, stroke: int):
    """Draw a lowercase 'i' — vertical stem with horizontal top and bottom bars."""
    outer_right = FontConfig.WIDTH / 2 + FontConfig.X_WIDTH / 2
    outer_left = outer_right - FontConfig.I_FOOT_RATIO * FontConfig.X_WIDTH

    center_stem = FontConfig.WIDTH / 2 + (FontConfig.IJ_OFFSET * FontConfig.X_WIDTH) / 2
    stem_left = center_stem - stroke / 2
    stem_right = center_stem + stroke / 2

    # Bottom horizontal bar
    pen.moveTo((outer_left, 0))
    pen.lineTo((outer_left, stroke))
    pen.lineTo((outer_right, stroke))
    pen.lineTo((outer_right, 0))
    pen.closePath()

    # Vertical stem
    pen.moveTo((stem_left, 0))
    pen.lineTo((stem_left, FontConfig.X_HEIGHT))
    pen.lineTo((stem_right, FontConfig.X_HEIGHT))
    pen.lineTo((stem_right, 0))
    pen.closePath()

    # Top horizontal bar
    top_left = FontConfig.WIDTH / 2 - FontConfig.X_WIDTH / 2
    pen.moveTo((top_left, FontConfig.X_HEIGHT - stroke))
    pen.lineTo((top_left, FontConfig.X_HEIGHT))
    pen.lineTo((stem_right, FontConfig.X_HEIGHT))
    pen.lineTo((stem_right, FontConfig.X_HEIGHT - stroke))
    pen.closePath()

    # Dot above the stem
    dot_left = stem_right - FontConfig.X_WIDTH * FontConfig.IJ_DOT_WIDTH
    rect(
        pen,
        dot_left,
        FontConfig.ACCENT + stroke / 2,
        stem_right,
        FontConfig.ACCENT - stroke / 2,
    )
