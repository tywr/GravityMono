from glyph import Glyph
from shapes.rect import draw_rect


class UppercaseLGlyph(Glyph):
    name = "uppercase_l"
    unicode = "0x4C"
    offset = 0

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, height="ascent")

        # Vertical stem
        draw_rect(pen, b.x1, b.y1, b.x1 + dc.stroke, b.y2)
        # Bottom bar
        draw_rect(pen, b.x1, b.y1, b.x2, b.y1 + dc.stroke)
