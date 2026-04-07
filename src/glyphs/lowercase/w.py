from glyphs import Glyph
from draw.parallelogramm import draw_parallelogramm


class LowercaseWGlyph(Glyph):
    name = "lowercase_w"
    unicode = "0x77"
    offset = 0
    overlap = 0.3
    width_ratio = 1.25
    inner_stroke_ratio = 0.75
    inner_height_ratio = 0.7
    inner_angle_ratio = 0.18

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, width_ratio=self.width_ratio)
        ov = self.overlap * dc.stroke_x

        inner_height = self.inner_height_ratio * b.height
        theta, delta = draw_parallelogramm(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.xmid + self.inner_angle_ratio * b.width,
            0,
            b.x2,
            b.y2,
        )
        draw_parallelogramm(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.xmid - self.inner_angle_ratio * b.width,
            0,
            b.x1,
            b.y2,
            direction="top-left",
        )
        draw_parallelogramm(
            pen,
            self.inner_stroke_ratio * dc.stroke_x,
            self.inner_stroke_ratio * dc.stroke_y,
            b.xmid + self.inner_angle_ratio * b.width - ov + delta,
            0,
            b.xmid - ov,
            inner_height,
            direction="top-left",
        )
        draw_parallelogramm(
            pen,
            self.inner_stroke_ratio * dc.stroke_x,
            self.inner_stroke_ratio * dc.stroke_y,
            b.xmid - self.inner_angle_ratio * b.width + ov - delta,
            0,
            b.xmid + ov,
            inner_height,
        )
