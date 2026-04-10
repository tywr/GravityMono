from glyphs import Glyph
from draw.rect import draw_rect


class ExclamationMarkGlyph(Glyph):
    name = "exclamation_mark"
    unicode = "0x21"
    offset = 0
    width_ratio = 1
    gap = 0.4
    height_overflow = 0.05

    def draw(self, pen, dc):
        from glyphs.special.full_stop import FullStopGlyph

        b = dc.body_bounds(
            offset=self.offset, height="ascent", width_ratio=self.width_ratio
        )
        g = self.gap * b.height
        dh = self.height_overflow * b.height
        draw_rect(
            pen, b.xmid - dc.stroke_x / 2, b.y1 + g, b.xmid + dc.stroke_x / 2, b.y2 + dh
        )

        fsp = FullStopGlyph()
        fsp.draw(pen, dc)
