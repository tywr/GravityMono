from glyphs.uppercase import UppercaseGlyph
from draw.superellipse_loop import draw_superellipse_loop
from draw.rect import draw_rect


class UppercasePGlyph(UppercaseGlyph):
    name = "uppercase_p"
    unicode = "0x50"
    offset = 0
    loop_ratio = 0.55

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_right=True,
            width_ratio=self.width_ratio,
        )
        hx, hy = dc.hx, dc.hy * self.loop_ratio * dc.cap / dc.x_height
        ymid = b.ymid - (self.loop_ratio * b.height / 4)

        # Left stem
        draw_rect(pen, b.x1, 0, b.x1 + dc.stroke_x, dc.cap)

        # Upper loop (narrower, displaced left)
        draw_superellipse_loop(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            ymid,
            b.x2,
            b.y2,
            hx,
            hy,
            cut="left",
        )

        # Connecting bars
        draw_rect(pen, b.x1, b.y2 - dc.stroke_y, b.x2 - b.width / 2, b.y2)
        draw_rect(
            pen,
            b.x1,
            ymid,
            b.x2 - b.width / 2,
            ymid + dc.stroke_y,
        )
