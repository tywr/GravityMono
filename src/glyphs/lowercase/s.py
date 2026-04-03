from glyph import Glyph
from shapes.superellipse_loop import draw_superellipse_loop
from shapes.cross_curve import draw_cross_curve


class LowercaseSGlyph(Glyph):
    name = "lowercase_s"
    unicode = "0x73"
    offset = 0
    loop_ratio = 0.6  # Controls the height of each half-loop
    rx = 0.8  # Horizontal curve dampening (dc.hx * rx)
    rm = 0.75

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_left=True,
            overshoot_right=True,
        )
        hx, hy = dc.hx * self.rx, dc.hy * self.loop_ratio

        # Height of each half-loop from its respective baseline
        loop_len = b.y2 * self.loop_ratio
        ym1 = b.y1 + loop_len - dc.stroke / 2  # Top of the bottom half-loop
        ym2 = b.y2 - loop_len + dc.stroke / 2  # Bottom of the top half-loop

        # Bottom half-loop (cut at top)
        draw_superellipse_loop(pen, dc.stroke, b.x1, b.y1, b.x2, ym1, hx, hy, cut="top")
        # Top half-loop (cut at bottom)
        draw_superellipse_loop(
            pen, dc.stroke, b.x1, ym2, b.x2, b.y2, hx, hy, cut="bottom"
        )
        # Middle cross junction connecting the two half-loops
        draw_cross_curve(
            pen,
            dc.stroke,
            b.x1,
            (b.y1 + ym1) / 2,
            b.x2,
            (b.y2 + ym2) / 2,
            self.rm * hx,
            self.rm * hy,
            invert=True,
        )
