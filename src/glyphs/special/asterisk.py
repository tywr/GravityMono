from glyphs import Glyph
from draw.rect import draw_rect


class AsteriskGlyph(Glyph):
    name = "asterisk"
    unicode = "0x2A"
    offset = 0
    width_ratio = 1.31

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="x_height", width_ratio=self.width_ratio
        )
        ymid = dc.math
        draw_rect(pen, b.x1, ymid - dc.stroke_alt / 2, b.x2, ymid + dc.stroke_alt / 2, rotate=30)
        draw_rect(pen, b.x1, ymid - dc.stroke_alt / 2, b.x2, ymid + dc.stroke_alt / 2, rotate=-30)
        draw_rect(
            pen,
            b.xmid - dc.stroke_alt / 2,
            ymid - b.width / 2,
            b.xmid + dc.stroke_alt / 2,
            ymid + b.width / 2,
        )
