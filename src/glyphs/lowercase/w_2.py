from glyphs import Glyph
from draw.rect import draw_rect
from draw.arch import draw_arch
from draw.square_corner import draw_square_corner


class LowercaseW2Glyph(Glyph):
    name = "lowercase_w_2"
    default_italic = True
    width_ratio = 1.2
    unicode = "0x77"
    offset = 0
    tail_ratio = 0.2
    mid_ratio = 0.47

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            width_ratio=self.width_ratio,
            overshoot_bottom=True,
        )
        xmid = b.x1 + self.mid_ratio * b.width
        sy = dc.stroke_y
        sx = max(0, 0.9 * (dc.stroke_x - 90)) + min(90, dc.stroke_x)
        xt = b.x2 - self.tail_ratio * b.width - sx / 2

        draw_rect(
            pen,
            b.x1,
            b.ymid,
            b.x1 + sx,
            b.y2,
        )
        draw_rect(
            pen,
            xmid - sx / 2,
            b.ymid,
            xmid + sx / 2,
            b.y2,
        )
        draw_rect(
            pen,
            xmid - sx / 2,
            b.ymid,
            xmid + sx / 2,
            b.y2,
        )
        draw_arch(
            pen,
            sx,
            sy,
            b.x1,
            b.y1,
            xmid + sx / 2,
            b.y2,
            b.hx * (1 - self.mid_ratio),
            b.hy,
            cut="top",
            taper=0.6,
        )
        draw_arch(
            pen,
            sx,
            sy,
            xmid - sx / 2,
            b.y1,
            b.x2,
            b.y2,
            b.hx * self.mid_ratio,
            b.hy,
            side="left",
            cut="top",
            taper=0.6,
        )
        draw_square_corner(pen, sx, sy, b.x2, b.ymid, xt, b.y2, orientation="top-left")
