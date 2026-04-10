from glyphs import Glyph
from draw.rect import draw_rect


class DollarSignGlyph(Glyph):
    name = "dollar_sign"
    unicode = "0x24"
    offset = 0
    width_ratio = 1
    overflow_ratio = 0.15

    def draw(self, pen, dc):
        from glyphs.uppercase.s import UppercaseSGlyph

        b = dc.body_bounds(
            offset=self.offset, height="cap", width_ratio=self.width_ratio
        )
        sg = UppercaseSGlyph()
        sg.draw(pen, dc)

        dh = self.overflow_ratio * b.height
        draw_rect(
            pen,
            b.xmid - dc.stroke_x / 2,
            b.y1 - dh,
            b.xmid + dc.stroke_x / 2,
            b.y2 + dh,
        )
