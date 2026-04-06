from glyphs.uppercase import UppercaseGlyph
from draw.rect import draw_rect
from draw.parallelogramm import draw_parallelogramm


class UppercaseNGlyph(UppercaseGlyph):
    name = "uppercase_n"
    unicode = "0x4E"
    offset = 0

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="cap", width_ratio=self.width_ratio
        )
        # Vertical stems
        draw_rect(pen, b.x1, b.y1, b.x1 + dc.stroke_x, b.y2)
        draw_rect(pen, b.x2 - dc.stroke_x, b.y1, b.x2, b.y2)

        # Diagonal
        draw_parallelogramm(
            pen, dc.stroke_x, dc.stroke_y, b.x2, b.y1, b.x1, b.y2, direction="top-left"
        )
