from glyphs import Glyph
from draw.superellipse_loop import draw_superellipse_loop


class LowercaseOGlyph(Glyph):
    name = "lowercase_o"
    unicode = "0x6F"
    offset = 0

    def draw(
        self,
        pen,
        dc,
    ):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_left=True,
            overshoot_right=True,
        )
        draw_superellipse_loop(
            pen, dc.stroke_x, dc.stroke_y, b.x1, b.y1, b.x2, b.y2, b.hx, b.hy
        )
