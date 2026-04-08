from glyphs import Glyph
from draw.corner import draw_corner
from draw.cross_curve import draw_cross_curve_2_h


class TildeGlyph(Glyph):
    name = "tilde"
    unicode = "0x7E"
    offset = 0
    height_ratio = 0.35
    corner_ratio = 0.25
    width_ratio = 1
    stroke_ratio = 0.8

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="x_height", width_ratio=self.width_ratio
        )
        h = self.height_ratio * b.height
        cr = self.corner_ratio
        y1 = b.y1 + b.height * (1 - self.height_ratio) / 2
        y2 = b.y2 - b.height * (1 - self.height_ratio) / 2
        s = dc.stroke_alt * self.stroke_ratio

        draw_corner(
            pen,
            s,
            s,
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
            s,
            s,
            b.x1 + cr * b.width,
            y2 - s,
            b.x2 - cr * b.width,
            y1 + s,
            b.hx * cr,
            b.hy * self.height_ratio,
        )
        draw_corner(
            pen,
            s,
            s,
            b.x2,
            y2,
            b.x2 - cr * b.width,
            y1,
            b.hx * cr,
            b.hy,
            orientation="bottom-left",
        )
