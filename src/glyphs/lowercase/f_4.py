from glyphs import Glyph
from draw.smooth_corner import draw_smooth_corner
from draw.rect import draw_rect


class LowercaseF4Glyph(Glyph):
    name = "lowercase_f_4"
    unicode = "0x66"
    font_feature = {"cv11": 1}
    italic_only = True
    offset = -22
    rl_ratio = 0.55
    width_ratio = 1.05
    cross_bar_height = 0.9

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="x_height", width_ratio=self.width_ratio
        )
        right_len = b.width * self.rl_ratio - dc.stroke_x / 2
        left_len = b.width * (1 - self.rl_ratio) - dc.stroke_x / 2
        yc = self.cross_bar_height * dc.x_height

        # Stem
        draw_rect(
            pen,
            b.xmid - dc.stroke_x / 2,
            0,
            b.xmid + dc.stroke_x / 2,
            dc.x_height,
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
        draw_smooth_corner(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.xmid - dc.stroke_x / 2,
            dc.x_height,
            b.xmid + right_len + dc.stroke_x / 2,
            dc.ascent,
            right_len + dc.stroke_x,
            dc.ascent - dc.x_height,
            orientation="top-right",
        )

        draw_smooth_corner(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.xmid + dc.stroke_x / 2,
            0,
            b.x1,
            dc.descent,
            b.hx,
            b.hy,
            orientation="bottom-left",
        )
