from glyph import Glyph
from shapes.corner import draw_corner
from shapes.rect import draw_rect


class LowercaseTGlyph(Glyph):
    name = "lowercase_t"
    unicode = "0x74"
    offset = -40
    rl_ratio = 0.6  # Right/left split of the cross-bar and footer

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, height="x_height")
        right_len = b.width * self.rl_ratio - dc.stroke / 2
        left_len = b.width * (1 - self.rl_ratio) - dc.stroke / 2

        # Stem
        draw_rect(
            pen,
            b.xmid - dc.stroke / 2,
            b.ymid,
            b.xmid + dc.stroke / 2,
            dc.ascent,
        )
        # Cross-bar at x_height
        draw_rect(
            pen,
            b.xmid - left_len - dc.stroke / 2,
            dc.x_height - dc.stroke,
            b.xmid + right_len + dc.stroke / 2,
            dc.x_height,
        )
        # Corner curving down-right (shorter/flatter than f)
        draw_corner(
            pen,
            dc.stroke,
            b.xmid - dc.stroke / 2,
            b.ymid,
            b.xmid + b.width / 2,
            0,
            b.hx,
            b.hy,
            orientation="bottom-right",
        )
        # Footer extension from corner to right edge
        draw_rect(
            pen, b.xmid + b.width / 2, 0, b.xmid + right_len + dc.stroke / 2, dc.stroke
        )
