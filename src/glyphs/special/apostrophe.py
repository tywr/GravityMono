from glyphs import Glyph
from draw.rect import draw_rect


class ApostropheMarkGlyph(Glyph):
    name = "apostrophe"
    unicode = "0x27"
    offset = 0
    width_ratio = 1
    height_ratio = 0.7

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="x_height", width_ratio=self.width_ratio
        )
        h = self.height_ratio * b.height
        s = dc.stroke_x
        draw_rect(pen, b.xmid - s / 2, dc.ascent - h, b.xmid + s / 2, dc.ascent)
