from math import tan
from glyphs import LigatureGlyph
from draw.parallelogramm import draw_parallelogramm_vertical
from draw.rect import draw_rect


class DoubleLeftArrowGlyph(LigatureGlyph):
    """Ligature glyph for <="""

    name = "double_left_arrow"
    components = ["less_than_sign", "equals_sign"]
    number_characters = 2
    width_ratio = 1
    overlap = 0.6
    gap = 0.4

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="x_height", width_ratio=self.width_ratio
        )
        ymid = dc.math
        ov = self.overlap * dc.stroke_y
        h = dc.parenthesis_length
        theta, delta = draw_parallelogramm_vertical(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            ymid - ov,
            b.x2,
            ymid + h / 2,
        )
        draw_parallelogramm_vertical(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x2,
            ymid - h / 2,
            b.x1,
            ymid + ov,
            direction="top-left",
        )

        g = self.gap * b.height
        draw_rect(
            pen,
            b.x1 + (g / 2) / tan(theta),
            dc.math + g / 2 - dc.stroke_y / 2,
            b.x2 + dc.window_width,
            dc.math + g / 2 + dc.stroke_y / 2,
        )
        draw_rect(
            pen,
            b.x1 + (g / 2) / tan(theta),
            dc.math - g / 2 - dc.stroke_y / 2,
            b.x2 + dc.window_width,
            dc.math - g / 2 + dc.stroke_y / 2,
        )
