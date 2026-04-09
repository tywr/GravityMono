from glyphs import Glyph
from draw.rect import draw_rect


class FullStopGlyph(Glyph):
    name = "full_stop"
    unicode = "0x2E"
    offset = 0
    width_ratio = 1
    taper = 0.5
    stroke_ratio = 1.5

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="x_height", width_ratio=self.width_ratio
        )
        s = self.stroke_ratio * dc.stroke_x
        draw_rect(pen, b.xmid - s / 2, 0, b.xmid + s / 2, s)
