from glyph import Glyph
from shapes.rect import draw_rect


class UppercaseTGlyph(Glyph):
    name = "uppercase_t"
    unicode = "0x54"
    offset = 0

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, height="ascent")

        # Vertical stem (centered)
        draw_rect(pen, b.xmid - dc.stroke / 2, b.y1, b.xmid + dc.stroke / 2, b.y2)
        # Top bar
        draw_rect(pen, b.x1, b.y2 - dc.stroke, b.x2, b.y2)
