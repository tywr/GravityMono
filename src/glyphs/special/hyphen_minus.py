from glyphs import Glyph
from draw.rect import draw_rect


class HyphenMinusGlyph(Glyph):
    name = "hyphen-minus"
    unicode = "0x2D"
    offset = 0
    width_ratio = 1

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="x_height", width_ratio=self.width_ratio
        )
        draw_rect(pen, b.x1, b.ymid + dc.stroke_y / 2, b.x2, b.ymid - dc.stroke_y / 2)
