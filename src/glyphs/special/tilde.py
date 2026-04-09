from glyphs import Glyph
from draw.corner import draw_corner
from draw.cross_curve import draw_cross_curve_2_h


class TildeGlyph(Glyph):
    name = "tilde"
    unicode = "0x7E"
    offset = 0
    height_ratio = 0.36
    corner_ratio = 0.26
    width_ratio = 1.2
    stroke_ratio = 1

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="x_height", width_ratio=self.width_ratio
        )
        cr = self.corner_ratio
        y1 = b.y1 + b.height * (1 - self.height_ratio) / 2
        y2 = b.y2 - b.height * (1 - self.height_ratio) / 2

        draw_corner(
            pen,
            dc.stroke_y,
            dc.stroke_y,
            b.x1,
            y1,
            b.x1 + cr * b.width,
            y2,
            b.hx * cr,
            b.hy,
            orientation="top-right",
        )
        draw_cross_curve_2_h(
            pen,
            dc.stroke_y,
            dc.stroke_y,
            b.x1 + cr * b.width,
            y2 - dc.stroke_y,
            b.x2 - cr * b.width,
            y1 + dc.stroke_y,
            b.hx * cr,
            b.hy * self.height_ratio,
        )
        draw_corner(
            pen,
            dc.stroke_y,
            dc.stroke_y,
            b.x2,
            y2,
            b.x2 - cr * b.width,
            y1,
            b.hx * cr,
            b.hy,
            orientation="bottom-left",
        )
