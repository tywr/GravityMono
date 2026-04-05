from glyph import Glyph
from shapes.rect import draw_rect


class UppercaseFGlyph(Glyph):
    name = "uppercase_f"
    unicode = "0x46"
    offset = 0
    mid_bar_ratio = 0.95

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, height="ascent")

        # Vertical stem
        draw_rect(pen, b.x1, b.y1, b.x1 + dc.stroke, b.y2)
        # Top bar
        draw_rect(pen, b.x1, b.y2 - dc.stroke, b.x2, b.y2)
        # Middle bar
        draw_rect(
            pen,
            b.x1,
            b.ymid - dc.stroke / 2,
            b.x1 + self.mid_bar_ratio * b.width,
            b.ymid + dc.stroke / 2,
        )
