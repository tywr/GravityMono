from glyphs import Glyph
from draw.arch import draw_arch
from draw.square_corner import draw_square_corner
from draw.rect import draw_rect
# from draw.arch import draw_arch
# from draw.corner import draw_corner


class LowercaseX2Glyph(Glyph):
    name = "lowercase_x_2"
    default_italic = True
    unicode = "0x78"
    offset = 0
    width_ratio = 1.25
    stroke_ratio = 1.1
    mid_ratio = 0.49
    tail_ratio = 0.33
    hy_ratio = 0.66
    taper = 1.5
    overlap = 0.4

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            width_ratio=self.width_ratio,
            overshoot_bottom=True,
            overshoot_top=True,
        )
        yt1 = b.y1 + self.tail_ratio * b.height
        yt2 = b.y2 - self.tail_ratio * b.height
        sx, sy = dc.stroke_x, dc.stroke_y
        ov = self.overlap * dc.stroke_x
        xmid = b.x1 + self.mid_ratio * b.width
        hy = self.hy_ratio * b.hy
        draw_rect(
            pen,
            b.x1,
            dc.x_height - sy,
            xmid - sx / 2,
            dc.x_height,
        )
        draw_rect(
            pen,
            xmid - sx / 2,
            yt1,
            xmid + sx / 2 - ov,
            dc.x_height,
        )
        draw_square_corner(
            pen,
            sx * (1 - self.overlap),
            sy,
            xmid - sx / 2 + ov,
            yt2,
            b.x2,
            0,
            orientation="bottom-right",
        )
        draw_arch(
            pen,
            sx,
            sy,
            xmid - sx / 2,
            yt1,
            b.x2,
            b.y2,
            b.hx * (1 - self.mid_ratio),
            hy,
            cut="bottom",
            side="left",
            taper=dc.taper * self.taper,
        )
        draw_arch(
            pen,
            sx,
            sy,
            b.x1,
            b.y1,
            xmid + sx / 2,
            yt2,
            b.hx * self.mid_ratio,
            hy,
            cut="top",
            side="right",
            taper=dc.taper * self.taper,
        )

        # draw_corner(
        #     pen,
        #     sx * (1 - self.overlap),
        #     sy,
        #     xmid + sx / 2 - ov,
        #     b.ymid,
        #     b.x1,
        #     b.y1,
        #     b.hx * (1 - self.mid_ratio) * 2,
        #     b.hy,
        #     orientation="bottom-left",
        # )
        # draw_corner(
        #     pen,
        #     sx * (1 - self.overlap),
        #     sy,
        #     xmid - sx / 2 + ov,
        #     b.ymid,
        #     b.x2,
        #     b.y2,
        #     b.hx * self.mid_ratio * 2,
        #     b.hy,
        #     orientation="top-right",
        # )
