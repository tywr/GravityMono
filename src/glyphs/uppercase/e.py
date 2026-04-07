from glyphs.uppercase import UppercaseGlyph
from draw.rect import draw_rect


class UppercaseEGlyph(UppercaseGlyph):
    name = "uppercase_e"
    unicode = "0x45"
    offset = 0
    mid_bar_ratio = 0.95

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="cap", width_ratio=self.width_ratio
        )

        # Vertical stem
        draw_rect(pen, b.x1, b.y1, b.x1 + dc.stroke_x, b.y2)

        # Top bar
        draw_rect(pen, b.x1, b.y2 - dc.stroke_y, b.x2, b.y2)

        # Middle bar
        draw_rect(
            pen,
            b.x1,
            b.ymid - dc.stroke_y / 2,
            b.x1 + self.mid_bar_ratio * b.width,
            b.ymid + dc.stroke_y / 2,
        )

        # Bottom bar
        draw_rect(pen, b.x1, b.y1, b.x2, b.y1 + dc.stroke_y)
