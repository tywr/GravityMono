from glyphs import Glyph
from draw.square_corner import draw_square_corner
from draw.rect import draw_rect


class LowercaseF3Glyph(Glyph):
    name = "lowercase_f_3"
    unicode = "0x66"
    font_feature = {"cv11": 1}
    offset = -36
    rl_ratio = 0.59
    width_ratio = 1.04
    cross_bar_height = 0.9

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="x_height", width_ratio=self.width_ratio
        )
        width = dc.width + dc.default_stroke
        right_len = width * self.rl_ratio - dc.stroke_x / 2
        left_len = width * (1 - self.rl_ratio) - dc.stroke_x / 2
        yc = self.cross_bar_height * dc.x_height

        # Stem
        draw_rect(
            pen, b.xmid - dc.stroke_x / 2, 0, b.xmid + dc.stroke_x / 2, dc.x_height
        )

        # Cross-bar
        draw_rect(
            pen,
            b.xmid - left_len - dc.stroke_x / 2,
            yc - dc.stroke_y,
            b.xmid + right_len + dc.stroke_x / 2,
            yc,
        )

        # Corner
        draw_square_corner(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.xmid - dc.stroke_x / 2,
            dc.x_height,
            b.xmid + right_len + dc.stroke_x / 2,
            dc.ascent,
            orientation="top-right",
        )
