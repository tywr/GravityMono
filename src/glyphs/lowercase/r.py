from glyph import Glyph
from shapes.superellipse_arch import draw_superellipse_arch
from shapes.rect import draw_rect


class LowercaseRGlyph(Glyph):
    name = "lowercase_r"
    unicode = "0x72"
    offset = 20
    loop_ratio = 0.6
    rx = 0.8

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, overshoot_top=True)
        hx, hy = dc.hx * self.rx, dc.hy * self.loop_ratio

        # Top arch, cut at the bottom (only upper half drawn)
        draw_superellipse_arch(
            pen,
            dc.stroke,
            b.x1,
            b.y2 - b.height * self.loop_ratio,
            b.x2,
            b.y2,
            hx,
            hy,
            dent=dc.dent + dc.v_overshoot,
            side="left",
            cut="bottom",
        )
        # Left stem
        draw_rect(pen, b.x1, 0, b.x1 + dc.stroke, dc.x_height - dc.dent)
        draw_rect(pen, b.x1, 0, b.x1 + dc.stroke - dc.gap, dc.x_height)
