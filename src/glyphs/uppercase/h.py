from glyph import Glyph
from shapes.rect import draw_rect


class UppercaseHGlyph(Glyph):
    name = "uppercase_h"
    unicode = "0x48"
    offset = 0

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, height="ascent")

        # Left stem
        draw_rect(pen, b.x1, b.y1, b.x1 + dc.stroke, b.y2)
        # Right stem
        draw_rect(pen, b.x2 - dc.stroke, b.y1, b.x2, b.y2)
        # Middle bar
        draw_rect(pen, b.x1, b.ymid - dc.stroke / 2, b.x2, b.ymid + dc.stroke / 2)
