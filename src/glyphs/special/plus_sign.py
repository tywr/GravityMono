from glyphs import Glyph
from draw.rect import draw_rect


class PlusSignGlyph(Glyph):
    name = "plus_sign"
    unicode = "0x2B"
    offset = 0
    width_ratio = 1

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="cap", width_ratio=self.width_ratio
        )

        draw_rect(pen, b.x1, dc.math - dc.stroke_y / 2, b.x2, dc.math + dc.stroke_y / 2)
        draw_rect(pen, b.xmid - dc.stroke_x / 2, dc.math - b.width / 2, b.xmid + dc.stroke_x / 2, dc.math + b.width / 2)
