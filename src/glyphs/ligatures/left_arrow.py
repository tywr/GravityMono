from glyphs import LigatureGlyph
from draw.parallelogramm import draw_parallelogramm_vertical
from draw.rect import draw_rect


class LeftArrowGlyph(LigatureGlyph):
    """Ligature glyph for ->"""

    name = "left_arrow"
    components = ["less_than_sign", "hyphen_minus"]
    number_characters = 2
    width_ratio = 1
    overlap = 0.6

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="x_height", width_ratio=self.width_ratio
        )
        ymid = dc.math
        ov = self.overlap * dc.stroke_y
        h = dc.parenthesis_length
        draw_parallelogramm_vertical(
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
            direction="top-left"
        )
        draw_rect(pen, b.x1, dc.math - dc.stroke_y / 2, b.x2 + dc.window_width, dc.math + dc.stroke_y / 2)
