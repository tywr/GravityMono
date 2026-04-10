from glyphs import Glyph
from draw.parallelogramm import draw_parallelogramm_vertical


class LessThenSignGlyph(Glyph):
    name = "less_than_sign"
    unicode = "0x3C"
    offset = 0
    width_ratio = 1
    overlap = 0.6
    height = 1.7

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="x_height", width_ratio=self.width_ratio
        )
        ymid = dc.math
        ov = self.overlap * dc.stroke_y
        h = self.height * b.height
        draw_parallelogramm_vertical(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            ymid - ov,
            b.x2,
            ymid - ov + h / 2,
        )
        draw_parallelogramm_vertical(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x2,
            ymid + ov - h / 2,
            b.x1,
            ymid + ov,
            direction="top-left"
        )
