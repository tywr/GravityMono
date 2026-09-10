from draw.rect import draw_rect
from draw.square_corner import draw_square_corner
from glyphs.lowercase.dotted import DottedLowercaseGlyph


class LowercaseI2Glyph(DottedLowercaseGlyph):
    name = "lowercase_i_2"
    unicode = "0x69"
    default_italic = True
    offset = -24
    width_ratio = 1.08
    cap = 0.45

    def draw_base(self, pen, dc):
        """Draw the letter without the dot (for use with accents)."""
        b = dc.body_bounds(offset=self.offset, width_ratio=self.width_ratio)
        xmid = b.x1 + self.rl_ratio * b.width
        ym4 = b.y1 + b.height / 4

        # Stem
        draw_rect(
            pen, xmid - dc.stroke_x / 2, ym4, xmid + dc.stroke_x / 2, dc.x_height
        )

        draw_square_corner(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            xmid - dc.stroke_x / 2,
            ym4,
            b.x2,
            b.y1,
            orientation="bottom-right",
        )
        draw_rect(
            pen,
            xmid - b.width * self.cap,
            dc.x_height - dc.stroke_y,
            xmid,
            dc.x_height,
        )
