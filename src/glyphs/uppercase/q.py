from glyphs.uppercase import UppercaseGlyph
from draw.superellipse_loop import draw_superellipse_loop
from draw.parallelogramm import draw_parallelogramm


class UppercaseQGlyph(UppercaseGlyph):
    name = "uppercase_q"
    unicode = "0x51"
    offset = 0
    tail_offset = 0.1

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_left=True,
            overshoot_right=True,
            width_ratio=self.width_ratio,
        )

        hx, hy = dc.hx * self.width_ratio, dc.hy * dc.cap / dc.x_height
        oy = self.tail_offset * b.height

        draw_superellipse_loop(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1,
            b.x2,
            b.y2,
            hx,
            hy,
        )

        draw_parallelogramm(
            pen, dc.stroke_x, dc.stroke_y, b.x2, -oy, b.xmid - dc.stroke_x / 2, b.ymid - oy, direction="top-left"
        )
