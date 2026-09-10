from draw.rect import draw_rect
from glyphs.uppercase import UppercaseGlyph
from draw.arch import draw_arch


class UppercaseOeGlyph(UppercaseGlyph):
    name = "uppercase_oe"
    unicode = "0x153"
    offset = 0
    bar_height = 0.35
    overlap = 0.25
    stroke_x_ratio = 1.02
    width_ratio = 1.2
    mid_ratio = 0.52
    xmid_ratio = 0.55
    hx_ratio = 0.7

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="cap", width_ratio=self.width_ratio
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio

        ymid = self.mid_ratio * b.height
        xmid = b.x1 + self.xmid_ratio * b.width

        draw_arch(
            pen,
            sx,
            sy,
            b.x1,
            b.y1,
            xmid + sx / 2,
            b.y2,
            b.hx * self.hx_ratio,
            b.hy,
        )

        draw_rect(pen, xmid - sx / 2, b.y1, xmid + sx / 2, b.y2)

        # Vertical stem
        draw_rect(pen, xmid, ymid - sy / 2, b.x2, ymid + sy / 2)

        # Top bar
        draw_rect(pen, xmid, b.y2 - sy, b.x2, b.y2)

        # Middle bar
        draw_rect(
            pen,
            xmid,
            b.y1,
            b.x2,
            b.y1 + sy,
        )
